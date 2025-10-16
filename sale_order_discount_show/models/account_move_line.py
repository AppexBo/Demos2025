from odoo import api, models, fields
from odoo.exceptions import UserError

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.onchange('amount_discount')
    def _onchange_amount_discount(self):
        """
        Actualiza el campo discount cuando cambia amount_discount
        y valida que no supere el subtotal
        """
        for record in self:
            if record.amount_discount:
                # Calcular el subtotal sin descuento
                subtotal = record.quantity * record.price_unit
                
                # Validar que el descuento fijo no supere el subtotal
                if record.amount_discount > subtotal:
                    raise UserError('El descuento fijo no puede superar el subtotal')
                
                # Calcular el porcentaje de descuento equivalente
                if subtotal > 0:
                    discount = (record.amount_discount / subtotal) * 100
                    record.discount = discount
                else:
                    record.discount = 0.0

    @api.onchange('discount')
    def _onchange_discount(self):
        """
        Actualiza el campo discount cuando cambia discount
        y valida que no supere el subtotal
        """
        for record in self:
            if record.discount:
                # Calcular el subtotal sin descuento
                subtotal = record.quantity * record.price_unit
                # Validar que el descuento fijo no supere el subtotal
                if record.discount > 100:
                    raise UserError('El descuento no puede ser mayor o igual al 100%')
                elif record.discount > 0:
                    discount = (record.discount/100) * subtotal
                    record.amount_discount = discount
                else:
                    record.amount_discount = 0

    @api.onchange('quantity', 'price_unit')
    def _onchange_subtotal(self):
        for record in self:
            if record.quantity or record.price_unit: 
                record.amount_discount = 0
                record.discount = 0