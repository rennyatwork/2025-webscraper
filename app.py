import streamlit as st
import requests

# Title of the web app
st.title("Web Scraper")

# Input for the URL to scrape
url = st.text_input("Enter the URL to scrape:")

# When the button is pressed, send the request to FastAPI
if st.button("Scrape"):
    # Make the request to FastAPI using the correct URL for communication
    response = requests.get(f"http://scraper:8000/scrape?url={url}")
    
    if response.status_code == 200:
        st.write("Scraping successful!")
        st.write(response.json())
    else:
        st.write("Failed to scrape the URL. Please check the input or server status.")

