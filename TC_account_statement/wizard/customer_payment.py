from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CustomerPayment(models.TransientModel):
    _name = 'customer.payment'

    partner_id = fields.Many2one('res.partner')
    from_date = fields.Date(string="From")
    to_date = fields.Date(string="To")

    def action_confirm(self):
        action = self.env['ir.actions.actions']._for_xml_id('TC_account_statement.account_statement_action')
        action['domain'] = [('partner_id', '=', self.partner_id.id), ('date', '>=', self.from_date),
                            ('date', '<=', self.to_date)]

        return action
