import pandas as pd
import numpy as np
import vectorbt as vbt
import os

def run_ofi_simulation():
    data_path = '/Users/kennylee/Documents/Saxo/AA_Research/data/challenger_ticks.parquet'
    
    if not os.path.exists(data_path):
        print("Data not found.")
        return
        
    print("Loading Parquet data...")
    df = pd.read_parquet(data_path)
    df = df[df['symbol'] == 'EURUSD'].copy()
    df['created_at'] = pd.to_datetime(df['created_at'], format='ISO8601', utc=True)
    df = df.sort_values('created_at')
    df.set_index('created_at', inplace=True)
    
    # Resample to 1-minute bars
    bars = df['mid'].resample('1min').ohlc()
    bars.dropna(inplace=True)
    
    # 1. Base Signal: 60-minute Momentum Z-Score
    bars['momentum_60'] = bars['close'].diff(60)
    bars['mom_zscore'] = (bars['momentum_60'] - bars['momentum_60'].rolling(60).mean()) / (bars['momentum_60'].rolling(60).std() + 1e-8)
    
    base_entries_long = bars['mom_zscore'] > 1.5
    base_entries_short = bars['mom_zscore'] < -1.5
    exits = (bars['mom_zscore'] < 0.5) & (bars['mom_zscore'] > -0.5)
    
    # 2. OFI Proxy: Tick Imbalance (Up-ticks vs Down-ticks in the 1-minute bar)
    # We will count how many ticks moved up vs down in each minute
    tick_diffs = np.sign(df['mid'].diff())
    
    # Resample tick signs to get sum of up/down ticks per minute
    tick_imbalance = tick_diffs.resample('1min').sum()
    tick_imbalance = tick_imbalance.reindex(bars.index).fillna(0)
    
    # Veto condition: 
    # If momentum says LONG, but the tick imbalance in the last 5 minutes is heavily SHORT, veto.
    rolling_imbalance = tick_imbalance.rolling(5).sum()
    
    # Filtered Signals
    filtered_entries_long = base_entries_long & (rolling_imbalance > 0)
    filtered_entries_short = base_entries_short & (rolling_imbalance < 0)
    
    print(f"\n--- Simulating Order Flow Imbalance (Tick Proxy) on EURUSD ({len(bars)} 1-min bars) ---")
    
    pf_base = vbt.Portfolio.from_signals(
        bars['close'],
        entries=base_entries_long,
        exits=exits,
        short_entries=base_entries_short,
        short_exits=exits,
        init_cash=100000,
        fees=0.0001,
        freq='1min'
    )
    
    pf_filtered = vbt.Portfolio.from_signals(
        bars['close'],
        entries=filtered_entries_long,
        exits=exits,
        short_entries=filtered_entries_short,
        short_exits=exits,
        init_cash=100000,
        fees=0.0001,
        freq='1min'
    )
    
    print("\n[UNFILTERED BASE MOMENTUM]")
    print(f"Total Trades: {pf_base.stats()['Total Trades']}")
    print(f"Win Rate: {pf_base.stats()['Win Rate [%]']:.2f}%")
    print(f"Profit Factor: {pf_base.stats()['Profit Factor']:.2f}")
    
    print("\n[OFI-FILTERED MOMENTUM]")
    print(f"Total Trades: {pf_filtered.stats()['Total Trades']}")
    print(f"Win Rate: {pf_filtered.stats()['Win Rate [%]']:.2f}%")
    print(f"Profit Factor: {pf_filtered.stats()['Profit Factor']:.2f}")
    
    if pf_filtered.stats()['Profit Factor'] > pf_base.stats()['Profit Factor']:
        print("\nCONCLUSION: Order Flow Imbalance (Tick Proxy) successfully filters toxic entries and improves expectancy.")
    else:
        print("\nCONCLUSION: The OFI filter failed to improve edge on this dataset.")

if __name__ == '__main__':
    run_ofi_simulation()
