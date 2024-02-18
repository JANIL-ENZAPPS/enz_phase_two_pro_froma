from odoo import fields,models,_
from datetime import datetime, date,time,timedelta
from datetime import datetime as dt  # Rename datetime to avoid conflict


class ResCompany(models.Model):
    _inherit = "res.company"

    advance_product_id = fields.Many2one('product.product')

class ProFormaInvoice(models.Model):
    _inherit = 'pro.forma.invoice'

    state = fields.Selection([('draft','Draft'),('done','Done'),('invoiced','Invoiced'),('invoiced_send','Invoice Send'),('cancel','Credit Note'),('cancel_send','Credit Note Send')],default="draft")
    invoice_id = fields.Many2one('account.move')
    credit_invoice_id = fields.Many2one('account.move')
    credit_invoice_date = fields.Date()
    credit_note_reason = fields.Char()
    # invoiced = fields.Boolean()
    # credit_invoiced = fields.Boolean()

    def convert_to_credit_note_new(self):
        self.credit_invoice_id.action_post()
        self.state = 'cancel_send'

    def convert_to_credit_note(self):
        products = self.invoice_line_ids.mapped('product_id.name')
        if products:
            products = set(products)
        else:
            products = []
        taxs = self.invoice_line_ids.mapped('tax_ids')
        if taxs:
            taxs = set(taxs.ids)
        else:
            taxs = []
        self.credit_invoice_id = self.env['account.move'].create({
            'partner_id': self.partner_id.id,
            'invoice_date': self.invoice_date_time,
            'invoice_date_time': self.credit_invoice_date.strftime('%d/%m/%Y'),
            'customer_po': self.customer_po,
            'payment_reference': self.name,
            'move_type': 'out_refund',
            'ref':'Reversal of: ' + self.invoice_id.name + ',' + self.credit_note_reason,
            'pro_forma_invoice': True,
            'currency_id':self.currency_id.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.company_id.advance_product_id.id,
                'name': "Advance For Products " + str(products),
                'account_id': self.company_id.advance_product_id.property_account_income_id.id,
                'vat_category': 'S',
                'quantity': 1,
                'price_unit': self.advance_amount,
                'tax_ids': [(6, 0, taxs)]
            })]
        }).id
        self.state = 'cancel'
        invoicedate = self.credit_invoice_id.invoice_date_time
        date_obj = dt.strptime(invoicedate, "%d/%m/%Y")
        date_obj_with_time = dt.combine(date_obj.date(), time(0, 0, 0))
        formatted_date_with_time = date_obj_with_time.strftime("%Y-%m-%d %H:%M:%S")
        self.credit_invoice_id.invoice_datetime = formatted_date_with_time
        self.credit_invoice_id.invoice_datetime = self.credit_invoice_id.invoice_datetime - timedelta(hours=self.company_id.hours,
                                                                                        minutes=self.company_id.minutes)
        self.credit_invoice_id._onchange_invoice_datetime()

        # value = self.invoice_id.action_reverse()
        # # print([(6,0,self.invoice_id.ids)])
        # # value['move_ids'] = [(6,0,self.invoice_id.ids)]
        # # value['move_ids'] = self.invoice_id.ids
        # print(value)
        # return {
        #     'name': _('Reversal'),
        #     'type': 'ir.actions.act_window',
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'res_model': 'account.move.reversal',
        #     # 'views': [(compose_form.id, 'form')],
        #     # 'view_id': compose_form.id,
        #     'target': 'new',
        #     'context': {
        #         'default_display_name':'Reverse',
        #         'default_move_ids':[(6,0,self.invoice_id.ids)],
        #         'default_refund_method':'cancel',
        #         'default_reason':'Converting To Invoice'
        #                 },
        # }

        # return value


    def convert_to_invoice_new(self):
        self.invoice_id.action_post()
        self.state = 'invoiced_send'


    def convert_to_invoice(self):
        products = self.invoice_line_ids.mapped('product_id.name')
        if products:
            products = set(products)
        else:
            products = []
        taxs = self.invoice_line_ids.mapped('tax_ids')
        if taxs:
            taxs = set(taxs.ids)
        else:
            taxs = []
        self.invoice_id = self.env['account.move'].create({
            'partner_id':self.partner_id.id,
            'invoice_date':self.invoice_date_time,
            'invoice_date_time':self.invoice_date_time.strftime('%d/%m/%Y'),
            'customer_po':self.customer_po,
            'payment_reference':self.name,
            'move_type':'out_invoice',
            'pro_forma_invoice':True,
            'system_inv_no':self.name,
            'currency_id':self.currency_id.id,
            'invoice_line_ids':[(0,0,{
                'product_id':self.company_id.advance_product_id.id,
                'name':"Advance For Products " + str(products),
                'account_id':self.company_id.advance_product_id.property_account_income_id.id,
                'vat_category':'S',
                'quantity':1,
                'price_unit':self.advance_amount,
                'tax_ids':[(6,0,taxs)]
            })]
        }).id
        self.state = 'invoiced'
        invoicedate = self.invoice_id.invoice_date_time
        date_obj = dt.strptime(invoicedate, "%d/%m/%Y")
        date_obj_with_time = dt.combine(date_obj.date(), time(0, 0, 0))
        formatted_date_with_time = date_obj_with_time.strftime("%Y-%m-%d %H:%M:%S")
        self.invoice_id.invoice_datetime = formatted_date_with_time
        self.invoice_id.invoice_datetime = self.invoice_id.invoice_datetime - timedelta(hours=self.company_id.hours,
                                                                                  minutes=self.company_id.minutes)
        self.invoice_id._onchange_invoice_datetime()
