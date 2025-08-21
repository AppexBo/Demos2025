from odoo import models, api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def create(self, vals):
        # Si el campo 'name' no está definido o es '/', lo generamos
        if vals.get('name', '/') == '/':
            session = self.env['pos.session'].browse(vals['session_id'])
            pos_config = session.config_id
            sequence = pos_config.sequence_id

            # Obtener el siguiente número de secuencia como "0001", "0002", etc.
            sec_number = sequence.next_by_id()
            
            # Construimos el nuevo valor para el campo name/ref
            vals['name'] = f"{pos_config.name}/{sec_number.split('/')[-1]}"

        return super(PosOrder, self).create(vals)
    
    #@api.model
    def actualizar_nombres_ordenes_antiguas(self):
        orders = self.search([])  # busca todas las órdenes
        for order in orders:
            # Aseguramos que tenga una sesión y un punto de venta asociado
            if order.session_id and order.session_id.config_id:
                pdv_name = order.session_id.config_id.name

                # Obtenemos solo el número correlativo, quitando lo que haya antes del slash
                if '/' in order.name:
                    number = order.name.split('/')[-1]
                else:
                    number = order.name

                # Formamos el nuevo nombre
                new_name = f"{pdv_name}/{number}"

                # Solo actualizamos si cambió
                if order.name != new_name:
                    order.name = new_name