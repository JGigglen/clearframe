from __future__ import annotations
import shutil
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, List

# Internal Clearframe Imports
from .planner import build_plan, load_ticket
from .executor import execute_plan
from ..core.engine import ClearframeEngine 

def run_local_loop(repo_root: Path, fail_step_id: Optional[int] = None):
    """
    The Orchestrator: Moves tickets through the Clearframe pipeline.
    """
    incoming_dir = repo_root / "clearframe" / "tickets" / "incoming"
    runs_dir = repo_root / "clearframe" / "tickets" / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Collect all tickets that aren't finished yet
    tickets = [f for f in incoming_dir.glob("*.json") if not f.name.endswith(".done.json")]
    processed_count = 0
    latest_run_dir = None
    
    # 2. Initialize the Engine (The logic-center)
    engine = ClearframeEngine()

    for ticket_path in tickets:
        # Create a timestamped folder for this specific run
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        run_dir = runs_dir / timestamp
        run_dir.mkdir(parents=True, exist_ok=True)
        latest_run_dir = run_dir

        # STEP A: Load the ticket (Planner calculates signal_strength here)
        ticket = load_ticket(ticket_path)
        
        # STEP B: Consult the Engine (The 'Contract Freeze' move)
        # We don't call Gemini here anymore; the Engine handles that.
        output = engine.analyze(
            text=ticket.body, 
            bias_type=ticket.bias_type, 
            signal_strength=ticket.signal_strength
        )
        
        # STEP C: Decide what steps to show the user
        if output.intervention_type != "NO":
            # If the engine detected a bias, we show the Analysis
            combined_text = f"{output.analysis}\n\n--- REFRAME ---\nQ: {output.counterfactual}"
            steps_to_execute = [{
                "id": 1, 
                "description": f"Engine Analysis ({output.intervention_type})", 
                "output": combined_text, 
                "status": "completed"
            }]
        else:
            # If signal is low, we stay SILENT and just show the normal task steps
            plan = build_plan(ticket)
            # Convert Step objects to dictionaries for the executor
            steps_to_execute = [
                {"id": s.id, "description": s.description, "status": s.status, "output": s.output} 
                for s in plan.steps
            ]

        # STEP D: Record the results and move the ticket to 'done'
        execute_plan(ticket.ticket_id, steps_to_execute, run_dir, fail_step_id)
        
        done_path = ticket_path.with_suffix(".done.json")
        shutil.move(str(ticket_path), str(done_path))
        processed_count += 1

    # Return a simple result object for the CLI to print
    return type('Result', (), {'processed': processed_count, 'run_dir': latest_run_dir})