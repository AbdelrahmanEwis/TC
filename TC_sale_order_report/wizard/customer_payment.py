from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CustomerPayment(models.TransientModel):
    _name = 'customer.payment'

    partner_id = fields.Many2one('res.partner')
    date = fields.Date()

    def action_confirm(self):
        action = self.env['ir.actions.actions']._for_xml_id('TC_sale_order_report.sale_order_report_action')
        action['domain'] = [('partner_id', '=', self.partner_id.id), ('date', '=', self.date)]

        return action
