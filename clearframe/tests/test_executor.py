from pathlib import Path
from clearframe.app.builder.executor import execute_plan
from clearframe.app.builder.planner import Step


def test_execute_plan_creates_artifact(tmp_path: Path):
    run_dir = tmp_path / "runs"
    run_dir.mkdir(parents=True, exist_ok=True)

    steps = [
        Step(id=1, description="step1"),
        Step(id=2, description="step2"),
    ]

    result = execute_plan(
        ticket_id="T1",
        steps=steps,
        run_dir=run_dir,
    )

    assert result.step_count == 2
    assert Path(result.artifact_path).exists()
    assert result.failed is False

