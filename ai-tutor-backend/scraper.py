import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from sqlalchemy.exc import IntegrityError


def fetch_atomic_news_sciencedaily():
    """Targeted scientific source for 2026 breakthroughs"""
    url = "https://www.sciencedaily.com/news/matter_energy/nuclear_energy/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        latest_updates = []
        # Extracting the top 5 2026 tech headlines
        for item in soup.find_all('h3', class_='latest-head', limit=5):
            link_node = item.find('a')
            if link_node:
                latest_updates.append({
                    "title": item.text.strip(),
                    "content": "Latest breakthrough in nuclear energy and subatomic physics.",
                    "category": "Atomic Future",
                    "timestamp": datetime.now().strftime("%H:%M")
                })
        return latest_updates
    except Exception as e:
        print(f"ScienceDaily Scraping Error: {e}")
        return []

def fetch_atomic_news():
    """Combines Phys.org and ScienceDaily for a robust news stream"""
    all_news = []
    
    # Source 1: ScienceDaily (User's preferred 2026 source)
    all_news.extend(fetch_atomic_news_sciencedaily())
    
    # Source 2: Phys.org (Legacy fallback/supplement)
    url = "https://phys.org/physics-news/quantum-physics/"
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = soup.find_all('div', class_='sorted-article-content', limit=3)
        for item in news_items:
            title_node = item.find('h3') or item.find('h4')
            if not title_node: continue
            desc_node = item.find('p')
            all_news.append({
                "title": title_node.text.strip(),
                "content": desc_node.text.strip() if desc_node else "",
                "category": "Atomic Future",
                "timestamp": datetime.now().strftime("%H:%M")
            })
    except Exception as e:
        print(f"Phys.org Scraping Error: {e}")
        
    return all_news


def update_vault_database(app, new_data):
    from app.extensions import db
    from app.models.knowledge import NewsArticle
    
    with app.app_context():
        for item in new_data:
            exists = NewsArticle.query.filter_by(title=item['title']).first()
            if not exists:
                article = NewsArticle(
                    title=item['title'],
                    content=item['content'],
                    category=item['category'],
                    timestamp=item['timestamp']
                )
                db.session.add(article)
        try:
            db.session.commit()
            print("Successfully updated Atomic Vault with news.")
        except IntegrityError:
            db.session.rollback()

def start_hourly_update(app):
    while True:
        print("Scraping latest Atomic Science news...")
        new_data = fetch_atomic_news()
        if new_data:
            update_vault_database(app, new_data)
        time.sleep(3600)
