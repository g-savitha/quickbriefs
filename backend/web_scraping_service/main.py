from fastapi import HTTPException, FastAPI
from fastapi.responses import JSONResponse
from bs4 import BeautifulSoup
import requests
from pydantic import BaseModel
import os

# environment variable to test between local and prod.
# Railway doesnt support docker compose. so push each service individually.
SUMMARIZATION_SERVICE_URL = os.environ.get(
    "SUMMARIZATION_SERVICE_URL", "http://localhost:8081/summarize/")


class Url(BaseModel):
    url: str
    desired_length: str  # Values can be: 'short', 'medium', 'long'


app = FastAPI()


def scrape_webpage(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None

    webpage_content = response.text
    soup = BeautifulSoup(webpage_content, 'html.parser')
    # # Replace code blocks with placeholder text
    # for code_block in soup.find_all('pre'):
    #     code_block.replace_with("[code block]")
    # clean the scraped content by removing extra whitespaces and newlines
    text_content = [p.text for p in soup.find_all('p')]
    cleaned_content = ' '.join(
        ' '.join(text_content).split())  # Clean the content
    print("--------------------------------------------------")
    print(cleaned_content)
    return cleaned_content


@app.post("/scrape/", response_class=JSONResponse)
async def scrape(url: Url):
    scraped_content = scrape_webpage(url.url)
    if not scraped_content:
        raise HTTPException(
            status_code=404, detail="Webpage content not found")

    # Check content length and adjust summary_length if needed
    content_length = len(scraped_content.split())
    print("************************************************************")
    print(content_length)

    if content_length < 500:  # Arbitrary number, adjust as needed
        summary_length = 'short'
    elif content_length < 750:  # Another arbitrary number
        if url.desired_length == 'long':
            summary_length = 'medium'
        else:
            summary_length = url.desired_length
    else:
        summary_length = url.desired_length

    summary_endpoint = SUMMARIZATION_SERVICE_URL
    summary_response = requests.post(
        summary_endpoint,
        json={
            "content": scraped_content,
            "summary_length": summary_length
        }
    )

    # Check the status code of the summary_response and return its JSON content
    if summary_response.status_code == 200:
        return summary_response.json()
    else:
        raise HTTPException(
            status_code=500, detail="Summarization service failed")


# @app.exception_handler(Exception)
# async def general_exception_handler(request, exc):
#     return JSONResponse(status_code=500, content={"message": "An unexpected error occurred."})
