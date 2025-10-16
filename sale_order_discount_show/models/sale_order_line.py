from odoo import api, models, fields
from odoo.exceptions import UserError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    amount_discount = fields.Float(
        string='Desc. Fijo',
        default= 0.0,
        compute='_compute_amount_discount', 
        store=True,
        readonly=False
    )


    @api.onchange('amount_discount')
    def _onchange_amount_discount(self):
        """
        Actualiza el campo discount cuando cambia amount_discount
        y valida que no supere el subtotal
        """
        for record in self:
            if record.amount_discount:
                # Calcular el subtotal sin descuento
                subtotal = record.product_uom_qty * record.price_unit
                
                # Validar que el descuento fijo no supere el subtotal
                if record.amount_discount > subtotal:
                    raise UserError('El descuento fijo no puede superar el subtotal')
                
                # Calcular el porcentaje de descuento equivalente
                if subtotal > 0:
                    discount_percentage = (record.amount_discount / subtotal) * 100
                    record.discount = discount_percentage
                else:
                    record.discount = 0.0

    @api.depends('discount')
    def _compute_amount_discount(self):
        """Este método SÍ se ejecutará con write()"""
        for record in self:
            if record.discount:
                subtotal = record.product_uom_qty * record.price_unit
                if record.discount > 100:
                    raise UserError('El descuento no puede ser mayor o igual al 100%')
                record.amount_discount = (record.discount / 100) * subtotal
            else:
                record.amount_discount = 0

    @api.onchange('discount')
    def _onchange_discount(self):
        """
        Actualiza el campo discount cuando cambia discount
        y valida que no supere el subtotal
        """
        for record in self:
            if record.discount:
                # Calcular el subtotal sin descuento
                subtotal = record.product_uom_qty * record.price_unit
                # Validar que el descuento fijo no supere el subtotal
                if record.discount > 100:
                    raise UserError('El descuento no puede ser mayor o igual al 100%')
                elif record.discount > 0:
                    discount_percentage = (record.discount/100) * subtotal
                    record.amount_discount = discount_percentage
                else:
                    record.amount_discount = 0

    @api.onchange('product_uom_qty', 'price_unit')
    def _onchange_subtotal(self):
        for record in self:
            if record.product_uom_qty or record.price_unit: 
                record.amount_discount = 0
                record.discount = 0