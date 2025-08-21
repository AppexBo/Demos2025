from odoo import api, models, fields

import logging
_logger = logging.getLogger(__name__)

class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    #analytic_distribution = fields.Json(
    #    string='Analytic Distribution',
    #    copy=True,
    #    compute='_compute_analytic_distribution',
    #    store=True,
    #    readonly=False,
    #    precompute=True
    #)

    #analytic_precision = fields.Integer(
    #    string='Analytic Precision',
    #    compute='_compute_analytic_precision',
    #    store=False
    #)
    
    #def _compute_analytic_precision(self):
    #    for line in self:
    #        _logger.info("entroooooooooo: %s", line.read())
    #        if line.order_id.company_id.currency_id:
    #            line.analytic_precision = line.order_id.company_id.currency_id.decimal_places
    #        else:
    #            line.analytic_precision = 2  # Default precision
    #    """Compute analytic precision based on company currency"""
    #    for line in self:
    #        line.analytic_precision = line.order_id.company_id.currency_id.decimal_places

    #@api.depends('order_id.partner_id', 'product_id')
    #def _compute_analytic_distribution(self):
    #    _logger.info("entroooooooooo: %s", self.read())
    #    for line in self:
    #        distribution = line.env['account.analytic.distribution.model']._get_distribution({
    #            "product_id": line.product_id.id,
    #            "product_categ_id": line.product_id.categ_id.id,
    #            "partner_id": line.order_id.partner_id.id,
    #            "partner_category_id": line.order_id.partner_id.category_id.ids,
    #            "company_id": line.company_id.id,
    #        })
    #        line.analytic_distribution = distribution or line.analytic_distribution

    #analytic_distribution, 
    #analytic_distribution_search, 
    #analytic_line_ids, 
    #analytic_precision,
    #distribution_analytic_account_ids