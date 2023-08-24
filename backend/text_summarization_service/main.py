from fastapi import Body, FastAPI, HTTPException, Request
from pydantic import BaseModel
import openai
from config import OPENAI_API_KEY

app = FastAPI()

# Initialize OpenAI API key
# Replace with your actual API key

openai.api_key = OPENAI_API_KEY


class Item(BaseModel):
    content: str
    summary_length: str  # Values can be: 'short', 'medium', 'long'


@app.post("/summarize/")
async def summarize_content(item: Item):
    if item.summary_length == "short":
        max_tokens = 150
    elif item.summary_length == "medium":
        max_tokens = 500
    elif item.summary_length == "long":
        max_tokens = 750
    else:
        raise HTTPException(
            status_code=400, detail="Invalid summary length specified")
    # Construct a message for GPT-3.5 Turbo
    messages = [
        {"role": "system", "content": "You are a helpful assistant that summarizes content."},
        {"role": "user", "content": f"Explain the following content to a teenager in a {item.summary_length} manner and provide the summary in bullet points: {item.content}"}
    ]

    # Send the message to GPT-3.5 Turbo
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=max_tokens,
        temperature=0.8
    )

    # Extract the summarized content from the response
    summary = response.choices[0].message['content'].strip()

    return {"summary": summary}
