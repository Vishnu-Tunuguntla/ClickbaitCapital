import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification, TextClassificationPipeline

# Load pre-trained FinBERT model and tokenizer
model_name = "yiyanghkust/finbert-tone"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Create a pipeline for sentiment analysis
pipeline = TextClassificationPipeline(model=model, tokenizer=tokenizer, return_all_scores=True)

def sentiment_analysis_setup():
    pass  # No setup needed for transformers

def calculate_sentiment(df):
    # Function to calculate sentiment using FinBERT
    def text_to_sentiment(text):
        result = pipeline(text)[0]
        # Choose the sentiment with the highest score
        most_likely_sentiment = max(result, key=lambda x: x['score'])
        label = most_likely_sentiment['label']
        score = most_likely_sentiment['score']
        # Adjust the score based on the sentiment label
        if label == 'Positive':
            return score
        elif label == 'Negative':
            return -score
        else:  # neutral
            return 0

    # Apply the sentiment analysis to each post
    df['sentiment'] = df['post_content'].apply(text_to_sentiment)

    # Display the DataFrame with sentiment scores
    print(df)
    return df

def testing_sentiment_analysis():
    sentiment_analysis_setup()

    # Sample DataFrame creation (You can replace this with your actual DataFrame)
    data = {
        'post_content': [
            "The company’s quarterly earnings exceeded expectations, driving a significant uptick in share prices. Analysts are bullish about its future prospects.",
            "Despite the recent product launch, the company's stock plummeted due to concerns over supply chain disruptions. Investors are bearish and worried about long-term impacts.",
            "The firm announced a new partnership, which was met with mixed reactions from the market. While some see it as a strategic move, others are skeptical about its immediate benefits.",
            "Oh great, another 'innovative' strategy that will probably result in layoffs. Just what the employees needed."
        ]
    }
    df = pd.DataFrame(data)
    calculate_sentiment(df)

# Example usage
if __name__ == "__main__":
    testing_sentiment_analysis()
