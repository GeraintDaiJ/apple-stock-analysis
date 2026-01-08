# Fetch Apple stock data from Yahoo Finance and store it in a Postgres database.
# 1. Connect to Postgres
# 2. Create table if it does not already exists
# 3. Fetch stock data
# 4. Insert into table

# Firstly, import the required libraries
import os
import yfinance as yf
import psycopg2
from dotenv import load_dotenv

# load environment variables and set database connection parameters
load_dotenv()
DB_NAME = os.getenv("DB_NAME", "apple_stock_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")

if not DB_PASSWORD:
    raise ValueError("DB_PASSWORD is not set")

# use a main guard to allow importing without executing 
if __name__ == "__main__":
    # connect to postgres
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()

    # create table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS apple_stock (
        date DATE NOT NULL,
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        volume BIGINT,
        dividends FLOAT,
        stock_splits FLOAT,
        PRIMARY KEY (date)
    );
    """
    cur.execute(create_table_query)
    conn.commit()
    print("Table 'apple_stock' is ready.")

    # fetch Apple stock data
    ticker = yf.Ticker("AAPL")
    df = ticker.history(period="1mo", interval="1d")
    df.reset_index(inplace=True)

    print("Data fetched from Yahoo Finance:")
    print(df.head())

    # insert rows
    for i, row in df.iterrows():
        cur.execute(
            """
            INSERT INTO apple_stock (date, open, high, low, close, volume, dividends, stock_splits)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (date) DO NOTHING;
            """,
            (row['Date'], row['Open'], row['High'], row['Low'], row['Close'],
             row['Volume'], row['Dividends'], row['Stock Splits'])
        )

    conn.commit()
    print(f"{len(df)} rows inserted into 'apple_stock' table.")

    # close connection
    cur.close()
    conn.close()
    print("Database connection closed.")
