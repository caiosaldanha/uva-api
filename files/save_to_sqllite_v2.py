import requests
import pandas as pd
import sqlite3
from typing import List

def fetch_data_from_api(base_url: str, route: str, year: int) -> pd.DataFrame:
    """Fetch data from API for a specific route and year."""
    url = f"{base_url}/api/v1/{route}/{year}"
    response = requests.get(url, verify=False)
    response.raise_for_status()
    return pd.DataFrame(response.json())

def save_to_sqlite(df: pd.DataFrame, db_file: str, table_name: str, if_exists: str = "append"):
    """Save a Pandas DataFrame to an SQLite database."""
    with sqlite3.connect(db_file) as conn:
        df.to_sql(table_name, conn, if_exists=if_exists, index=False)

def concatenate_and_save_years(base_url: str, routes: List[str], years: List[int], db_file: str):
    """Concatenate data from 1970 to 2023 for each route and save to SQLite."""
    for route in routes:
        all_years_data = []  # List to collect data for all years
        for year in years:
            try:
                df = fetch_data_from_api(base_url, route, year)
                df['year'] = year  # Add a column to indicate the year of the data
                all_years_data.append(df)
                print(f"Fetched data for {route} ({year}).")
            except Exception as e:
                print(f"Error fetching data for {route} ({year}): {e}")
        
        # Concatenate all years' data for the current route
        if all_years_data:
            concatenated_df = pd.concat(all_years_data, ignore_index=True)
            table_name = route  # Use the route name as the table name
            save_to_sqlite(concatenated_df, db_file, table_name, if_exists="replace")
            print(f"Saved concatenated data for {route} to database.")

def main():
    base_url = "http://backend:8000"  # Replace with your API base URL
    routes = ["production", "processing", "commercialization", "importation", "exportation"]
    years = list(range(1970, 2024))
    db_file = "vitibrasil_data_v2.db"

    concatenate_and_save_years(base_url, routes, years, db_file)

if __name__ == "__main__":
    main()