from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, Article, Source, UpdateHistory, Tag, ArticleTag
from news_aggregator import aggregator
from typing import List
from datetime import datetime
import threading

app = FastAPI()

# Allow requests from your frontend (on localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://portfolio-izbm-n4d26bwzc-will-andersons-projects-9a9eeb33.vercel.app, https://portfolio-izbm.vercel.app"],  # Or use ["*"] for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Start the news aggregator scheduler
@app.on_event("startup")
async def startup_event():
    """Start the news aggregator when the app starts"""
    scheduler_thread = aggregator.start_scheduler()
    print("News aggregator started in background")

@app.on_event("shutdown")
async def shutdown_event():
    """Stop the news aggregator when the app shuts down"""
    print("Stopping news aggregator...")
    aggregator.stop_scheduler()
    print("News aggregator stopped")

@app.get("/api/news")
def get_news(db: Session = Depends(get_db)):
    # Query only active articles, sorted by significance score (highest first)
    articles = db.query(Article).filter(
        Article.is_active == True
    ).order_by(Article.significance_score.desc()).all()
    
    result_articles = []
    for article in articles:
        # Get sources for this article
        sources = db.query(Source).filter(Source.article_id == article.id).all()
        sources_data = [
            {
                "name": source.name,
                "url": source.url,
                "citation": source.citation
            }
            for source in sources
        ]
        
        # Get update history for this article
        update_history = db.query(UpdateHistory).filter(UpdateHistory.article_id == article.id).all()
        update_history_data = [
            {
                "dateTime": update.date_time.isoformat() + "Z",
                "description": update.description
            }
            for update in update_history
        ]
        
        # Get tags for this article
        article_tags = db.query(ArticleTag).filter(ArticleTag.article_id == article.id).all()
        tags = []
        for article_tag in article_tags:
            tag = db.query(Tag).filter(Tag.id == article_tag.tag_id).first()
            if tag:
                tags.append(tag.name)
        
        # Format the article data
        article_data = {
            "title": article.title,
            "imageUrl": article.image_url,
            "sources": sources_data,
            "url": article.url,
            "latestUpdateDateTime": article.latest_update_datetime.isoformat() + "Z",
            "updateHistory": update_history_data,
            "description": article.description,
            "tags": tags,
            "significanceScore": article.significance_score,
            "eventId": article.event_id
        }
        
        result_articles.append(article_data)
    
    return {"articles": result_articles}

@app.post("/api/aggregate")
def trigger_aggregation(db: Session = Depends(get_db)):
    """Manually trigger news aggregation"""
    try:
        # Get stats before aggregation
        active_before = db.query(Article).filter(Article.is_active == True).count()
        total_before = db.query(Article).count()
        
        # Run aggregation
        aggregator.aggregate_news()
        
        # Get stats after aggregation
        active_after = db.query(Article).filter(Article.is_active == True).count()
        total_after = db.query(Article).count()
        
        # Get recent updates
        recent_updates = db.query(UpdateHistory).order_by(UpdateHistory.date_time.desc()).limit(5).all()
        update_log = [
            {
                "dateTime": update.date_time.isoformat() + "Z",
                "description": update.description
            }
            for update in recent_updates
        ]
        
        return {
            "message": "News aggregation completed successfully",
            "stats": {
                "active_events_before": active_before,
                "active_events_after": active_after,
                "total_articles_before": total_before,
                "total_articles_after": total_after,
                "new_events": active_after - active_before,
                "new_articles": total_after - total_before
            },
            "recent_updates": update_log
        }
    except Exception as e:
        return {"error": str(e)}