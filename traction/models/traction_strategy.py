from odoo import api, models, fields, _
from datetime import datetime


class TractionStrategy(models.Model):
    _name = 'traction.strategy'
    _description = 'Marketing Strategy'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    target_market = fields.Html(string='Target market')
    proven_process = fields.Html(string='Proven Process')
    guarantee = fields.Html(string='Guarantee')
    uniques = fields.Html(string='Unique')

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )
