import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd

def sentiment_analysis_setup():
    nltk.download('vader_lexicon')

def calculate_sentiment(df):
    sia = SentimentIntensityAnalyzer()

    def text_to_sentiment(text):
        sentiment = sia.polarity_scores(text)
        return sentiment['compound']

    if 'Combined' in df.columns:
        # For Reddit and Twitter posts
        df['sentiment'] = df['Combined'].apply(text_to_sentiment)
    elif 'Stock' in df.columns:
        # For news articles
        article_columns = [col for col in df.columns if col.startswith('Article_')]
        
        def calculate_average_sentiment(row):
            sentiments = [text_to_sentiment(row[col]) for col in article_columns if pd.notna(row[col])]
            return sum(sentiments) / len(sentiments) if sentiments else 0

        df['sentiment'] = df.apply(calculate_average_sentiment, axis=1)

    # Remove rows where sentiment is 0
    df = df[df['sentiment'] != 0]

    return df

def testing_sentiment_analysis():
    sentiment_analysis_setup()

    # Sample DataFrame for Reddit/Twitter
    data1 = {
        'Combined': [
            "The company's quarterly earnings exceeded expectations, driving a significant uptick in share prices.",
            "Despite the recent product launch, the company's stock plummeted due to concerns over supply chain disruptions."
        ]
    }
    df1 = pd.DataFrame(data1)
    print("Reddit/Twitter sentiment:")
    print(calculate_sentiment(df1))

    # Sample DataFrame for news articles
    data2 = {
        'Stock': ['AAPL', 'GOOGL'],
        'Article_1': ['Apple reports record profits', 'Google launches new AI product'],
        'Article_2': ['iPhone sales surge', 'Alphabet stock hits all-time high']
    }
    df2 = pd.DataFrame(data2)
    print("\nNews sentiment:")
    print(calculate_sentiment(df2))

if __name__ == "__main__":
    testing_sentiment_analysis()