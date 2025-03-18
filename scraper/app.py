import os
import debugpy
from fastapi import FastAPI
import requests
app = FastAPI()

# Check if we are in development mode (use an environment variable)
if os.getenv("DEBUG_MODE", "false") == "true":
    # Start debugpy to listen for debugger connection
    debugpy.listen(('0.0.0.0', 5679))  # Listen on port 5679
    print("Waiting for debugger to attach...")
    debugpy.wait_for_client()  # Wait for VSCode debugger to attach

@app.get("/scrape")
def scrape(url: str):
    try:
        # Scraping logic here
        response = requests.get(url)
        return {"content": response.text[:200]}  # Returning the first 200 characters of the response content
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

