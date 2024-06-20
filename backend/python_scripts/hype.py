from finvizfinance.screener.performance import Performance
import yfinance as yf
import pandas as pd

def get_top_gainers(limit=15):
    fperf = Performance()
    filters_dict = {'Performance': 'Today +10%', 'Performance 2': 'Today +10%', 'Change from Open': 'Up 20%'}
    fperf.set_filter(filters_dict=filters_dict)
    top_gainers_df = fperf.screener_view()
    return top_gainers_df['Ticker'].head(limit).tolist()

def get_news_for_ticker(ticker):
    stock = yf.Ticker(ticker)
    news = stock.news
    return [article['title'] for article in news]

def create_news_dataframe(tickers):
    data = []
    for ticker in tickers:
        news_titles = get_news_for_ticker(ticker)
        row = {'Stock': ticker}
        for i, title in enumerate(news_titles, 1):
            row[f'Article_{i}'] = title
        data.append(row)
    return pd.DataFrame(data)

# Get top gainers
top_gainers = get_top_gainers()

# Create news dataframe
news_df = create_news_dataframe(top_gainers)

# Display the result
print(news_df)