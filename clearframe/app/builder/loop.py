from pathlib import Path
from ..core.engine import ClearframeEngine
from ..core.llm import MockClient, GeminiClient
from .planner import load_ticket
import os
import json
import time
from types import SimpleNamespace

def run_local_loop(repo_root=None, fail_step_id=None):
    provider = os.getenv("CLEARFRAME_LLM_PROVIDER", "mock")
    
    if provider == "gemini":
         try:
             from google import genai
             llm = GeminiClient(os.getenv("GEMINI_API_KEY"))
         except ImportError:
             print("⚠️ Gemini library missing. Falling back to Mock.")
             llm = MockClient()
    else:
         llm = MockClient()

    engine = ClearframeEngine(llm_client=llm)
    
    root = Path(repo_root) if repo_root else Path(".")
    incoming = root / "clearframe/tickets/incoming"
    runs_dir = root / "clearframe/tickets/runs"
    
    timestamp = time.strftime("%Y%m%dT%H%M%SZ")
    run_path = runs_dir / timestamp
    run_path.mkdir(parents=True, exist_ok=True)
    
    print(f"🚀 Starting Loop [Provider: {provider.upper()}]")
    
    processed_count = 0
    if not incoming.exists():
        print(f"⚠️  No incoming folder found at {incoming}")
        return SimpleNamespace(processed=0, run_dir=run_path)

    for ticket_file in incoming.glob("*.json"):
        if ticket_file.name.endswith(".done.json"): continue

        try:
            ticket = load_ticket(ticket_file)
            print(f"Processing {ticket.ticket_id}...")
            
            output = engine.analyze(ticket.body, ticket.bias_type, ticket.signal_strength)
            
            if output.intervention_type == "NO":
                print(f"⚪ [SKIP] Silence maintained for {ticket.ticket_id}")
                continue

            icon = "🟢" if output.intervention_type == "YES" else "🟡"
            print(f"{icon} [{output.intervention_type}] Bias Detected: {output.bias_context}")
            
            with open(run_path / f"{ticket.ticket_id}.execution.json", "w") as f:
                json.dump({"ticket": str(ticket), "analysis": str(output)}, f, indent=2)

            new_name = ticket_file.with_name(f"{ticket_file.stem}.done.json")
            ticket_file.rename(new_name)
            processed_count += 1
            
        except Exception as e:
            print(f"❌ Error: {e}")
            
    if processed_count == 0:
        print("✨ No new tickets to process.")

    # --- FINAL FIX: Return processed AND run_dir ---
    return SimpleNamespace(processed=processed_count, run_dir=run_path)
