import pandas as pd
import numpy as np
import os

def simulate_inventory_pegging():
    data_path = '/Users/kennylee/Documents/Saxo/AA_Research/data/challenger_ticks.parquet'
    
    if not os.path.exists(data_path):
        print("Data not found.")
        return
        
    print("Loading Parquet data...")
    df = pd.read_parquet(data_path)
    df = df[df['symbol'] == 'EURUSD'].copy()
    df['created_at'] = pd.to_datetime(df['created_at'], format='ISO8601', utc=True)
    df = df.sort_values('created_at')
    
    # Take a small snapshot of actual market conditions
    sample = df.iloc[-1000:].copy()
    
    # Calculate rolling variance (proxy for sigma^2)
    sample['variance'] = sample['mid'].rolling(100).var() * 100000 # scale up for FX pips
    
    # Grab the final tick
    last_tick = sample.iloc[-1]
    mid = last_tick['mid']
    ask = last_tick['ask']
    bid = last_tick['bid']
    market_spread = ask - bid
    sigma2 = last_tick['variance']
    
    # Avellaneda-Stoikov Parameters
    gamma = 0.05 # Risk aversion
    
    print("\n=== AVELLANEDA & STOIKOV: INVENTORY PEGGING SIMULATION ===")
    print(f"Market Snapshot -> MID: {mid:.5f} | BID: {bid:.5f} | ASK: {ask:.5f} | SPREAD: {market_spread:.5f}")
    print(f"Risk Aversion (Gamma): {gamma} | Variance Proxy: {sigma2:.5f}\n")
    
    print(f"{'Inventory (q)':<15} | {'Reservation (r)':<15} | {'Our Bid Peg':<15} | {'Our Ask Peg':<15} | {'Behavior'}")
    print("-" * 90)
    
    # Simulate various inventory levels (e.g., -5 (heavy short) to +5 (heavy long))
    for q in range(-5, 6):
        # Reservation price shifts based on inventory
        reservation_price = mid - (q * gamma * sigma2)
        
        # Our optimal quotes around the reservation price
        # (Assuming we want to capture the market spread, but skewed by inventory)
        our_bid = reservation_price - (market_spread / 2)
        our_ask = reservation_price + (market_spread / 2)
        
        if q == 0:
            behavior = "Neutral (Pegged exactly to Market Mid)"
        elif q > 0:
            behavior = "Dumping Risk (Ask peg crosses spread, Bid peg retreats)"
        else:
            behavior = "Covering Risk (Bid peg crosses spread, Ask peg retreats)"
            
        print(f"{q:<15} | {reservation_price:<15.5f} | {our_bid:<15.5f} | {our_ask:<15.5f} | {behavior}")

    print("\nCONCLUSION: Institutional Scale-In must adopt this equation.")
    print("If Ari scales into 4 positions and is heavily long, her next limit-exit must artificially lower its peg to cross the spread and exit risk faster.")

if __name__ == '__main__':
    simulate_inventory_pegging()
