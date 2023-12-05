from odoo import api, models, fields, _
from datetime import datetime, timedelta


class TractionMeasurable(models.Model):
    _name = 'traction.measurable'
    _description = 'Measurable'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')

    vision_id = fields.Many2one(
        comodel_name='traction.vision',
        string='Vision'
    )

    responsible = fields.Many2one(
        comodel_name='res.users',
        string='Responsibility of',
        index=True,
        tracking=2
    )

    goal_unit = fields.Many2one('uom.uom', string='Unit of Measure')

    goal_variation_type = fields.Selection(
        selection=[
            ('Percentage', 'Percentage'),
            ('Absolute', 'Absolute')
        ],
        string='Variation Type'
    )

    goal_variation = fields.Float(string='Variation')

    goal = fields.Float(string='Goal')

    goal_type = fields.Selection(
        selection=[
            ('greater', 'Greater than'),
            ('less', 'Less than'),
        ],
        string='Goal type',
        default='greater'
    )

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

    average_value_ever = fields.Float(
        string='Average',
        compute='_compute_measurable',
        compute_sudo=True,
        store=True
    )

    average_value_year = fields.Float(
        string='Average this year',
        compute='_compute_measurable',
        compute_sudo=True,
        store=True
    )

    average_value_12mth = fields.Float(
        string='Average 12 months',
        compute='_compute_measurable',
        compute_sudo=True,
        store=True
    )

    cumulative_value_ever = fields.Float(
        string='Cumulative',
        compute='_compute_measurable',
        compute_sudo=True,
        store=True
    )

    cumulative_value_year = fields.Float(
        string='Cumulative this year',
        compute='_compute_measurable',
        compute_sudo=True,
        store=True
    )

    cumulative_value_12mth = fields.Float(
        string='Cumulative 12 months',
        compute='_compute_measurable',
        compute_sudo=True,
        store=True
    )

    last_value_color = fields.Integer(
        string='Last value color',
        compute='_compute_measurable',
        compute_sudo=True,
    )

    @api.depends('value_ids')
    def _compute_measurable(self):
        for record in self:
            # Initializing variables for averages and totals
            total_value_ever = 0.0
            total_value_year = 0.0
            total_value_12mth = 0.0

            count_ever = 0
            count_year = 0
            count_12mth = 0

            # Current date-related calculations
            current_year = datetime.now().year
            date_12_months_ago = datetime.now() - timedelta(days=365)

            # Iterate over related values
            for value in record.value_ids:
                total_value_ever += value.value
                count_ever += 1

                # Check if the value is from the current year
                if value.date and value.date.year == current_year:
                    total_value_year += value.value
                    count_year += 1

                # Check if the value is from the last 12 months
                if value.date and value.date >= date_12_months_ago.date():
                    total_value_12mth += value.value
                    count_12mth += 1

            # Compute averages
            record.average_value_ever = total_value_ever / count_ever if count_ever else 0.0
            record.average_value_year = total_value_year / count_year if count_year else 0.0
            record.average_value_12mth = total_value_12mth / count_12mth if count_12mth else 0.0

            # Assign cumulative values
            record.cumulative_value_ever = total_value_ever
            record.cumulative_value_year = total_value_year
            record.cumulative_value_12mth = total_value_12mth

            # Initialize variation
            variation = 0.0

            # Determine the target range based on goal_variation_type
            if record.goal_variation_type == 'Percentage':
                variation = record.goal * record.goal_variation / 100
            elif record.goal_variation_type == 'Absolute':
                variation = record.goal_variation

            # Compute last value color based on goal_type and range
            if record.goal_type == 'greater':
                target_value = record.goal - variation
                if record.last_value >= record.goal:
                    record.last_value_color = 4  # Blue color when better than range
                elif record.last_value >= target_value:
                    record.last_value_color = 3  # Green color when in range but not better than goal
                else:
                    record.last_value_color = 1  # Red color when below range

            elif record.goal_type == 'less':
                target_value = record.goal + variation
                if record.last_value <= record.goal:
                    record.last_value_color = 4  # Blue color when better than range
                elif record.last_value <= target_value:
                    record.last_value_color = 3  # Green color when in range but not less than goal
                else:
                    record.last_value_color = 1  # Red color when above range
