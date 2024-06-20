import pandas as pd
import numpy as np

def score_stocks(df, website_preferences):
    # Normalize the preferences to sum to 1
    total_preference = sum(website_preferences.values())
    website_preferences = {k: v / total_preference for k, v in website_preferences.items()}

    # Function to calculate preference score
    def calculate_preference_score(row):
        website = row['website']
        sentiment = abs(row['sentiment'])
        preference = website_preferences.get(website, 0)  # Default to 0 if website not in preferences
        return sentiment * preference

    # Apply the preference score calculation
    df['preference_score'] = df.apply(calculate_preference_score, axis=1)

    # Sort by preference score and select top 5 stocks
    top_stocks = df.sort_values(by='preference_score', ascending=False).head(5)

    return top_stocks

def test_score_stocks():
    # WIP
# Sample DataFrame creation (replace this with your actual DataFrame)
    data = {
        'Combined': [
            "I think AAPL is going to skyrocket next quarter.",
            "MSFT is showing some promising signs.",
            "What are your thoughts on TSLA?",
            "Investing in GOOGL has been really profitable.",
            "I am worried about AMZN's recent performance.",
            "General comment about the market without any stock mention."
        ],
        'website': [
            "website1.com",
            "website2.com",
            "website3.com",
            "website1.com",
            "website2.com",
            "website3.com"
        ],
        'Stock': ["AAPL", "MSFT", "TSLA", "GOOGL", "AMZN", None],
        'sentiment': [0.9, 0.75, 0.85, 0.8, -0.4, 0]
    }
    df = pd.DataFrame(data)
    df = df[df['Stock'].notna()]  # Remove rows without stock names
    top_stocks = score_stocks(df, {'website1.com': 0.5, 'website2.com': 0.5, 'website3.com': 0.5})

    # Display the top 5 stocks
    print("Top 5 Suggested Stocks:")
    print(top_stocks[['Stock', 'preference_score']])

if __name__ == "__main__":
    test_score_stocks()
