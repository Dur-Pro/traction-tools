from odoo import models, fields


class TractionOrganizer(models.Model):
    _name = 'traction.organizer'
    _description = 'Vision and Traction Tool'
    name = fields.Char(String='Name')
    core_values_ids = fields.One2many('traction.organizer.line', 'core_values_id', string='Core Values')
    core_focus = fields.Char(string='Core Focus')
    purpose = fields.Char(string='Purpose/Cause/Passion')
    niche = fields.Char()
    target = fields.Char(string='10 Year Target')
    target_market = fields.Char()
    proven_process = fields.Char('Proven Process')
    guarantee = fields.Char('Guarantee')
    future_date = fields.Date(string='Future Date')
    revenue = fields.Char(string='Revenue')
    profit = fields.Char(string='profit')
    three_uniques_ids = fields.One2many('traction.organizer.line', 'three_uniques_id', string='three uniques')
    measurable=fields.Many2many('traction.measurable')
    one_yr_planning_date = fields.Date('Future Date')
    one_yr_revenue = fields.Char('Revenue')
    one_yr_profit = fields.Char('Profit')
    two_yr_planning_date = fields.Date('Future Date')
    two_yr_revenue = fields.Char('Revenue')
    two_yr_profit = fields.Char('Profit')
    goal_ids = fields.One2many('traction.organizer.line','goal_id')
    rocks_ids = fields.One2many('traction.organizer.line','rocks_id')
    issue_list_ids = fields.One2many('traction.organizer.line','issue_list_id')


class TractionOrganizerLine(models.Model):

    _name = 'traction.organizer.line'
    core_values_id = fields.Many2one('traction.organizer')
    goal_id = fields.Many2one('traction.organizer')
    rocks_id = fields.Many2one('traction.organizer')
    issue_list_id = fields.Many2one('traction.organizer')
    issue_list = fields.Char('')
    goal = fields.Char(' ')
    rocks = fields.Char('Rocks for the Quarter:')
    rocks_user = fields.Many2one('res.users',string='Who',default=lambda self: self.env.user)
    core_values = fields.Char('Core Values')
    three_uniques_id = fields.Many2one('traction.organizer')
    three_uniques = fields.Char('Three Uniques',readonly= False)













