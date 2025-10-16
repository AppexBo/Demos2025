from odoo import models, fields


class MailActivitySchedule(models.TransientModel):
    _inherit = "mail.activity.schedule"

    activity_user_id = fields.Many2one(
        comodel_name="res.users",
        string="Asignada a",
        domain=[
            ("active", "in", [True, False]),
            ("id", "not in", ["1", "3", "4", "5"]),
        ],  # Mostrar activos e inactivos
    )
