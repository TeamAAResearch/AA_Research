import pandas as pd
import numpy as np
import vectorbt as vbt
import os

def run_simulation():
    data_path = '/Users/kennylee/Documents/Saxo/AA_Research/data/challenger_ticks.parquet'
    
    if not os.path.exists(data_path):
        print("Data not found.")
        return
        
    print("Loading Parquet data...")
    df = pd.read_parquet(data_path)
    df['created_at'] = pd.to_datetime(df['created_at'], format='ISO8601', utc=True)
    df = df.sort_values('created_at')
    
    # We will test on a basket of major pairs
    target_symbols = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD']
    
    results = []
    
    for symbol in target_symbols:
        df_sym = df[df['symbol'] == symbol].copy()
        if df_sym.empty:
            continue
            
        df_sym.set_index('created_at', inplace=True)
        
        # Resample to 1-minute bars for indicator calculation (using mid price)
        # Ticks can be irregular, so resampling standardizes the time series
        bars = df_sym['mid'].resample('1min').ohlc()
        bars.dropna(inplace=True)
        
        if len(bars) < 100:
            continue
            
        print(f"\n--- Processing {symbol} ({len(bars)} 1-min bars) ---")
        
        # 1. Calculate Unscaled Momentum (Return over 60 mins)
        bars['momentum_60'] = bars['close'].diff(60)
        
        # 2. Calculate ATR (14-period)
        # True Range: max(high-low, abs(high-prev_close), abs(low-prev_close))
        tr1 = bars['high'] - bars['low']
        tr2 = (bars['high'] - bars['close'].shift(1)).abs()
        tr3 = (bars['low'] - bars['close'].shift(1)).abs()
        bars['tr'] = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        bars['atr_14'] = bars['tr'].rolling(14).mean()
        
        # 3. Calculate Volatility-Scaled Momentum (Moskowitz)
        # We add a tiny epsilon to prevent division by zero
        epsilon = 1e-6
        bars['vol_scaled_mom'] = bars['momentum_60'] / (bars['atr_14'] + epsilon)
        
        # Define Thresholds
        # Unscaled threshold (e.g., 20 pips... varies heavily by pair, but we'll use a fixed percentage for fairness)
        # Instead, let's just use rolling Z-score for unscaled to be perfectly fair
        bars['mom_zscore'] = (bars['momentum_60'] - bars['momentum_60'].rolling(60).mean()) / (bars['momentum_60'].rolling(60).std() + epsilon)
        
        # Signals: Unscaled (Z-score > 1.5)
        entries_unscaled = bars['mom_zscore'] > 1.5
        exits_unscaled = bars['mom_zscore'] < 0.0 # Exit when momentum dies
        
        # Signals: Volatility-Scaled (Score > 1.5)
        entries_scaled = bars['vol_scaled_mom'] > 1.5
        exits_scaled = bars['vol_scaled_mom'] < 0.0
        
        # Run Backtests
        pf_unscaled = vbt.Portfolio.from_signals(
            bars['close'],
            entries_unscaled,
            exits_unscaled,
            init_cash=100000,
            fees=0.0001,
            freq='1min'
        )
        
        pf_scaled = vbt.Portfolio.from_signals(
            bars['close'],
            entries_scaled,
            exits_scaled,
            init_cash=100000,
            fees=0.0001,
            freq='1min'
        )
        
        unscaled_win = pf_unscaled.stats()['Win Rate [%]']
        scaled_win = pf_scaled.stats()['Win Rate [%]']
        
        unscaled_pf = pf_unscaled.stats()['Profit Factor']
        scaled_pf = pf_scaled.stats()['Profit Factor']
        
        print(f"UNSCALED -> Win Rate: {unscaled_win:.2f}% | Profit Factor: {unscaled_pf:.2f}")
        print(f"SCALED   -> Win Rate: {scaled_win:.2f}% | Profit Factor: {scaled_pf:.2f}")
        
        results.append({
            'symbol': symbol,
            'unscaled_win': unscaled_win,
            'scaled_win': scaled_win,
            'unscaled_pf': unscaled_pf,
            'scaled_pf': scaled_pf
        })
        
    print("\n=== SUMMARY OF VOLATILITY SCALING ===")
    df_res = pd.DataFrame(results)
    print(f"Average Unscaled Win Rate: {df_res['unscaled_win'].mean():.2f}%")
    print(f"Average Scaled Win Rate: {df_res['scaled_win'].mean():.2f}%")
    print(f"Average Unscaled Profit Factor: {df_res['unscaled_pf'].mean():.2f}")
    print(f"Average Scaled Profit Factor: {df_res['scaled_pf'].mean():.2f}")
    
    if df_res['scaled_pf'].mean() > df_res['unscaled_pf'].mean():
        print("\nCONCLUSION: Volatility-Scaling (Moskowitz) outperforms raw momentum.")
    else:
        print("\nCONCLUSION: Raw momentum outperformed scaling on this dataset.")

if __name__ == '__main__':
    run_simulation()
