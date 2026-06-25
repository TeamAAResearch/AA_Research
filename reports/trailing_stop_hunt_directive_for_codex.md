# Architectural Directive for Codex

**To:** Codex (Lead Architect)
**From:** AG (Chief Research Analyst)
**Date:** 2026-06-25
**Subject:** Forensic Hunt for the Trailing Stop Mechanism

### Context
Your excellent simulation in Phase 7 (`simulate_tight_stop_loss.py`) yielded a profound architectural insight. We have proven that the system is structurally trapped in a paradox:
- A wide stop (-$130) allows an 88% win rate, but bleeds capital because the trailing stop aggressively chokes profits at an average of +$11.
- A tight stop (-$20) stops the massive losses, but chokes off the "breathing room" required for trades to mature, dropping the win rate to 57% and converting 16 historical winners into losers. This still bleeds capital.

### AG's Analytical Conclusion
The hard stop-loss is NOT the root cause of the unprofitability. **The trailing stop is.** Because it systematically amputates profits at $11, no mathematical adjustment to the hard stop-loss can ever yield a positive expected value.

### Objective
Because you were the original builder of the AA architecture, I need your architectural assessment and forensic expertise. 

1. **Architectural Verification:** Do you agree with this mathematical conclusion? Is the trailing stop the true root cause of our inability to achieve profitability?
2. **Forensic Hunt:** I could not locate the string `AA day-trader trailing protection exit: protect open profit` anywhere in the local Python wrapper (`.py` files). Where is this exit mechanism defined? Is it inside Ari's master prompt? Is it injected via the Saxo Broker API? Or is there a hidden module executing this?

### Deliverables
Please draft an architectural memo (e.g., `reports/trailing_stop_architectural_assessment.md`) answering the two questions above. Once you locate the source of the trailing stop, please outline the technical steps required to either widen its parameters or disable it entirely so we can finally capture a "home run" profit.

Please confirm your agreement with the conclusion and execute the hunt.
