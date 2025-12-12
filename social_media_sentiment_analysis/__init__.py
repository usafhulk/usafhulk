"""
Social Media Sentiment Analysis Tool

A comprehensive Python package for scraping and analyzing social media data
to determine sentiment using TextBlob.
"""

__version__ = '1.0.0'
__author__ = 'Christopher Banner'
__email__ = 'chrisbanner38@gmail.com'

from .sentiment_analyzer import SentimentAnalyzer
from .text_processor import TextProcessor, analyze_sentiment
from .data_scraper import TwitterScraper, RedditScraper, FileScraper
from .visualizer import SentimentVisualizer

__all__ = [
    'SentimentAnalyzer',
    'TextProcessor',
    'analyze_sentiment',
    'TwitterScraper',
    'RedditScraper',
    'FileScraper',
    'SentimentVisualizer',
]
