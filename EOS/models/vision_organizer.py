from odoo import models, fields


class TractionOrganizer(models.Model):
    _name = 'traction.organizer'
    name = fields.Char(String='Name')
    core_values_ids = fields.One2many('traction.organizer.line', 'core_values_id',string='Core Values')
    core_focus = fields.Char(string='Core Focus')
    purpose = fields.Char(string='Purpose/Cause/Passion')
    niche = fields.Char()
    target = fields.Char(string='10 Year Target')
    target_market=fields.Char()
    proven_process = fields.Char('Proven Process')
    guarantee = fields.Char('Guarantee')
    future_date=fields.Date(string='Future Date')
    revenue=fields.Char(string='Revenue')
    profit=fields.Char(string='profit')
    three_uniques_ids = fields.One2many('traction.organizer.line', 'three_uniques_id', string='three uniques')
    measurable=fields.Many2many('traction.measurable')
    one_yr_planning_date=fields.Date('Future Date')
    one_yr_revenue=fields.Char('Revenue')
    one_yr_profit=fields.Char('Profit')
    # measurable=fields.Many2many('traction.measurable')




class TractionOrganizerLine(models.Model):
    _name = 'traction.organizer.line'
    core_values_id=fields.Many2one('traction.organizer')
    core_values = fields.Char('Core Values')
    three_uniques_id=fields.Many2one('traction.organizer')
    three_uniques=fields.Char('Three Uniques',readonly= False)













