import streamlit as st
import requests

# Title of the web app
st.title("Web Scraper")

# Input for the URL to scrape
url = st.text_input("Enter the URL to scrape:")

# Allow the user to choose between Scrapy or BeautifulSoup
scraper_choice = st.radio(
    "Choose a scraper:",
    ("Scrapy", "BeautifulSoup")
)

# Scraping request
if st.button("Scrape"):
    if scraper_choice == "Scrapy":
        # Call Scrapy service (FastAPI scraper)
        response = requests.get(f"http://scrapy:8000/scrape?url={url}")
    elif scraper_choice == "BeautifulSoup":
        # Call BeautifulSoup service (FastAPI scraper)
        response = requests.get(f"http://beautifulsoup:8000/scrape?url={url}")

    if response.status_code == 200:
        st.write("Scraping successful!")
        st.write(response.json())
    else:
        st.write("Failed to scrape the URL. Please check the input or server status.")
