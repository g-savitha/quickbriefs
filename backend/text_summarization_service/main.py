from fastapi import FastAPI, HTTPException
from transformers import BartForConditionalGeneration, BartTokenizer
from pydantic import BaseModel

app = FastAPI()

# Load pre-trained BART model and tokenizer
model_name = 'facebook/bart-large-cnn'
model = BartForConditionalGeneration.from_pretrained(model_name)
tokenizer = BartTokenizer.from_pretrained(model_name)


class Item(BaseModel):
    content: str
    available_time: float  # time in minutes


@app.post("/summarize/")
async def summarize_content(item: Item):
    # Estimate reading speed
    average_words_per_minute = 225
    max_words = int(item.available_time * average_words_per_minute)

    # Convert to max tokens (assuming an average of 1.5 tokens per word for safety)
    max_tokens = int(1.5 * max_words)

    # Tokenize the content and generate summary IDs
    inputs = tokenizer([item.content], max_length=1024,
                       return_tensors='pt', truncation=True)
    summary_ids = model.generate(
        inputs['input_ids'], num_beams=4, min_length=30, max_length=max_tokens, early_stopping=True)

    # Decode the summary IDs and return the summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    # Construct a response JSON
    response_data = {"summary": summary}

    # Return the constructed response
    return response_data
