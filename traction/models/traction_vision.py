from odoo import models, fields


class Project(models.Model):
    _inherit = "project.project"

    is_rock = fields.Boolean(string="Is a rock", copy=False)
    is_lv10 = fields.Boolean(string="Is a L-10", copy=False)
    projection_id = fields.Many2one(comodel_name='traction.projection',
                                    string='Projection')
    issue_ids = fields.One2many(comodel_name='traction.issue',
                                inverse_name='project_id',
                                string='Issues')
    lv10_member_ids = fields.Many2one(comodel_name='res.user',
                                      string='Members')


class TractionHeadline(models.Model):
    _name = 'traction.headline'
    _description = 'Headline'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    description = fields.Char(string='Description')
    LV10_id = fields.Many2one(comodel_name='project.project', string='Level 10', domain="[('is_level10', '=', True)]")
    announcer = fields.Many2one(comodel_name='res.users', string='Responsibility of', index=True, tracking=2)
    impact = fields.Selection([
        ('none', 'Informative'),
        ('saleplus', 'Good for sale'),
        ('saleless', 'Bad for sale'),
        ('custplus', 'Good for customer'),
        ('custless', 'Bad for customer'),
        ('emplplus', 'Good for employee'),
        ('emplless', 'Bad for employee'),
        ('suppplus', 'Good for supplier'),
        ('suppless', 'Bad to supplier')
        ], string='Headline impact', store=True, default='none')
    issue_ids = fields.Many2one(comodel_name='traction.issue',
                                string='Issues')
    todo_ids = fields.Many2one(comodel_name='project.task',
                               string='Todos')


class TractionIssue(models.Model):
    _name = 'traction.issue'
    _description = 'Issue'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(string="Not solved", copy=False)
    name = fields.Char(string='Name')
    description = fields.Char(string='Description')
    projection_id = fields.Many2one(comodel_name='traction.projection', string='Projection')
    project_id = fields.Many2one(comodel_name='project.project', string='Project')
    LV10_id = fields.Many2one(comodel_name='project.project', string='Level 10',domain="[('is_level10', '=', True)]")


class TractionMeasurable(models.Model):
    _name = 'traction.measurable'
    _description = 'Measurable'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    projection_id = fields.Many2one(comodel_name='traction.projection',
                                    string='Projection')
    responsible = fields.Many2one(comodel_name='res.users', string='Responsibility of', index=True, tracking=2)
    unit = fields.Many2one(comodel_name='uom.uom', string='Unit of Measure')
    goal = fields.Float(string='Goal')
    show_average = fields.Boolean(string='Show average', default=False)
    show_cumulative = fields.Boolean(string='Show cumulative',
                                     default=False)
    level10_ids = fields.Many2many(comodel_name='project.project', string='Level 10', copy=False,
                                   domain="[('is_level10', '=', True)]")
    value_ids = fields.One2many(comodel_name='traction.measurable.value',
                                inverse_name='measurable_id', string='Values')


class TractionMeasurableValue(models.Model):
    _name = 'traction.measurable.value'
    _description = 'Measurable'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    value = fields.Float(string='Value')
    date = fields.Date(string="Date")
    measurable_id = fields.Many2one(comodel_name='traction.measurable', string='Measurable')


class TractionProjection(models.Model):
    _name = 'traction.projection'
    _description = 'Projection'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    vision_id = fields.Many2one(comodel_name='traction.vision',
                                string='Vision')
    target_range = fields.Selection([('3mth', 'Three months'),
                                     ('1yr', 'One year'),
                                     ('3yr', 'Three years'),
                                     ('10yr', 'Ten years')],
                                    default='3mth',
                                    string='Projection date')
    target_revenue = fields.Float(string='Revenue')
    target_profit = fields.Float(string='Profit')
    target_date = fields.Date(string='Target date')
    target_picture = fields.Html(string='Pictures/Goals')
    measurable_ids = fields.One2many(comodel_name='traction.measurable',
                                     inverse_name='projection_id',
                                     string='Measurable')
    rock_ids = fields.One2many(comodel_name='project.project',
                               inverse_name='projection_id',
                               string='Rocks')
    issue_ids = fields.One2many(comodel_name='traction.issue',
                                inverse_name='projection_id',
                                string='Issues')


class TractionValue(models.Model):
    _name = 'traction.value'
    _description = 'Core Value'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    vision_id = fields.Many2one(comodel_name='traction.vision', string='Vision' )


class TractionStrategy(models.Model):
    _name = 'traction.strategy'
    _description = 'Marketing Strategy'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    vision_id = fields.Many2one(comodel_name='traction.vision', string='Vision')
    target_market = fields.Html(string='Target market')
    proven_process = fields.Html(string='Proven Process')
    guarantee = fields.Html(string='Guarantee')
    uniques = fields.Html(string='Unique')


class TractionVision(models.Model):
    _name = 'traction.vision'
    _description = 'EOS Vision>'

    value_ids = fields.One2many(comodel_name='traction.value',
                                inverse_name='vision_id',
                                string='Core Values')
    purpose = fields.Html(string='Purpose/Cause/Passion')
    niche = fields.Html(string='Our target customer')
    target_10yr = fields.Html(string='10 Year Target')
    strategies_ids = fields.One2many(comodel_name='traction.strategy',
                                     inverse_name='vision_id',
                                     string='Strategies')
    projection_ids = fields.One2many(comodel_name='traction.projection',
                                     inverse_name='vision_id',
                                     string='Projections')
