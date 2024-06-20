def sentiment_analysis_setup():
    import nltk
    # Download the VADER lexicon for sentiment analysis
    nltk.download('vader_lexicon')

def calculate_sentimate(df):
    # might be a trouble point here, might have to download it every time if the lexicon is not being recognized when running.
    from nltk.sentiment import SentimentIntensityAnalyzer

    # Initialize SentimentIntensityAnalyzer
    sia = SentimentIntensityAnalyzer()

    # Function to calculate sentiment
    def text_to_sentiment(text):
        sentiment = sia.polarity_scores(text)
        return sentiment['compound']

    # Apply the sentiment analysis to each post
    df['sentiment'] = df['Combined'].apply(text_to_sentiment)

    # Remove rows where sentiment is 0
    df = df[df['sentiment'] != 0]

    # Display the DataFrame with sentiment scores
    return df

def testing_sentiment_analysis():
    sentiment_analysis_setup()

    # Sample DataFrame creation (You can replace this with your actual DataFrame)
    import pandas as pd
    data = {
        'Combined': [
            "The company’s quarterly earnings exceeded expectations, driving a significant uptick in share prices. Analysts are bullish about its future prospects.",
            "Despite the recent product launch, the company's stock plummeted due to concerns over supply chain disruptions. Investors are bearish and worried about long-term impacts.",
            "The firm announced a new partnership, which was met with mixed reactions from the market. While some see it as a strategic move, others are skeptical about its immediate benefits.",
            "Oh great, another 'innovative' strategy that will probably result in layoffs. Just what the employees needed."
        ]
    }
    df = pd.DataFrame(data)
    calculate_sentimate(df)

# Example usage
if __name__ == "__main__":
    testing_sentiment_analysis()
