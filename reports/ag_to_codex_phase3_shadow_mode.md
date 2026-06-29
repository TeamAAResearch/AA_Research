# RESEARCH DIRECTIVE: Phase 3 Alpha-Decay Shadow-Mode Integration
**From:** AG (Research & Analysis)
**To:** Codex (Engineering & Execution)
**Date:** 2026-06-29

## Context
Phase 2 successfully built the standalone `exit_alpha_decay.py` logic. The GM has approved moving to Phase 3: integrating the module into the live `challenger.py` bot.

However, the HFT Architect and Systems Engineer rigorously rejected your initial "SQLite O(1)" caching proposal, citing severe latency and lock contention in the hot loop. The integration must strictly adhere to a zero-allocation, zero-I/O execution path.

## Phase 3 Engineering Task: Shadow-Mode Loop Integration

Please modify `saxo_trader/challenger.py` and any necessary background jobs to implement the following:

### 1. Zero-I/O Causal Baseline Precomputation
*   **Background Cron/Job:** Build a background mechanism (perhaps via `macro_regime_analyst.py` or a dedicated cron script) to calculate the 60-day baseline every 1-4 hours and save the `AlphaBaselineEstimate` to the SQLite `research_cache`.
*   **Zero-Allocation Hot Loop:** You must not query SQLite on every tick. The `challenger.py` trading loop must load the SQLite cache into a native Python dictionary (`_global_baseline_cache`) only on a heartbeat (e.g., every 5 minutes). 
*   **CachedAlphaBaseline:** Create a `CachedAlphaBaseline` class (inheriting from `CausalAlphaBaseline`) that is instantiated **once** at system startup. The hot loop must simply call `cached_baseline.estimate(...)` which reads from the in-memory dict with $O(1)$ memory lookup latency and zero GC instantiation pressure.

### 2. Catastrophic Fallbacks & Freshness Gateway
*   **Freshness Check:** The `CachedAlphaBaseline` estimate must include a `computed_at` timestamp. If the baseline is older than 6 hours, it must return `None` or throw an error, forcing `evaluate_alpha_decay_exit` into a fail-closed `ERROR` action.
*   **Absolute Hard Stop:** You must leave the absolute Catastrophic Hard Time-Stop (240 minutes) intact in the legacy code as the ultimate circuit breaker.

### 3. Shadow-Mode Routing
Inside `challenger.py._manage_open_positions`:
*   Construct the `AlphaExitInput` and call `safe_evaluate_alpha_decay_exit(exit_input, cached_baseline)`.
*   If the result is `SCALE_OUT` or `FLATTEN`, write a throttled, high-priority telemetry log to the `AA_JOURNAL` labeled `[SHADOW MODE: ALPHA DECAY TRIGGERED]`.
*   **CRITICAL:** Do NOT execute the physical scale-out or close commands. The live positions must remain governed by the legacy stops and time-decay rules for now.

## Next Steps for Codex
1. Implement the background caching logic and `CachedAlphaBaseline`.
2. Integrate the shadow-mode router into `challenger.py`.
3. Test thoroughly and run your engineering Red-Team review to verify zero-I/O compliance before committing.
