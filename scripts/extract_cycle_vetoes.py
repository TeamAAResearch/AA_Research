import sqlite3
import csv
from pathlib import Path

DB_PATH = Path("../trading_system.sqlite3")
OUTPUT_PATH = Path("ledgers/cycle_vetoes.csv")

def run():
    if not DB_PATH.exists():
        print(f"Database not found at {DB_PATH.resolve()}")
        return

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    vetoes = []
    
    print("Extracting cycle vetoes...")
    journal = conn.execute("SELECT * FROM aa_journal WHERE action = 'BLOCK_NEW_ENTRIES'").fetchall()
    
    for row in journal:
        # Determine the vetoing agent based on staff advice or outcome snapshot
        blockers = row["outcome_snapshot"]
        veto_agent = "Unknown"
        if "Concentration veto" not in row["staff_advice"] and "Risk Officer" not in row["staff_advice"]:
            pass # Fallback parsing
            
        if "Portfolio Manager" in row["staff_advice"] and "Concentration veto" not in row["staff_advice"]:
            # Actually, staff_advice contains the full advice string, e.g. "{'agent': 'Risk Officer', 'advice': 'CLEAR'...}"
            # It's easier to parse outcome_snapshot which contains the exact blockers list
            pass
            
        if "Concentration limit" in blockers or "max exposure" in blockers.lower():
            veto_agent = "Portfolio Manager"
        elif "daily loss" in blockers.lower() or "downside gate" in blockers.lower():
            veto_agent = "Downside Limit"
        elif "Anomaly gate" in blockers.lower() or "critical anomaly" in blockers.lower():
            veto_agent = "Anomaly Scanner"
        elif "Risk" in blockers:
            veto_agent = "Risk Officer"
        else:
            veto_agent = blockers # Just use the exact block string if unknown
            
        vetoes.append({
            "timestamp": row["created_at"],
            "veto_agent": veto_agent,
            "raw_blockers": blockers
        })
        
    print(f"Writing {len(vetoes)} cycle vetoes to {OUTPUT_PATH}...")
    headers = ["timestamp", "veto_agent", "raw_blockers"]
    with open(OUTPUT_PATH, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(vetoes)
        
    print("Done.")

if __name__ == "__main__":
    run()
