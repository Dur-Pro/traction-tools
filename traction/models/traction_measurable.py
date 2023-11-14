from odoo import api, models, fields, _
from datetime import datetime


class TractionMeasurable(models.Model):
    _name = 'traction.measurable'
    _description = 'Measurable'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # goal_unit = fields.Many2one('uom.uom', string='Unit of Measure')

    name = fields.Char(string='Name')
    vision_id = fields.Many2one(
        comodel_name='traction.vision',
        string='Vision')

    responsible = fields.Many2one(
        comodel_name='res.users',
        string='Responsibility of',
        index=True,
        tracking=2)

    goal = fields.Float(string='Goal')

    goal_type = fields.Selection(
        [
            ('gt', 'Greater than'),
            ('gteq', 'Greater or equal'),
            ('eq', 'Equal to'),
            ('lteq', 'Less or equal'),
            ('lt', 'Less than'),
        ],
        string='Goal type',
        default='eq')

    show_average = fields.Boolean(string='Show average', default=False)

    show_cumulative = fields.Boolean(string='Show cumulative', default=False)

    team_ids = fields.Many2many(
        comodel_name='traction.team',
        string='Traction Teams',
        copy=False
    )

    value_ids = fields.One2many(
        comodel_name='traction.measurable.value',
        inverse_name='measurable_id',
        string='Values'
    )


