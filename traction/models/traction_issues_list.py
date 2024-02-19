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

    members_count = fields.Integer(
        compute="_compute_members_count",
        compute_sudo=True,
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

    stage_ids = fields.One2many(
        string="Stages",
        comodel_name="traction.issue.stage",
        inverse_name="issues_list_id",
    )

    @api.depends("issue_ids")
    def _compute_issues_count(self):
        for rec in self:
            rec.issues_count = len(rec.issue_ids)

    @api.depends("team_ids.member_ids")
    def _compute_members_count(self):
        for rec in self:
            rec.members_count = len(rec.team_ids.member_ids)

    def action_view_issues(self):
        self.ensure_one()
        return {
            "name": self.name,
            "type": "ir.actions.act_window",
            "view_mode": "kanban,tree,form,activity",
            "res_model": "traction.issue",
            "domain": [["issues_list_id", "=", self.id]],
            "context": {
                "default_issues_list_id": self.id
            }
        }