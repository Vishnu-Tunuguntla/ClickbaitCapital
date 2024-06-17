import os
import pandas as pd
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from pydantic import BaseModel, Field
from typing import Optional, List
from fetch_reddit import get_reddit_instance, fetch_reddit_posts

# Define the response schema
class StockResponse(BaseModel):
    stock_name: Optional[str] = Field(description="The extracted stock name or ticker")

# Initialize the OpenAI client
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("OpenAI API key not found in environment variables")

llm = OpenAI(api_key=openai_api_key, model="gpt-3.5-turbo-instruct")

# Define the prompt template
prompt_template = PromptTemplate(
    input_variables=["post"],
    template="Extract only the stock names or tickers from this post. For multiple stocks, separate stocks using commas. If there is no stock, return Absent: \"{post}\""
)

# Create the LLMChain
chain = prompt_template | llm

def extract_stock_names(post: str) -> List[str]:
    """
    Extract the stock names or tickers from the post content.

    Parameters:
    post (str): The combined title and content of the post.

    Returns:
    List[str]: The extracted stock names or tickers.
    """
    response = chain.invoke({"post": post})
    stock_names = response.strip()
    if stock_names.lower() == "absent":
        return []
    return [name.strip() for name in stock_names.split(',')]

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
            all_split_posts.append({
                    "Stock": stock_names[0],
                    "Combined": row['Combined']
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
