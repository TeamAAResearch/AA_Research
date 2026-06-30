import pandas as pd
import vectorbt as vbt
import time
import os

def run_prototype():
    data_path = '/Users/kennylee/Documents/Saxo/AA_Research/data/challenger_ticks.parquet'
    
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Please run export_to_parquet.py first.")
        return
        
    print("Loading Parquet data...")
    start_time = time.time()
    
    # Load the Parquet file
    df = pd.read_parquet(data_path)
    
    load_time = time.time() - start_time
    print(f"Loaded {len(df)} ticks in {load_time:.2f} seconds.")
    
    # Let's filter for a specific symbol to prototype the simulator
    symbol = 'EURUSD'
    df_sym = df[df['symbol'] == symbol].copy()
    
    if df_sym.empty:
        print(f"No data for {symbol}. Trying the first available symbol.")
        symbol = df['symbol'].iloc[0]
        df_sym = df[df['symbol'] == symbol].copy()
        
    print(f"Prototyping VectorBT Simulation on {len(df_sym)} ticks of {symbol}...")
    
    # Sort by time and set as index
    df_sym = df_sym.sort_values('created_at')
    df_sym.set_index('created_at', inplace=True)
    
    # We will use 'mid' price for the simulation
    price = df_sym['mid']
    
    sim_start = time.time()
    
    # Define a simple fast vs slow moving average crossover using VectorBT's optimized indicators
    # This represents the kind of rapid parameter sweeping we can do
    fast_ma = vbt.MA.run(price, window=50, short_name='fast')
    slow_ma = vbt.MA.run(price, window=200, short_name='slow')
    
    # Generate entry and exit signals
    entries = fast_ma.ma_crossed_above(slow_ma)
    exits = fast_ma.ma_crossed_below(slow_ma)
    
    # Run the backtest instantly using vectorbt's portfolio engine
    pf = vbt.Portfolio.from_signals(
        price,
        entries,
        exits,
        init_cash=100000,
        fees=0.0001, # Simulate slippage/spread
        freq='1s' # Approximate tick frequency
    )
    
    sim_time = time.time() - sim_start
    
    print(f"\nSimulation Complete in {sim_time:.4f} seconds!")
    print("\n--- VectorBT Portfolio Performance ---")
    print(pf.stats())
    
    print("\nVectorBT Prototype Successful. Infrastructure is ready for Phase 5 Exits & VC Filter implementation.")

if __name__ == '__main__':
    run_prototype()
