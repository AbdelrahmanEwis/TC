# -*- coding: utf-8 -*-
from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    def _action_to_open_ui(self):
        if not self.current_session_id:
            self.env['pos.session'].create({'user_id': self.env.uid, 'config_id': self.id})
        path = '/pos/web' if self._force_http() else '/pos/ui'
        return {
            'type': 'ir.actions.act_url',
            'url': path + '?config_id=%d' % self.id,
            'target': 'new',
        }
