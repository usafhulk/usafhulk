"""
Text preprocessing utilities for sentiment analysis
"""
import re
import string
import logging
from typing import List
import nltk
from textblob import TextBlob

logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except Exception as e:
    logger.warning(f"Failed to download NLTK data: {e}")


class TextProcessor:
    """Handle text cleaning and preprocessing"""
    
    def __init__(self, remove_urls=True, remove_mentions=True, 
                 remove_hashtags=False, lowercase=True):
        """
        Initialize text processor with configuration
        
        Args:
            remove_urls: Remove URLs from text
            remove_mentions: Remove @mentions from text
            remove_hashtags: Remove hashtags (if False, keeps hashtag content)
            lowercase: Convert text to lowercase
        """
        self.remove_urls = remove_urls
        self.remove_mentions = remove_mentions
        self.remove_hashtags = remove_hashtags
        self.lowercase = lowercase
        
    def clean_text(self, text: str) -> str:
        """
        Clean and preprocess text for sentiment analysis
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text string
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Remove URLs
        if self.remove_urls:
            text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove @mentions
        if self.remove_mentions:
            text = re.sub(r'@\w+', '', text)
        
        # Handle hashtags
        if self.remove_hashtags:
            text = re.sub(r'#\w+', '', text)
        else:
            # Remove the # but keep the word
            text = re.sub(r'#(\w+)', r'\1', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Convert to lowercase
        if self.lowercase:
            text = text.lower()
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?\'-]', '', text)
        
        return text.strip()
    
    def process_batch(self, texts: List[str]) -> List[str]:
        """
        Process a batch of texts
        
        Args:
            texts: List of text strings to process
            
        Returns:
            List of cleaned text strings
        """
        return [self.clean_text(text) for text in texts]
    
    def extract_emojis(self, text: str) -> List[str]:
        """
        Extract emojis from text
        
        Args:
            text: Text to extract emojis from
            
        Returns:
            List of emojis found
        """
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
        return emoji_pattern.findall(text)
    
    def get_word_tokens(self, text: str) -> List[str]:
        """
        Tokenize text into words
        
        Args:
            text: Text to tokenize
            
        Returns:
            List of word tokens
        """
        blob = TextBlob(text)
        return blob.words
    
    def remove_stopwords(self, text: str) -> str:
        """
        Remove common stopwords from text
        
        Args:
            text: Text to process
            
        Returns:
            Text with stopwords removed
        """
        try:
            from nltk.corpus import stopwords
            stop_words = set(stopwords.words('english'))
            words = text.split()
            filtered_words = [word for word in words if word.lower() not in stop_words]
            return ' '.join(filtered_words)
        except Exception as e:
            logger.warning(f"Could not remove stopwords: {e}")
            return text


def analyze_sentiment(text: str) -> dict:
    """
    Analyze sentiment of text using TextBlob
    
    Args:
        text: Text to analyze
        
    Returns:
        Dictionary containing polarity, subjectivity, and classification
    """
    if not text:
        return {
            'polarity': 0.0,
            'subjectivity': 0.0,
            'classification': 'neutral'
        }
    
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    # Classify sentiment
    if polarity > 0.1:
        classification = 'positive'
    elif polarity < -0.1:
        classification = 'negative'
    else:
        classification = 'neutral'
    
    return {
        'polarity': polarity,
        'subjectivity': subjectivity,
        'classification': classification
    }
