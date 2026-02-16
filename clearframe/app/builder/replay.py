from __future__ import annotations
import json
from pathlib import Path

def show_last_run(runs_dir: Path) -> None:
    # 1. Find all subfolders in the runs directory
    # These are named like 20260216T...
    folders = [d for d in runs_dir.iterdir() if d.is_dir()]
    
    if not folders:
        print("No run folders found.")
        return

    # 2. Sort folders by name (since they are timestamped, the last is the newest)
    # This is more reliable than the index.json for local testing
    latest_folder = sorted(folders)[-1]
    
    # 3. Find the execution artifact inside that folder
    artifact_files = list(latest_folder.glob("*.execution.json"))

    if not artifact_files:
        print(f"No artifact found in the newest folder: {latest_folder.name}")
        return

    # 4. Show the most recent file found in that folder
    # Sort these too, just in case there are multiple (like T1 and T2)
    latest_artifact = sorted(artifact_files, key=lambda p: p.stat().st_mtime)[-1]
    details = json.loads(latest_artifact.read_text(encoding="utf-8"))

    print("\n" + "═"*40)
    print(f" 📺 REPLAYING RUN: {details.get('ticket_id', 'Unknown')}")
    print(f" Status: {details.get('status')}")
    print("─" * 40)
    
    for step in details.get("steps", []):
        status = step.get("status", "pending")
        # Now we handle the 'failed' status visually
        icon = "✅" if status in ["done", "completed"] else "❌" if status == "failed" else "⏳"
        print(f" {icon} Step {step.get('id')}: {step.get('description')}")
        
        # If it failed, show why!
        if status == "failed":
            print(f"    ⚠️  Error: {step.get('output', 'Unknown error')}")
    
    print("═"*40 + "\n")