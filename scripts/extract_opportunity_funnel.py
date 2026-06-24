import sqlite3
import csv
import json
import os
from pathlib import Path

DB_PATH = Path("../trading_system.sqlite3")
OUTPUT_PATH = Path("ledgers/opportunity_funnel.csv")

def run():
    if not DB_PATH.exists():
        print(f"Database not found at {DB_PATH.resolve()}")
        return

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    funnel = []
    
    # 1. Extract Admitted Trades (challenger_positions)
    print("Extracting admitted trades...")
    positions = conn.execute("SELECT * FROM challenger_positions").fetchall()
    for row in positions:
        r = dict(row)
        funnel.append({
            "timestamp": r["opened_at"],
            "symbol": r["symbol"],
            "side": r["side"],
            "score": r["entry_score"],
            "decision": "Admitted",
            "block_reason": "",
            "entry_price": r["entry"],
            "stop_loss": r["stop_loss"],
            "take_profit": r["take_profit"],
            "session": r.get("session", "UNKNOWN")
        })
        
    # 2. Extract Blocked Trades (blocked_signals)
    print("Extracting blocked signals...")
    blocked = conn.execute("SELECT * FROM blocked_signals").fetchall()
    for row in blocked:
        metadata = {}
        if row["raw_metadata"]:
            try:
                metadata = json.loads(row["raw_metadata"])
            except Exception:
                pass
                
        admission_data = metadata.get("admission", {})
        score = admission_data.get("score", row["signal_score"])
        
        # Decide if it's a risk block or an admission block
        decision = "Blocked_Risk" if "Planned risk cap active" in row["block_reason"] else "Blocked_Admission"
        
        funnel.append({
            "timestamp": row["created_at"],
            "symbol": row["symbol"],
            "side": row["side"],
            "score": score,
            "decision": decision,
            "block_reason": row["block_reason"],
            "entry_price": metadata.get("entry_price", 0.0),
            "stop_loss": metadata.get("stop_loss", 0.0),
            "take_profit": metadata.get("take_profit", 0.0),
            "session": "UNKNOWN" # Session not explicitly tracked in blocked raw metadata currently, we can infer later if needed
        })
        
    # Sort chronologically
    funnel.sort(key=lambda x: x["timestamp"])
    
    # Write to CSV
    print(f"Writing {len(funnel)} records to {OUTPUT_PATH}...")
    headers = ["timestamp", "symbol", "side", "score", "decision", "block_reason", "entry_price", "stop_loss", "take_profit", "session"]
    with open(OUTPUT_PATH, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(funnel)
        
    print("Done.")

if __name__ == "__main__":
    run()
