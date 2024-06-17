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
    df['sentiment'] = df['post_content'].apply(text_to_sentiment)

    # Display the DataFrame with sentiment scores
    print(df)
    return df

def testing_sentiment_analysis():
    sentiment_analysis_setup()

    # Sample DataFrame creation (You can replace this with your actual DataFrame)
    import pandas as pd
    data = {
        'post_content': [
            "I love this product! It has changed my life.",
            "This is the worst service I have ever experienced.",
            "I feel neutral about this.",
            "This is an amazing opportunity, I'm thrilled!",
            "I'm so sad about the outcome."
        ]
    }
    df = pd.DataFrame(data)
    calculate_sentimate(df)