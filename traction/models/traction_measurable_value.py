from odoo import api, models, fields, _
from datetime import datetime


class TractionMeasurableValue(models.Model):
    _name = 'traction.measurable.value'
    _description = 'Measurable value'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    value = fields.Float(string='Value')
    date = fields.Date(string="Date", default=lambda self: datetime.today())

    measurable_id = fields.Many2one(
        comodel_name='traction.measurable',
        string='Measurable'
    )
