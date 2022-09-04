from odoo import api, models, fields, _
from datetime import datetime

class TractionRock(models.Model):
    _name = 'traction.rock'
    _description = 'Rock'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    # issue_ids = fields.One2many(comodel_name='traction.issue',
    #                             inverse_name='lv10_id',
    #                             string='Issues')
    vision_id = fields.Many2one(comodel_name='traction.vision',
                                string='Vision')
    user_id = fields.Many2one(comodel_name='res.users', string='Responsible', index=True)


class TractionLevel10(models.Model):
    _name = 'traction.level10'
    _description = 'Level 10'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    member_ids = fields.Many2many(comodel_name='res.users', string='Members')
    issue_ids = fields.Many2many(comodel_name='mail.activity',
                                 relation='traction_level_10_activity_rel',
                                 string='Issues')
    measurable_ids = fields.Many2many(comodel_name='traction.measurable', string='Measurable')

    meeting_ids = fields.One2many(comodel_name='calendar.event', inverse_name='level10_id', string='Meetings')


class TractionMeasurable(models.Model):
    _name = 'traction.measurable'
    _description = 'Measurable'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # goal_unit = fields.Many2one('uom.uom', string='Unit of Measure')

    name = fields.Char(string='Name')
    vision_id = fields.Many2one(comodel_name='traction.vision',
                                string='Vision')
    responsible = fields.Many2one(comodel_name='res.users',
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
    show_cumulative = fields.Boolean(string='Show cumulative',
                                     default=False)
    level10_ids = fields.Many2many(comodel_name='traction.level10',
                                   string='Level 10',
                                   copy=False)
    value_ids = fields.One2many(comodel_name='traction.measurable.value',
                                inverse_name='measurable_id',
                                string='Values')


class TractionMeasurableValue(models.Model):
    _name = 'traction.measurable.value'
    _description = 'Measurable value'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    value = fields.Float(string='Value')
    date = fields.Date(string="Date", default=lambda self: datetime.today())
    measurable_id = fields.Many2one(comodel_name='traction.measurable',
                                    string='Measurable')


class TractionVision(models.Model):
    _name = 'traction.vision'
    _description = 'Vision'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Vision',
                       copy=False,
                       readonly=True,
                       index=True,
                       default=lambda self: _('New'))

    company_id = fields.Many2one('res.company', string='Company', required=True,
        default=lambda self: self.env.company)

    vision_range = fields.Selection([('3mth', 'Three months'),
                                     ('1yr', 'One year'),
                                     ('3yr', 'Three years'),
                                     ('10yr', 'Ten years')],
                                    default='3mth',
                                    string='Vision range')
    target_revenue = fields.Float(string='Revenue')
    target_profit = fields.Float(string='Profit')
    target_date = fields.Date(string='Target date')
    target_picture = fields.Html(string='Pictures/Goals')
    measurable_ids = fields.One2many(comodel_name='traction.measurable',
                                     inverse_name='vision_id',
                                     string='Measurable')
    rock_ids = fields.One2many(comodel_name='traction.rock',
                               inverse_name='vision_id',
                               string='Rocks')
    # issue_ids = fields.One2many(comodel_name='traction.issue',
    #                             inverse_name='traction_id',
    #                             string='Issues')


    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vision_range_key = vals.get('vision_range')
            range_code = self._fields['vision_range'].selection
            range_code_dict = dict(range_code)
            range_name = range_code_dict.get(vision_range_key)
            company_id = self.env.company
            vals['name'] = company_id.name + " in " + range_name

        result = super(TractionVision, self).create(vals)
        return result


class TractionValue(models.Model):
    _name = 'traction.value'
    _description = 'Core Value'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    company_id = fields.Many2one('res.company', string='Company', required=True,
        default=lambda self: self.env.company)

class TractionStrategy(models.Model):
    _name = 'traction.strategy'
    _description = 'Marketing Strategy'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    target_market = fields.Html(string='Target market')
    proven_process = fields.Html(string='Proven Process')
    guarantee = fields.Html(string='Guarantee')
    uniques = fields.Html(string='Unique')
    company_id = fields.Many2one('res.company', string='Company', required=True,
        default=lambda self: self.env.company)

class Traction(models.Model):
    _inherit = 'res.company'

    purpose = fields.Html(string='Purpose/Cause/Passion')
    niche = fields.Html(string='Our target customer')

    value_ids = fields.One2many(comodel_name='traction.value',
                                inverse_name='company_id',
                                string='Core Values')

    strategy_ids = fields.One2many(comodel_name='traction.strategy',
                                   inverse_name='company_id',
                                   string='Strategies')

    vision_ids = fields.One2many(comodel_name='traction.vision',
                                 inverse_name='company_id',
                                 string='Visions')

