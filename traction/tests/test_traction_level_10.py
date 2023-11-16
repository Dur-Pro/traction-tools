from odoo.tests import TransactionCase, tagged, Form
from odoo import Command
from datetime import datetime, timedelta
from odoo.exceptions import MissingError


class TractionLevel10Test(TransactionCase):

    @classmethod
    def _generate_partner(cls, name="Test Partner", is_company=True, parent_id=None):
        return cls.env['res.partner'].create({
            'name': name,
            'is_company': is_company,
            'parent_id': parent_id,
        })

    @classmethod
    def _generate_team(cls, name="Test Team"):
        user_id = cls.env.user.id
        return cls.env['traction.team'].create({
            'name': name,
            'member_ids': [Command.set([user_id])]
        })

    @classmethod
    def _generate_issue(cls, applicable_object, team_id, summary="Test Issue", ):
        return applicable_object.activity_schedule(summary=summary,
                                                   activity_type_id=cls.env.ref(
                                                       'traction.mail_activity_data_issue').id,
                                                   team_id=team_id)

    @classmethod
    def _generate_headline(cls, applicable_object, team_id, summary="Test Issue", ):
        return applicable_object.activity_schedule(summary=summary,
                                                   activity_type_id=cls.env.ref(
                                                       'traction.mail_activity_data_headline').id,
                                                   team_id=team_id)

    @classmethod
    def _generate_meeting(cls, team_id):
        return cls.env['calendar.event'].create({
            'name': 'Test Meeting',
            'start': '2021-01-01 10:00:00',
            'stop': '2021-01-01 11:00:00',
            'team_id': team_id,
        })

    @tagged('post_install', '-at_install')
    def test_issue_visible_in_team_when_raised(self):
        partner = self._generate_partner()
        team = self._generate_team()

        issue = self._generate_issue(partner, team.id)

        self.assertTrue(issue in team.issue_ids)

    @tagged('post_install', '-at_install')
    def test_headline_visible_in_team_when_raised(self):
        partner = self._generate_partner()
        team = self._generate_team()

        headline = self._generate_headline(partner, team.id)

        self.assertTrue(headline in team.headline_ids)

    @tagged('post_install', '-at_install')
    def test_solving_issue_removes_from_team_list(self):
        pass

    @tagged('post_install', '-at_install')
    def test_unsolved_issues_stay_unsolved_after_meeting_close(self):
        partner = self._generate_partner()
        team = self._generate_team()
        issue = self._generate_issue(partner, team.id)
        meeting = self._generate_meeting(team.id)

        meeting.action_start()
        issue.with_context({'active_id': meeting.id}).action_start_ids()
        meeting.action_close_meeting(send_minutes=False)

        self.assertTrue(issue in team.issue_ids)

    @tagged('post_install', '-at_install')
    def test_closing_meeting_creates_next_one(self):
        team = self._generate_team()
        meeting = self._generate_meeting(team.id)
        next_meeting_time = datetime.now() + timedelta(days=30)
        meeting.action_start()
        wizard = self.env['close.meeting.wizard'].with_context(active_id=meeting.id).create({})
        wizard.next_meeting_time = next_meeting_time
        wizard.action_close_meeting()

        next_meeting = team.meeting_ids.filtered(lambda x: x != meeting)

        self.assertTrue(next_meeting)
        self.assertEqual(next_meeting.start, next_meeting_time)
        self.assertEqual(next_meeting.team_id, team)

    def test_making_headlines_creates_no_agenda_items(self):
        team = self._generate_team()
        meeting = self._generate_meeting(team.id)
        partner = self._generate_partner()

        headline1 = self._generate_headline(partner, team.id)
        headline2 = self._generate_headline(partner, team.id, summary='Test issue 2')

        self.assertFalse(headline1.agenda_item_ids)
        self.assertFalse(headline2.agenda_item_ids)
        self.assertFalse(any([item.activity_id in (headline1 | headline2) for item in meeting.agenda_item_ids]))

    def test_starting_meeting_makes_headlines_into_agenda_items(self):
        team = self._generate_team()
        meeting = self._generate_meeting(team.id)
        partner = self._generate_partner()
        headline1 = self._generate_headline(partner, team.id)
        headline2 = self._generate_headline(partner, team.id, summary='Test issue 2')

        meeting.action_start()

        self.assertTrue(headline1.agenda_item_ids)
        self.assertTrue(headline2.agenda_item_ids)
        self.assertEqual(len(meeting.agenda_item_ids.filtered(lambda rec: rec.item_type == 'headline')), 2)
        self.assertTrue(headline1.agenda_item_ids in meeting.agenda_item_ids)
        self.assertTrue(headline2.agenda_item_ids in meeting.agenda_item_ids)

    def test_closing_meeting_closes_discussed_headlines(self):
        team = self._generate_team()
        meeting = self._generate_meeting(team.id)
        partner = self._generate_partner()
        headline1 = self._generate_headline(partner, team.id)
        headline2 = self._generate_headline(partner, team.id)
        meeting.action_start()

        headline1.agenda_item_ids.action_discussed()

        meeting.action_close_meeting(send_minutes=False)

        with self.assertRaises(MissingError):
            test = headline1.summary
        # Should still exist, so no error
        test = headline2.summary
