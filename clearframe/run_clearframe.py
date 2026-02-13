from app.core.engine import analyze

def main():
    print("\nClearframe v0 (Offline) — Sunk Cost Check")
    print("Paste a decision and press Enter. Ctrl+C to quit.\n")

    while True:
        try:
            text = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        out = analyze(text)

        print("\nClassification:", out.detection.classification)
        print("Reasoning:", out.detection.reasoning)

        if out.intervention_text:
            print("\n" + out.intervention_text)
        else:
            print("\n(No intervention.)")

        print("\n---\n")

if __name__ == "__main__":
    main()
