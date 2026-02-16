from clearframe.app.builder.planner import build_plan
from clearframe.app.builder.ticket_io import Ticket


def test_build_plan_returns_steps():
    ticket = Ticket(
    ticket_id="T1",
    title="Test",
    body="Do something",
    source_path="fake.json",
    status="NEW",
)


    plan = build_plan(ticket)

    assert plan.ticket_id == "T1"
    assert len(plan.steps) == 4
    assert plan.steps[0].description == "Validate ticket structure"
