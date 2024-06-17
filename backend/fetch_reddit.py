import praw
import pandas as pd

# Set up Reddit API credentials
reddit = praw.Reddit(
    client_id="BH00w0qrrJHescIT_ICeOQ",
    client_secret="UXmHLc1vkiX_xW6jn3qxR1CVI1l1_Q", 
    user_agent="ClickbaitCapital:v1.0.0 (by u/Ok_Nobody6511)",
    username="Ok_Nobody6511",
    password="nrb!vuf6ezw5ENK9wjp"  # Replace with your actual password
)

post_size = 10

def fetch_and_display_posts(reddit_instance, subreddit_name, post_limit):
    """
    Fetch the last `post_limit` posts from the specified subreddit and display them.
    """
    subreddit = reddit_instance.subreddit(subreddit_name)
    posts = subreddit.new(limit=post_limit)

    # Collect titles and selftexts of the last `post_limit` posts
    data = []

    for post in posts:
        data.append({
            "Title": post.title,
            "Content": post.selftext
        })

    # Create a pandas DataFrame
    df = pd.DataFrame(data)

    # Display the DataFrame
    print(df)

    # Save the DataFrame to a CSV file (optional)
    df.to_csv('wallstreetbets_posts.csv', index=False)

# Main execution
if __name__ == "__main__":
    fetch_and_display_posts(reddit, "wallstreetbets", post_size)
