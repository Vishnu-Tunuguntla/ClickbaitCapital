import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification, TextClassificationPipeline

# Load pre-trained FinBERT model and tokenizer
model_name = "yiyanghkust/finbert-tone"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Create a pipeline for sentiment analysis
pipeline = TextClassificationPipeline(model=model, tokenizer=tokenizer, return_all_scores=True)

def calculate_sentiment(df):
    # Function to calculate sentiment using FinBERT
    def text_to_sentiment(text):

        result = pipeline(text)[0]
        # Choose the sentiment with the highest score
        print(text)
        print(result)
        most_likely_sentiment = max(result, key=lambda x: x['score'])
        print(most_likely_sentiment)
        label = most_likely_sentiment['label']
        score = most_likely_sentiment['score']
        # Adjust the score based on the sentiment label
        print("LABELS")
        print(label, score)
        if label == 'Positive':
            return score
        elif label == 'Negative':
            return -score
        else:  # neutral
            return 0

    # Apply the sentiment analysis to each post
    df['sentiment'] = df['Combined'].apply(text_to_sentiment)

    # Display the DataFrame with sentiment scores
    print(df)
    return df

def testing_sentiment_analysis():
    # Sample DataFrame creation (You can replace this with your actual DataFrame)
    data = {
        'Combined': [
            "The company’s quarterly earnings exceeded expectations, driving a significant uptick in share prices. Analysts are bullish about its future prospects.",
            "Despite the recent product launch, the company's stock plummeted due to concerns over supply chain disruptions. Investors are bearish and worried about long-term impacts.",
            "The firm announced a new partnership, which was met with mixed reactions from the market. While some see it as a strategic move, others are skeptical about its immediate benefits.",
            "Oh great, another 'innovative' strategy that will probably result in layoffs. Just what the employees needed.",
            "I think $Amzn breaks $200 The earning aren’t far away and it’s lagging other mega cap tech, I think it busts through $200 before August. It had to clear and hold 188.35 but then it breaks out."
        ]
    }
    df = pd.DataFrame(data)
    calculate_sentiment(df)

# Example usage
if __name__ == "__main__":
    testing_sentiment_analysis()
