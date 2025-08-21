from odoo import api, fields, models

import logging

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    pos_analytic_account_ids = fields.Many2many(
        related='pos_config_id.analytic_account_ids', 
        readonly=False
    )