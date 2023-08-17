import os
import pandas as pd
import sqlite3
import datetime as dt
today = dt.date.today().strftime("%d_%m_%Y")

def main():
    # Set the base directory
    base_dir = '../Archive/Modified/'
    # List all files in the base directory
    file_dir = os.listdir(base_dir)
    
    # Filter for ADT CSV files
    adt_csv = [f for f in file_dir if f.endswith('.csv') and 'ADT' in f]
    
    if adt_csv:
        adt_csv_file = os.path.join(base_dir, adt_csv[0])  # Combine base directory with filename
        df = pd.read_csv(adt_csv_file)

        bonus_dir = '../Archive/Bonus/'
        os.mkdir(bonus_dir)

        # Connect to the SQLite database (this will create a new database if it doesn't exist)
        conn = sqlite3.connect(os.path.join(bonus_dir, 'ADT.db'))

        # Write the DataFrame to the SQLite database
        df.to_sql('table_name', conn, if_exists='replace', index=False)

        # Close the connection
        conn.close()

if __name__ == "__main__":
    main()

