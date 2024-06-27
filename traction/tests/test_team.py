from .test_traction_common import TractionTestCommon
from odoo.tests.common import Form


class TestTractionTeam(TractionTestCommon):
    def test_create_team(self):
        users = self._create_users()
        channel = self._create_discuss_channel()

        with Form(channel) as form:
            for user in users:
                with form.channel_member_ids.new() as member:
                    member.partner_id = user.partner_id
            form.is_traction_team = True

        self.assertTrue(channel.traction_team_id)
        for user in users:
            self.assertIn(user, channel.traction_team_id.member_ids)

    def test_remove_member(self):
        users = self._create_users()
        channel = self._create_discuss_channel()

        with Form(channel) as form:
            for user in users:
                with form.channel_member_ids.new() as member:
                    member.partner_id = user.partner_id
            form.is_traction_team = True
        channel.channel_partner_ids -= users[0].partner_id

        self.assertNotIn(users[0], channel.traction_team_id.member_ids)
