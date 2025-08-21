# -*- coding: utf-8 -*-

from odoo import api, models, fields,_
from odoo.exceptions import UserError

class PosSession(models.Model):
    _inherit = ['pos.session']
    

    #def _get_pos_ui_res_users(self, params):
        
    def _get_pos_ui_res_users(self, params):
        #raise UserError(f"{params['search_params']}")
        
        user = self.with_context(active_test = False).env['res.users'].search_read(**params['search_params'], limit=1)
        if not user:
            raise UserError(_("You do not have permission to open a POS session. Please try opening a session with a different user"))
        user = user[0]
        user['role'] = 'manager' if any(id == self.config_id.group_pos_manager_id.id for id in user['groups_id']) else 'cashier'
        del user['groups_id']
        return user