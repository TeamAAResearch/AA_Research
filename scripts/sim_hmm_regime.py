import pandas as pd
import numpy as np
import vectorbt as vbt
from sklearn.mixture import GaussianMixture
import os

def run_hmm_simulation():
    data_path = '/Users/kennylee/Documents/Saxo/AA_Research/data/challenger_ticks.parquet'
    
    if not os.path.exists(data_path):
        print("Data not found.")
        return
        
    print("Loading Parquet data...")
    df = pd.read_parquet(data_path)
    df = df[df['symbol'] == 'USDJPY'].copy() # JPY has good regime shifts
    df['created_at'] = pd.to_datetime(df['created_at'], format='ISO8601', utc=True)
    df = df.sort_values('created_at')
    df.set_index('created_at', inplace=True)
    
    # Resample to 1-minute bars
    bars = df['mid'].resample('1min').ohlc()
    bars.dropna(inplace=True)
    
    # 1. Base Signal: 60-minute Momentum Z-Score
    bars['momentum_60'] = bars['close'].diff(60)
    bars['mom_zscore'] = (bars['momentum_60'] - bars['momentum_60'].rolling(60).mean()) / (bars['momentum_60'].rolling(60).std() + 1e-8)
    
    # 2. Regime Detection (HMM/GMM Proxy)
    # We use 60-minute rolling variance as the feature to cluster
    bars['variance_60'] = bars['close'].rolling(60).var()
    bars.dropna(inplace=True)
    
    entries_long = bars['mom_zscore'] > 1.5
    entries_short = bars['mom_zscore'] < -1.5
    exits = (bars['mom_zscore'] < 0.5) & (bars['mom_zscore'] > -0.5)
    
    print(f"\n--- Training Gaussian Mixture Model on USDJPY ({len(bars)} 1-min bars) ---")
    
    # Fit a 2-state GMM to the variance (0 = Low Vol/Chop, 1 = High Vol/Turbulent)
    X = bars['variance_60'].values.reshape(-1, 1)
    gmm = GaussianMixture(n_components=2, covariance_type='full', random_state=42)
    bars['regime'] = gmm.fit_predict(X)
    
    # Ensure Regime 1 is the high volatility regime
    mean_0 = bars[bars['regime'] == 0]['variance_60'].mean()
    mean_1 = bars[bars['regime'] == 1]['variance_60'].mean()
    if mean_0 > mean_1:
        bars['regime'] = 1 - bars['regime'] # Swap them
        
    # 3. Dynamic Sizing based on Regime
    # Base size is 1.0 (100k units). 
    # If in Regime 1 (High Vol), size is 0.5 (50k units) to cut risk during turbulence.
    size = np.where(bars['regime'] == 1, 0.5, 1.0)
    
    # Run Backtests
    pf_base = vbt.Portfolio.from_signals(
        bars['close'],
        entries=entries_long,
        exits=exits,
        short_entries=entries_short,
        short_exits=exits,
        size=1.0, # Fixed size
        init_cash=100000,
        fees=0.0001,
        freq='1min'
    )
    
    pf_regime = vbt.Portfolio.from_signals(
        bars['close'],
        entries=entries_long,
        exits=exits,
        short_entries=entries_short,
        short_exits=exits,
        size=size, # Dynamic regime-based size
        init_cash=100000,
        fees=0.0001,
        freq='1min'
    )
    
    print("\n[UNFILTERED STATIC SIZING]")
    print(f"Max Drawdown: {pf_base.stats()['Max Drawdown [%]']:.2f}%")
    print(f"Profit Factor: {pf_base.stats()['Profit Factor']:.2f}")
    print(f"Sharpe Ratio: {pf_base.stats()['Sharpe Ratio']:.2f}")
    
    print("\n[HMM REGIME-AWARE SIZING]")
    print(f"Max Drawdown: {pf_regime.stats()['Max Drawdown [%]']:.2f}%")
    print(f"Profit Factor: {pf_regime.stats()['Profit Factor']:.2f}")
    print(f"Sharpe Ratio: {pf_regime.stats()['Sharpe Ratio']:.2f}")
    
    if pf_regime.stats()['Max Drawdown [%]'] > pf_base.stats()['Max Drawdown [%]']: # Less negative is better
        print("\nCONCLUSION: HMM Regime-Switching successfully protected capital during high-volatility turbulence.")
    else:
        print("\nCONCLUSION: Regime-Switching failed to improve risk-adjusted returns on this dataset.")

if __name__ == '__main__':
    run_hmm_simulation()
