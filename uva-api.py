from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/")
def read_root():
    try:
        url = "https://uol.com.br"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP issues
        soup = BeautifulSoup(response.content, "html.parser")

        # Example of extracting data from the soup object
        title = soup.title.string if soup.title else "No title found"
        return {"site_title": title}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
