import sqlite3
import pandas as pd
import os
import time

def export_table_to_parquet(conn, table_name, output_dir):
    print(f"Exporting {table_name} to Parquet...")
    start_time = time.time()
    
    # Read data from SQLite into a Pandas DataFrame
    query = f"SELECT * FROM {table_name};"
    
    try:
        df = pd.read_sql_query(query, conn)
        
        # Ensure we have data
        if df.empty:
            print(f"  Warning: Table {table_name} is empty. Skipping.")
            return
            
        # Convert datetime strings to actual datetime objects where applicable
        for col in df.columns:
            if 'time' in col.lower() or 'date' in col.lower() or col.endswith('_at'):
                try:
                    df[col] = pd.to_datetime(df[col])
                except Exception as e:
                    pass # If it fails, keep it as string
                    
        # Define output path
        output_path = os.path.join(output_dir, f"{table_name}.parquet")
        
        # Save to Parquet using pyarrow engine
        df.to_parquet(output_path, engine='pyarrow', index=False)
        
        file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        elapsed = time.time() - start_time
        
        print(f"  Success: Exported {len(df)} rows to {output_path}")
        print(f"  Size: {file_size_mb:.2f} MB")
        print(f"  Time: {elapsed:.2f} seconds\n")
        
    except Exception as e:
        print(f"  Error exporting {table_name}: {e}")

def main():
    db_path = '/Users/kennylee/Documents/Saxo/trading_system.sqlite3'
    output_dir = '/Users/kennylee/Documents/Saxo/AA_Research/data'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print(f"Connecting to database: {db_path}")
    conn = sqlite3.connect(db_path)
    
    tables_to_export = [
        'challenger_ticks',
        'challenger_positions',
        'challenger_trades'
    ]
    
    for table in tables_to_export:
        export_table_to_parquet(conn, table, output_dir)
        
    conn.close()
    print("Export pipeline complete.")

if __name__ == '__main__':
    main()
