import os
import pandas as pd
from openai import OpenAI


from pydantic import BaseModel, Field
from typing import Optional, List, Dict

# Sample DataFrame creation (replace this with your actual DataFrame)
data = {
    'post_content': [
        "I think AAPL is going to skyrocket next quarter.",
        "MSFT is showing some promising signs.",
        "What are your thoughts on TSLA?",
        "Investing in GOOGL has been really profitable.",
        "I am worried about AMZN's recent performance.",
        "This is just a general comment without any stock mention."
    ]
}
df = pd.DataFrame(data)

# Get the OpenAI API key from the environment variable
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)
if not openai_api_key:
    raise ValueError("OpenAI API key not found in environment variables")

# Initialize OpenAI API key

# Define the response schema
class StockResponse(BaseModel):
    stock_name: Optional[str] = Field(description="The extracted stock name or ticker")

# Create the prompt template
def create_prompt(post: str) -> str:
    return f"Extract only the stock name or ticker from this post: \"{post}\""

# Initialize the LLM
def extract_stock_name(post: str) -> str:
    response = client.chat.completions.create(model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that extracts stock names or tickers from posts."},
        {"role": "user", "content": create_prompt(post)}
    ])
    stock_name = response.choices[0].message.content.strip()
    return stock_name if stock_name else None

# Apply the extraction function to each post and filter out empty results
df['stock_name'] = df['post_content'].apply(extract_stock_name)
df = df[df['stock_name'].notna()]

# Display the DataFrame with stock names/tickers
print(df)
