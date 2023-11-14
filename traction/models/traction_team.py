from odoo import api, models, fields, _
from datetime import datetime


class TractionTeam(models.Model):
    _name = 'traction.team'
    _description = 'Traction Team'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')

    member_ids = fields.Many2many(
        comodel_name='res.users',
        string='Members'
    )

    activity_ids = fields.One2many(
        comodel_name='mail.activity',
        inverse_name='team_id',
        string='Activity'
    )

    issue_ids = fields.One2many(
        comodel_name='mail.activity',
        compute='_compute_issues_headlines',
        inverse='_inverse_issues_headlines'
    )

    headline_ids = fields.One2many(
        comodel_name='mail.activity',
        compute='_compute_issues_headlines',
        inverse='_inverse_issues_headlines'
    )

    measurable_ids = fields.Many2many(
        comodel_name='traction.measurable',
        string='Measurable'
    )

    meeting_ids = fields.One2many(
        comodel_name='calendar.event',
        inverse_name='team_id',
        string='Meetings'
    )

    @api.depends('activity_ids')
    def _compute_issues_headlines(self):
        for rec in self:
            rec.issue_ids = rec.activity_ids.filtered(lambda l: l.activity_type_id == self.env.ref(
                'traction.mail_activity_data_issue'))
            rec.headline_ids = rec.activity_ids.filtered(
                lambda l: l.activity_type_id == self.env.ref('traction.mail_activity_data_headline'))

    def _inverse_issues_headlines(self):
        pass


