from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    cr.execute("DELETE FROM traction_strategy")
    cr.execute("DELETE FROM traction_measurable")
    cr.execute("DELETE FROM traction_measurable_value")
    cr.execute("DELETE from traction_value")
    cr.execute("DELETE FROM traction_rock")
    cr.execute("DELETE FROM traction_vision")
    cr.execute("DELETE FROM calendar_event_action_item")
    cr.execute("DELETE FROM ir_model_fields WHERE model='traction.strategy'")
    cr.execute("DELETE FROM ir_model_fields WHERE model='traction.measurable'")
    cr.execute("DELETE FROM ir_model_fields WHERE model='traction.measurable.value'")
    cr.execute("DELETE FROM ir_model_fields WHERE model='traction.value'")
    cr.execute("DELETE FROM ir_model_fields WHERE model='traction.rock'")
    cr.execute("DELETE FROM ir_model_fields WHERE model='traction.vision'")
    cr.execute("DELETE FROM ir_model_fields WHERE model='calendar.event.action.item'")
