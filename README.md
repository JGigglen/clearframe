# ⚖️ Clearframe (v0.2.2)
### The Deterministic Reasoning Analysis Engine

Clearframe is a specialized framework designed to bridge the gap between deterministic software execution and probabilistic machine reasoning. It detects when human decisions are influenced by cognitive biases and generates counterfactual frames to reset perspective before a commitment is made.

> **The Clearframe Constitution:**
> 1. Clearframe is decision hygiene, not decision control.
> 2. It does **not** give advice. It does **not** recommend actions.
> 3. It identifies patterns and presents mirrors.
> 4. **Silence-First:** If signal strength is < 0.3, the engine remains silent.
> 5. The human always decides.

[Image of a software architecture diagram showing the separation between a deterministic logic layer and an LLM reasoning layer]

---

## 🛠 Core Architecture: Logic-First, Model-Second

Unlike typical AI "wrappers," Clearframe treats the LLM as a modular advisory component, not the core controller. The system follows a strict linear pipeline:

1.  **Ticket Ingestion:** Raw JSON inputs are parsed with defensive error handling (v0.2.2).
2.  **Weighted Election:** The engine calculates keyword density across multiple bias signatures simultaneously.
3.  **The Constitutional Gate:** Signal strength is measured. If the "Silence" threshold is met, the engine acts.
4.  **Conditional Intelligence (LLM Consult):** The engine consults **Gemini 2026 Standard** using a unified `analyze_bias` contract.
5.  **Structured Artifact Generation:** Results are saved in immutable JSON run-logs for total auditability.

---

## 🧠 v0.2 Scope: Multi-Bias Detection & Reframing

Clearframe now utilizes **Election Logic** to detect the strongest signal among competing biases:

* **T5 (Sunk Cost):** Removes past investment (time/money/effort) from the reasoning.
* **T6 (Confirmation Bias):** Challenges the "proves I'm right" feedback loop.
* **T7 (Recency Bias):** Mitigates the weight of "breaking news" or "latest posts."

### The ClearframeReframe™ Move
When a bias is detected, the engine doesn't tell the user "you are wrong." Instead, it generates a **Counterfactual Frame**:
* **Constraint:** A single question under 25 words.
* **Goal:** A "Day Zero" perspective that allows for rational capital allocation.

[Image of a cognitive bias flowchart showing the transition from sunk cost reasoning to a counterfactual decision point]

---

## 🚀 Execution & Stabilization

Clearframe is now a fully-discoverable Python package.

### Installation
```powershell
# Install in editable mode to enable constitutional testing
pip install -e .

Command,Action
python -m clearframe.app.builder.cli run,Processes all incoming tickets and runs the engine.
python -m clearframe.app.builder.cli replay,Replays the most recent run with beautiful terminal formatting.
pytest tests/test_constitution.py,Verifies the engine adheres to the Silence-First policy.

📐 Design Philosophy: The Engineering Rules
Contract Freeze: One canonical engine interface (analyze) prevents interface drift.

Defensive Ingestion: Handles malformed JSON and plain-text inputs without crashing.

Minimal Abstraction: Pure Python, zero complex frameworks.

Conservative Outputs: If the engine cannot confidently identify a pattern, it remains silent.

📊 Roadmap & Current Status
[x] v0.1.0 — Engine Stable: Deterministic loop and artifact logging.

[x] v0.1.1 — Intelligence Integrated: Gemini integration and Sunk Cost Reframer.

[x] v0.2.2 — Stabilization & Multi-Bias: Weighted Election logic and Constitutional Testing.

[ ] v0.3.0 — Evaluation Layer: A system for humans to rate the quality of the Reframer's questions.

👨‍💻 Author
JGigglen
Developing tools for safer, saner human-AI collaboration.

⚖️ License
MIT License - See LICENSE for details.