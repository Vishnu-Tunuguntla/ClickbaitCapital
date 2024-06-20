import os
import pandas as pd
from fetch_reddit import get_reddit_instance, fetch_reddit_posts
from stock_name_parser import filter_posts_with_stock_info
from sentimentanalysis import sentiment_analysis_setup, calculate_sentiment
from stock_scorer import score_stocks
from fetch_twitter import fetch_twitter_posts, get_twitter_client
from finvizfinance.screener.performance import Performance
import yfinance as yf

def fetch_and_process_reddit_posts(subreddit_name, post_limit=10):
    reddit_instance = get_reddit_instance()
    fetched_posts_df = fetch_reddit_posts(reddit_instance, "wallstreetbets", post_limit // 2)
    fetched_posts_df2 = fetch_reddit_posts(reddit_instance, "stocks", post_limit // 2)
    combined_df = pd.concat([fetched_posts_df, fetched_posts_df2], ignore_index=True)
    return combined_df

def fetch_and_process_twitter_posts(keyword, tweet_limit=10):   
    twitter_client = get_twitter_client()
    fetched_posts_df = fetch_twitter_posts(twitter_client, "stocks", tweet_limit)
    return fetched_posts_df

def get_top_gainers(limit=15):
    fperf = Performance()
    filters_dict = {'Performance': 'Today +10%', 'Performance 2': 'Today +10%', 'Change from Open': 'Up 20%'}
    fperf.set_filter(filters_dict=filters_dict)
    
    # Get the screener view
    screener_df = fperf.screener_view()
    
    # Check if the DataFrame is empty
    if screener_df.empty:
        return []
    
    # If not empty, return the top tickers
    return screener_df['Ticker'].head(limit).tolist()

def get_stock_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        price = stock.info.get("currentPrice")
        return price if price else "NA"
    except:
        return "NA"

def get_stock_history(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d")
        if not hist.empty:
            hist['Daily_Change'] = hist['Close'].pct_change() * 100
            changes = hist['Daily_Change'].dropna().tolist()
            dates = hist.index.strftime('%Y-%m-%d').tolist()[1:]  # Skip the first date as it has no change
            return list(zip(dates, changes))
        return []
    except Exception as e:
        print(f"Error fetching history for {ticker}: {str(e)}")
        return []

def get_news_for_ticker(ticker):
    stock = yf.Ticker(ticker)
    news = stock.news
    return [article['title'] for article in news]

def create_news_dataframe(tickers):
    data = []
    for ticker in tickers:
        news_titles = get_news_for_ticker(ticker)
        row = {'Stock': ticker, 'Price': get_stock_price(ticker), 'History': get_stock_history(ticker)}
        for i, title in enumerate(news_titles, 1):
            row[f'Article_{i}'] = title
        data.append(row)
    return pd.DataFrame(data)

def backend_pipeline(subreddit_name, post_limit, website_preferences):
    # Fetch and process Reddit posts
    posts_reddit_df = fetch_and_process_reddit_posts(subreddit_name, post_limit)

    # Fetch and process Twitter posts
    posts_twitter_df = fetch_and_process_twitter_posts("stocks", post_limit)

    # Process reddit posts to extract stock names and relevant info
    reddit_df = filter_posts_with_stock_info(posts_reddit_df)
    
    # Process twitter post to extract stock names and relevant info
    twitter_df = filter_posts_with_stock_info(posts_twitter_df)

    # Add price information to reddit and twitter dataframes
    reddit_df['Price'] = reddit_df['Stock'].apply(get_stock_price)
    twitter_df['Price'] = twitter_df['Stock'].apply(get_stock_price)

    # Add historical data to reddit and twitter dataframes
    reddit_df['History'] = reddit_df['Stock'].apply(get_stock_history)
    twitter_df['History'] = twitter_df['Stock'].apply(get_stock_history)

    # Perform sentiment analysis
    sentiment_analysis_setup() # MOVE TO ONE TIME SETUP LATER
    reddit_df = calculate_sentiment(reddit_df)
    twitter_df = calculate_sentiment(twitter_df)

    # Get top gainers and their news
    top_gainers = get_top_gainers()
    news_df = create_news_dataframe(top_gainers)
    news_df = calculate_sentiment(news_df)

    # Add website information
    reddit_df['website'] = 'reddit.com'
    twitter_df['website'] = 'twitter.com'
    news_df['website'] = 'news'

    # Combine all DataFrames
    combined_df = pd.concat([reddit_df, twitter_df, news_df], ignore_index=True)

    # Score stocks based on sentiment and user preferences and return top stocks
    top_stocks_df = score_stocks(combined_df, website_preferences)
    
    return top_stocks_df

# Example usage
if __name__ == "__main__":
    subreddit_name = "wallstreetbets"
    post_limit = 30
    reddit_weight = 0.3
    twitter_weight = 0.3
    news_weight = 0.4
    website_preferences = {"reddit.com": reddit_weight, 
                           "twitter.com": twitter_weight, 
                           "news": news_weight}

    top_stocks_df = backend_pipeline(subreddit_name, post_limit, website_preferences)
    print(top_stocks_df)