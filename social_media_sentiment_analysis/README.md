# Social Media Sentiment Analysis Tool

A comprehensive Python application for scraping and analyzing social media data to determine sentiment using TextBlob. This tool supports multiple data sources including Twitter/X, Reddit, and file-based inputs, with powerful visualization capabilities.

## Features

- 📊 **Multi-Source Data Collection**: Scrape data from Twitter/X, Reddit, or load from CSV/JSON files
- 🎯 **Sentiment Analysis**: Analyze polarity (positive/negative) and subjectivity using TextBlob
- 📈 **Rich Visualizations**: Generate multiple charts including pie charts, histograms, word clouds, and time-series plots
- 🧹 **Text Processing**: Clean and preprocess text data (URLs, mentions, hashtags, special characters)
- 💾 **Flexible Output**: Save results in CSV or JSON format
- 🔧 **CLI Interface**: Easy-to-use command-line interface with comprehensive options
- 📝 **Detailed Logging**: Track progress and debug issues

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or download this repository**

2. **Navigate to the project directory**
   ```bash
   cd social_media_sentiment_analysis
   ```

3. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data** (TextBlob dependency)
   ```bash
   python -m textblob.download_corpora
   ```

5. **Set up environment variables** (for API access)
   ```bash
   cp .env.example .env
   # Edit .env with your actual API credentials
   ```

## API Setup Guides

### Twitter/X API Setup

1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Create a developer account if you don't have one
3. Create a new app/project
4. Navigate to "Keys and tokens" section
5. Generate and copy:
   - API Key and Secret
   - Access Token and Secret
   - Bearer Token (for API v2)
6. Add these credentials to your `.env` file

**Note**: Twitter API access levels:
- **Essential** (Free): Limited to 500k tweets/month
- **Elevated**: More endpoints and higher limits
- **Academic**: For research purposes

### Reddit API Setup

1. Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Scroll down and click "create another app" or "create app"
3. Fill in the details:
   - Name: Your app name
   - App type: Select "script"
   - Description: Brief description
   - Redirect URI: http://localhost:8080
4. Copy the client ID (under the app name) and client secret
5. Add these credentials to your `.env` file
6. Set an appropriate user agent (e.g., "SentimentAnalyzer/1.0 by YourRedditUsername")

## Usage

### Basic Command Structure

```bash
python sentiment_analyzer.py --source <source> [options]
```

### Examples

#### 1. Analyze Twitter Data

Search for tweets containing a specific keyword:

```bash
python sentiment_analyzer.py --source twitter --keyword "python programming" --count 100
```

Search for tweets with a hashtag:

```bash
python sentiment_analyzer.py --source twitter --keyword "#datascience" --count 200
```

#### 2. Analyze Reddit Data

Analyze posts from a subreddit:

```bash
python sentiment_analyzer.py --source reddit --subreddit technology --limit 200 --time-filter week
```

Analyze comments instead of posts:

```bash
python sentiment_analyzer.py --source reddit --subreddit python --limit 150 --comments
```

#### 3. Analyze Data from File

Analyze data from a CSV file:

```bash
python sentiment_analyzer.py --source file --input sample_data.csv
```

Analyze data from a JSON file with custom text column:

```bash
python sentiment_analyzer.py --source file --input data.json --text-column content
```

### Command-Line Arguments

#### General Arguments

- `--source`: **(Required)** Data source - `twitter`, `reddit`, or `file`
- `--output-format`: Output format for results - `csv` or `json` (default: csv)
- `--no-visualize`: Skip creating visualizations

#### Twitter Arguments

- `--keyword`: **(Required for Twitter)** Keyword or hashtag to search
- `--count`: Number of tweets to collect (default: 100)

#### Reddit Arguments

- `--subreddit`: **(Required for Reddit)** Subreddit name (without 'r/')
- `--limit`: Number of posts/comments to collect (default: 100)
- `--time-filter`: Time filter - `hour`, `day`, `week`, `month`, `year`, `all` (default: week)
- `--comments`: Scrape comments instead of posts

#### File Arguments

- `--input`: **(Required for file)** Input file path (CSV or JSON)
- `--text-column`: Column name containing text data (default: text)

## Understanding Sentiment Scores

### Polarity Score

Range: **-1.0 to 1.0**

- **-1.0 to -0.1**: Negative sentiment
- **-0.1 to 0.1**: Neutral sentiment
- **0.1 to 1.0**: Positive sentiment

### Subjectivity Score

Range: **0.0 to 1.0**

- **0.0**: Very objective (factual information)
- **1.0**: Very subjective (personal opinions/emotions)

### Example Interpretations

| Text | Polarity | Subjectivity | Classification |
|------|----------|--------------|----------------|
| "I love this product!" | 0.5 | 0.6 | Positive |
| "This is terrible and awful." | -0.8 | 1.0 | Negative |
| "The meeting is at 3 PM." | 0.0 | 0.0 | Neutral |
| "I think it's okay." | 0.1 | 0.4 | Neutral/Positive |

## Output

### Generated Files

The tool creates an `output` directory with the following structure:

```
output/
├── data/
│   └── sentiment_results_YYYYMMDD_HHMMSS.csv (or .json)
├── visualizations/
│   ├── sentiment_distribution.png
│   ├── polarity_histogram.png
│   ├── subjectivity_histogram.png
│   ├── sentiment_boxplot.png
│   ├── positive_wordcloud.png
│   ├── negative_wordcloud.png
│   └── sentiment_over_time.png (if timestamps available)
└── sentiment_analysis.log
```

### Visualization Examples

1. **Sentiment Distribution Pie Chart**: Shows the percentage breakdown of positive, negative, and neutral sentiments

2. **Polarity Histogram**: Displays the distribution of polarity scores across all analyzed items

3. **Subjectivity Histogram**: Shows how objective or subjective the analyzed content is

4. **Sentiment Boxplot**: Visualizes the polarity distribution for each sentiment classification

5. **Word Clouds**: Separate word clouds for positive and negative sentiments, highlighting frequently used words

6. **Time Series Plot**: Shows sentiment trends over time (when timestamp data is available)

### Console Output

The tool prints a summary to the console:

```
============================================================
SENTIMENT ANALYSIS RESULTS
============================================================

Total items analyzed: 100

Sentiment Distribution:
  Positive: 45 (45.0%)
  Negative: 30 (30.0%)
  Neutral:  25 (25.0%)

Polarity Statistics:
  Mean:   0.1234
  Median: 0.1500
  Std:    0.4567

Subjectivity Statistics:
  Mean:   0.5234
  Median: 0.5500
============================================================
```

## File Structure

```
social_media_sentiment_analysis/
├── sentiment_analyzer.py      # Main script with CLI
├── data_scraper.py            # Data collection module
├── text_processor.py          # Text preprocessing utilities
├── visualizer.py              # Visualization functions
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
├── .env.example               # Example environment variables
├── README.md                  # This file
├── sample_data.csv            # Sample dataset for testing
└── output/                    # Generated output (created automatically)
    ├── data/                  # Analysis results
    ├── visualizations/        # Generated charts
    └── sentiment_analysis.log # Log file
```

## Testing Without API Access

You can test the tool using the provided sample data:

```bash
python sentiment_analyzer.py --source file --input sample_data.csv
```

This will analyze 50 pre-made sample posts covering various sentiments without requiring any API credentials.

## Configuration

Edit `config.py` to customize:

- Sentiment classification thresholds
- Default collection limits
- Output directories
- Text processing options (URL removal, mention handling, etc.)
- Logging settings

## Troubleshooting

### Common Issues

#### 1. Import Errors

**Problem**: `ModuleNotFoundError: No module named 'textblob'`

**Solution**: 
```bash
pip install -r requirements.txt
```

#### 2. TextBlob Corpora Missing

**Problem**: `LookupError: Resource punkt not found`

**Solution**:
```bash
python -m textblob.download_corpora
```

#### 3. Twitter API Errors

**Problem**: `401 Unauthorized` or `403 Forbidden`

**Solutions**:
- Verify API credentials in `.env` file
- Check if your Twitter Developer account is approved
- Ensure you have the correct access level for your use case
- Check if your bearer token is valid for API v2

#### 4. Reddit API Errors

**Problem**: `praw.exceptions.ResponseException: received 401 HTTP response`

**Solutions**:
- Verify Reddit credentials in `.env` file
- Ensure your app type is set to "script"
- Check that your user agent is properly formatted

#### 5. Rate Limiting

**Problem**: `Rate limit exceeded`

**Solutions**:
- Wait for the rate limit to reset (usually 15 minutes)
- Reduce the number of items requested
- For Twitter: Consider upgrading your API access level
- For Reddit: PRAW automatically handles rate limiting

#### 6. Empty Results

**Problem**: No data collected or analyzed

**Solutions**:
- Check your search keywords/parameters
- Verify API credentials are correct
- Check internet connection
- Review log file (`output/sentiment_analysis.log`) for errors
- For file input: verify the file path and text column name

### Getting Help

If you encounter issues:

1. Check the log file: `output/sentiment_analysis.log`
2. Verify your API credentials and permissions
3. Test with sample data first: `python sentiment_analyzer.py --source file --input sample_data.csv`
4. Ensure all dependencies are installed: `pip install -r requirements.txt`

## Best Practices

1. **Start Small**: Begin with small data collections (e.g., 50-100 items) to test functionality
2. **Monitor Rate Limits**: Be mindful of API rate limits to avoid being temporarily blocked
3. **Clean Data**: The tool handles basic cleaning, but manual review of results is recommended
4. **Timestamp Data**: Include timestamps when possible for time-series analysis
5. **Regular Backups**: Save important results as the output directory may be overwritten

## Advanced Usage

### Customizing Sentiment Thresholds

Edit `config.py`:

```python
SENTIMENT_THRESHOLDS = {
    'positive': 0.2,    # More strict: only very positive is classified as positive
    'negative': -0.2,   # More strict: only very negative is classified as negative
}
```

### Batch Processing

Create a script to process multiple queries:

```bash
#!/bin/bash
for keyword in "AI" "machine learning" "data science"; do
    python sentiment_analyzer.py --source twitter --keyword "$keyword" --count 100
done
```

### Custom Text Processing

Modify `text_processor.py` to add custom preprocessing steps:

```python
# Example: Add custom filtering
def custom_filter(text):
    # Your custom logic here
    return filtered_text
```

## Dependencies

- **textblob**: Sentiment analysis
- **tweepy**: Twitter/X API wrapper
- **praw**: Reddit API wrapper
- **pandas**: Data manipulation
- **matplotlib**: Plotting library
- **seaborn**: Statistical visualizations
- **wordcloud**: Word cloud generation
- **nltk**: Natural language processing
- **python-dotenv**: Environment variable management

## Future Enhancements

Potential improvements for future versions:

- [ ] Support for additional social media platforms (Instagram, LinkedIn)
- [ ] Real-time streaming analysis
- [ ] Advanced NLP models (BERT, GPT-based sentiment analysis)
- [ ] Sentiment comparison across multiple keywords/topics
- [ ] Export to database (SQL, MongoDB)
- [ ] Web dashboard for interactive visualization
- [ ] Multi-language support
- [ ] Emotion detection (joy, anger, sadness, etc.)

## License

This project is provided as-is for educational and research purposes.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Acknowledgments

- TextBlob for sentiment analysis capabilities
- Tweepy and PRAW for API wrappers
- The open-source community for the excellent Python libraries

---

**Author**: Christopher Banner  
**Contact**: chrisbanner38@gmail.com  
**LinkedIn**: [linkedin.com/in/christopher-banner-094b59174](https://www.linkedin.com/in/christopher-banner-094b59174)

Happy analyzing! 🚀📊
