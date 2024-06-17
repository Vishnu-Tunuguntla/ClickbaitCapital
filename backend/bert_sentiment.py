from transformers import BertTokenizer, BertForSequenceClassification, TextClassificationPipeline

# Load pre-trained FinBERT model and tokenizer
model_name = "yiyanghkust/finbert-tone"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Create a pipeline for sentiment analysis
pipeline = TextClassificationPipeline(model=model, tokenizer=tokenizer, return_all_scores=True)

# Sample texts
texts = [
    "The company’s quarterly earnings exceeded expectations, driving a significant uptick in share prices. Analysts are bullish about its future prospects.",
    "Despite the recent product launch, the company's stock plummeted due to concerns over supply chain disruptions. Investors are bearish and worried about long-term impacts.",
    "The firm announced a new partnership, which was met with mixed reactions from the market. While some see it as a strategic move, others are skeptical about its immediate benefits.",
    "Oh great, another 'innovative' strategy that will probably result in layoffs. Just what the employees needed."
]

# Analyze sentiments
results = pipeline(texts)
for text, result in zip(texts, results):
    print(f"Text: {text}\nSentiments: {result}\n")


for text, result in zip(texts, results):
    most_likely_sentiment = max(result, key=lambda x: x['score'])
    print(f"Text: {text}\nMost Likely Sentiment: {most_likely_sentiment['label']}, Score: {most_likely_sentiment['score']}\n")