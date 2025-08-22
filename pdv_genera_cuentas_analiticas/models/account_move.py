from odoo import api, models, fields

import logging
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    @api.model
    def create(self, vals):
        vals_copy = vals.copy()
        move = super(AccountMove, self).create(vals)
        if vals.get('invoice_origin') and vals.get('move_type') == 'out_invoice':
            self._asignar_distribucion_analitica(move)
        return move

    def _asignar_distribucion_analitica(self, move):
        try:
            # Buscar la primera cuenta analítica disponible
            analytic_account = self.env['account.analytic.account'].search([], limit=1)
            
            if analytic_account:
                # Preparar la distribución analítica (100% para la cuenta encontrada)
                analytic_distribution = {str(analytic_account.id): 100.0}
                
                # Recorrer todas las líneas del movimiento y asignar la distribución analítica
                for line in move.line_ids:
                    line.write({
                        'analytic_distribution': analytic_distribution
                    })
                
                _logger.info("Distribución analítica asignada al move %s: %s", move.name, analytic_distribution)
            else:
                _logger.warning("No se encontraron cuentas analíticas para asignar al move %s", move.name)
                
        except Exception as e:
            _logger.error("Error al asignar distribución analítica al move %s: %s", move.name, str(e))
        