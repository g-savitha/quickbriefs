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
    summary_percentage: float  # e.g., 0.2 for 20%


@app.post("/summarize/")
async def summarize_content(item: Item):
    # Tokenize the content
    inputs = tokenizer([item.content], max_length=1024,
                       return_tensors='pt', truncation=True)

    # Calculate desired length based on percentage
    desired_length = int(item.summary_percentage / 100 *
                         len(inputs['input_ids'][0]))
    min_gen_length = max(30, int(0.8 * desired_length))
    max_gen_length = int(1.2 * desired_length)

    # Generate summary IDs with adjusted parameters
    summary_ids = model.generate(
        inputs['input_ids'],
        num_beams=6,
        min_length=min_gen_length,
        max_length=max_gen_length,
        early_stopping=True,
        length_penalty=0.8
    )

    # Decode the summary IDs and return the summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    # Construct a response JSON
    response_data = {"summary": summary}

    # Return the constructed response
    return response_data
