from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests
from pydantic import BaseModel

class Url(BaseModel):
    url: str

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
    text_content = [p.text for p in soup.find_all('p')]
    return ' '.join(text_content)

@app.post("/scrape/")
async def scrape(url: Url):
    return {"text": scrape_webpage(url.url)}
