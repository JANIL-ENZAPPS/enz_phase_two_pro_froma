from odoo import fields,models

class ProFormaWiz(models.TransientModel):
    _name = 'pro.forma.wiz'

    pro_forma_id = fields.Many2one('pro.forma.invoice')
    credit_note_date = fields.Date()
    reason = fields.Char(default="Converting From Pro Forma To Invoice")

    def post(self):
        self.pro_forma_id.credit_invoice_date = self.credit_note_date
        self.pro_forma_id.credit_note_reason = self.reason
        self.pro_forma_id.convert_to_credit_note()