"""
Data scraping module for collecting social media data
"""
import logging
import time
import json
import csv
from typing import List, Dict, Optional
from datetime import datetime
import pandas as pd

logger = logging.getLogger(__name__)


class BaseScraper:
    """Base class for data scrapers"""
    
    def __init__(self):
        self.data = []
    
    def get_data(self) -> List[Dict]:
        """Return collected data"""
        return self.data


class TwitterScraper(BaseScraper):
    """Scraper for Twitter/X data using tweepy"""
    
    def __init__(self, api_key: str, api_secret: str, 
                 access_token: str, access_secret: str,
                 bearer_token: str = None):
        """
        Initialize Twitter scraper
        
        Args:
            api_key: Twitter API key
            api_secret: Twitter API secret
            access_token: Twitter access token
            access_secret: Twitter access token secret
            bearer_token: Twitter bearer token (optional, for API v2)
        """
        super().__init__()
        self.client = None
        self.api = None
        
        try:
            import tweepy
            
            # Try to use API v2 if bearer token is provided
            if bearer_token:
                self.client = tweepy.Client(bearer_token=bearer_token)
            
            # Also set up API v1.1 for fallback
            if api_key and api_secret and access_token and access_secret:
                auth = tweepy.OAuth1UserHandler(
                    api_key, api_secret,
                    access_token, access_secret
                )
                self.api = tweepy.API(auth, wait_on_rate_limit=True)
                
        except ImportError:
            logger.error("tweepy not installed. Install with: pip install tweepy")
        except Exception as e:
            logger.error(f"Failed to initialize Twitter scraper: {e}")
    
    def search_tweets(self, keyword: str, count: int = 100) -> List[Dict]:
        """
        Search for tweets containing keyword
        
        Args:
            keyword: Search keyword or hashtag
            count: Number of tweets to retrieve
            
        Returns:
            List of tweet dictionaries
        """
        if not self.client and not self.api:
            logger.error("Twitter API not initialized")
            return []
        
        try:
            tweets = []
            
            # Try API v2 first
            if self.client:
                response = self.client.search_recent_tweets(
                    query=keyword,
                    max_results=min(count, 100),
                    tweet_fields=['created_at', 'text', 'author_id', 'public_metrics']
                )
                
                if response.data:
                    for tweet in response.data:
                        tweets.append({
                            'id': tweet.id,
                            'text': tweet.text,
                            'created_at': tweet.created_at.isoformat() if tweet.created_at else None,
                            'author_id': tweet.author_id,
                            'source': 'twitter'
                        })
            
            # Fallback to API v1.1
            elif self.api:
                for tweet in tweepy.Cursor(
                    self.api.search_tweets,
                    q=keyword,
                    lang="en",
                    tweet_mode="extended"
                ).items(count):
                    tweets.append({
                        'id': tweet.id,
                        'text': tweet.full_text,
                        'created_at': tweet.created_at.isoformat(),
                        'author_id': tweet.user.id,
                        'source': 'twitter'
                    })
            
            self.data.extend(tweets)
            logger.info(f"Collected {len(tweets)} tweets for keyword: {keyword}")
            return tweets
            
        except Exception as e:
            logger.error(f"Error searching tweets: {e}")
            return []


class RedditScraper(BaseScraper):
    """Scraper for Reddit data using PRAW"""
    
    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        """
        Initialize Reddit scraper
        
        Args:
            client_id: Reddit app client ID
            client_secret: Reddit app client secret
            user_agent: Reddit API user agent
        """
        super().__init__()
        self.reddit = None
        
        try:
            import praw
            self.reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent
            )
            logger.info("Reddit scraper initialized successfully")
        except ImportError:
            logger.error("praw not installed. Install with: pip install praw")
        except Exception as e:
            logger.error(f"Failed to initialize Reddit scraper: {e}")
    
    def scrape_subreddit(self, subreddit_name: str, limit: int = 100, 
                         time_filter: str = 'week') -> List[Dict]:
        """
        Scrape posts from a subreddit
        
        Args:
            subreddit_name: Name of subreddit (without r/)
            limit: Number of posts to retrieve
            time_filter: Time filter (hour, day, week, month, year, all)
            
        Returns:
            List of post dictionaries
        """
        if not self.reddit:
            logger.error("Reddit API not initialized")
            return []
        
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            posts = []
            
            for submission in subreddit.top(time_filter=time_filter, limit=limit):
                post_data = {
                    'id': submission.id,
                    'title': submission.title,
                    'text': submission.selftext,
                    'score': submission.score,
                    'created_at': datetime.fromtimestamp(submission.created_utc).isoformat(),
                    'num_comments': submission.num_comments,
                    'source': 'reddit',
                    'subreddit': subreddit_name
                }
                posts.append(post_data)
            
            self.data.extend(posts)
            logger.info(f"Collected {len(posts)} posts from r/{subreddit_name}")
            return posts
            
        except Exception as e:
            logger.error(f"Error scraping subreddit: {e}")
            return []
    
    def scrape_comments(self, subreddit_name: str, limit: int = 100) -> List[Dict]:
        """
        Scrape comments from a subreddit
        
        Args:
            subreddit_name: Name of subreddit
            limit: Number of comments to retrieve
            
        Returns:
            List of comment dictionaries
        """
        if not self.reddit:
            logger.error("Reddit API not initialized")
            return []
        
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            comments = []
            
            for comment in subreddit.comments(limit=limit):
                comment_data = {
                    'id': comment.id,
                    'text': comment.body,
                    'score': comment.score,
                    'created_at': datetime.fromtimestamp(comment.created_utc).isoformat(),
                    'source': 'reddit',
                    'subreddit': subreddit_name
                }
                comments.append(comment_data)
            
            self.data.extend(comments)
            logger.info(f"Collected {len(comments)} comments from r/{subreddit_name}")
            return comments
            
        except Exception as e:
            logger.error(f"Error scraping comments: {e}")
            return []


class FileScraper(BaseScraper):
    """Scraper for reading data from files"""
    
    def __init__(self):
        super().__init__()
    
    def load_csv(self, filepath: str, text_column: str = 'text') -> List[Dict]:
        """
        Load data from CSV file
        
        Args:
            filepath: Path to CSV file
            text_column: Name of column containing text data
            
        Returns:
            List of data dictionaries
        """
        try:
            df = pd.read_csv(filepath)
            
            if text_column not in df.columns:
                logger.error(f"Column '{text_column}' not found in CSV")
                return []
            
            data = df.to_dict('records')
            self.data = data
            logger.info(f"Loaded {len(data)} records from {filepath}")
            return data
            
        except Exception as e:
            logger.error(f"Error loading CSV file: {e}")
            return []
    
    def load_json(self, filepath: str) -> List[Dict]:
        """
        Load data from JSON file
        
        Args:
            filepath: Path to JSON file
            
        Returns:
            List of data dictionaries
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Ensure data is a list
            if not isinstance(data, list):
                data = [data]
            
            self.data = data
            logger.info(f"Loaded {len(data)} records from {filepath}")
            return data
            
        except Exception as e:
            logger.error(f"Error loading JSON file: {e}")
            return []


def save_data(data: List[Dict], output_path: str, format: str = 'csv'):
    """
    Save collected data to file
    
    Args:
        data: List of data dictionaries
        output_path: Path to save file
        format: Output format ('csv' or 'json')
    """
    try:
        if format == 'csv':
            df = pd.DataFrame(data)
            df.to_csv(output_path, index=False)
        elif format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Data saved to {output_path}")
    except Exception as e:
        logger.error(f"Error saving data: {e}")
