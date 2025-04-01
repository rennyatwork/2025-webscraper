from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
#from text_processing.summarizer.summarizer import summarize_text
#from text_processing.translator.translator import translate_text


app = FastAPI()

# Create a Pydantic model for the response
class ScrapeResponse(BaseModel):
    description: str

# Web scraping function
def scrape_description(url: str) -> str:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Example scraping logic (you may need to adjust based on your website)
    description = soup.find('meta', {'name': 'description'})
    if description:
        return description.get('content', 'No description available.')
    else:
        return 'No description available.'

# FastAPI route to handle scraping request
@app.get("/scrape", response_model=ScrapeResponse)
def scrape(url: str):
    description = scrape_description(url)
    return ScrapeResponse(description=description)

