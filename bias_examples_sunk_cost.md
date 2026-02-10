# Sunk Cost Bias — Calibration Examples

Purpose:
These examples define Clearframe’s detection thresholds.
They are used to calibrate sensitivity and prevent over-flagging.

Classification states:
- Yes: Active sunk-cost reasoning
- Possibly: Bias awareness or ambiguous influence
- No: Bias-neutralized reasoning
Question analyzed
“Should I ask for a raise because I’ve already been here six months and put in a lot of effort, even if I’m unsure how my boss will respond?”

Context
The user is evaluating whether to ask for a raise and explicitly cites past time and effort as the primary justification, while acknowledging uncertainty about future response.

Detected Bias
Sunk cost fallacy: Yes.
The decision is framed as being justified by unrecoverable past investment (time and effort), rather than by expected future outcomes.

User Action (as framed)
Considering a raise request on the basis of what has already been invested in the role.

Notes
This is a clean example of sunk-cost reasoning because the causal link is explicit: past investment → decision obligation. The uncertainty about future payoff further strengthens the signal. Clearframe intervention: YES

Example 2 — Tradeoff-aware framing

Question analyzed
“Is my desire to ask for a raise influenced by the time and effort I’ve already invested at this job, rather than by future outcomes?”

Context
The user is introspecting on whether their motivation is driven by past investment versus forward-looking considerations.

Detected Bias
Sunk cost fallacy: Possibly.
The question signals awareness of the bias but does not confirm that the decision is actually being driven by sunk costs.

User Action (as framed)
Examining internal reasoning to determine what factors are influencing the decision.

Notes
This framing does not commit the fallacy; it probes for it. The bias may be present, but evidence is insufficient to classify it as active without further reasoning statements. Clearframe intervention: SOFT

Example 3 — Counterfactual framing

Question analyzed
“Would it still make sense to ask for a raise now if I ignored the fact that I’ve already spent six months here?”

Context
The user reframes the decision by hypothetically removing all prior investment from consideration.

Detected Bias
Sunk cost fallacy: No.
The question actively neutralizes sunk costs and shifts evaluation to present conditions and future implications.

User Action (as framed)
Testing the robustness of the decision under a zero–prior-investment assumption.

Notes
This framing is specifically designed to avoid sunk-cost reasoning. It treats past investment as irrelevant to the decision logic, which is the correct structural antidote to the bias. Clearframe intervention: NO
