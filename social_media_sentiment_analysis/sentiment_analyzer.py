"""
Main sentiment analysis script with command-line interface
"""
import argparse
import logging
import sys
import os
from datetime import datetime
import pandas as pd
from typing import List, Dict

# Import local modules
import config
from text_processor import TextProcessor, analyze_sentiment
from data_scraper import (TwitterScraper, RedditScraper, FileScraper, save_data)
from visualizer import SentimentVisualizer


# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT,
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """Main sentiment analysis orchestrator"""
    
    def __init__(self):
        """Initialize sentiment analyzer"""
        self.text_processor = TextProcessor(
            remove_urls=config.REMOVE_URLS,
            remove_mentions=config.REMOVE_MENTIONS,
            remove_hashtags=config.REMOVE_HASHTAGS,
            lowercase=config.LOWERCASE
        )
        self.visualizer = SentimentVisualizer(config.VISUALIZATIONS_DIR)
        self.data = []
        self.results = []
    
    def collect_data(self, source: str, **kwargs) -> List[Dict]:
        """
        Collect data from specified source
        
        Args:
            source: Data source ('twitter', 'reddit', 'file')
            **kwargs: Additional arguments for the scraper
            
        Returns:
            List of collected data
        """
        logger.info(f"Collecting data from {source}...")
        
        if source == 'twitter':
            scraper = TwitterScraper(
                api_key=config.TWITTER_API_KEY,
                api_secret=config.TWITTER_API_SECRET,
                access_token=config.TWITTER_ACCESS_TOKEN,
                access_secret=config.TWITTER_ACCESS_SECRET,
                bearer_token=config.TWITTER_BEARER_TOKEN
            )
            keyword = kwargs.get('keyword', '')
            count = kwargs.get('count', config.DEFAULT_TWEET_COUNT)
            self.data = scraper.search_tweets(keyword, count)
            
        elif source == 'reddit':
            scraper = RedditScraper(
                client_id=config.REDDIT_CLIENT_ID,
                client_secret=config.REDDIT_CLIENT_SECRET,
                user_agent=config.REDDIT_USER_AGENT
            )
            subreddit = kwargs.get('subreddit', '')
            limit = kwargs.get('limit', config.DEFAULT_REDDIT_LIMIT)
            time_filter = kwargs.get('time_filter', 'week')
            
            if kwargs.get('comments', False):
                self.data = scraper.scrape_comments(subreddit, limit)
            else:
                self.data = scraper.scrape_subreddit(subreddit, limit, time_filter)
            
        elif source == 'file':
            scraper = FileScraper()
            filepath = kwargs.get('input', '')
            text_column = kwargs.get('text_column', 'text')
            
            if filepath.endswith('.csv'):
                self.data = scraper.load_csv(filepath, text_column)
            elif filepath.endswith('.json'):
                self.data = scraper.load_json(filepath)
            else:
                logger.error(f"Unsupported file format: {filepath}")
                return []
        else:
            logger.error(f"Unknown data source: {source}")
            return []
        
        logger.info(f"Collected {len(self.data)} items")
        return self.data
    
    def analyze_data(self) -> pd.DataFrame:
        """
        Perform sentiment analysis on collected data
        
        Returns:
            DataFrame with sentiment analysis results
        """
        if not self.data:
            logger.error("No data to analyze")
            return pd.DataFrame()
        
        logger.info("Performing sentiment analysis...")
        
        results = []
        for item in self.data:
            # Get text content
            text = item.get('text', item.get('title', ''))
            
            if not text:
                continue
            
            # Clean text
            cleaned_text = self.text_processor.clean_text(text)
            
            # Analyze sentiment
            sentiment = analyze_sentiment(cleaned_text)
            
            # Combine original data with sentiment results
            result = {
                **item,
                'cleaned_text': cleaned_text,
                'polarity': sentiment['polarity'],
                'subjectivity': sentiment['subjectivity'],
                'classification': sentiment['classification']
            }
            results.append(result)
        
        self.results = results
        df = pd.DataFrame(results)
        
        logger.info(f"Analyzed {len(results)} items")
        return df
    
    def generate_statistics(self, df: pd.DataFrame) -> Dict:
        """
        Generate summary statistics
        
        Args:
            df: DataFrame with sentiment results
            
        Returns:
            Dictionary of statistics
        """
        if df.empty:
            return {}
        
        stats = {
            'total_items': len(df),
            'positive_count': len(df[df['classification'] == 'positive']),
            'negative_count': len(df[df['classification'] == 'negative']),
            'neutral_count': len(df[df['classification'] == 'neutral']),
            'mean_polarity': df['polarity'].mean(),
            'median_polarity': df['polarity'].median(),
            'std_polarity': df['polarity'].std(),
            'mean_subjectivity': df['subjectivity'].mean(),
            'median_subjectivity': df['subjectivity'].median(),
        }
        
        # Calculate percentages
        stats['positive_percent'] = (stats['positive_count'] / stats['total_items']) * 100
        stats['negative_percent'] = (stats['negative_count'] / stats['total_items']) * 100
        stats['neutral_percent'] = (stats['neutral_count'] / stats['total_items']) * 100
        
        return stats
    
    def print_statistics(self, stats: Dict):
        """Print statistics to console"""
        print("\n" + "="*60)
        print("SENTIMENT ANALYSIS RESULTS")
        print("="*60)
        print(f"\nTotal items analyzed: {stats['total_items']}")
        print(f"\nSentiment Distribution:")
        print(f"  Positive: {stats['positive_count']} ({stats['positive_percent']:.1f}%)")
        print(f"  Negative: {stats['negative_count']} ({stats['negative_percent']:.1f}%)")
        print(f"  Neutral:  {stats['neutral_count']} ({stats['neutral_percent']:.1f}%)")
        print(f"\nPolarity Statistics:")
        print(f"  Mean:   {stats['mean_polarity']:.4f}")
        print(f"  Median: {stats['median_polarity']:.4f}")
        print(f"  Std:    {stats['std_polarity']:.4f}")
        print(f"\nSubjectivity Statistics:")
        print(f"  Mean:   {stats['mean_subjectivity']:.4f}")
        print(f"  Median: {stats['median_subjectivity']:.4f}")
        print("="*60 + "\n")
    
    def save_results(self, df: pd.DataFrame, output_format: str = 'csv'):
        """
        Save analysis results to file
        
        Args:
            df: DataFrame with results
            output_format: Output format ('csv' or 'json')
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"sentiment_results_{timestamp}.{output_format}"
        output_path = os.path.join(config.DATA_DIR, filename)
        
        if output_format == 'csv':
            df.to_csv(output_path, index=False)
        elif output_format == 'json':
            df.to_json(output_path, orient='records', indent=2)
        
        logger.info(f"Results saved to {output_path}")
        print(f"Results saved to: {output_path}")
    
    def create_visualizations(self, df: pd.DataFrame):
        """
        Create all visualizations
        
        Args:
            df: DataFrame with sentiment results
        """
        logger.info("Creating visualizations...")
        
        # Sentiment distribution pie chart
        self.visualizer.plot_sentiment_distribution(df)
        
        # Polarity histogram
        self.visualizer.plot_polarity_histogram(df)
        
        # Subjectivity histogram
        self.visualizer.plot_subjectivity_histogram(df)
        
        # Sentiment boxplot
        self.visualizer.plot_sentiment_boxplot(df)
        
        # Word clouds for positive/negative sentiments
        text_column = 'cleaned_text' if 'cleaned_text' in df.columns else 'text'
        self.visualizer.create_sentiment_wordclouds(df, text_column)
        
        # Time series if timestamps available
        if 'created_at' in df.columns:
            self.visualizer.plot_sentiment_over_time(df)
        
        logger.info(f"Visualizations saved to {config.VISUALIZATIONS_DIR}")
        print(f"Visualizations saved to: {config.VISUALIZATIONS_DIR}")
    
    def run(self, source: str, output_format: str = 'csv', 
            visualize: bool = True, **kwargs):
        """
        Run complete sentiment analysis pipeline
        
        Args:
            source: Data source
            output_format: Output format for results
            visualize: Whether to create visualizations
            **kwargs: Additional arguments for data collection
        """
        try:
            # Collect data
            self.collect_data(source, **kwargs)
            
            if not self.data:
                logger.error("No data collected. Exiting.")
                return
            
            # Analyze data
            df = self.analyze_data()
            
            if df.empty:
                logger.error("No data to analyze. Exiting.")
                return
            
            # Generate and print statistics
            stats = self.generate_statistics(df)
            self.print_statistics(stats)
            
            # Save results
            self.save_results(df, output_format)
            
            # Create visualizations
            if visualize:
                self.create_visualizations(df)
            
            logger.info("Sentiment analysis completed successfully!")
            
        except Exception as e:
            logger.error(f"Error during analysis: {e}", exc_info=True)
            sys.exit(1)


def main():
    """Main entry point with CLI argument parsing"""
    parser = argparse.ArgumentParser(
        description='Social Media Sentiment Analysis Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze Twitter data
  python sentiment_analyzer.py --source twitter --keyword "python programming" --count 100

  # Analyze Reddit data
  python sentiment_analyzer.py --source reddit --subreddit technology --limit 200

  # Analyze from CSV file
  python sentiment_analyzer.py --source file --input sample_data.csv
        """
    )
    
    # Required arguments
    parser.add_argument(
        '--source',
        required=True,
        choices=['twitter', 'reddit', 'file'],
        help='Data source to use'
    )
    
    # Twitter arguments
    parser.add_argument(
        '--keyword',
        help='Keyword or hashtag to search (Twitter)'
    )
    parser.add_argument(
        '--count',
        type=int,
        default=100,
        help='Number of tweets to collect (default: 100)'
    )
    
    # Reddit arguments
    parser.add_argument(
        '--subreddit',
        help='Subreddit name (Reddit)'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=100,
        help='Number of posts/comments to collect (default: 100)'
    )
    parser.add_argument(
        '--time-filter',
        choices=['hour', 'day', 'week', 'month', 'year', 'all'],
        default='week',
        help='Time filter for Reddit posts (default: week)'
    )
    parser.add_argument(
        '--comments',
        action='store_true',
        help='Scrape comments instead of posts (Reddit)'
    )
    
    # File arguments
    parser.add_argument(
        '--input',
        help='Input file path (CSV or JSON)'
    )
    parser.add_argument(
        '--text-column',
        default='text',
        help='Column name containing text data (default: text)'
    )
    
    # Output arguments
    parser.add_argument(
        '--output-format',
        choices=['csv', 'json'],
        default='csv',
        help='Output format for results (default: csv)'
    )
    parser.add_argument(
        '--no-visualize',
        action='store_true',
        help='Skip creating visualizations'
    )
    
    args = parser.parse_args()
    
    # Validate arguments based on source
    if args.source == 'twitter' and not args.keyword:
        parser.error("--keyword is required for Twitter source")
    if args.source == 'reddit' and not args.subreddit:
        parser.error("--subreddit is required for Reddit source")
    if args.source == 'file' and not args.input:
        parser.error("--input is required for file source")
    
    # Create analyzer and run
    analyzer = SentimentAnalyzer()
    
    kwargs = {
        'keyword': args.keyword,
        'count': args.count,
        'subreddit': args.subreddit,
        'limit': args.limit,
        'time_filter': args.time_filter,
        'comments': args.comments,
        'input': args.input,
        'text_column': args.text_column,
    }
    
    analyzer.run(
        source=args.source,
        output_format=args.output_format,
        visualize=not args.no_visualize,
        **kwargs
    )


if __name__ == '__main__':
    main()
