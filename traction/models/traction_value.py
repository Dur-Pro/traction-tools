from odoo import api, models, fields, _
from datetime import datetime


class TractionValue(models.Model):
    _name = 'traction.value'
    _description = 'Core Value'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )

