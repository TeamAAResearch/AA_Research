# RESEARCH DIRECTIVE: Repository Structural Cleanup
**From:** AG (Research & Analysis)
**To:** Codex (Engineering & Execution)
**Date:** 2026-06-30

## Context
A forensic scan of the repository revealed severe technical debt and structural pollution in the root directory. The GM has approved a ruthless cleanup plan. 

As per the Role Boundary doctrine, AG has designed the cleanup map, and Codex must execute it.

## Engineering Tasks

Please execute the following file operations immediately:

### 1. Nuke Legacy `saxo_bot` Tree
- Execute `rm -rf saxo_bot`. This recursive directory is entirely obsolete. The active engine is `saxo_trader`.

### 2. Purge Dead Database
- Execute `rm trade_store.sqlite3`. This database has 0 references in the codebase. (`trading_system.sqlite3` and `trading_memory.sqlite3` remain active).

### 3. Organize Mac Shortcuts
- `mkdir mac_shortcuts`
- Move all `*.command` files (there are ~15 in the root) into `mac_shortcuts/`.

### 4. Sandbox Scripts
- `mkdir -p tests/sandbox`
- Move `test_sqlite.py`, `test_vol.py`, and `test_yf.py` into `tests/sandbox/`.

### 5. Orphaned Data & Scripts
- Move `DAT_ASCII_USDJPY_M1_2022.zip` into `outputs/histdata/`.
- `rm start_ari.sh` (Obsolete, superseded by `scripts/start_challenger.sh` and the `.command` files).

## Verification
Ensure `pytest` still passes after the relocation and that no active `.plist` launchagents have broken paths due to the `.command` relocation.
