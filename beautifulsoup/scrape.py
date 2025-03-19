from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

app = FastAPI()

class ScrapeResponse(BaseModel):
    description: str

def scrape_description(url: str) -> str:
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Try getting the meta description or fall back to other options
    description = soup.find('meta', {'name': 'description'})
    if description:
        return description.get('content', 'No description available.')
    description = soup.find('meta', {'property': 'og:description'})
    if description:
        return description.get('content', 'No description available.')
    return 'No description available.'

@app.get("/scrape", response_model=ScrapeResponse)
def scrape(url: str):
    description = scrape_description(url)
    return ScrapeResponse(description=description)
