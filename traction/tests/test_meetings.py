from .test_traction_common import TractionTestCommon
from odoo.tests.common import Form
from datetime import datetime as dt
from datetime import timedelta


class TestMeetings(TractionTestCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.users = cls._create_users()
        cls.channel = cls._create_discuss_channel()
        with Form(cls.channel) as form:
            for user in cls.users:
                with form.channel_member_ids.new() as member:
                    member.partner_id = user.partner_id
            form.is_traction_team = True
        cls.team = cls.channel.traction_team_id

    def test_meeting_attendees_set_by_default(self):
        meeting = self._create_meeting(
            start_time=dt.now() + timedelta(days=7),
            end_time=dt.now() + timedelta(days=7, hours=1, minutes=30),
            team=self.team,
        )

        self.assertEqual(
            meeting.attendee_ids.mapped("partner_id"),
            self.users.mapped("partner_id"),
        )
