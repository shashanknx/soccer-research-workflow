"""
Extractor Agent
Normalizes collected data into EvidenceItems schema.
"""
import sys
import json
import uuid
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# Add parent directory to path to import schemas
sys.path.insert(0, str(Path(__file__).parent.parent))

from schemas.evidence_item import EvidenceItem


class ExtractorAgent:
    """
    Extractor Agent normalizes raw collected data into EvidenceItem schema.
    """
    
    def __init__(self):
        """Initialize the Extractor Agent."""
        self.evidence_items = []
    
    def extract_all(self, raw_data: List[Dict[str, Any]]) -> List[EvidenceItem]:
        """
        Extract and normalize all raw data items into EvidenceItems.
        
        Args:
            raw_data: List of raw data dictionaries from collector
            
        Returns:
            List of EvidenceItem objects
        """
        print("\nStarting data extraction and normalization...")
        
        evidence_items = []
        
        for item in raw_data:
            try:
                evidence = self._extract_item(item)
                evidence_items.append(evidence)
            except Exception as e:
                print(f"Warning: Failed to extract item: {e}")
                continue
        
        self.evidence_items = evidence_items
        print(f"✓ Extracted and normalized {len(evidence_items)} evidence items")
        
        return evidence_items
    
    def _extract_item(self, raw_item: Dict[str, Any]) -> EvidenceItem:
        """
        Extract a single item and normalize it to EvidenceItem schema.
        
        Args:
            raw_item: Raw data dictionary
            
        Returns:
            EvidenceItem object
        """
        source = raw_item.get("source", "other")
        source_type = raw_item.get("source_type", "unknown")
        
        # Generate unique ID
        item_id = f"{source}_{source_type}_{uuid.uuid4().hex[:8]}"
        
        # Extract common fields
        title = raw_item.get("title")
        content = raw_item.get("content", "")
        author = raw_item.get("author")
        source_url = raw_item.get("source_url", "")
        
        # Parse published date
        published_at = None
        if "published_at" in raw_item:
            try:
                if isinstance(raw_item["published_at"], str):
                    published_at = datetime.fromisoformat(raw_item["published_at"].replace('Z', '+00:00'))
                elif isinstance(raw_item["published_at"], datetime):
                    published_at = raw_item["published_at"]
            except:
                pass
        
        # Extract engagement metrics based on source
        engagement_metrics = self._extract_engagement_metrics(raw_item, source)
        
        # Extract additional metadata
        metadata = self._extract_metadata(raw_item, source)
        
        # Create EvidenceItem
        evidence = EvidenceItem(
            id=item_id,
            source=source,
            source_url=source_url,
            source_type=source_type,
            title=title,
            content=content,
            author=author,
            published_at=published_at,
            engagement_metrics=engagement_metrics,
            metadata=metadata
        )
        
        return evidence
    
    def _extract_engagement_metrics(self, raw_item: Dict[str, Any], source: str) -> Dict[str, Any]:
        """
        Extract engagement metrics from raw item based on source.
        
        Args:
            raw_item: Raw data dictionary
            source: Source platform
            
        Returns:
            Dictionary of engagement metrics
        """
        metrics = {}
        
        if source == "reddit":
            metrics["upvotes"] = raw_item.get("upvotes", 0)
            metrics["comments"] = raw_item.get("comments", 0)
            metrics["score"] = raw_item.get("upvotes", 0)  # Reddit score
        
        elif source == "youtube":
            metrics["views"] = raw_item.get("views", 0)
            metrics["likes"] = raw_item.get("likes", 0)
            metrics["comments"] = raw_item.get("comments", 0)
        
        elif source == "app_store":
            metrics["rating"] = raw_item.get("rating", 0)
            metrics["helpful_count"] = raw_item.get("helpful_count", 0)
        
        elif source == "media":
            metrics["shares"] = raw_item.get("shares", 0)
            metrics["views"] = raw_item.get("views", 0)
        
        elif source == "tiktok":
            metrics["views"] = raw_item.get("views", 0)
            metrics["likes"] = raw_item.get("likes", 0)
            metrics["shares"] = raw_item.get("shares", 0)
            metrics["comments"] = raw_item.get("comments", 0)
        
        # Calculate total engagement score
        total_engagement = sum(metrics.values())
        metrics["total_engagement"] = total_engagement
        
        return metrics
    
    def _extract_metadata(self, raw_item: Dict[str, Any], source: str) -> Dict[str, Any]:
        """
        Extract platform-specific metadata.
        
        Args:
            raw_item: Raw data dictionary
            source: Source platform
            
        Returns:
            Dictionary of metadata
        """
        metadata = {}
        
        if source == "reddit":
            metadata["subreddit"] = raw_item.get("subreddit", "")
            metadata["post_type"] = raw_item.get("post_type", "")
        
        elif source == "youtube":
            metadata["duration"] = raw_item.get("duration", "")
            metadata["channel"] = raw_item.get("channel", "")
        
        elif source == "app_store":
            metadata["app_name"] = raw_item.get("app_name", "")
            metadata["version"] = raw_item.get("version", "")
        
        elif source == "media":
            metadata["website"] = raw_item.get("website", "")
            metadata["category"] = raw_item.get("category", "")
        
        return metadata
    
    def save_evidence(self, output_path: str = "data/evidence_items.json"):
        """
        Save evidence items to JSON file.
        
        Args:
            output_path: Path to save the evidence items
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to dictionaries for JSON serialization
        evidence_dicts = [item.model_dump(mode='json') for item in self.evidence_items]
        
        with open(output_file, 'w') as f:
            json.dump(evidence_dicts, f, indent=2, default=str)
        
        print(f"✓ Evidence items saved to {output_path}")
        return output_path
    
    def load_evidence(self, evidence_path: str) -> List[EvidenceItem]:
        """
        Load evidence items from JSON file.
        
        Args:
            evidence_path: Path to evidence items JSON file
            
        Returns:
            List of EvidenceItem objects
        """
        with open(evidence_path, 'r') as f:
            evidence_data = json.load(f)
        
        evidence_items = [EvidenceItem(**item) for item in evidence_data]
        self.evidence_items = evidence_items
        
        return evidence_items


def main():
    """
    Main function to demonstrate the Extractor Agent.
    """
    print("Starting Extractor Agent...")
    
    # Load raw collected data
    raw_data_path = Path("data/raw_collected_data.json")
    if not raw_data_path.exists():
        print("Error: Raw data not found. Run collector_agent.py first.")
        return
    
    with open(raw_data_path, 'r') as f:
        raw_data = json.load(f)
    
    print(f"Loaded {len(raw_data)} raw items")
    
    # Create extractor and extract data
    extractor = ExtractorAgent()
    evidence_items = extractor.extract_all(raw_data)
    
    # Save evidence items
    extractor.save_evidence()
    
    print(f"\nExtraction complete. {len(evidence_items)} evidence items created.")
    
    # Print sample
    if evidence_items:
        print("\nSample evidence item:")
        print(f"  ID: {evidence_items[0].id}")
        print(f"  Source: {evidence_items[0].source}")
        print(f"  Title: {evidence_items[0].title}")
        print(f"  Engagement: {evidence_items[0].engagement_metrics}")


if __name__ == "__main__":
    main()
