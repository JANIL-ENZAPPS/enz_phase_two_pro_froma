from odoo import fields,models

class AccountMove(models.Model):
    _inherit = 'account.move'

    pro_forma_invoice = fields.Boolean()