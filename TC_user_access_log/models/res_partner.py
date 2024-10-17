from odoo.exceptions import ValidationError
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # default func for return the value before saving
    def default_user_ids(self):
        if self.env.is_admin():
            res = self.env['crm.team'].search([])
        else:
            res = self.env['crm.team'].search([('user_id', '=', self.env.user.id)], limit=1)
        members = res.mapped('member_ids')
        return members.ids

    def default_team_ids(self):
        if self.env.is_admin():
            res = self.env['crm.team'].search([])
        else:
            res = self.env['crm.team'].search([('user_id', '=', self.env.user.id)])
        return res.ids

    user_ids = fields.Many2many('res.users', compute='_compute_user_ids', default=default_user_ids)
    team_ids = fields.Many2many('crm.team', compute='_compute_team_ids', default=default_team_ids)

    # func for return all members ids and store it in user_ids field to set domain for sales person
    def _compute_user_ids(self):
        if self.env.is_admin():
            res = self.env['crm.team'].search([])
        else:
            res = self.env['crm.team'].search([('user_id', '=', self.env.user.id)], limit=1)
        members = res.mapped('member_ids')
        self.user_ids = members.ids

    # func return sales team ids in team_ids field to set domain for sales team
    def _compute_team_ids(self):
        if self.env.is_admin():
            res = self.env['crm.team'].search([])
        else:
            res = self.env['crm.team'].search([('user_id', '=', self.env.user.id)])
        self.team_ids = res.ids
