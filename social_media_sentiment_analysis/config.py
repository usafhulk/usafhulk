"""
Configuration settings for sentiment analysis
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Credentials (loaded from environment variables)
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY', '')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET', '')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN', '')
TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET', '')
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN', '')

REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID', '')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET', '')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'SentimentAnalyzer/1.0')

# Sentiment Analysis Thresholds
SENTIMENT_THRESHOLDS = {
    'positive': 0.1,    # Polarity > 0.1 is positive
    'negative': -0.1,   # Polarity < -0.1 is negative
    # Between -0.1 and 0.1 is neutral
}

# Data Collection Settings
DEFAULT_TWEET_COUNT = 100
DEFAULT_REDDIT_LIMIT = 100
MAX_RETRIES = 3
RATE_LIMIT_WAIT = 15  # seconds to wait on rate limit

# Output Settings
OUTPUT_DIR = 'output'
VISUALIZATIONS_DIR = os.path.join(OUTPUT_DIR, 'visualizations')
DATA_DIR = os.path.join(OUTPUT_DIR, 'data')

# Logging Configuration
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = os.path.join(OUTPUT_DIR, 'sentiment_analysis.log')

# Text Processing Settings
REMOVE_URLS = True
REMOVE_MENTIONS = True
REMOVE_HASHTAGS = False  # Keep hashtags but clean them
LOWERCASE = True

# Create output directories if they don't exist
for directory in [OUTPUT_DIR, VISUALIZATIONS_DIR, DATA_DIR]:
    os.makedirs(directory, exist_ok=True)
