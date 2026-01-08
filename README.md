# Apple Stock Analysis

This project fetches Apple stock data, stores it in a PostgreSQL database, and uses FastAPI API to view the data
Using Docker, this project can be run from anywhere



# 1. Architecture

- Data Fetching: Uses `yfinance` to retrieve the last month of Apple stock data with a days interval.
- Data Storage/Schema: PostgreSQL database stores the stock data with `date` as the primary key to avoid duplicates and preventing SQL injection
- API: We use FastAPI to run the `/stocks/aapl` endpoint that returns recent stock data as a JSON object with a count and a title that includes the date range. We can also limit the rows retrieved using ?limit="n"
- Docker: `docker-compose` creates a container with a copy of the architecture that allows us to run this project elsewhere.
- Environment Variables: `.env` file stores DB credentials securely (not committed to GitHub) as contains local password.



# 2. What works and what doesn't

Works:
- Fetches and stores Apple stock data into PostgreSQL.
- API endpoint `/stocks/aapl` returns JSON with recent stock data.
- Docker setup allows this to be run elsewhere.

**Doesn't work:
- No automation, has to be manually run



# 3. How to run it using docker

1. Clone the repository and navigate to apple-stock-analysis
You can do this by running git clone https://github.com/GeraintDaiJ/apple-stock-analysis.git in vscode terminal

2. Create a ".env" file in the new folder containing the following:

DB_NAME=apple_stock_db
DB_USER=postgres
DB_PASSWORD=your_local_password
DB_HOST=db
DB_PORT=5432

3. Run docker and view API respone on the web:

Open a new terminal
Run "docker-compose up --build"
PGS container will run
fetch_and_store will run
The API will be available at http://localhost:8000/stocks/aapl



# 4. Improvements I would make with more time
- I would add automation so we do not have to run manually and the API response is always the latest stock data
- Create automated tests so we know if anything has gone wrong
- Improve the API to have more filtering option and API security (authentication)
