import json
from pathlib import Path

def show_last_run(runs_dir: Path):
    folders = sorted([d for d in runs_dir.iterdir() if d.is_dir()])
    if not folders:
        print("No runs found.")
        return

    latest_run = folders[-1]
    exec_files = list(latest_run.glob("*.execution.json"))
    if not exec_files:
        print(f"No execution artifact in {latest_run.name}")
        return

    data = json.loads(exec_files[0].read_text(encoding="utf-8"))

    print("\n" + "═"*40)
    print(f" 📺 REPLAYING RUN: {data.get('ticket_id')}")
    print(f" Status: {data.get('status')}")
    print("─"*40)

    for step in data.get("steps", []):
        status_icon = "✅" if step.get("status") == "completed" else "❌"
        print(f" {status_icon} {step.get('description')}")
        
        output = step.get("output")
        if output:
            print(f"\n   🧠 BRAIN OUTPUT:\n   {output}\n")
            print("─"*40)

    print("═"*40 + "\n")