import pandas as pd
import numpy as np
import vectorbt as vbt
import os

def run_stat_arb_simulation():
    data_path = '/Users/kennylee/Documents/Saxo/AA_Research/data/challenger_ticks.parquet'
    
    if not os.path.exists(data_path):
        print("Data not found.")
        return
        
    print("Loading Parquet data...")
    df = pd.read_parquet(data_path)
    df['created_at'] = pd.to_datetime(df['created_at'], format='ISO8601', utc=True)
    df = df.sort_values('created_at')
    
    # Extract EURUSD and GBPUSD
    df_eur = df[df['symbol'] == 'EURUSD'].copy()
    df_gbp = df[df['symbol'] == 'GBPUSD'].copy()
    
    df_eur.set_index('created_at', inplace=True)
    df_gbp.set_index('created_at', inplace=True)
    
    # Resample to 1-minute bars and synchronize
    eur_bars = df_eur['mid'].resample('1min').last()
    gbp_bars = df_gbp['mid'].resample('1min').last()
    
    # Forward fill missing minutes to keep them perfectly synced
    data = pd.DataFrame({'EURUSD': eur_bars, 'GBPUSD': gbp_bars}).ffill().dropna()
    
    print(f"\n--- Processing Statistical Arbitrage ({len(data)} synchronized 1-min bars) ---")
    
    # Simple Log Spread (Proxy for Cointegration)
    # Log prices stabilize the variance of the spread
    data['log_eur'] = np.log(data['EURUSD'])
    data['log_gbp'] = np.log(data['GBPUSD'])
    
    # Calculate rolling hedge ratio (simple ratio of means over 120 minutes)
    window = 120
    data['hedge_ratio'] = data['log_eur'].rolling(window).mean() / data['log_gbp'].rolling(window).mean()
    
    # Calculate the Spread
    data['spread'] = data['log_eur'] - (data['hedge_ratio'] * data['log_gbp'])
    
    # Calculate Rolling Z-Score of the Spread
    spread_mean = data['spread'].rolling(window).mean()
    spread_std = data['spread'].rolling(window).std()
    data['z_score'] = (data['spread'] - spread_mean) / (spread_std + 1e-8)
    
    # Trading Logic (Avellaneda & Lee)
    # Short the spread if Z > 2 (EURUSD is overpriced relative to GBPUSD)
    # Buy the spread if Z < -2 (EURUSD is underpriced relative to GBPUSD)
    # Exit when Z crosses 0
    
    entries_short_spread = data['z_score'] > 2.0
    exits_short_spread = data['z_score'] <= 0.0
    
    entries_long_spread = data['z_score'] < -2.0
    exits_long_spread = data['z_score'] >= 0.0
    
    # We will simulate the PnL of trading the spread directly (e.g. trading the EURGBP cross pair)
    # For simplicity in vectorbt, we backtest a synthetic asset whose price is the spread itself
    # But since spread can be negative, we use absolute price changes for PnL.
    
    # Let's simulate just the EURUSD leg of the trade to see if it mean-reverts 
    # If Z > 2 (EUR overvalued), we SHORT EURUSD
    # If Z < -2 (EUR undervalued), we LONG EURUSD
    
    pf = vbt.Portfolio.from_signals(
        data['EURUSD'],
        entries=entries_long_spread, # Long EURUSD when spread is too low
        exits=exits_long_spread,
        short_entries=entries_short_spread, # Short EURUSD when spread is too high
        short_exits=exits_short_spread,
        init_cash=100000,
        fees=0.0001,
        freq='1min'
    )
    
    stats = pf.stats()
    
    print("\n=== CROSS-PAIR STATISTICAL ARBITRAGE RESULTS ===")
    print(f"Total Trades: {stats['Total Trades']}")
    print(f"Win Rate: {stats['Win Rate [%]']:.2f}%")
    print(f"Profit Factor: {stats['Profit Factor']:.2f}")
    print(f"Sharpe Ratio: {stats['Sharpe Ratio']:.2f}")
    
    if stats['Profit Factor'] > 1.0:
        print("\nCONCLUSION: The Cointegration Mean-Reversion is mathematically profitable.")
        print("When EURUSD decouples from GBPUSD by > 2 Standard Deviations, it snaps back.")
    else:
        print("\nCONCLUSION: The spread failed to mean-revert profitably after fees.")

if __name__ == '__main__':
    run_stat_arb_simulation()
