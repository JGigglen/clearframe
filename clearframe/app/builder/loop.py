from __future__ import annotations
import shutil
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

from .planner import build_plan, load_ticket
from .executor import execute_plan
from ..core.llm import get_llm

def run_local_loop(repo_root: Path, fail_step_id: Optional[int] = None):
    incoming_dir = repo_root / "clearframe" / "tickets" / "incoming"
    runs_dir = repo_root / "clearframe" / "tickets" / "runs"
    
    runs_dir.mkdir(parents=True, exist_ok=True)
    
    tickets = [f for f in incoming_dir.glob("*.json") if not f.name.endswith(".done.json")]
    processed_count = 0
    latest_run_dir = None

    for ticket_path in tickets:
        # 1. Setup Run Directory
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        run_dir = runs_dir / timestamp
        run_dir.mkdir(parents=True, exist_ok=True)
        latest_run_dir = run_dir

        # 2. Load Ticket
        ticket = load_ticket(ticket_path)
        
        # 3. Reasoning Gate
        if ticket.ticket_id.startswith("T5"):
            print(f"🧠 Consulting Gemini: {ticket.ticket_id}")
            client = get_llm()
            
            analysis = client.consult_sunk_cost(ticket.body)
            reframe = client.reframe_sunk_cost({"text": ticket.body, "classification": "YES"})
            
            q = reframe.get('counterfactual') or reframe.get('Counterfactual', "N/A")
            r = reframe.get('rationale') or reframe.get('Rationale', "N/A")
            
            combined_output = (
                f"{analysis}\n\n"
                f"--- COUNTERFACTUAL FRAME ---\n"
                f"QUESTION: {q}\n"
                f"RATIONALE: {r}"
            )
            
            steps_to_execute = [{
                "id": 1, 
                "description": "Reasoning & Reframing Analysis", 
                "output": combined_output, 
                "status": "completed"
            }]
        else:
            plan = build_plan(ticket)
            steps_to_execute = plan.steps

        # 4. Execute and Archive
        execute_plan(ticket.ticket_id, steps_to_execute, run_dir, fail_step_id)
        done_path = ticket_path.with_suffix(".done.json")
        shutil.move(str(ticket_path), str(done_path))
        processed_count += 1

    class Result:
        def __init__(self, count, r_dir):
            self.processed = count
            self.run_dir = r_dir

    return Result(processed_count, latest_run_dir)