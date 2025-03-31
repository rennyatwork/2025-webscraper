"""
from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/scrape")
def scrape(url: str):
    try:
        # Scraping logic here
        response = requests.get(url)
        return {"content": response.text[:200]}  # Returning the first 200 characters of the response content
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

"""