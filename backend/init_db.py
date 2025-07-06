import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from database import create_tables, SessionLocal, Article, Source, UpdateHistory, Tag, ArticleTag
from datetime import datetime
import os
from dotenv import load_dotenv
from sqlalchemy import text

# Load .env.local from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env.prod'))

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            host=os.getenv("DB_URL", "localhost"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", ""),
            port=os.getenv("DB_PORT", "5432")
        )
        print(conn)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Create database
        db_name = "news_pim0"
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f'CREATE DATABASE {db_name}')
            print(f"Database '{db_name}' created successfully")
        else:
            print(f"Database '{db_name}' already exists")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error creating database: {e}")

def populate_test_data():
    """Populate the database with test articles"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Article).count() > 0:
            print("Database already contains articles. Skipping population.")
            return
        
        # Test data
        articles_data = [
            {
                "title": "Breaking: New AI Technology Revolutionizes Healthcare",
                "image_url": "https://source.unsplash.com/random/400x250?healthcare",
                "url": "https://example.com/ai-healthcare-breakthrough",
                "description": "Researchers develop breakthrough AI system that can predict health issues with 95% accuracy, potentially saving millions of lives through early detection.",
                "latest_update_datetime": datetime(2024, 1, 15, 10, 30, 0),
                "sources": [
                    {"name": "TechCrunch", "url": "https://techcrunch.com/ai-healthcare", "citation": "TechCrunch, 2024"},
                    {"name": "MIT Technology Review", "url": "https://technologyreview.com/ai-health", "citation": "MIT Tech Review, 2024"}
                ],
                "update_history": [
                    {"date_time": datetime(2024, 1, 15, 10, 30, 0), "description": "Initial publication"},
                    {"date_time": datetime(2024, 1, 15, 14, 20, 0), "description": "Updated with additional research findings"}
                ],
                "tags": ["AI", "Healthcare", "Technology", "Medical Research"]
            },
            {
                "title": "Global Climate Summit Reaches Historic Agreement",
                "image_url": "https://source.unsplash.com/random/400x250?climate",
                "url": "https://example.com/climate-summit-agreement",
                "description": "World leaders commit to ambitious carbon reduction targets at landmark climate conference, marking a turning point in global environmental policy.",
                "latest_update_datetime": datetime(2024, 1, 14, 16, 45, 0),
                "sources": [
                    {"name": "BBC News", "url": "https://bbc.com/climate-summit", "citation": "BBC News, 2024"},
                    {"name": "The Guardian", "url": "https://theguardian.com/climate-agreement", "citation": "The Guardian, 2024"}
                ],
                "update_history": [
                    {"date_time": datetime(2024, 1, 14, 16, 45, 0), "description": "Agreement announced"}
                ],
                "tags": ["Climate Change", "Environment", "Politics", "Global Summit"]
            },
            {
                "title": "SpaceX Successfully Launches Mars Mission",
                "image_url": "https://kubrick.htvapps.com/htv-prod-media.s3.amazonaws.com/images/gettyimages-2159785451-66870f3f7239e.jpg?crop=1.00xw:0.853xh;0,0.111xh&resize=640:*",
                "url": "https://example.com/spacex-mars-mission",
                "description": "Elon Musk's company achieves another milestone in space exploration with latest rocket launch, bringing humanity one step closer to Mars colonization.",
                "latest_update_datetime": datetime(2024, 1, 13, 8, 15, 0),
                "sources": [
                    {"name": "Space.com", "url": "https://space.com/spacex-mars-launch", "citation": "Space.com, 2024"},
                    {"name": "NASA", "url": "https://nasa.gov/spacex-mars", "citation": "NASA, 2024"}
                ],
                "update_history": [
                    {"date_time": datetime(2024, 1, 13, 8, 15, 0), "description": "Launch successful"},
                    {"date_time": datetime(2024, 1, 13, 12, 30, 0), "description": "Spacecraft enters Mars transfer orbit"}
                ],
                "tags": ["SpaceX", "Mars", "Space Exploration", "Elon Musk"]
            },
            {
                "title": "Revolutionary Electric Vehicle Battery Breakthrough",
                "image_url": "https://source.unsplash.com/random/400x250?electric-car",
                "url": "https://example.com/ev-battery-breakthrough",
                "description": "New battery technology promises 1000-mile range and 10-minute charging times, potentially revolutionizing the electric vehicle industry.",
                "latest_update_datetime": datetime(2024, 1, 12, 11, 20, 0),
                "sources": [
                    {"name": "Reuters", "url": "https://reuters.com/ev-battery-breakthrough", "citation": "Reuters, 2024"},
                    {"name": "Bloomberg", "url": "https://bloomberg.com/ev-technology", "citation": "Bloomberg, 2024"}
                ],
                "update_history": [
                    {"date_time": datetime(2024, 1, 12, 11, 20, 0), "description": "Technology announced"}
                ],
                "tags": ["Electric Vehicles", "Battery Technology", "Automotive", "Innovation"]
            },
            {
                "title": "Major Cybersecurity Threat Discovered",
                "image_url": "https://source.unsplash.com/random/400x250?cybersecurity",
                "url": "https://example.com/cybersecurity-threat",
                "description": "Security researchers identify critical vulnerability affecting millions of devices worldwide, prompting urgent security updates.",
                "latest_update_datetime": datetime(2024, 1, 11, 9, 45, 0),
                "sources": [
                    {"name": "Wired", "url": "https://wired.com/cybersecurity-threat", "citation": "Wired, 2024"},
                    {"name": "Ars Technica", "url": "https://arstechnica.com/security-threat", "citation": "Ars Technica, 2024"}
                ],
                "update_history": [
                    {"date_time": datetime(2024, 1, 11, 9, 45, 0), "description": "Vulnerability discovered"},
                    {"date_time": datetime(2024, 1, 11, 15, 10, 0), "description": "Patch released by affected vendors"}
                ],
                "tags": ["Cybersecurity", "Vulnerability", "Security", "Technology"]
            },
            {
                "title": "Breakthrough in Quantum Computing",
                "image_url": "https://source.unsplash.com/random/400x250?quantum",
                "url": "https://example.com/quantum-computing-breakthrough",
                "description": "Scientists achieve quantum supremacy with new 1000-qubit processor, opening new possibilities for computational research.",
                "latest_update_datetime": datetime(2024, 1, 10, 13, 25, 0),
                "sources": [
                    {"name": "Nature", "url": "https://nature.com/quantum-computing", "citation": "Nature, 2024"},
                    {"name": "Science", "url": "https://science.org/quantum-breakthrough", "citation": "Science, 2024"}
                ],
                "update_history": [
                    {"date_time": datetime(2024, 1, 10, 13, 25, 0), "description": "Research published"}
                ],
                "tags": ["Quantum Computing", "Research", "Technology", "Science"]
            }
        ]
        
        # Create tags first
        tag_map = {}
        for article_data in articles_data:
            for tag_name in article_data["tags"]:
                if tag_name not in tag_map:
                    tag = db.query(Tag).filter(Tag.name == tag_name).first()
                    if not tag:
                        tag = Tag(name=tag_name)
                        db.add(tag)
                        db.flush()  # Get the ID
                    tag_map[tag_name] = tag
        
        # Create articles
        for article_data in articles_data:
            # Create article
            article = Article(
                title=article_data["title"],
                image_url=article_data["image_url"],
                url=article_data["url"],
                description=article_data["description"],
                latest_update_datetime=article_data["latest_update_datetime"]
            )
            db.add(article)
            db.flush()  # Get the article ID
            
            # Create sources
            for source_data in article_data["sources"]:
                source = Source(
                    article_id=article.id,
                    name=source_data["name"],
                    url=source_data["url"],
                    citation=source_data["citation"]
                )
                db.add(source)
            
            # Create update history
            for history_data in article_data["update_history"]:
                update = UpdateHistory(
                    article_id=article.id,
                    date_time=history_data["date_time"],
                    description=history_data["description"]
                )
                db.add(update)
            
            # Create article tags
            for tag_name in article_data["tags"]:
                article_tag = ArticleTag(
                    article_id=article.id,
                    tag_id=tag_map[tag_name].id
                )
                db.add(article_tag)
        
        db.commit()
        print("Test data populated successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error populating data: {e}")
    finally:
        db.close()

def truncate_all_tables():
    """Delete all data from all tables and reset sequences (for PostgreSQL)"""
    db = SessionLocal()
    try:
        # Delete from child tables first
        db.execute(text('DELETE FROM raw_feeds'))
        db.execute(text('DELETE FROM article_tags'))
        db.execute(text('DELETE FROM update_history'))
        db.execute(text('DELETE FROM sources'))
        db.execute(text('DELETE FROM articles'))
        db.execute(text('DELETE FROM tags'))
        db.execute(text('DELETE FROM feed_sources'))
        db.commit()
        print("All tables truncated.")
        # Reset sequences (PostgreSQL only)
        for table in [
            'raw_feeds', 'article_tags', 'update_history', 'sources', 'articles', 'tags', 'feed_sources']:
            db.execute(text(f"ALTER SEQUENCE {table}_id_seq RESTART WITH 1;"))
        db.commit()
        print("Primary key sequences reset.")
    except Exception as e:
        db.rollback()
        print(f"Error truncating tables: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    if '--truncate' in sys.argv:
        print("Truncating all tables...")
        truncate_all_tables()
        print("Done.")
        sys.exit(0)
    print("Creating database...")
    create_database()
    
    print("Creating tables...")
    create_tables()
    
    print("Populating test data...")
    # populate_test_data()
    
    print("Database setup complete!") 