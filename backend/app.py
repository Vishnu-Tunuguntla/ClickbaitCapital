# app.py
import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from backend_pipeline import backend_pipeline

app = Flask(__name__)

# Get the frontend host from environment variables or use a default value
frontend_host = os.environ.get('FRONTEND_HOST', "*")

# Enable CORS for the specified frontend host
CORS(app, resources={r"/api/*": {"origins": [frontend_host]}})

@app.route('/api/top-stocks', methods=['GET'])
def get_top_stocks():
    subreddit_name = request.args.get('subreddit', default='wallstreetbets', type=str)
    post_limit = request.args.get('limit', default=25, type=int)
    reddit_weight = request.args.get('reddit_weight', default=0.5, type=float)
    twitter_weight = request.args.get('twitter_weight', default=0.3, type=float)
    facebook_weight = request.args.get('facebook_weight', default=0.2, type=float)
    
    website_preferences = {
        "reddit.com": reddit_weight,
        "twitter.com": twitter_weight,
        "facebook.com": facebook_weight
    }
    
    try:
        top_stocks_df = backend_pipeline(subreddit_name, post_limit, website_preferences)
        filtered_df = top_stocks_df[['Stock', 'sentiment', 'website', 'preference_score']]
        top_stocks_json = filtered_df.to_dict(orient='records')
        return jsonify(top_stocks_json)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
