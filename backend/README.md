# News Aggregation System

A comprehensive news aggregation system that automatically fetches news from RSS feeds and NewsAPI, processes them with LLM, and maintains a curated list of the most significant events.

## Features

- **Automatic News Aggregation**: Fetches news every 15 minutes from multiple RSS feeds and NewsAPI
- **LLM Processing**: Uses OpenAI GPT-4 to compile events and assign significance scores
- **Intelligent Event Management**: Maintains only the 12 most significant active events
- **Age-based Ranking**: Events older than 1 day get reduced significance scores
- **Event Updates**: Automatically updates existing events with new information
- **PostgreSQL Database**: Robust data storage with proper relationships

## Setup

### 1. Install Dependencies

```bash
# Activate virtual environment
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 2. Set up PostgreSQL

```bash
# Start PostgreSQL service
brew services start postgresql@14

# Create postgres user (if not exists)
createuser -s postgres
```

### 3. Configure Environment Variables

Copy `env.example` to `.env.local` and fill in your API keys:

```bash
cp env.example .env.local
```

Required API keys:
- `OPENAI_API_KEY`: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
- `NEWSAPI_KEY`: Get from [NewsAPI](https://newsapi.org/register)

### 4. Initialize Database

```bash
# Create database and tables
python init_db.py

# Run migration (if updating existing database)
python migrate_db.py
```

### 5. Start the Application

```bash
# Start the FastAPI server
uvicorn main:app --reload --port 8000
```

The news aggregator will automatically start in the background and begin fetching news every 15 minutes.

## API Endpoints

### GET `/api/news`
Returns the current active events, sorted by significance score.

### POST `/api/aggregate`
Manually trigger news aggregation.

### GET `/api/stats`
Get statistics about the news aggregation system.

## Database Schema

### Articles Table
- `id`: Primary key
- `title`: Article title
- `description`: Article description
- `url`: Article URL
- `image_url`: Featured image URL
- `significance_score`: LLM-assigned significance (0-100)
- `is_active`: Whether event is currently active
- `event_id`: Unique event identifier
- `age_penalty`: Penalty for being old
- `created_at`, `updated_at`: Timestamps

### Related Tables
- `sources`: Article sources
- `tags`: Article tags
- `update_history`: Event update history
- `raw_feeds`: Raw RSS/NewsAPI data
- `feed_sources`: RSS feed configurations

## RSS Feeds

The system currently monitors these RSS feeds:
- BBC News
- CNN
- Reuters
- The Guardian
- NPR
- New York Times

## NewsAPI Categories

Fetches from these categories:
- General
- Technology
- Business
- Science

## Event Management

### Significance Scoring
The LLM assigns significance scores based on:
- Global impact
- Number of people affected
- Economic significance
- Political importance
- Scientific/technological breakthrough
- Urgency/timeliness

### Age Penalty
Events older than 1 day receive a penalty that reduces their significance score:
- 1 day old: -10 points
- 2 days old: -20 points
- Maximum penalty: -50 points

### Event Eviction
When more than 12 events are active, the least significant events are automatically deactivated.

## Customization

### Adding RSS Feeds
Edit the `rss_feeds` list in `news_aggregator.py`:

```python
self.rss_feeds = [
    "https://your-feed-url.com/rss",
    # ... more feeds
]
```

### Modifying Aggregation Interval
Change the schedule in `news_aggregator.py`:

```python
schedule.every(15).minutes.do(self.aggregate_news)  # Change 15 to desired minutes
```

### Adjusting Max Events
Modify `max_active_events` in the `NewsAggregator` class.

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running: `brew services start postgresql@14`
- Check database exists: `psql -U postgres -l`
- Verify connection string in `.env.local`

### API Key Issues
- Ensure API keys are correctly set in `.env.local`
- Check API key quotas and limits
- Verify internet connectivity

### LLM Processing Issues
- Check OpenAI API key and quota
- Monitor API response parsing
- Review LLM prompt effectiveness

## Logging

The system logs all activities to help with debugging:
- RSS feed fetching
- NewsAPI requests
- LLM processing
- Database operations
- Event management

Check the console output for detailed logs. 