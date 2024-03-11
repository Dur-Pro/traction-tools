from odoo import api, models, fields, _
from datetime import datetime


class MailChannel(models.Model):
    _inherit = ['mail.channel']

    traction_team_id = fields.Many2one(
        comodel_name='traction.team',
        string='Traction Team',
        index=True,
    )
