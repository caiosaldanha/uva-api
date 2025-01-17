import requests
import pandas as pd
import sqlite3
from typing import List

def fetch_data_from_api(base_url: str, route: str, year: int) -> pd.DataFrame:
    """Fetch data from API for a specific route and year."""
    url = f"{base_url}/api/v1/{route}/{year}"
    response = requests.get(url)
    response.raise_for_status()
    return pd.DataFrame(response.json())

def save_to_sqlite(df: pd.DataFrame, db_file: str, table_name: str, if_exists: str = "append"):
    """Save a Pandas DataFrame to an SQLite database."""
    with sqlite3.connect(db_file) as conn:
        df.to_sql(table_name, conn, if_exists=if_exists, index=False)

def main():
    base_url = "https://35.208.17.104"  # Replace with your API base URL
    routes = ["production", "processing", "comercialization", "importation", "exportation"]
    years = list(range(1970, 2024))
    db_file = "vitibrasil_data.db"

    for route in routes:
        for year in years:
            try:
                df = fetch_data_from_api(base_url, route, year)
                table_name = f"{route}_{year}"  # Use route name as table name
                save_to_sqlite(df, db_file, table_name)
                print(f"Saved data for {route} ({year}) to database.")
            except Exception as e:
                print(f"Error processing {route} ({year}): {e}")

if __name__ == "__main__":
    main()