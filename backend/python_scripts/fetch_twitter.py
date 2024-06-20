import os
import pandas as pd
from twikit import Client

def get_twitter_client():
    """
    Initialize and return a Twitter client with credentials from environment variables.
    """
    username = os.getenv('TWITTER_USERNAME')
    email = os.getenv('TWITTER_EMAIL')
    password = os.getenv('TWITTER_PASSWORD')

    if not all([username, email, password]):
        raise ValueError("Twitter credentials not found in environment variables")

    client = Client('en-US')
    client.login(
        auth_info_1=username,
        auth_info_2=email,
        password=password
    )
    return client

def fetch_twitter_posts(client, keyword, tweet_limit=10):
    """
    Fetch the latest tweets based on a keyword.

    Parameters:
    client (Client): The Twitter client to use for fetching tweets.
    keyword (str): The keyword to search for in tweets.
    tweet_limit (int): The number of tweets to fetch.

    Returns:
    pd.DataFrame: A DataFrame containing the fetched tweets.
    """
    tweets = client.search_tweet(keyword, 'Latest', count=tweet_limit)

    # Collect tweet text and other relevant information
    data = []

    for tweet in tweets:
        data.append({
            "Title": tweet.id,
            "Content": tweet.text,
            "Combined": tweet.text + tweet.id
        })

    # Create a pandas DataFrame
    df = pd.DataFrame(data)
    return df

# Example usage
if __name__ == "__main__":
    twitter_client = get_twitter_client()
    keyword = "stocks"
    tweet_limit = 20
    fetched_tweets_df = fetch_twitter_posts(twitter_client, keyword, tweet_limit)
    print(fetched_tweets_df)
