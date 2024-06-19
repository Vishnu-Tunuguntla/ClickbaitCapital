import os
import pandas as pd
from fetch_reddit import get_reddit_instance, fetch_reddit_posts
from stock_name_parser import filter_posts_with_stock_info
# from bert_sentiment import calculate_sentiment
from sentimentanalysis import sentiment_analysis_setup, calculate_sentimate
from stock_scorer import score_stocks
from fetch_twitter import fetch_twitter_posts
from fetch_twitter import get_twitter_client
def fetch_and_process_reddit_posts(subreddit_name, post_limit=10):
    reddit_instance = get_reddit_instance()
    fetched_posts_df = fetch_reddit_posts(reddit_instance, subreddit_name, post_limit)
    return fetched_posts_df

def fetch_and_process_twitter_posts(keyword, tweet_limit=10):   
    twitter_client = get_twitter_client()
    fetched_posts_df = fetch_twitter_posts(twitter_client, "stocks", tweet_limit)
    return fetched_posts_df

def perform_sentiment_analysis(stock_df):
    return stock_df


def get_top_stocks(stock_df, top_n=5):
    top_stocks_df = stock_df.nlargest(top_n, 'Score')
    return top_stocks_df

def backend_pipeline(subreddit_name,  post_limit, website_preferences):
    # Fetch and process Reddit posts
    posts_reddit_df = fetch_and_process_reddit_posts(subreddit_name, post_limit)

    # Fetch and process Twitter posts
    posts_twitter_df = fetch_and_process_twitter_posts("stocks", post_limit)
    # Process reddit posts to extract stock names and relevant info
    reddit_df = filter_posts_with_stock_info(posts_reddit_df)
    
    # Process twitter post to extract stock names and relevant info
    twitter_df = filter_posts_with_stock_info(posts_twitter_df)

    # Perform sentiment analysis
    sentiment_analysis_setup() # MOVE TO ONE TIME SETUP LATER
    reddit_df = calculate_sentimate(reddit_df)
    twitter_df = calculate_sentimate(twitter_df)

    #SPECIFIC TO REDDIT
    reddit_df['website'] = 'reddit.com'
    twitter_df['website'] = 'twitter.com'
    # Combine Reddit and Twitter DataFrames
    combined_df = pd.concat([reddit_df, twitter_df], ignore_index=True)
    # Score stocks based on sentiment and user preferences and return top stocks
    top_stocks_df = score_stocks(combined_df, website_preferences)
    
    return top_stocks_df

# Example usage
if __name__ == "__main__":
    subreddit_name = "wallstreetbets"
    post_limit = 10
    reddit_weight = 0.5
    twitter_weight = 0.5
    facebook_weight = 0.0
    website_preferences = {"reddit.com" : reddit_weight, 
                           "twitter.com" : twitter_weight, 
                           "facebook.com" : facebook_weight}

    top_stocks_df = backend_pipeline(subreddit_name, post_limit, website_preferences)
    print(top_stocks_df)