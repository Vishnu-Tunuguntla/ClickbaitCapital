from transformers import AutoModel, AutoTokenizer, AutoModelForCausalLM, LlamaForCausalLM, LlamaTokenizerFast, BitsAndBytesConfig
from peft import PeftModel  # 0.5.0
import pandas as pd

# Load Models
base_model = "NousResearch/Llama-2-13b-hf" 
peft_model = "FinGPT/fingpt-sentiment_llama2-13b_lora"
tokenizer = LlamaTokenizerFast.from_pretrained(base_model)
tokenizer.pad_token = tokenizer.eos_token

# Check if GPU is available
import torch
if torch.cuda.is_available():
    quantization_config = BitsAndBytesConfig(load_in_8bit=True)
    model = LlamaForCausalLM.from_pretrained(base_model, device_map="cuda:0", quantization_config=quantization_config)
else:
    model = LlamaForCausalLM.from_pretrained(base_model)

model = PeftModel.from_pretrained(model, peft_model)
model = model.eval()

def sentiment_analysis_setup():
    # No setup needed for this model
    pass

def calculate_sentimate(df):
    # Function to calculate sentiment using FinGPT model
    def text_to_sentiment(text):
        prompt = f'''Instruction: What is the sentiment of this news? Please choose an answer from {{negative/neutral/positive}}
Input: {text}
Answer: '''
        tokens = tokenizer(prompt, return_tensors='pt', padding=True, max_length=512)
        res = model.generate(**tokens, max_length=512)
        res_sentence = tokenizer.decode(res[0])
        sentiment = res_sentence.split("Answer: ")[1].strip()
        return sentiment

    # Apply the sentiment analysis to each post
    df['sentiment'] = df['Combined'].apply(text_to_sentiment)

    # Display the DataFrame with sentiment scores
    return df

def testing_sentiment_analysis():
    # Sample DataFrame creation (You can replace this with your actual DataFrame)
    data = {
        'Combined': [
            "The company’s quarterly earnings exceeded expectations, driving a significant uptick in share prices. Analysts are bullish about its future prospects.",
            "Despite the recent product launch, the company's stock plummeted due to concerns over supply chain disruptions. Investors are bearish and worried about long-term impacts.",
            "The firm announced a new partnership, which was met with mixed reactions from the market. While some see it as a strategic move, others are skeptical about its immediate benefits.",
            "Oh great, another 'innovative' strategy that will probably result in layoffs. Just what the employees needed."
        ]
    }
    df = pd.DataFrame(data)
    df = calculate_sentimate(df)
    print(df)

# Example usage
if __name__ == "__main__":
    testing_sentiment_analysis()
