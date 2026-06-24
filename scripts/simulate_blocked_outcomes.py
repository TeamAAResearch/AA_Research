import sqlite3
import csv
import os
from datetime import datetime
from pathlib import Path

DB_PATH = Path("../trading_system.sqlite3")
FUNNEL_PATH = Path("ledgers/opportunity_funnel.csv")
OUTPUT_PATH = Path("ledgers/opportunity_funnel_simulated.csv")

def run():
    if not DB_PATH.exists() or not FUNNEL_PATH.exists():
        print("Missing database or funnel CSV.")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    funnel = []
    with open(FUNNEL_PATH, "r") as f:
        reader = csv.DictReader(f)
        funnel = list(reader)
        
    print(f"Simulating outcomes for {len(funnel)} opportunities...")
    
    for row in funnel:
        if row["decision"] == "Admitted":
            # Realized outcomes are not MFE/MAE here for simplicity, but could be queried
            row["simulated_outcome"] = "Executed_Real"
            row["simulated_mfe"] = ""
            row["simulated_mae"] = ""
            continue
            
        entry_price = float(row["entry_price"])
        stop_loss = float(row["stop_loss"])
        take_profit = float(row["take_profit"])
        
        if entry_price <= 0 or stop_loss <= 0 or take_profit <= 0:
            row["simulated_outcome"] = "No_Risk_Brackets"
            row["simulated_mfe"] = ""
            row["simulated_mae"] = ""
            continue
            
        # Query ticks
        symbol = row["symbol"]
        side = row["side"]
        start_time = row["timestamp"]
        
        ticks = conn.execute(
            "SELECT mid FROM challenger_ticks WHERE symbol = ? AND created_at > ? ORDER BY id ASC LIMIT 5000",
            (symbol, start_time)
        ).fetchall()
        
        if not ticks:
            row["simulated_outcome"] = "No_Ticks_Found"
            row["simulated_mfe"] = ""
            row["simulated_mae"] = ""
            continue
            
        mfe = 0.0
        mae = 0.0
        outcome = "Open/Timeout"
        
        for tick in ticks:
            mid = tick["mid"]
            
            # Calculate current PNL in price terms
            if side == "Buy":
                pnl = mid - entry_price
                current_mfe = max(0, pnl)
                current_mae = min(0, pnl)
            else:
                pnl = entry_price - mid
                current_mfe = max(0, pnl)
                current_mae = min(0, pnl)
                
            mfe = max(mfe, current_mfe)
            mae = min(mae, current_mae)
            
            # Check stops
            if side == "Buy":
                if mid <= stop_loss:
                    outcome = "Hit_Stop_Loss"
                    break
                elif mid >= take_profit:
                    outcome = "Hit_Take_Profit"
                    break
            else:
                if mid >= stop_loss:
                    outcome = "Hit_Stop_Loss"
                    break
                elif mid <= take_profit:
                    outcome = "Hit_Take_Profit"
                    break
                    
        row["simulated_outcome"] = outcome
        row["simulated_mfe"] = round(mfe, 5)
        row["simulated_mae"] = round(mae, 5)

    print(f"Writing simulated outcomes to {OUTPUT_PATH}...")
    headers = list(funnel[0].keys())
    with open(OUTPUT_PATH, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(funnel)
        
    # Replace old funnel with new one
    os.replace(OUTPUT_PATH, FUNNEL_PATH)
    print("Done.")

if __name__ == "__main__":
    run()
