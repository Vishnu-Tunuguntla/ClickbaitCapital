import os
import pandas as pd
from fetch_reddit import get_reddit_instance, fetch_reddit_posts
from stock_name_parser import filter_posts_with_stock_info
# from bert_sentiment import calculate_sentiment
from sentimentanalysis import sentiment_analysis_setup, calculate_sentimate
from stock_scorer import score_stocks

def fetch_and_process_reddit_posts(subreddit_name, post_limit=10):
    reddit_instance = get_reddit_instance()
    fetched_posts_df = fetch_reddit_posts(reddit_instance, subreddit_name, post_limit)
    return fetched_posts_df

def perform_sentiment_analysis(stock_df):
    return stock_df


def get_top_stocks(stock_df, top_n=5):
    top_stocks_df = stock_df.nlargest(top_n, 'Score')
    return top_stocks_df

def backend_pipeline(subreddit_name, post_limit, website_preferences):
    # Fetch and process Reddit posts
    posts_df = fetch_and_process_reddit_posts(subreddit_name, post_limit)

    # Process posts to extract stock names and relevant info
    stock_df = filter_posts_with_stock_info(posts_df)

    # Perform sentiment analysis
    sentiment_analysis_setup() # MOVE TO ONE TIME SETUP LATER
    stock_df = calculate_sentimate(stock_df)

    #SPECIFIC TO REDDIT
    stock_df['website'] = 'reddit.com'
    # Score stocks based on sentiment and user preferences and return top stocks
    top_stocks_df = score_stocks(stock_df, website_preferences)

    return top_stocks_df

# Example usage
if __name__ == "__main__":
    subreddit_name = "wallstreetbets"
    post_limit = 25
    reddit_weight = 0.5
    twitter_weight = 0.3
    facebook_weight = 0.2
    website_preferences = {"reddit.com" : reddit_weight, 
                           "twitter.com" : twitter_weight, 
                           "facebook.com" : facebook_weight}

    top_stocks_df = backend_pipeline(subreddit_name, post_limit, website_preferences)
    print(top_stocks_df)