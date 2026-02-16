from __future__ import annotations
import shutil
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

from .planner import build_plan
from .executor import execute_plan
from ..core.llm import get_llm  # The brain socket we just built

def run_local_loop(repo_root: Path, fail_step_id: Optional[int] = None):
    incoming_dir = repo_root / "clearframe" / "tickets" / "incoming"
    runs_dir = repo_root / "clearframe" / "tickets" / "runs"
    
    tickets = list(incoming_dir.glob("*.json"))
    processed_count = 0
    latest_run_dir = None

    for ticket_path in tickets:
        if ticket_path.name.endswith(".done.json"):
            continue

        # 1. Setup Deterministic Run Directory
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        run_dir = runs_dir / timestamp
        run_dir.mkdir(parents=True, exist_ok=True)
        latest_run_dir = run_dir

        # 2. Load and Prepare
        from .planner import load_ticket # Assuming your loader is here
        ticket = load_ticket(ticket_path)
        
        # 3. CONSTITUTIONAL GATE: Intelligence vs. Scaffolding
        # If the ticket is a T5 (Bias Test), we consult the LLM directly
        if ticket.ticket_id.startswith("T5"):
            print(f"🧠 Consulting Gemini for reasoning analysis on {ticket.ticket_id}...")
            client = get_llm() # Automatically gets Gemini via your env var
            analysis_result = client.consult_sunk_cost(ticket.body)
            
            # We inject the analysis into a virtual 'plan' so the executor can log it
            plan = build_plan(ticket) 
            # We override the first step to show the brain's output
            steps_to_execute = [{"id": 1, "description": "Reasoning Analysis", "output": analysis_result, "status": "completed"}]
        else:
            # Standard Builder Path (Code Writing)
            plan = build_plan(ticket)
            steps_to_execute = plan.steps

        # 4. Execute and Generate Artifact
        execute_plan(ticket.ticket_id, steps_to_execute, run_dir, fail_step_id)

        # 5. Archive Ticket (Smallest Safe Step)
        done_path = ticket_path.with_suffix(".done.json")
        shutil.move(str(ticket_path), str(done_path))
        processed_count += 1

    class Result:
        def __init__(self, count, r_dir):
            self.processed = count
            self.run_dir = r_dir

    return Result(processed_count, latest_run_dir)