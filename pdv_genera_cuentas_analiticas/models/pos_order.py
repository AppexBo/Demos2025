from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)

class PosOrder(models.Model):
    _inherit = 'pos.order'

    analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string="Analytic Account",
        copy=False, 
        check_company=True,  # Unrequired company
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )


    #@api.model
    #def create(self, vals):
    #    pos_order = super(PosOrder, self).create(vals)
    #    try:
    #        if not pos_order.analytic_account_id:
    #            analytic_account = pos_order._create_analytic_account()
    #            if analytic_account:
    #                pos_order.write(
    #                    {
    #                        'analytic_account_id': analytic_account.id
    #                    }
    #                )
    #    except Exception as e:
    #        _logger.error("Error creando cuenta analítica: %s", str(e))
    #        pos_order.unlink()  # Rollback manual
    #    return pos_order

    #def _create_analytic_account(self, prefix=None):
    #    if not self.analytic_account_id:
    #        _logger.info("crear cuenta analitica")
    #            analytic = self.env['account.analytic.account'].create(
    #        )
    #        return analytic

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