from __future__ import annotations

import json
import platform
import sys
from dataclasses import asdict, dataclass, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Any, Optional

@dataclass(frozen=True)
class ExecutionResult:
    artifact_path: str
    step_count: int
    failed: bool 

def execute_plan(
    ticket_id: str, 
    steps: List[Any], 
    run_dir: Path, 
    fail_step_id: Optional[int] = None
) -> ExecutionResult:
    """
    Executes a plan by performing file system operations within a 
    deterministic sandbox (workspace).
    """
    run_dir.mkdir(parents=True, exist_ok=True)
    
    # Define the Workspace (The Sandbox)
    workspace = run_dir / "workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    
    processed_steps = []
    run_failed = False

    for step in steps:
        # 1. Setup Step Data
        if is_dataclass(step):
            s_data = asdict(step)
        elif hasattr(step, "copy"):
            s_data = step.copy()
        else:
            s_data = dict(step)

        # 2. Constitutional Check: Failure Simulation
        if fail_step_id is not None and s_data.get("id") == fail_step_id:
            s_data["status"] = "failed"
            s_data["output"] = f"Simulated failure at Step {fail_step_id}"
            processed_steps.append(s_data)
            run_failed = True
            break 
        
        desc = s_data.get("description", "")
        desc_lower = desc.lower().strip()

        # 3. COMMAND: WRITE (filename: content)
        if "write " in desc_lower:
            try:
                if ":" in desc:
                    parts = desc.split(":", 1)
                    cmd_and_path = parts[0].strip()
                    content = parts[1].strip()
                    
                    target_rel_path = cmd_and_path.replace("write ", "", 1).strip()
                    target_path = workspace / target_rel_path
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    target_path.write_text(content, encoding="utf-8")
                    s_data["output"] = f"Successfully wrote {len(content)} chars to {target_rel_path}"
                    s_data["status"] = "completed"
                else:
                    s_data["output"] = "Write command missing content (expected 'write file: content')"
                    s_data["status"] = "failed"
                    run_failed = True
            except Exception as e:
                s_data["status"] = "failed"
                s_data["output"] = f"Write Error: {str(e)}"
                run_failed = True

        # 4. COMMAND: CREATE (simple file touch)
        elif "create " in desc_lower:
            try:
                target_rel_path = desc_lower.replace("create ", "").strip()
                target_path = workspace / target_rel_path
                target_path.parent.mkdir(parents=True, exist_ok=True)
                
                target_path.write_text(f"# Created by Clearframe\n# Ticket: {ticket_id}", encoding="utf-8")
                s_data["output"] = f"Successfully created {target_rel_path}"
                s_data["status"] = "completed"
            except Exception as e:
                s_data["status"] = "failed"
                s_data["output"] = f"Create Error: {str(e)}"
                run_failed = True

        # 5. DEFAULT: Mark as completed if no command matched
        if (s_data.get("status") == "pending" or not s_data.get("status")) and not run_failed:
            s_data["status"] = "completed"
            
        processed_steps.append(s_data)
        if run_failed:
            break

    # 6. Construct Artifact
    status_label = "DRY_RUN_FAILED" if run_failed else "DRY_RUN"
    artifact = {
        "ticket_id": ticket_id,
        "status": status_label,
        "workspace_path": str(workspace),
        "steps": processed_steps,
        "meta": {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "python_version": sys.version,
            "platform": platform.platform(),
            "simulated_failure": run_failed
        },
    }

    out_path = run_dir / f"{ticket_id}.execution.json"
    out_path.write_text(json.dumps(artifact, indent=2), encoding="utf-8")

    return ExecutionResult(
        artifact_path=str(out_path),
        step_count=len(processed_steps),
        failed=run_failed
    )