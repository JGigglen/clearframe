# Clearframe (v0.1.1)
### The Deterministic Reasoning Analysis Engine

Clearframe is a specialized framework designed to bridge the gap between deterministic software execution and probabilistic machine reasoning. It detects when human decisions are influenced by cognitive biases and generates counterfactual frames to reset perspective before a commitment is made.

> **The Clearframe Constitution:**
> 1. Clearframe is decision hygiene, not decision control.
> 2. It does **not** give advice. It does **not** recommend actions.
> 3. It identifies patterns and presents mirrors.
> 4. The human always decides.

[Image of a software architecture diagram showing the separation between a deterministic logic layer and an LLM reasoning layer]

---

## 🛠 Core Architecture: Logic-First, Model-Second

Unlike typical AI "wrappers," Clearframe treats the LLM as a modular advisory component, not the core controller. The system follows a strict linear pipeline:

1.  **Ticket Ingestion:** Raw JSON inputs are parsed for structural integrity.
2.  **Prefix Routing:** The system identifies the "Intent" via prefixes (e.g., `T5-` for Reasoning Analysis).
3.  **Heuristic Filtering:** Signal strength is measured. If a bias is detected with high confidence by deterministic rules, the system acts immediately.
4.  **Conditional Intelligence (LLM Consult):** Only when deep semantic analysis is required does the engine consult **Gemini 2.5 Flash**.
5.  **Structured Artifact Generation:** Results are saved in immutable JSON run-logs for total auditability.

---

## 🧠 v0 Scope: Sunk Cost Detection & Reframing

For the v0 release, Clearframe is hyper-focused on the **Sunk Cost Fallacy**—the most common reasoning error in project management and software development.

### The ClearframeReframe™ Move
When a bias is detected, the engine doesn't tell the user "you are wrong." Instead, it generates a **Counterfactual Frame**:
* **Constraint:** A single question under 25 words.
* **Goal:** Remove past investment (time/money/effort) from the reasoning.
* **Result:** A "Day Zero" perspective that allows for rational capital allocation.

[Image of a cognitive bias flowchart showing the transition from sunk cost reasoning to a counterfactual decision point]

---

## 🚀 Execution Loop & Artifact System

Clearframe features a robust execution loop that ensures every reasoning analysis is reproducible.

* **Ticket Path:** `clearframe/tickets/incoming/`
* **Run Path:** `clearframe/tickets/runs/[timestamp]/`
* **Artifacts:** Every run produces an `.execution.json` file containing:
    * The raw input reasoning.
    * The LLM's narrative analysis.
    * The structured Counterfactual Question and Rationale.

### CLI Commands
| Command | Action |
| :--- | :--- |
| `python -m clearframe.app.builder.cli run` | Processes all incoming tickets and runs the engine. |
| `python -m clearframe.app.builder.cli replay` | Replays the most recent run with beautiful terminal formatting. |

---

## 📐 Design Philosophy: The Engineering Rules

Clearframe is built under a set of "Senior-Grade" constraints to ensure long-term stability:

* **Minimal Abstraction:** We avoid complex frameworks. The code is pure Python, making the logic transparent and the boundaries modular.
* **Scaffolding Before Automation:** The execution loop was perfected with "Mock" data before a single AI call was integrated.
* **Zero-Hallucination Policy:** By using **Constrained Output (JSON Mode)**, we force the AI to adhere to our data schemas, preventing conversational "drift."
* **Conservative Outputs:** If the engine cannot confidently identify a pattern, it remains silent rather than risking a false positive.

---

## 📊 Roadmap & Current Status

- [x] **v0.1.0 — Engine Stable:** Deterministic loop, ticket system, and artifact logging.
- [x] **v0.1.1 — Intelligence Integrated:** Gemini 2.5 Flash integration and Sunk Cost Reframer.
- [ ] **v0.2.0 — Multi-Bias Support:** Integration of Confirmation Bias and Recency Bias gates.
- [ ] **v0.3.0 — Evaluation Layer:** A system for humans to rate the quality of the Reframer's questions.

---

## 👨‍💻 Author
**JGigglen**
*Developing tools for safer, saner human-AI collaboration.*

---

## ⚖️ License
MIT License - See LICENSE for details.

