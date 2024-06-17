import os
import pandas as pd
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import Optional, List
from fetch_reddit import get_reddit_instance, fetch_reddit_posts

# Define the response schema
class StockResponse(BaseModel):
    stock_name: Optional[str] = Field(description="The extracted stock name or ticker")

# Create the prompt templates
def create_stock_extraction_prompt(post: str) -> str:
    return f"Extract only the stock names or tickers from this post. For multiple stocks, separate stocks using commas. If there is no stock, return Absent: \"{post}\""

def create_relevant_info_prompt(post: str, stock: str) -> str:
    return f"Extract only the information relevant to the stock {stock} from this post without altering the information: \"{post}\""

# Initialize the OpenAI client
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)
if not openai_api_key:
    raise ValueError("OpenAI API key not found in environment variables")

def extract_stock_names(post: str) -> List[str]:
    """
    Extract the stock names or tickers from the post content.

    Parameters:
    post (str): The combined title and content of the post.

    Returns:
    List[str]: The extracted stock names or tickers.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts stock names or tickers from posts."},
            {"role": "user", "content": create_stock_extraction_prompt(post)}
        ]
    )
    stock_names = response.choices[0].message.content.strip()
    if stock_names.lower() == "absent":
        return []
    return [name.strip() for name in stock_names.split(',')]

def extract_relevant_info(post: str, stock: str) -> str:
    """
    Extract the information relevant to the stock from the post content.

    Parameters:
    post (str): The combined title and content of the post.
    stock (str): The stock name or ticker.

    Returns:
    str: The relevant information for the stock.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts relevant information for a specific stock from posts without altering the information."},
            {"role": "user", "content": create_relevant_info_prompt(post, stock)}
        ]
    )
    relevant_info = response.choices[0].message.content.strip()
    return relevant_info

def split_post_by_stocks(post: str, stock_names: List[str]) -> List[dict]:
    """
    Split the post content based on the extracted stock names and extract relevant information for each stock.

    Parameters:
    post (str): The combined title and content of the post.
    stock_names (List[str]): The list of extracted stock names or tickers.

    Returns:
    List[dict]: A list of dictionaries with stock names and corresponding relevant post content.
    """
    split_posts = []
    for stock in stock_names:
        relevant_info = extract_relevant_info(post, stock)
        split_posts.append({
            "Stock": stock,
            "Content": relevant_info
        })
    return split_posts

def filter_posts_with_stock_info(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter out posts without stock information and split posts with multiple stocks.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the Reddit posts.

    Returns:
    pd.DataFrame: A DataFrame with each stock having its own relevant description.
    """
    all_split_posts = []
    for _, row in df.iterrows():
        stock_names = extract_stock_names(row['Combined'])
        if stock_names:
            if len(stock_names) > 1:
                split_posts = split_post_by_stocks(row['Combined'], stock_names)
                all_split_posts.extend(split_posts)
            else:
                all_split_posts.append({
                    "Stock": stock_names[0],
                    "Content": row['Combined']
                })

    return pd.DataFrame(all_split_posts)
    

# Example usage
if __name__ == "__main__":
    # Initialize Reddit instance
    reddit_instance = get_reddit_instance()

    # Fetch posts
    subreddit_name = "wallstreetbets"
    post_limit = 10
    fetched_posts_df = fetch_reddit_posts(reddit_instance, subreddit_name, post_limit)

    # Filter posts with stock information
    stock_posts_df = filter_posts_with_stock_info(fetched_posts_df)

    # Print the results
    print(stock_posts_df)