import pandas as pd
import numpy as np

# Sample DataFrame creation (replace this with your actual DataFrame)
data = {
    'post_content': [
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
    'sentiment': [0.9, 0.75, 0.85, 0.8, -0.4, 0],
    'stock_name': ["AAPL", "MSFT", "TSLA", "GOOGL", "AMZN", None]
}
df = pd.DataFrame(data)
df = df[df['stock_name'].notna()]  # Remove rows without stock names

# User-defined preferences for websites (example)
website_preferences = {
    "website1.com": 5,  # Preference scale from 1 to 5
    "website2.com": 3,
    "website3.com": 1
}

# Normalize the preferences to sum to 1
total_preference = sum(website_preferences.values())
website_preferences = {k: v / total_preference for k, v in website_preferences.items()}

# Function to calculate preference score
def calculate_preference_score(row):
    website = row['website']
    sentiment = row['sentiment']
    preference = website_preferences.get(website, 0)  # Default to 0 if website not in preferences
    return sentiment * preference

# Apply the preference score calculation
df['preference_score'] = df.apply(calculate_preference_score, axis=1)

# Sort by preference score and select top 5 stocks
top_stocks = df.sort_values(by='preference_score', ascending=False).head(5)

# Display the top 5 stocks
print("Top 5 Suggested Stocks:")
print(top_stocks[['stock_name', 'preference_score']])
