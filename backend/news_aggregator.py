import feedparser
from newsapi import NewsApiClient
import openai
import google.generativeai as genai
import schedule
import time
import threading
import hashlib
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from database import SessionLocal, Article, Source, UpdateHistory, Tag, ArticleTag, RawFeed, FeedSource
import os
from dotenv import load_dotenv
import logging

# Load .env.local from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env.local'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

class NewsAggregator:
    def __init__(self):
        # Configure LLM provider (can be 'openai' or 'gemini')
        self.llm_provider = os.getenv("LLM_PROVIDER", "gemini").lower()
        
        # Initialize API clients based on provider
        if self.llm_provider == "openai":
            self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            logger.info("Using OpenAI GPT-4 for LLM processing")
        elif self.llm_provider == "gemini":
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
            logger.info("Using Google Gemini for LLM processing")
        else:
            raise ValueError(f"Unsupported LLM provider: {self.llm_provider}")
        
        self.newsapi_client = NewsApiClient(api_key=os.getenv("NEWSAPI_KEY"))
        self.max_active_events = 12
        self.rss_feeds = [
            "https://feeds.bbci.co.uk/news/rss.xml",
            "https://rss.cnn.com/rss/edition.rss",
            "https://feeds.reuters.com/Reuters/worldNews",
            "https://www.theguardian.com/world/rss",
            "https://feeds.npr.org/1001/rss.xml",
            "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"
        ]
        
        # New event significance score bonus
        self.new_event_bonus = float(os.getenv("NEW_EVENT_BONUS", 25))
        
        # Scheduler control
        self.scheduler_running = False
        self.scheduler_thread = None
        
    def get_db(self) -> Session:
        return SessionLocal()
    
    def generate_event_id(self, title: str, description: str) -> str:
        """Generate a unique event ID based on content"""
        content = f"{title}:{description}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def fetch_rss_feeds(self) -> List[Dict[str, Any]]:
        """Fetch articles from RSS feeds"""
        articles = []
        
        for feed_url in self.rss_feeds:
            try:
                feed = feedparser.parse(feed_url)
                logger.info(f"Fetched {len(feed.entries)} articles from {feed_url}")
                
                for entry in feed.entries[:10]:  # Limit to 10 articles per feed
                    article = {
                        'title': entry.get('title', ''),
                        'description': entry.get('summary', ''),
                        'url': entry.get('link', ''),
                        'published_at': entry.get('published_parsed'),
                        'source': feed.feed.get('title', 'Unknown'),
                        'source_type': 'rss',
                        'feed_url': feed_url
                    }
                    articles.append(article)
                    
            except Exception as e:
                logger.error(f"Error fetching RSS feed {feed_url}: {e}")
                
        return articles
    
    def fetch_newsapi(self) -> List[Dict[str, Any]]:
        """Fetch articles from NewsAPI"""
        try:
            # Get top headlines from multiple categories
            articles = []
            
            try:
                response = self.newsapi_client.get_top_headlines(
                    language='en',
                    country='us',
                    page_size=30
                )
                
                for article in response.get('articles', []):
                    article_data = {
                        'title': article.get('title', ''),
                        'description': article.get('description', ''),
                        'url': article.get('url', ''),
                        'published_at': article.get('publishedAt'),
                        'source': article.get('source', {}).get('name', 'Unknown'),
                        'source_type': 'newsapi',
                        'category': article.get('category')
                    }
                    articles.append(article_data)
                    
            except Exception as e:
                logger.error(f"Error fetching NewsAPI: {e}")
            logger.info(f"Fetched {str(len(articles))} from NewsAPI")  
            return articles
            
        except Exception as e:
            logger.error(f"Error with NewsAPI: {e}")
            return []
    
    def get_existing_events_for_matching(self, db: Session) -> List[Dict[str, Any]]:
        """Get existing active events for LLM to match against"""
        existing_articles = db.query(Article).filter(Article.is_active == True).all()
        
        existing_events = []
        for article in existing_articles:
            # Get tags for this article
            article_tags = db.query(ArticleTag).filter(ArticleTag.article_id == article.id).all()
            tags = []
            for article_tag in article_tags:
                tag = db.query(Tag).filter(Tag.id == article_tag.tag_id).first()
                if tag:
                    tags.append(tag.name)
            
            existing_events.append({
                'event_id': article.event_id,
                'title': article.title,
                'description': article.description,
                'tags': tags,
                'significance_score': article.significance_score
            })
        
        return existing_events
    
    def call_openai_llm(self, prompt: str) -> str:
        """Call OpenAI API"""
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=2000
        )
        return response.choices[0].message.content
    
    def call_gemini_llm(self, prompt: str) -> str:
        """Call Gemini API"""
        response = self.gemini_model.generate_content(prompt)
        return response.text
    
    def process_with_llm(self, articles: List[Dict[str, Any]], existing_events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Use LLM to compile events and assign significance scores"""
        if not articles:
            return []
        
        # Prepare articles for LLM processing
        articles_text = ""
        for i, article in enumerate(articles[:20]):  # Limit to 20 articles for processing
            articles_text += f"{i+1}. {article['title']}\n"
            articles_text += f"   Description: {article['description']}\n"
            articles_text += f"   Source: {article['source']}\n\n"
        
        # Prepare existing events for matching
        existing_events_text = ""
        if existing_events:
            existing_events_text = "\nExisting Active Events:\n"
            for i, event in enumerate(existing_events):
                existing_events_text += f"{i+1}. Event ID: {event['event_id']}\n"
                existing_events_text += f"   Title: {event['title']}\n"
                existing_events_text += f"   Description: {event['description']}\n"
                existing_events_text += f"   Tags: {', '.join(event['tags'])}\n"
                existing_events_text += f"   Current Score: {event['significance_score']}\n\n"
        
        try:
            # LLM prompt for event compilation and ranking
            prompt = f"""
            Analyze the following news articles and existing events:
            
            {existing_events_text}
            
            New Articles:
            {articles_text}
            
            Your task:
            1. For each new article, determine if it relates to an existing event or represents a new event
            2. If it relates to an existing event, compare the information and determine if there are meaningful new developments
            3. If it's a new event, generate a new event_id (use the title and description to create a unique identifier)
            4. Compile comprehensive summaries for each event
            5. Assign significance scores (0-100) based on:
               - Global impact
               - Number of people affected
               - Economic significance
               - Political importance
               - Scientific/technological breakthrough
               - Urgency/timeliness
            
            CRITICAL: For updates to existing events, ONLY mark as update if there are substantial new developments such as:
            - New facts or numbers (e.g., "Death toll rises to 50", "100 people affected")
            - New statements or accusations (e.g., "Trump blames Biden", "Company admits fault")
            - Breaking developments (e.g., "New evidence emerges", "CEO resigns")
            - Major changes in the story (e.g., "Investigation reveals", "Court rules against")
            
            DO NOT update for:
            - Minor rephrasing with same meaning
            - Small score adjustments without new info
            - Duplicate information from different sources
            - Minor editorial changes
            
            Return a JSON array with objects containing:
            - event_id: existing event_id if updating, or new unique identifier if new event
            - title: compelling headline
            - description: comprehensive summary
            - significance_score: 0-100
            - tags: relevant categories
            - sources: list of source names
            - urls: list of article URLs
            - is_update: true if updating existing event with meaningful new info, false if new event
            - update_description: brief description of what changed (only for meaningful updates, max 100 chars)
            - changes_significant: true/false - whether the changes warrant a new update record
            """
            
            # Call appropriate LLM based on provider
            if self.llm_provider == "openai":
                content = self.call_openai_llm(prompt)
            elif self.llm_provider == "gemini":
                content = self.call_gemini_llm(prompt)
            else:
                raise ValueError(f"Unsupported LLM provider: {self.llm_provider}")
            
            try:
                # Extract JSON from response
                json_start = content.find('[')
                json_end = content.rfind(']') + 1
                if json_start != -1 and json_end != -1:
                    json_str = content[json_start:json_end]
                    events = json.loads(json_str)
                    return events
                else:
                    logger.error("Could not find JSON in LLM response")
                    return []
                    
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing LLM response: {e}")
                logger.error(f"Raw response: {content}")
                return []
                
        except Exception as e:
            logger.error(f"Error with LLM processing: {e}")
            return []
    
    def update_existing_events(self, new_events: List[Dict[str, Any]], db: Session):
        """Update existing events with new information"""
        for event in new_events:
            event_id = event.get('event_id')
            is_update = event.get('is_update', False)
            changes_significant = event.get('changes_significant', True)  # Default to True for backward compatibility
            
            if not event_id or not is_update:
                continue
                
            existing_article = db.query(Article).filter(Article.event_id == event_id).first()
            if existing_article:
                # Check if the LLM determined changes are significant
                if not changes_significant:
                    logger.info(f"LLM determined no significant changes for event: {event_id}")
                    continue
                
                # Get the update description from LLM
                update_description = event.get('update_description', 'Updated with new information')
                
                # Update with new information
                existing_article.title = event.get('title') or existing_article.title
                existing_article.description = event.get('description') or existing_article.description
                existing_article.significance_score = event.get('significance_score', existing_article.significance_score)
                existing_article.updated_at = datetime.utcnow()
                existing_article.last_ranked_at = datetime.utcnow()
                
                # Add update to history with meaningful description
                update = UpdateHistory(
                    article_id=existing_article.id,
                    date_time=datetime.utcnow(),
                    description=update_description
                )
                db.add(update)
                
                # Update tags if new ones provided
                if event.get('tags'):
                    # Remove existing tags
                    db.query(ArticleTag).filter(ArticleTag.article_id == existing_article.id).delete()
                    
                    # Add new tags
                    for tag_name in event.get('tags', []):
                        tag = db.query(Tag).filter(Tag.name == tag_name).first()
                        if not tag:
                            tag = Tag(name=tag_name)
                            db.add(tag)
                            db.flush()
                        
                        article_tag = ArticleTag(
                            article_id=existing_article.id,
                            tag_id=tag.id
                        )
                        db.add(article_tag)
                
                logger.info(f"Updated existing event: {event_id} - {update_description}")
    
    def create_new_events(self, new_events: List[Dict[str, Any]], db: Session):
        """Create new events in the database"""
        for event in new_events:
            event_id = event.get('event_id')
            is_update = event.get('is_update', False)
            
            if not event_id or is_update:
                continue
                
            # Check if event already exists
            existing = db.query(Article).filter(Article.event_id == event_id).first()
            if existing:
                continue
            
            # Apply significance score bonus for new events
            base_score = event.get('significance_score', 0.0)
            significance_score = base_score + self.new_event_bonus
            
            # Create new article
            article = Article(
                title=event.get('title', ''),
                description=event.get('description', ''),
                url=event.get('urls', [''])[0] if event.get('urls') else '',
                event_id=event_id,
                significance_score=significance_score,
                is_active=True,
                last_ranked_at=datetime.utcnow()
            )
            db.add(article)
            db.flush()  # Get the article ID
            
            # Add sources
            for source_name in event.get('sources', []):
                source = Source(
                    article_id=article.id,
                    name=source_name,
                    url='',
                    citation=f"{source_name}, {datetime.now().year}"
                )
                db.add(source)
            
            # Add tags
            for tag_name in event.get('tags', []):
                tag = db.query(Tag).filter(Tag.name == tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.add(tag)
                    db.flush()
                
                article_tag = ArticleTag(
                    article_id=article.id,
                    tag_id=tag.id
                )
                db.add(article_tag)
            
            # Add initial update history with descriptive message
            initial_description = f"Event created: {event.get('title', '')[:50]}..."
            update = UpdateHistory(
                article_id=article.id,
                date_time=datetime.utcnow(),
                description=initial_description
            )
            db.add(update)
            
            logger.info(f"Created new event: {event_id} - {initial_description}")
    
    def calculate_age_penalty(self, db: Session):
        """Calculate age penalty for events older than 1 day"""
        one_day_ago = datetime.utcnow() - timedelta(days=1)
        
        old_articles = db.query(Article).filter(
            Article.created_at < one_day_ago,
            Article.is_active == True
        ).all()
        
        for article in old_articles:
            days_old = (datetime.utcnow() - article.created_at).days
            age_penalty = min(days_old * 10, 50)  # Max 50% penalty
            article.age_penalty = age_penalty
            article.significance_score = max(0, article.significance_score - age_penalty)
            
        db.commit()
    
    def evict_oldest_events(self, db: Session):
        """Evict the least significant events to maintain max_active_events limit"""
        active_articles = db.query(Article).filter(
            Article.is_active == True
        ).order_by(Article.significance_score.asc()).all()
        
        if len(active_articles) > self.max_active_events:
            # Deactivate the least significant events
            to_deactivate = active_articles[:len(active_articles) - self.max_active_events]
            
            for article in to_deactivate:
                article.is_active = False
                logger.info(f"Deactivated event: {article.title} (score: {article.significance_score})")
            
            db.commit()
    
    def deactivate_old_events(self, db: Session, days: int = 2):
        """Deactivate events older than a given number of days (default: 2)"""
        cutoff = datetime.utcnow() - timedelta(days=days)
        old_articles = db.query(Article).filter(
            Article.is_active == True,
            Article.created_at < cutoff
        ).all()
        for article in old_articles:
            article.is_active = False
            logger.info(f"Deactivated event due to age: {article.title} (created at: {article.created_at})")
        db.commit()
    
    def aggregate_news(self):
        """Main function to aggregate news from all sources"""
        logger.info("Starting news aggregation...")
        
        db = self.get_db()
        try:
            # Fetch articles from all sources
            rss_articles = self.fetch_rss_feeds()
            newsapi_articles = self.fetch_newsapi()
            all_articles = rss_articles + newsapi_articles
            
            logger.info(f"Fetched {len(all_articles)} total articles")
            
            if not all_articles:
                return
            
            # Get existing events for matching
            existing_events = self.get_existing_events_for_matching(db)
            logger.info(f"Found {len(existing_events)} existing events for matching")
            
            # Process with LLM
            events = self.process_with_llm(all_articles, existing_events)
            logger.info(f"LLM processed {len(events)} events")
            
            if not events:
                return
            
            # Update existing events
            self.update_existing_events(events, db)
            
            # Create new events
            self.create_new_events(events, db)
            
            # Calculate age penalties
            self.calculate_age_penalty(db)
            
            # Deactivate events older than 2 days
            self.deactivate_old_events(db, days=2)
            
            # Evict oldest events if needed
            self.evict_oldest_events(db)
            
            # Clean up duplicate updates
            self.cleanup_duplicate_updates(db)
            
            db.commit()
            logger.info("News aggregation completed successfully")
            
        except Exception as e:
            logger.error(f"Error in news aggregation: {e}")
            db.rollback()
        finally:
            db.close()
    
    def start_scheduler(self):
        """Start the background scheduler"""
        if self.scheduler_running:
            logger.info("Scheduler is already running")
            return self.scheduler_thread
            
        # Schedule aggregation every 15 minutes
        schedule.every(15).minutes.do(self.aggregate_news)
        
        # Run initial aggregation
        self.aggregate_news()
        
        logger.info("News aggregator scheduler started")
        
        # Run the scheduler in a separate thread
        def run_scheduler():
            self.scheduler_running = True
            while self.scheduler_running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            logger.info("News aggregator scheduler stopped")
        
        self.scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        return self.scheduler_thread
    
    def stop_scheduler(self):
        """Stop the background scheduler gracefully"""
        if not self.scheduler_running:
            logger.info("Scheduler is not running")
            return
            
        logger.info("Stopping news aggregator scheduler...")
        self.scheduler_running = False
        
        # Clear all scheduled jobs
        schedule.clear()
        
        # Wait for scheduler thread to finish (with timeout)
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.scheduler_thread.join(timeout=5)
            if self.scheduler_thread.is_alive():
                logger.warning("Scheduler thread did not stop gracefully within timeout")
            else:
                logger.info("Scheduler thread stopped gracefully")
        
        self.scheduler_thread = None
    
    def cleanup_duplicate_updates(self, db: Session):
        """Remove duplicate or meaningless updates from the database"""
        try:
            # Find articles with multiple similar updates
            articles = db.query(Article).all()
            cleaned_count = 0
            
            for article in articles:
                updates = db.query(UpdateHistory).filter(
                    UpdateHistory.article_id == article.id
                ).order_by(UpdateHistory.date_time.asc()).all()
                
                if len(updates) <= 1:
                    continue
                
                # Keep the first update and remove duplicates
                first_update = updates[0]
                duplicate_descriptions = [
                    "Updated with new information from feeds",
                    "Updated with new information",
                    "Event created from news aggregation"
                ]
                
                for update in updates[1:]:
                    if update.description in duplicate_descriptions:
                        db.delete(update)
                        cleaned_count += 1
                
                # If we removed all updates except the first, and the first is also generic,
                # replace it with a better description
                remaining_updates = db.query(UpdateHistory).filter(
                    UpdateHistory.article_id == article.id
                ).count()
                
                if remaining_updates == 1 and first_update.description in duplicate_descriptions:
                    first_update.description = f"Event created: {article.title[:50]}..."
            
            db.commit()
            if cleaned_count > 0:
                logger.info(f"Cleaned up {cleaned_count} duplicate/meaningless updates")
                
        except Exception as e:
            logger.error(f"Error cleaning up updates: {e}")
            db.rollback()

# Global aggregator instance
aggregator = NewsAggregator() 