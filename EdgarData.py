import requests
from fuzzywuzzy import fuzz
from bs4 import BeautifulSoup
import json

def extract_information(prospectus_url, target_keywords):
    """
    Extracts indicative information from a prospectus using fuzzy search and Gemini AI.

    Args:
        prospectus_url (str): URL of the prospectus.
        target_keywords (list): List of keywords to search for.

    Returns:
        dict: A dictionary containing extracted information.
    """

    # 1. Fetch and parse the prospectus HTML
    # response = requests.get(prospectus_url)
    headers = {
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        "User-Agent": "anujwalia.itm@gmail.com"

    }  # Add a User-Agent header to mimic a browser
    response = requests.get(prospectus_url, headers=headers)
    response.raise_for_status()
    # print(response.text)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 2. Find relevant text sections using fuzzy matching
    relevant_sections = []
    sections=soup.find_all('div')
    for keyword in target_keywords:
        for section in sections:
            # print(paragraph.text)
            similarity = fuzz.ratio(section.text.lower(), keyword.lower())
            if similarity > 80:
                print(section.text)
                relevant_sections.append(section.text)

    return relevant_sections

target_keywords = ["underwriting discount","underwriting","discount"]

extracted_info = extract_information("https://www.sec.gov/Archives/edgar/data/947263/000114036124031123/ef20031597_424b2.htm", target_keywords)
# extracted_info = extract_information("./EdgarTD.html", target_keywords)
print(extracted_info)