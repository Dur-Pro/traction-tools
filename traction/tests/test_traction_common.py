from odoo.tests import TransactionCase
from odoo import Command


class TractionTestCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def _create_users(cls):
        return cls.env["res.users"].create(
            [
                {
                    "partner_id": cls.env["res.partner"]
                    .create(
                        {
                            "name": "Jim Smith",
                        }
                    )
                    .id,
                    "login": "jsmith@example.com",
                    "groups_id": [Command.link(cls.env.ref("base.group_user").id)],
                },
                {
                    "partner_id": cls.env["res.partner"]
                    .create(
                        {
                            "name": "John Doe",
                        }
                    )
                    .id,
                    "login": "jdoe@example.com",
                    "groups_id": [Command.link(cls.env.ref("base.group_user").id)],
                },
                {
                    "partner_id": cls.env["res.partner"]
                    .create(
                        {
                            "name": "Larry Page",
                        }
                    )
                    .id,
                    "login": "lpage@example.com",
                    "groups_id": [Command.link(cls.env.ref("base.group_user").id)],
                },
            ]
        )

    @classmethod
    def _create_discuss_channel(cls):
        return cls.env["discuss.channel"].create(
            {
                "name": "Test Channel",
                "channel_type": "channel",
            }
        )

    @classmethod
    def _create_meeting(cls, start_time, end_time, team):
        return cls.env["calendar.event"].create(
            {
                "team_id": team.id,
                "start": start_time,
                "stop": end_time,
            }
        )
