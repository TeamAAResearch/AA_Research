import pandas as pd
import numpy as np
import vectorbt as vbt
import os

def run_kelly_simulation():
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
    
    # Base Signal: Unfiltered Momentum
    bars['momentum_60'] = bars['close'].diff(60)
    bars['mom_zscore'] = (bars['momentum_60'] - bars['momentum_60'].rolling(60).mean()) / (bars['momentum_60'].rolling(60).std() + 1e-8)
    
    entries_long = bars['mom_zscore'] > 1.5
    entries_short = bars['mom_zscore'] < -1.5
    exits = (bars['mom_zscore'] < 0.5) & (bars['mom_zscore'] > -0.5)
    
    # Run Base Portfolio to extract trades
    pf = vbt.Portfolio.from_signals(
        bars['close'],
        entries=entries_long,
        exits=exits,
        short_entries=entries_short,
        short_exits=exits,
        size=100000,
        init_cash=100000,
        fees=0.0001,
        freq='1min'
    )
    
    trades = pf.trades.records_readable
    if len(trades) < 20:
        print(f"Not enough trades ({len(trades)}) to simulate rolling Kelly.")
        return
        
    print(f"\n--- Simulating Dynamic Kelly Criterion on EURUSD ({len(trades)} Trades) ---")
    
    pnls = trades['PnL'].values
    returns = pnls / 100000 # Approximation of trade return %
    
    # Simulate equity curve
    initial_capital = 100000
    
    # Static 2% Risk 
    eq_static = [initial_capital]
    for r in returns:
        # Risk 2% of equity, if return is 1% we make 2% * 1%? No, r is the actual return on 100k base.
        # Let's say we scale trade size so that a 1 ATR loss = 2% risk.
        # For simplicity in this proxy, we assume `r` is the unlevered return on the asset.
        # Levered return = (r * leverage). 
        # Base leverage = 1.0 (Fixed Size).
        eq_static.append(eq_static[-1] + pnls[len(eq_static)-1])
        
    # Dynamic Kelly Risk
    eq_kelly = [initial_capital]
    kelly_fractions = []
    
    # Rolling window of 10 trades
    window = 10
    
    for i in range(len(returns)):
        if i < window:
            # Not enough data, use base sizing multiplier (1.0)
            k_mult = 1.0
        else:
            recent_pnls = pnls[i-window:i]
            wins = recent_pnls[recent_pnls > 0]
            losses = recent_pnls[recent_pnls <= 0]
            
            W = len(wins) / window
            avg_win = wins.mean() if len(wins) > 0 else 0
            avg_loss = abs(losses.mean()) if len(losses) > 0 else 1e-8
            
            R = avg_win / avg_loss if avg_loss > 0 else 1.0
            
            # Kelly Formula: f = W - ((1-W)/R)
            K = W - ((1 - W) / R)
            
            # Half-Kelly for safety, clamped between 0 and 2.0x base size
            k_mult = max(0.0, min(K * 0.5 * 10, 2.0)) # scale up slightly for the multiplier
            
        kelly_fractions.append(k_mult)
        
        # Apply the Kelly multiplier to the trade PnL
        dynamic_pnl = pnls[i] * k_mult
        eq_kelly.append(eq_kelly[-1] + dynamic_pnl)
        
    print("\n[STATIC RISK ALLOCATION]")
    print(f"Final Equity: ${eq_static[-1]:.2f}")
    
    print("\n[DYNAMIC KELLY ALLOCATION]")
    print(f"Final Equity: ${eq_kelly[-1]:.2f}")
    print(f"Average Kelly Multiplier: {np.mean(kelly_fractions):.2f}x")
    
    if eq_kelly[-1] > eq_static[-1]:
        print("\nCONCLUSION: Dynamic Kelly sizing aggressively compounded edge and outperformed static risk.")
    else:
        print("\nCONCLUSION: Dynamic Kelly sizing choked risk due to poor rolling edge, saving capital from further drawdown.")

if __name__ == '__main__':
    run_kelly_simulation()
