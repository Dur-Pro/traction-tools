from odoo import models, fields, api, _


class IssuesList(models.Model):
    _name = "traction.issues.list"
    _description = "Issues List"

    name = fields.Char(translate=True)
    description = fields.Html(translate=True)

    team_ids = fields.Many2many(
        comodel_name='traction.team',
        string="Teams",
        relation='traction_team_issues_list_rel',
        column1='issues_list_id',
        column2='team_id',
        help="Teams that this issues list is shared with."
    )

    issue_ids = fields.One2many(
        comodel_name='traction.issue',
        inverse_name='issues_list_id',
        string="Issues",
    )

    issues_count = fields.Integer(
        compute="_compute_issues_count",
        string="Issue Count"
    )

    def _compute_issues_count(self):
        for rec in self:
            rec.issues_count = len(rec.issue_ids)




