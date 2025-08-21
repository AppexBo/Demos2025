from odoo import api, models, fields

import logging
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    @api.model
    def create(self, vals):
        vals_copy = vals.copy()
        _logger.info("CREATING AccountMove with values: %s", vals_copy)
        return super(AccountMove, self).create(vals)
        