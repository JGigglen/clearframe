from pathlib import Path
from clearframe.app.builder.executor import execute_plan
from clearframe.app.builder.planner import Step


def test_execute_plan_simulated_failure(tmp_path: Path):
    run_dir = tmp_path / "runs"

    steps = [
        Step(id=1, description="step1"),
        Step(id=2, description="step2"),
        Step(id=3, description="step3"),
    ]

    result = execute_plan(
        ticket_id="T_FAIL",
        steps=steps,
        run_dir=run_dir,
        fail_step_id=2,   # ← simulate failure here
    )

    # execution should stop early
    assert result.step_count == 2

    # system should mark failure
    assert result.failed is True

    # artifact should exist
    artifact_path = Path(result.artifact_path)
    assert artifact_path.exists()

    # artifact should reflect failure state
    text = artifact_path.read_text()
    assert "DRY_RUN_FAILED" in text
    assert '"status": "failed"' in text

