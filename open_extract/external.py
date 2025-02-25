import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()


def query_doc_type(doi: str) -> str:
    """Query the OpenAlex API to get the document type of a given DOI."""

    url = f"https://api.openalex.org/works/https://doi.org/{doi}"

    # Adding polite email to the request
    polite_email = os.getenv("API_POLITE_EMAIL")
    url = f"{url}?mailto={polite_email}" if polite_email else url
    response = requests.get(url)

    if response.status_code == 404:
        return "not_found"

    if response.status_code == 429:  # Rate limit exceeded
        time.sleep(10)
        response = requests.get(url)

    try:
        return response.json()["type"]
    except KeyError:
        return ""
