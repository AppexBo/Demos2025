from odoo import api, models, fields


class ProjectTask(models.Model):
    _inherit = "project.task"

    user_ids = fields.Many2many(
        comodel_name="res.users",
        string="Usuarios",
        domain=[
            ("active", "in", [True, False]),
            ("id", "not in", ['1', '3', '4', '5']),
        ],  # Muestra usuarios activos e inactivos
    )
