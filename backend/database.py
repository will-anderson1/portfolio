from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, JSON, ForeignKey, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

# Load .env.local from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env.local'))

# Database URL - you can set this in your .env.local file
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/portfolio_news")
print(DATABASE_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Database Models
class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    image_url = Column(String)
    url = Column(String)
    description = Column(Text)
    latest_update_datetime = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # New fields for event management
    significance_score = Column(Float, default=0.0)  # LLM-assigned significance (0-100)
    is_active = Column(Boolean, default=True)  # Whether this event is currently active
    event_id = Column(String, unique=True, index=True)  # Unique identifier for the event
    last_ranked_at = Column(DateTime, default=datetime.utcnow)  # When significance was last calculated
    age_penalty = Column(Float, default=0.0)  # Penalty for being old (reduces significance)
    
    # Relationships
    sources = relationship("Source", back_populates="article", cascade="all, delete-orphan")
    update_history = relationship("UpdateHistory", back_populates="article", cascade="all, delete-orphan")
    tags = relationship("ArticleTag", back_populates="article", cascade="all, delete-orphan")
    raw_feeds = relationship("RawFeed", back_populates="article", cascade="all, delete-orphan")

class Source(Base):
    __tablename__ = "sources"
    
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"))
    name = Column(String, nullable=False)
    url = Column(String)
    citation = Column(String)
    
    # Relationship
    article = relationship("Article", back_populates="sources")

class UpdateHistory(Base):
    __tablename__ = "update_history"
    
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"))
    date_time = Column(DateTime, nullable=False)
    description = Column(Text)
    
    # Relationship
    article = relationship("Article", back_populates="update_history")

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

class ArticleTag(Base):
    __tablename__ = "article_tags"
    
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"))
    tag_id = Column(Integer, ForeignKey("tags.id"))
    
    # Relationships
    article = relationship("Article", back_populates="tags")
    tag = relationship("Tag")

class RawFeed(Base):
    """Store raw RSS and NewsAPI data for processing"""
    __tablename__ = "raw_feeds"
    
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"))
    source_type = Column(String, nullable=False)  # 'rss' or 'newsapi'
    source_name = Column(String, nullable=False)
    feed_url = Column(String)
    raw_data = Column(JSON)  # Store the complete raw feed data
    processed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    article = relationship("Article", back_populates="raw_feeds")

class FeedSource(Base):
    """Configuration for RSS feeds and NewsAPI sources"""
    __tablename__ = "feed_sources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    source_type = Column(String, nullable=False)  # 'rss' or 'newsapi'
    url = Column(String)
    api_key = Column(String)  # For NewsAPI
    is_active = Column(Boolean, default=True)
    last_fetched = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all tables
def create_tables():
    Base.metadata.create_all(bind=engine) 