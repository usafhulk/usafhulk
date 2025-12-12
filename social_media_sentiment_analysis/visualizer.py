"""
Visualization functions for sentiment analysis results
"""
import logging
from typing import List, Dict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os

logger = logging.getLogger(__name__)

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)


class SentimentVisualizer:
    """Create visualizations for sentiment analysis results"""
    
    def __init__(self, output_dir: str = 'output/visualizations'):
        """
        Initialize visualizer
        
        Args:
            output_dir: Directory to save visualizations
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def plot_sentiment_distribution(self, data: pd.DataFrame, 
                                    save_path: str = None) -> str:
        """
        Create pie chart showing distribution of sentiment classifications
        
        Args:
            data: DataFrame with sentiment data
            save_path: Path to save the plot
            
        Returns:
            Path to saved plot
        """
        try:
            if 'classification' not in data.columns:
                logger.error("DataFrame missing 'classification' column")
                return None
            
            # Count sentiments
            sentiment_counts = data['classification'].value_counts()
            
            # Create pie chart
            plt.figure(figsize=(10, 8))
            colors = ['#90EE90', '#FFB6C1', '#FFD700']  # green, pink, gold
            plt.pie(sentiment_counts.values, 
                   labels=sentiment_counts.index,
                   autopct='%1.1f%%',
                   startangle=90,
                   colors=colors)
            plt.title('Sentiment Distribution', fontsize=16, fontweight='bold')
            plt.axis('equal')
            
            # Save plot
            if not save_path:
                save_path = os.path.join(self.output_dir, 'sentiment_distribution.png')
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Sentiment distribution plot saved to {save_path}")
            return save_path
            
        except Exception as e:
            logger.error(f"Error creating sentiment distribution plot: {e}")
            return None
    
    def plot_polarity_histogram(self, data: pd.DataFrame, 
                                save_path: str = None) -> str:
        """
        Create histogram of polarity scores
        
        Args:
            data: DataFrame with sentiment data
            save_path: Path to save the plot
            
        Returns:
            Path to saved plot
        """
        try:
            if 'polarity' not in data.columns:
                logger.error("DataFrame missing 'polarity' column")
                return None
            
            plt.figure(figsize=(12, 6))
            plt.hist(data['polarity'], bins=50, edgecolor='black', alpha=0.7)
            plt.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Neutral')
            plt.xlabel('Polarity Score', fontsize=12)
            plt.ylabel('Frequency', fontsize=12)
            plt.title('Distribution of Polarity Scores', fontsize=16, fontweight='bold')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # Save plot
            if not save_path:
                save_path = os.path.join(self.output_dir, 'polarity_histogram.png')
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Polarity histogram saved to {save_path}")
            return save_path
            
        except Exception as e:
            logger.error(f"Error creating polarity histogram: {e}")
            return None
    
    def plot_subjectivity_histogram(self, data: pd.DataFrame, 
                                    save_path: str = None) -> str:
        """
        Create histogram of subjectivity scores
        
        Args:
            data: DataFrame with sentiment data
            save_path: Path to save the plot
            
        Returns:
            Path to saved plot
        """
        try:
            if 'subjectivity' not in data.columns:
                logger.error("DataFrame missing 'subjectivity' column")
                return None
            
            plt.figure(figsize=(12, 6))
            plt.hist(data['subjectivity'], bins=50, edgecolor='black', 
                    alpha=0.7, color='skyblue')
            plt.xlabel('Subjectivity Score', fontsize=12)
            plt.ylabel('Frequency', fontsize=12)
            plt.title('Distribution of Subjectivity Scores', fontsize=16, fontweight='bold')
            plt.grid(True, alpha=0.3)
            
            # Save plot
            if not save_path:
                save_path = os.path.join(self.output_dir, 'subjectivity_histogram.png')
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Subjectivity histogram saved to {save_path}")
            return save_path
            
        except Exception as e:
            logger.error(f"Error creating subjectivity histogram: {e}")
            return None
    
    def create_wordcloud(self, texts: List[str], title: str = 'Word Cloud',
                        save_path: str = None) -> str:
        """
        Create word cloud from text data
        
        Args:
            texts: List of text strings
            title: Title for the word cloud
            save_path: Path to save the plot
            
        Returns:
            Path to saved plot
        """
        try:
            # Combine all texts
            combined_text = ' '.join(texts)
            
            if not combined_text.strip():
                logger.warning("No text data for word cloud")
                return None
            
            # Create word cloud
            wordcloud = WordCloud(
                width=1600,
                height=800,
                background_color='white',
                colormap='viridis',
                max_words=100
            ).generate(combined_text)
            
            # Plot
            plt.figure(figsize=(16, 8))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.title(title, fontsize=20, fontweight='bold')
            plt.axis('off')
            
            # Save plot
            if not save_path:
                filename = title.lower().replace(' ', '_') + '.png'
                save_path = os.path.join(self.output_dir, filename)
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Word cloud saved to {save_path}")
            return save_path
            
        except Exception as e:
            logger.error(f"Error creating word cloud: {e}")
            return None
    
    def plot_sentiment_over_time(self, data: pd.DataFrame, 
                                 date_column: str = 'created_at',
                                 save_path: str = None) -> str:
        """
        Create time series plot of sentiment trends
        
        Args:
            data: DataFrame with sentiment data
            date_column: Name of column containing timestamps
            save_path: Path to save the plot
            
        Returns:
            Path to saved plot
        """
        try:
            if date_column not in data.columns:
                logger.warning(f"DataFrame missing '{date_column}' column")
                return None
            
            # Convert to datetime
            data_copy = data.copy()
            data_copy[date_column] = pd.to_datetime(data_copy[date_column])
            data_copy = data_copy.sort_values(date_column)
            
            # Group by date and calculate average polarity
            data_copy['date'] = data_copy[date_column].dt.date
            daily_sentiment = data_copy.groupby('date')['polarity'].mean()
            
            # Plot
            plt.figure(figsize=(14, 6))
            plt.plot(daily_sentiment.index, daily_sentiment.values, 
                    marker='o', linewidth=2, markersize=6)
            plt.axhline(y=0, color='red', linestyle='--', alpha=0.5, label='Neutral')
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Average Polarity', fontsize=12)
            plt.title('Sentiment Trend Over Time', fontsize=16, fontweight='bold')
            plt.xticks(rotation=45)
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # Save plot
            if not save_path:
                save_path = os.path.join(self.output_dir, 'sentiment_over_time.png')
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Sentiment over time plot saved to {save_path}")
            return save_path
            
        except Exception as e:
            logger.error(f"Error creating time series plot: {e}")
            return None
    
    def create_sentiment_wordclouds(self, data: pd.DataFrame, 
                                    text_column: str = 'text') -> Dict[str, str]:
        """
        Create separate word clouds for positive and negative sentiments
        
        Args:
            data: DataFrame with sentiment data
            text_column: Name of column containing text
            
        Returns:
            Dictionary with paths to saved plots
        """
        try:
            results = {}
            
            # Positive sentiments
            positive_texts = data[data['classification'] == 'positive'][text_column].tolist()
            if positive_texts:
                path = self.create_wordcloud(
                    positive_texts,
                    'Positive Sentiment Word Cloud',
                    os.path.join(self.output_dir, 'positive_wordcloud.png')
                )
                results['positive'] = path
            
            # Negative sentiments
            negative_texts = data[data['classification'] == 'negative'][text_column].tolist()
            if negative_texts:
                path = self.create_wordcloud(
                    negative_texts,
                    'Negative Sentiment Word Cloud',
                    os.path.join(self.output_dir, 'negative_wordcloud.png')
                )
                results['negative'] = path
            
            return results
            
        except Exception as e:
            logger.error(f"Error creating sentiment word clouds: {e}")
            return {}
    
    def plot_sentiment_boxplot(self, data: pd.DataFrame, 
                               save_path: str = None) -> str:
        """
        Create boxplot showing polarity distribution by classification
        
        Args:
            data: DataFrame with sentiment data
            save_path: Path to save the plot
            
        Returns:
            Path to saved plot
        """
        try:
            plt.figure(figsize=(10, 6))
            sns.boxplot(x='classification', y='polarity', data=data,
                       palette={'positive': '#90EE90', 'neutral': '#FFD700', 
                               'negative': '#FFB6C1'})
            plt.xlabel('Sentiment Classification', fontsize=12)
            plt.ylabel('Polarity Score', fontsize=12)
            plt.title('Polarity Distribution by Sentiment', fontsize=16, fontweight='bold')
            plt.grid(True, alpha=0.3)
            
            # Save plot
            if not save_path:
                save_path = os.path.join(self.output_dir, 'sentiment_boxplot.png')
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Sentiment boxplot saved to {save_path}")
            return save_path
            
        except Exception as e:
            logger.error(f"Error creating boxplot: {e}")
            return None
