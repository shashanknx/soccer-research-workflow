"""
Collector Agent
Fetches URLs/posts from Reddit, app stores, YouTube, TikTok, and media sources.
"""
import sys
import json
import time
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

import requests
from bs4 import BeautifulSoup

# Add parent directory to path to import schemas
sys.path.insert(0, str(Path(__file__).parent.parent))

from schemas.evidence_item import ResearchPlan


class CollectorAgent:
    """
    Collector Agent fetches raw data from various sources.
    """
    
    def __init__(self, plan: ResearchPlan, use_mock_data: bool = True):
        """
        Initialize the Collector Agent.
        
        Args:
            plan: Research plan with source configurations
            use_mock_data: If True, use mock data instead of real APIs
        """
        self.plan = plan
        self.use_mock_data = use_mock_data
        self.collected_items = []
    
    def collect_all(self) -> List[Dict[str, Any]]:
        """
        Collect data from all configured sources.
        
        Returns:
            List of raw data items
        """
        print("\nStarting data collection...")
        print(f"Using mock data: {self.use_mock_data}")
        
        all_items = []
        
        # Collect from each source
        if "reddit" in self.plan.sources:
            reddit_items = self.collect_reddit()
            all_items.extend(reddit_items)
            print(f"✓ Collected {len(reddit_items)} items from Reddit")
        
        if "youtube" in self.plan.sources:
            youtube_items = self.collect_youtube()
            all_items.extend(youtube_items)
            print(f"✓ Collected {len(youtube_items)} items from YouTube")
        
        if "app_store" in self.plan.sources:
            app_items = self.collect_app_store()
            all_items.extend(app_items)
            print(f"✓ Collected {len(app_items)} items from App Stores")
        
        if "media" in self.plan.sources:
            media_items = self.collect_media()
            all_items.extend(media_items)
            print(f"✓ Collected {len(media_items)} items from Media")
        
        self.collected_items = all_items
        print(f"\n✓ Total items collected: {len(all_items)}")
        
        return all_items
    
    def collect_reddit(self) -> List[Dict[str, Any]]:
        """
        Collect data from Reddit.
        """
        if self.use_mock_data:
            return self._mock_reddit_data()
        
        # Real Reddit API implementation would go here
        # Requires PRAW library and Reddit API credentials
        items = []
        # Implementation placeholder
        return items
    
    def collect_youtube(self) -> List[Dict[str, Any]]:
        """
        Collect data from YouTube.
        """
        if self.use_mock_data:
            return self._mock_youtube_data()
        
        # Real YouTube API implementation would go here
        items = []
        # Implementation placeholder
        return items
    
    def collect_app_store(self) -> List[Dict[str, Any]]:
        """
        Collect reviews from app stores.
        """
        if self.use_mock_data:
            return self._mock_app_store_data()
        
        # Real App Store scraping implementation would go here
        items = []
        # Implementation placeholder
        return items
    
    def collect_media(self) -> List[Dict[str, Any]]:
        """
        Collect articles from media sources.
        """
        if self.use_mock_data:
            return self._mock_media_data()
        
        # Real web scraping implementation would go here
        items = []
        # Implementation placeholder
        return items
    
    def _mock_reddit_data(self) -> List[Dict[str, Any]]:
        """Generate mock Reddit data for Billboard player rankings research."""
        quota = min(self.plan.quotas.get("reddit", 50), 50)
        
        mock_posts = [
            {
                "source": "reddit",
                "source_type": "post",
                "source_url": "https://reddit.com/r/soccer/comments/{i}",
                "title": "Who are your top 10 players right now?",
                "content": "Trying to settle a debate with friends about who the best players are. What makes a player truly elite? Stats alone or watching them play?",
                "author": "soccer_fan_{i}",
                "published_at": datetime.now().isoformat(),
                "upvotes": 45,
                "comments": 23,
                "subreddit": "soccer"
            },
            {
                "source": "reddit",
                "source_type": "post",
                "source_url": "https://reddit.com/r/FantasyPL/comments/{i}",
                "title": "Player comparison for this gameweek",
                "content": "Should I captain Haaland or Salah? Looking at form, fixtures, and recent stats. What do you guys think?",
                "author": "fpl_addict_{i}",
                "published_at": datetime.now().isoformat(),
                "upvotes": 67,
                "comments": 34,
                "subreddit": "FantasyPL"
            },
            {
                "source": "reddit",
                "source_type": "post",
                "source_url": "https://reddit.com/r/SoccerBetting/comments/{i}",
                "title": "Player performance predictions",
                "content": "Based on recent form and matchups, who do you think will score this weekend? Need some insights for my accumulator.",
                "author": "betting_pro_{i}",
                "published_at": datetime.now().isoformat(),
                "upvotes": 31,
                "comments": 18,
                "subreddit": "SoccerBetting"
            }
        ]
        
        items = []
        for i in range(quota // 3 + 1):
            for template in mock_posts:
                item = template.copy()
                item["source_url"] = template["source_url"].format(i=i)
                item["author"] = template["author"].format(i=i)
                item["upvotes"] = template["upvotes"] + i * 3
                item["comments"] = template["comments"] + i * 2
                items.append(item)
                if len(items) >= quota:
                    break
            if len(items) >= quota:
                break
        
        return items[:quota]
    
    def _mock_youtube_data(self) -> List[Dict[str, Any]]:
        """Generate mock YouTube data for Billboard player rankings research."""
        quota = min(self.plan.quotas.get("youtube", 30), 30)
        
        items = []
        for i in range(quota):
            items.append({
                "source": "youtube",
                "source_type": "video",
                "source_url": f"https://youtube.com/watch?v=video_{i}",
                "title": f"Top 10 Players in the World Right Now | 2024 Rankings",
                "content": f"Ranking the best players based on current form, statistics, and impact. Who makes the cut? Let me know if you agree with my list!",
                "author": f"FootballAnalysis{i}",
                "published_at": datetime.now().isoformat(),
                "views": 15000 + i * 500,
                "likes": 890 + i * 15,
                "comments": 234 + i * 3,
                "duration": "12:34"
            })
        
        return items
    
    def _mock_app_store_data(self) -> List[Dict[str, Any]]:
        """Generate mock app store review data for Billboard player rankings research."""
        quota = min(self.plan.quotas.get("app_store", 50), 50)
        
        items = []
        apps = ["FotMob", "OneFootball", "ESPN Fantasy", "SofaScore", "The Athletic"]
        
        for i in range(quota):
            app = apps[i % len(apps)]
            items.append({
                "source": "app_store",
                "source_type": "review",
                "source_url": f"https://apps.apple.com/app/{app.lower().replace(' ', '-')}/review_{i}",
                "title": f"Review of {app}",
                "content": f"Love the player ratings and comparisons! Wish there was a way to see historical rankings and share my predictions with friends.",
                "author": f"FootballFan{i}",
                "published_at": datetime.now().isoformat(),
                "rating": 4 + (i % 2),
                "helpful_count": 15 + i,
                "app_name": app
            })
        
        return items
    
    def _mock_media_data(self) -> List[Dict[str, Any]]:
        """Generate mock media article data for Billboard player rankings research."""
        quota = min(self.plan.quotas.get("media", 20), 20)
        
        items = []
        for i in range(quota):
            items.append({
                "source": "media",
                "source_type": "article",
                "source_url": f"https://theathletic.com/article/player-rankings-{i}",
                "title": f"Power Rankings: The 50 Best Players in World Football",
                "content": f"Our data-driven approach combines stats, expert analysis, and impact to rank the world's elite players. Featuring breakdowns of why each player earned their spot...",
                "author": f"Athletic Staff Writer {i}",
                "published_at": datetime.now().isoformat(),
                "shares": 125 + i * 8,
                "website": "theathletic.com"
            })
        
        return items
    
    def save_raw_data(self, output_path: str = "data/raw_collected_data.json"):
        """
        Save collected raw data to JSON file.
        
        Args:
            output_path: Path to save the data
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(self.collected_items, f, indent=2, default=str)
        
        print(f"✓ Raw data saved to {output_path}")
        return output_path


def main():
    """
    Main function to demonstrate the Collector Agent.
    """
    print("Starting Collector Agent...")
    
    # Load research plan
    plan_path = Path("data/research_plan.json")
    if not plan_path.exists():
        print("Error: Research plan not found. Run planner_agent.py first.")
        return
    
    with open(plan_path, 'r') as f:
        plan_data = json.load(f)
    
    plan = ResearchPlan(**plan_data)
    
    # Create collector and collect data
    collector = CollectorAgent(plan, use_mock_data=True)
    items = collector.collect_all()
    
    # Save raw data
    collector.save_raw_data()
    
    print(f"\nData collection complete. Collected {len(items)} items.")


if __name__ == "__main__":
    main()
