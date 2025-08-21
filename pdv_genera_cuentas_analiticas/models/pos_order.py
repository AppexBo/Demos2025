from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)

class PosOrder(models.Model):
    _inherit = 'pos.order'

    #analytic_account_id = fields.Many2one(
    #    comodel_name='account.analytic.account',
    #    string="Analytic Account",
    #    copy=False, 
    #    check_company=True,  # Unrequired company
    #    domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    #)
############################################
############################################
############################################
    #def _create_analytic_account(self, prefix=None):
    #    for order in self:
    #        if not order.analytic_account_id:
    #            _logger.info("2entroooooooooooooooooooooooooooooooooooooooooooooooooooo")
    #            analytic = self.env['account.analytic.account'].create(order._prepare_analytic_account_data(prefix))
    #            _logger.info("2saliooooooooooooooooooooooooooooooooooooooooooooooooooooo")
    #            order.analytic_account_id = analytic

    #def _prepare_analytic_account_data(self, prefix=None):
    #    """ Prepare analytic account creation values """
    #    self.ensure_one()
    #    name = self.name
    #    _logger.info("entroooooooooooooooooooooooooooooooooooooooooooooooooooo")
    #    if prefix:
    #        name = prefix + ": " + self.name
    #    plan = self.env['account.analytic.plan'].sudo().search([], limit=1)
    #    if not plan:
    #        _logger.info("secreo algooooooooooooooooooooooooooooooooooooooooooo")
    #        plan = self.env['account.analytic.plan'].sudo().create({
    #            'name': 'Default',
    #        })
    #    _logger.info("saliooooooooooooooooooooooooooooooooooooooooooooooooooooo")
    #    return {
    #        'name': name,
    #        'code': self.pos_reference,
    #        'company_id': self.company_id.id,
    #        'plan_id': plan.id,
    #        'partner_id': self.partner_id.id if self.partner_id else False,
    #    }