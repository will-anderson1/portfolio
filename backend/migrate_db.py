from sqlalchemy import text
from database import engine, SessionLocal
import os
from dotenv import load_dotenv

# Load .env.local from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env.local'))

def migrate_database():
    """Migrate the existing database to add new fields"""
    db = SessionLocal()
    
    try:
        # Add new columns to articles table
        migrations = [
            "ALTER TABLE articles ADD COLUMN IF NOT EXISTS significance_score FLOAT DEFAULT 0.0",
            "ALTER TABLE articles ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE",
            "ALTER TABLE articles ADD COLUMN IF NOT EXISTS event_id VARCHAR UNIQUE",
            "ALTER TABLE articles ADD COLUMN IF NOT EXISTS last_ranked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "ALTER TABLE articles ADD COLUMN IF NOT EXISTS age_penalty FLOAT DEFAULT 0.0",
            
            # Create new tables
            """
            CREATE TABLE IF NOT EXISTS raw_feeds (
                id SERIAL PRIMARY KEY,
                article_id INTEGER REFERENCES articles(id),
                source_type VARCHAR NOT NULL,
                source_name VARCHAR NOT NULL,
                feed_url VARCHAR,
                raw_data JSON,
                processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            
            """
            CREATE TABLE IF NOT EXISTS feed_sources (
                id SERIAL PRIMARY KEY,
                name VARCHAR NOT NULL,
                source_type VARCHAR NOT NULL,
                url VARCHAR,
                api_key VARCHAR,
                is_active BOOLEAN DEFAULT TRUE,
                last_fetched TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        ]
        
        for migration in migrations:
            try:
                db.execute(text(migration))
                print(f"Executed migration: {migration[:50]}...")
            except Exception as e:
                print(f"Migration failed (might already exist): {e}")
        
        db.commit()
        print("Database migration completed successfully!")
        
        # Update existing articles with default values
        db.execute(text("UPDATE articles SET is_active = TRUE WHERE is_active IS NULL"))
        db.execute(text("UPDATE articles SET significance_score = 50.0 WHERE significance_score IS NULL"))
        
        # Generate event IDs for existing articles
        articles = db.execute(text("SELECT id, title, description FROM articles WHERE event_id IS NULL")).fetchall()
        for article in articles:
            import hashlib
            content = f"{article.title}:{article.description}"
            event_id = hashlib.md5(content.encode()).hexdigest()
            db.execute(text("UPDATE articles SET event_id = :event_id WHERE id = :id"), 
                      {"event_id": event_id, "id": article.id})
        
        db.commit()
        print("Updated existing articles with default values")
        
    except Exception as e:
        print(f"Migration error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate_database() 