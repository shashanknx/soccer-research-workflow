"""
Tagger Agent
Classifies data into segments, moments, jobs, themes, and sentiment.
"""
import sys
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Set
from collections import Counter

# Add parent directory to path to import schemas
sys.path.insert(0, str(Path(__file__).parent.parent))

from schemas.evidence_item import EvidenceItem


class TaggerAgent:
    """
    Tagger Agent classifies evidence items using keyword rules and pattern matching.
    """
    
    def __init__(self):
        """Initialize the Tagger Agent with tagging rules for Billboard player rankings research."""
        
        # Segment classification rules (Billboard player rankings focus)
        self.segment_rules = {
            "potential_fan": ["new to soccer", "getting into", "don't know much", "learning about", "just started watching", "beginner"],
            "casual_fan": ["watch occasionally", "big games", "world cup", "casual", "highlights", "don't follow closely"],
            "engaged_fan": ["follow closely", "know the players", "watch every game", "fan forum", "statistics", "analysis", "tactics"],
            "bettor": ["bet", "odds", "gambling", "wager", "prediction", "betting", "stake", "parlay"],
            "fantasy_enthusiast": ["fantasy", "FPL", "fantasy premier league", "draft", "team selection", "points", "captain"]
        }
        
        # Moment classification rules (when fans engage with rankings/content)
        self.moment_rules = {
            "pre_match": ["before the game", "preview", "starting lineup", "team news", "pre-match", "before kickoff"],
            "post_match": ["after the game", "recap", "highlights", "post-match", "match review", "how did", "performance"],
            "weekly": ["this week", "weekend", "matchweek", "game week", "weekly", "round"],
            "transfer_window": ["transfer", "signing", "new player", "bought", "sold", "rumor", "transfer news"],
            "tournament": ["world cup", "champions league", "euros", "tournament", "knockout", "final"],
            "evergreen": ["all time", "best ever", "greatest", "top 10", "ranking", "compare", "versus"]
        }
        
        # Job-to-be-done classification rules (what users are trying to accomplish)
        self.job_rules = {
            "orientation": ["who is", "explain", "help me understand", "what does", "confused", "guide"],
            "validation": ["am I right", "do you agree", "what do you think", "is this correct", "validate"],
            "decision_support": ["should I watch", "worth watching", "who to pick", "best choice", "help me decide"],
            "entertainment": ["fun", "interesting", "enjoy", "entertaining", "exciting"],
            "social_currency": ["share", "tell my friends", "brag", "show off", "impress", "prove"],
            "credibility_check": ["reliable", "trustworthy", "accurate", "biased", "source", "methodology"]
        }
        
        # Theme keywords (aligned with de-risking questions RQ1-RQ5)
        self.theme_keywords = {
            "trust": ["trust", "reliable", "accurate", "credible", "biased", "fair", "methodology", "data source"],
            "explainability": ["why", "how", "explain", "understand", "algorithm", "calculation", "criteria"],
            "shareability": ["share", "screenshot", "post", "social media", "viral", "tweet", "instagram"],
            "notifications": ["notify", "alert", "push", "reminder", "update", "notification"],
            "usability": ["easy", "simple", "intuitive", "user friendly", "navigation", "interface", "design"],
            "engagement": ["addictive", "keep coming back", "daily", "habit", "retention", "sticky"],
            "comparison": ["compare", "versus", "vs", "better than", "rank", "tier list"],
            "personalization": ["my team", "favorite", "customize", "preferences", "filter", "personalize"]
        }
        
        # Sentiment keywords
        self.positive_words = [
            "great", "excellent", "amazing", "love", "best", "perfect", "awesome",
            "good", "happy", "satisfied", "recommend", "fantastic", "wonderful"
        ]
        
        self.negative_words = [
            "bad", "terrible", "awful", "hate", "worst", "poor", "disappointed",
            "frustrating", "useless", "waste", "horrible", "annoying", "painful"
        ]
    
    def tag_all(self, evidence_items: List[EvidenceItem]) -> List[EvidenceItem]:
        """
        Tag all evidence items with segments, moments, jobs, themes, and sentiment.
        
        Args:
            evidence_items: List of EvidenceItem objects
            
        Returns:
            List of tagged EvidenceItem objects
        """
        print("\nStarting tagging process...")
        
        tagged_items = []
        for item in evidence_items:
            tagged_item = self._tag_item(item)
            tagged_items.append(tagged_item)
        
        print(f"✓ Tagged {len(tagged_items)} evidence items")
        
        # Print tagging statistics
        self._print_tagging_stats(tagged_items)
        
        return tagged_items
    
    def _tag_item(self, item: EvidenceItem) -> EvidenceItem:
        """
        Tag a single evidence item.
        
        Args:
            item: EvidenceItem object
            
        Returns:
            Tagged EvidenceItem object
        """
        # Combine title and content for analysis
        text = f"{item.title or ''} {item.content}".strip().lower()
        
        # Tag segment
        item.segment = self._classify_segment(text)
        
        # Tag moment
        item.moment = self._classify_moment(text)
        
        # Tag job
        item.job = self._classify_job(text)
        
        # Tag themes (can have multiple)
        item.themes = self._classify_themes(text)
        
        # Tag sentiment
        item.sentiment = self._classify_sentiment(text, item.engagement_metrics)
        
        return item
    
    def _classify_segment(self, text: str) -> str:
        """
        Classify user segment based on text content.
        
        Args:
            text: Text content (title + content)
            
        Returns:
            Segment classification
        """
        scores = {}
        
        for segment, keywords in self.segment_rules.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                scores[segment] = score
        
        if scores:
            return max(scores, key=scores.get)
        
        return "general"
    
    def _classify_moment(self, text: str) -> str:
        """
        Classify user moment based on text content.
        
        Args:
            text: Text content (title + content)
            
        Returns:
            Moment classification
        """
        scores = {}
        
        for moment, keywords in self.moment_rules.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                scores[moment] = score
        
        if scores:
            return max(scores, key=scores.get)
        
        return "general_interest"
    
    def _classify_job(self, text: str) -> str:
        """
        Classify job-to-be-done based on text content.
        
        Args:
            text: Text content (title + content)
            
        Returns:
            Job classification
        """
        scores = {}
        
        for job, keywords in self.job_rules.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                scores[job] = score
        
        if scores:
            return max(scores, key=scores.get)
        
        return "general_inquiry"
    
    def _classify_themes(self, text: str) -> List[str]:
        """
        Classify themes based on text content (can have multiple).
        
        Args:
            text: Text content (title + content)
            
        Returns:
            List of theme classifications
        """
        themes = []
        
        for theme, keywords in self.theme_keywords.items():
            if any(keyword in text for keyword in keywords):
                themes.append(theme)
        
        # Return top 3 themes or all if fewer
        return themes[:3] if themes else ["general"]
    
    def _classify_sentiment(self, text: str, engagement: Dict[str, Any]) -> str:
        """
        Classify sentiment based on text and engagement metrics.
        
        Args:
            text: Text content (title + content)
            engagement: Engagement metrics dictionary
            
        Returns:
            Sentiment classification (positive, negative, neutral, mixed)
        """
        # Count positive and negative words
        positive_count = sum(1 for word in self.positive_words if word in text)
        negative_count = sum(1 for word in self.negative_words if word in text)
        
        # Consider engagement metrics
        total_engagement = engagement.get("total_engagement", 0)
        high_engagement = total_engagement > 100
        
        # Classify sentiment
        if positive_count > negative_count + 1:
            return "positive"
        elif negative_count > positive_count + 1:
            return "negative"
        elif positive_count > 0 and negative_count > 0:
            return "mixed"
        elif high_engagement:
            return "positive"  # High engagement usually indicates positive content
        else:
            return "neutral"
    
    def _print_tagging_stats(self, items: List[EvidenceItem]):
        """Print statistics about tagged items."""
        
        segments = Counter(item.segment for item in items)
        moments = Counter(item.moment for item in items)
        jobs = Counter(item.job for item in items)
        sentiments = Counter(item.sentiment for item in items)
        
        print("\nTagging Statistics:")
        print(f"\nSegments: {dict(segments)}")
        print(f"Moments: {dict(moments)}")
        print(f"Jobs: {dict(jobs)}")
        print(f"Sentiments: {dict(sentiments)}")
    
    def save_tagged_items(self, items: List[EvidenceItem], output_path: str = "data/tagged_evidence.json"):
        """
        Save tagged evidence items to JSON file.
        
        Args:
            items: List of tagged EvidenceItem objects
            output_path: Path to save the tagged items
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to dictionaries for JSON serialization
        items_dicts = [item.model_dump(mode='json') for item in items]
        
        with open(output_file, 'w') as f:
            json.dump(items_dicts, f, indent=2, default=str)
        
        print(f"✓ Tagged items saved to {output_path}")
        return output_path


def main():
    """
    Main function to demonstrate the Tagger Agent.
    """
    print("Starting Tagger Agent...")
    
    # Load evidence items
    evidence_path = Path("data/evidence_items.json")
    if not evidence_path.exists():
        print("Error: Evidence items not found. Run extractor_agent.py first.")
        return
    
    with open(evidence_path, 'r') as f:
        evidence_data = json.load(f)
    
    evidence_items = [EvidenceItem(**item) for item in evidence_data]
    print(f"Loaded {len(evidence_items)} evidence items")
    
    # Create tagger and tag items
    tagger = TaggerAgent()
    tagged_items = tagger.tag_all(evidence_items)
    
    # Save tagged items
    tagger.save_tagged_items(tagged_items)
    
    print(f"\nTagging complete. {len(tagged_items)} items tagged.")


if __name__ == "__main__":
    main()
