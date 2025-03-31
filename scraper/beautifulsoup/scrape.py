from fastapi import FastAPI, Query
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from Description_Company import creer_description_entreprise

app = FastAPI()

class ScrapeResponse(BaseModel):
    description: str

# Existing scrape route
@app.get("/scrape", response_model=ScrapeResponse)
def scrape(url: str = Query(...)):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    description = soup.find('meta', {'name': 'description'})
    if description:
        return ScrapeResponse(description=description.get('content', 'No description available.'))
    else:
        return ScrapeResponse(description='No description available.')

# New route for Description_Company.py
@app.get("/company-description", response_model=ScrapeResponse)
def company_description(url: str = Query(...)):
    description = creer_description_entreprise(url)
    return ScrapeResponse(description=description)
