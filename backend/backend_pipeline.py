from fetch_reddit import get_reddit_instance, fetch_reddit_posts
from stock_name_parser import filter_posts_with_stock_info

def calculate_reddit_sentiment_score():
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

calculate_reddit_sentiment_score()