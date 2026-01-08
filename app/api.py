# use fastapi to create an api that retrieves apple stock data from the postgres database
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables and set the database connection parameters
load_dotenv()
DB_NAME = os.getenv("DB_NAME", "apple_stock_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

if not DB_PASSWORD:
    raise ValueError("DB_PASSWORD is not set")

# create the FastAPI app which is used to define the api endpoints
app = FastAPI(title="Apple Stock API")

def get_db_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

# define the method and route to get apple stock data
@app.get("/stocks/aapl")
def get_aapl_stock(limit: int = Query(5, ge=1, le=100)):
    # connect to the database and fetch the stock data
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            f"SELECT date, open, high, low, close, volume FROM apple_stock ORDER BY date DESC LIMIT %s",
            (limit,)
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    if not rows:
        raise HTTPException(status_code=404, detail="No stock data found")
    
    # Convert query result to list for displaying in JSON format
    result = [
        {
            "date": str(row[0]),
            "open": row[1],
            "high": row[2],
            "low": row[3],
            "close": row[4],
            "volume": row[5]
        }
        for row in rows
    ]

    # Prepare the response
    response = {
        "title": f"Apple Stock Data ({result[-1]['date']} to {result[0]['date']})",
        "count": len(result),
        "data": result
    }

    return JSONResponse(content=response)