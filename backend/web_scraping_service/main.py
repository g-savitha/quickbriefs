from fastapi import HTTPException, FastAPI
from fastapi.responses import JSONResponse
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


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(status_code=500, content={"message": "An unexpected error occurred."})


@app.post("/scrape/", response_class=JSONResponse)
async def scrape(url: Url):
    content = scrape_webpage(url.url)
    if not content:
        raise HTTPException(
            status_code=404, detail="Webpage content not found")
    return {"text": content}
