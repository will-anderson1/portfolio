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
    allow_origins=["http://localhost:3000"],  # Or use ["*"] for development
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

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    """Get statistics about the news aggregation system"""
    total_articles = db.query(Article).count()
    active_articles = db.query(Article).filter(Article.is_active == True).count()
    total_tags = db.query(Tag).count()
    total_sources = db.query(Source).count()
    
    # Get significance score distribution
    high_significance = db.query(Article).filter(
        Article.is_active == True,
        Article.significance_score >= 80
    ).count()
    
    medium_significance = db.query(Article).filter(
        Article.is_active == True,
        Article.significance_score >= 50,
        Article.significance_score < 80
    ).count()
    
    low_significance = db.query(Article).filter(
        Article.is_active == True,
        Article.significance_score < 50
    ).count()
    
    return {
        "total_articles": total_articles,
        "active_articles": active_articles,
        "total_tags": total_tags,
        "total_sources": total_sources,
        "significance_distribution": {
            "high": high_significance,
            "medium": medium_significance,
            "low": low_significance
        }
    }

@app.get("/api/event/{event_id}/updates")
def get_event_updates(event_id: str, db: Session = Depends(get_db)):
    """Get detailed update history for a specific event"""
    article = db.query(Article).filter(Article.event_id == event_id).first()
    if not article:
        return {"error": "Event not found"}
    
    updates = db.query(UpdateHistory).filter(
        UpdateHistory.article_id == article.id
    ).order_by(UpdateHistory.date_time.desc()).all()
    
    update_history = [
        {
            "dateTime": update.date_time.isoformat() + "Z",
            "description": update.description
        }
        for update in updates
    ]
    
    return {
        "event_id": event_id,
        "title": article.title,
        "updates": update_history
    }

@app.post("/api/cleanup-updates")
def cleanup_updates(db: Session = Depends(get_db)):
    """Manually trigger cleanup of duplicate and meaningless updates"""
    try:
        # Get count before cleanup
        updates_before = db.query(UpdateHistory).count()
        
        # Run cleanup
        aggregator.cleanup_duplicate_updates(db)
        
        # Get count after cleanup
        updates_after = db.query(UpdateHistory).count()
        
        return {
            "message": "Update cleanup completed successfully",
            "updates_removed": updates_before - updates_after,
            "remaining_updates": updates_after
        }
    except Exception as e:
        return {"error": str(e)}
