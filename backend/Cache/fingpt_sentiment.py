import requests

# Define the API URL and headers
API_URL = "https://api-inference.huggingface.co/models/FinGPT/fingpt-sentiment_llama2-13b_lora"
headers = {"Authorization": "Bearer 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"}

# Define the prompts
prompts = [
    '''Instruction: What is the sentiment of this news? Please choose an answer from {negative/neutral/positive}
    Input: FINANCING OF ASPOCOMP 'S GROWTH Aspocomp is aggressively pursuing its growth strategy by increasingly focusing on technologically more demanding HDI printed circuit boards PCBs .
    Answer: ''',

    '''Instruction: What is the sentiment of this news? Please choose an answer from {negative/neutral/positive}
    Input: According to Gran , the company has no plans to move all production to Russia , although that is where the company is growing .
    Answer: ''',

    '''Instruction: What is the sentiment of this news? Please choose an answer from {negative/neutral/positive}
    Input: A tinyurl link takes users to a scamming site promising that users can earn thousands of dollars by becoming a Google ( NASDAQ : GOOG ) Cash advertiser .
    Answer: ''',
]

# Function to query the API
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Prepare the payload
data = {
    "inputs": prompts,
    "parameters": {
        "max_length": 512,
        "return_full_text": False
    }
}

# Make the API call
result = query(data)

# Debugging: Print the raw response
print("Raw API response:", result)

# Extract and print the results
for output in result:
    if isinstance(output, dict) and 'generated_text' in output:
        print(output['generated_text'].split("Answer: ")[1].strip())
    else:
        print("Unexpected response format:", output)
