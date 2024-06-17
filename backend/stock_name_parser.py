import os
import pandas as pd
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import Optional, List
from fetch_reddit import get_reddit_instance, fetch_reddit_posts

# Define the response schema
class StockResponse(BaseModel):
    stock_name: Optional[str] = Field(description="The extracted stock name or ticker")

# Create the prompt template
def create_prompt(post: str) -> str:
    return f"Extract only the stock name or ticker from this post. For multiple stocks seperate stocks using commas. If there is no stock return Absent: \"{post}\""

# Initialize the OpenAI client
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)
if not openai_api_key:
    raise ValueError("OpenAI API key not found in environment variables")

def extract_stock_name(post: str) -> str:
    """
    Extract the stock name or ticker from the post content.

    Parameters:
    post (str): The combined title and content of the post.

    Returns:
    str: The extracted stock name or ticker.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts stock names or tickers from posts."},
            {"role": "user", "content": create_prompt(post)}
        ]
    )
    stock_name = response.choices[0].message.content.strip()
    return stock_name

def filter_posts_with_stock_info(df: pd.DataFrame) -> List[str]:
    """
    Filter out posts without stock information.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the Reddit posts.

    Returns:
    List[str]: A list containing only the stock names or "None" for posts without stock information.
    """
    stock_names = df['Combined'].apply(extract_stock_name)
    return stock_names.tolist()

# Example usage
if __name__ == "__main__":
    

    # Initialize Reddit instance
    reddit_instance = get_reddit_instance()

    # Fetch posts
    subreddit_name = "wallstreetbets"
    post_limit = 10
    fetched_posts_df = fetch_reddit_posts(reddit_instance, subreddit_name, post_limit)

    # Filter posts with stock information
    stock_names = filter_posts_with_stock_info(fetched_posts_df)

    # Print the results
    print(stock_names)
