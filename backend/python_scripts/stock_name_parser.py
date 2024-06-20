import os
import pandas as pd
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from fetch_reddit import get_reddit_instance, fetch_reddit_posts

# Define the response schema
class StockResponse(BaseModel):
    stock_name: str = Field(description="OFFICIAL STOCK TICKER or absent")

# Initialize the OpenAI client
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("OpenAI API key not found in environment variables")

model = ChatOpenAI(api_key=openai_api_key, model="gpt-4o", temperature=0)
structured_llm = model.with_structured_output(StockResponse)

# Define the prompt template for extracting stock names
extract_prompt_template = PromptTemplate(
    input_variables=["post"],
    template="""
    Analyze the following post and follow these instructions:
    1. If multiple different stocks or tickers are mentioned:
       - Identify the most mentioned or most relevant stock Return OFFICIAL TICKER FORMAT.
    2. If only one type of stock or ticker is mentioned:
       - Return the stock in OFFICIAL TICKER FORMAT.
    3. If no stocks or tickers are mentioned:
       - Return "Absent".
    
    Post: "{post}" 
    """
)

# Define the prompt template for converting stock names to official ticker format
convert_prompt_template = PromptTemplate(
    input_variables=["stock"],
    template="""
    Convert this Stock to its official Ticker format, use web search if you don't know.
    
    Stock: "{stock}"
    """
)

# Create the LLMChains
extract_chain = extract_prompt_template | structured_llm
convert_chain = convert_prompt_template | structured_llm

def extract_stock_names(post: str):
    """
    Extract the stock names or tickers from the post content.

    Parameters:
    post (str): The combined title and content of the post.

    Returns:
    List[str]: The extracted stock names or tickers.
    """
    response = extract_chain.invoke({"post": post})
    stock_name = response.stock_name.strip()  # Extract the stock name from the structured response
    if stock_name.lower() == "absent":
        return []
    return [stock_name]

def convert_to_official_ticker(stock: str):
    """
    Convert the stock name to its official ticker format.

    Parameters:
    stock (str): The stock name to convert.

    Returns:
    str: The official stock ticker or "absent" if not found.
    """
    response = convert_chain.invoke({"stock": stock})
    return response.stock_name.strip()

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
        # Check if 'Combined' key exists and is not empty
        if 'Combined' not in row or not row['Combined'].strip():
            continue

        stock_names = extract_stock_names(row['Combined'])

        for stock_name in stock_names:
            # Check if the stock name is in all caps and has a length of 5 or less
            if not stock_name.isupper() or len(stock_name) > 5:
                stock_name = convert_to_official_ticker(stock_name)

            if stock_name.lower() != "absent":
                all_split_posts.append({
                    "Stock": stock_name,
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
