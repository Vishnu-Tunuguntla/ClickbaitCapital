import os
import json
import praw
import pandas as pd

def get_reddit_instance():
    """
    Initialize and return a Reddit instance with credentials from environment variable.
    """
    reddit_credentials = os.getenv('REDDIT_CREDENTIALS')
    if not reddit_credentials:
        raise ValueError("Reddit credentials not found in environment variables")
    
    credentials = json.loads(reddit_credentials)
    
    reddit = praw.Reddit(
        client_id=credentials['client_id'],
        client_secret=credentials['client_secret'],
        user_agent=credentials['user_agent'],
        username=credentials['username'],
        password=credentials['password']
    )
    return reddit

def fetch_reddit_posts(reddit_instance, subreddit_name, post_limit=10):
    """
    Fetch the last `post_limit` posts from the specified subreddit.

    Parameters:
    reddit_instance (praw.Reddit): The Reddit instance to use for fetching posts.
    subreddit_name (str): The name of the subreddit to fetch posts from.
    post_limit (int): The number of posts to fetch.

    Returns:
    pd.DataFrame: A DataFrame containing the fetched posts.
    """
    subreddit = reddit_instance.subreddit(subreddit_name)
    posts = subreddit.new(limit=post_limit)

    # Collect titles and selftexts of the last `post_limit` posts
    data = []

    for post in posts:
        combined_content = f"{post.title} {post.selftext}"
        data.append({
            "Title": post.title,
            "Content": post.selftext,
            "Combined": combined_content
        })

    # Create a pandas DataFrame
    df = pd.DataFrame(data)
    return df

# Example usage
if __name__ == "__main__":
    reddit_instance = get_reddit_instance()
    subreddit_name = "wallstreetbets"
    post_limit = 30
    fetched_posts_df = fetch_reddit_posts(reddit_instance, subreddit_name, post_limit)
    print(fetched_posts_df)
