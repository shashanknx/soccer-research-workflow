"""
Synthesizer Agent
Aggregates evidence, clusters themes, and produces product recommendations.
"""
import sys
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple
from collections import Counter, defaultdict

# Add parent directory to path to import schemas
sys.path.insert(0, str(Path(__file__).parent.parent))

from schemas.evidence_item import EvidenceItem


class SynthesizerAgent:
    """
    Synthesizer Agent aggregates evidence and generates insights.
    """
    
    def __init__(self, research_plan=None):
        """Initialize the Synthesizer Agent."""
        self.synthesis_results = {}
        self.research_plan = research_plan
    
    def synthesize(self, evidence_items: List[EvidenceItem]) -> Dict[str, Any]:
        """
        Synthesize evidence items into insights and recommendations.
        
        Args:
            evidence_items: List of tagged EvidenceItem objects
            
        Returns:
            Dictionary containing synthesis results
        """
        print("\nStarting synthesis process...")
        
        results = {
            "research_topic": self.research_plan.research_topic if self.research_plan else "Billboard-style soccer player rankings app - product de-risking research",
            "total_items": len(evidence_items),
            "sources_analyzed": self._analyze_sources(evidence_items),
            "segment_insights": self._analyze_segments(evidence_items),
            "moment_insights": self._analyze_moments(evidence_items),
            "job_insights": self._analyze_jobs(evidence_items),
            "theme_clusters": self._cluster_themes(evidence_items),
            "sentiment_analysis": self._analyze_sentiment(evidence_items),
            "top_evidence": self._identify_top_evidence(evidence_items),
            "recommendations": self._generate_recommendations(evidence_items)
        }
        
        self.synthesis_results = results
        print(f"✓ Synthesis complete. Generated {len(results)} insight categories.")
        
        return results
    
    def _analyze_sources(self, items: List[EvidenceItem]) -> Dict[str, Any]:
        """Analyze distribution across sources."""
        source_counts = Counter(item.source for item in items)
        
        total = len(items)
        source_percentages = {
            source: {
                "count": count,
                "percentage": round(count / total * 100, 1)
            }
            for source, count in source_counts.items()
        }
        
        return source_percentages
    
    def _analyze_segments(self, items: List[EvidenceItem]) -> Dict[str, Any]:
        """Analyze user segments."""
        segment_counts = Counter(item.segment for item in items)
        
        # Calculate average engagement per segment
        segment_engagement = defaultdict(list)
        for item in items:
            if item.segment:
                total_eng = item.engagement_metrics.get("total_engagement", 0)
                segment_engagement[item.segment].append(total_eng)
        
        segment_analysis = {}
        for segment, count in segment_counts.most_common():
            avg_engagement = (
                sum(segment_engagement[segment]) / len(segment_engagement[segment])
                if segment_engagement[segment] else 0
            )
            
            segment_analysis[segment] = {
                "count": count,
                "percentage": round(count / len(items) * 100, 1),
                "avg_engagement": round(avg_engagement, 1)
            }
        
        return segment_analysis
    
    def _analyze_moments(self, items: List[EvidenceItem]) -> Dict[str, Any]:
        """Analyze user moments."""
        moment_counts = Counter(item.moment for item in items)
        
        moment_analysis = {}
        for moment, count in moment_counts.most_common():
            moment_analysis[moment] = {
                "count": count,
                "percentage": round(count / len(items) * 100, 1)
            }
        
        return moment_analysis
    
    def _analyze_jobs(self, items: List[EvidenceItem]) -> Dict[str, Any]:
        """Analyze jobs-to-be-done."""
        job_counts = Counter(item.job for item in items)
        
        job_analysis = {}
        for job, count in job_counts.most_common():
            job_analysis[job] = {
                "count": count,
                "percentage": round(count / len(items) * 100, 1)
            }
        
        return job_analysis
    
    def _cluster_themes(self, items: List[EvidenceItem]) -> Dict[str, Any]:
        """Cluster and analyze themes."""
        # Flatten all themes
        all_themes = []
        for item in items:
            all_themes.extend(item.themes)
        
        theme_counts = Counter(all_themes)
        
        # Identify theme co-occurrence
        theme_cooccurrence = defaultdict(Counter)
        for item in items:
            themes = item.themes
            for i, theme1 in enumerate(themes):
                for theme2 in themes[i+1:]:
                    theme_cooccurrence[theme1][theme2] += 1
                    theme_cooccurrence[theme2][theme1] += 1
        
        theme_clusters = {}
        for theme, count in theme_counts.most_common(10):
            related = dict(theme_cooccurrence[theme].most_common(3))
            
            theme_clusters[theme] = {
                "count": count,
                "percentage": round(count / len(all_themes) * 100, 1) if all_themes else 0,
                "related_themes": related
            }
        
        return theme_clusters
    
    def _analyze_sentiment(self, items: List[EvidenceItem]) -> Dict[str, Any]:
        """Analyze sentiment distribution."""
        sentiment_counts = Counter(item.sentiment for item in items)
        
        sentiment_analysis = {}
        for sentiment, count in sentiment_counts.items():
            sentiment_analysis[sentiment] = {
                "count": count,
                "percentage": round(count / len(items) * 100, 1)
            }
        
        # Calculate sentiment by segment
        sentiment_by_segment = defaultdict(Counter)
        for item in items:
            if item.segment and item.sentiment:
                sentiment_by_segment[item.segment][item.sentiment] += 1
        
        sentiment_analysis["by_segment"] = dict(sentiment_by_segment)
        
        return sentiment_analysis
    
    def _identify_top_evidence(self, items: List[EvidenceItem], top_n: int = 10) -> List[Dict[str, Any]]:
        """Identify top evidence items by engagement."""
        # Sort by total engagement
        sorted_items = sorted(
            items,
            key=lambda x: x.engagement_metrics.get("total_engagement", 0),
            reverse=True
        )
        
        top_items = []
        for item in sorted_items[:top_n]:
            top_items.append({
                "id": item.id,
                "source": item.source,
                "title": item.title,
                "content": item.content[:200] + "..." if len(item.content) > 200 else item.content,
                "engagement": item.engagement_metrics.get("total_engagement", 0),
                "segment": item.segment,
                "themes": item.themes,
                "sentiment": item.sentiment
            })
        
        return top_items
    
    def _generate_recommendations(self, items: List[EvidenceItem]) -> List[Dict[str, Any]]:
        """Generate product recommendations based on evidence."""
        recommendations = []
        
        # Analyze jobs and themes to generate recommendations
        job_counts = Counter(item.job for item in items)
        theme_counts = Counter(theme for item in items for theme in item.themes)
        
        # Recommendation 1: Based on most common job
        if job_counts:
            top_job = job_counts.most_common(1)[0][0]
            recommendations.append({
                "priority": 1,
                "type": "Feature",
                "title": f"Focus on {top_job.replace('_', ' ').title()}",
                "rationale": f"Most common job-to-be-done ({job_counts[top_job]} occurrences)",
                "target_segment": self._get_segment_for_job(items, top_job),
                "confidence": "high"
            })
        
        # Recommendation 2: Based on most common theme
        if theme_counts:
            top_theme = theme_counts.most_common(1)[0][0]
            recommendations.append({
                "priority": 2,
                "type": "Content",
                "title": f"Create content about {top_theme.replace('_', ' ').title()}",
                "rationale": f"Most discussed theme ({theme_counts[top_theme]} mentions)",
                "target_segment": "all_segments",
                "confidence": "high"
            })
        
        # Recommendation 3: Based on segment with highest engagement
        segment_engagement = self._get_highest_engagement_segment(items)
        if segment_engagement:
            segment, avg_eng = segment_engagement
            recommendations.append({
                "priority": 3,
                "type": "Strategy",
                "title": f"Prioritize {segment.replace('_', ' ').title()} Segment",
                "rationale": f"Highest average engagement ({avg_eng:.1f})",
                "target_segment": segment,
                "confidence": "medium"
            })
        
        # Recommendation 4: Address negative sentiment
        negative_items = [item for item in items if item.sentiment == "negative"]
        if negative_items:
            negative_themes = Counter(theme for item in negative_items for theme in item.themes)
            if negative_themes:
                top_negative_theme = negative_themes.most_common(1)[0][0]
                recommendations.append({
                    "priority": 4,
                    "type": "Improvement",
                    "title": f"Address concerns about {top_negative_theme.replace('_', ' ').title()}",
                    "rationale": f"Common theme in negative feedback ({negative_themes[top_negative_theme]} mentions)",
                    "target_segment": "all_segments",
                    "confidence": "medium"
                })
        
        # Recommendation 5: Leverage positive sentiment
        positive_items = [item for item in items if item.sentiment == "positive"]
        if positive_items:
            positive_themes = Counter(theme for item in positive_items for theme in item.themes)
            if positive_themes:
                top_positive_theme = positive_themes.most_common(1)[0][0]
                recommendations.append({
                    "priority": 5,
                    "type": "Marketing",
                    "title": f"Highlight success in {top_positive_theme.replace('_', ' ').title()}",
                    "rationale": f"Strong positive sentiment ({len(positive_items)} positive mentions)",
                    "target_segment": "all_segments",
                    "confidence": "high"
                })
        
        return recommendations
    
    def _get_segment_for_job(self, items: List[EvidenceItem], job: str) -> str:
        """Get the most common segment for a given job."""
        segments = [item.segment for item in items if item.job == job and item.segment]
        if segments:
            return Counter(segments).most_common(1)[0][0]
        return "general"
    
    def _get_highest_engagement_segment(self, items: List[EvidenceItem]) -> Tuple[str, float]:
        """Get segment with highest average engagement."""
        segment_engagement = defaultdict(list)
        for item in items:
            if item.segment:
                total_eng = item.engagement_metrics.get("total_engagement", 0)
                segment_engagement[item.segment].append(total_eng)
        
        if segment_engagement:
            avg_engagements = {
                seg: sum(engs) / len(engs)
                for seg, engs in segment_engagement.items()
                if engs  # Ensure list is not empty
            }
            if avg_engagements:
                top_segment = max(avg_engagements, key=avg_engagements.get)
                return top_segment, avg_engagements[top_segment]
        
        return None, 0
    
    def save_synthesis(self, output_path: str = "data/synthesis_results.json"):
        """
        Save synthesis results to JSON file.
        
        Args:
            output_path: Path to save the synthesis results
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(self.synthesis_results, f, indent=2, default=str)
        
        print(f"✓ Synthesis results saved to {output_path}")
        return output_path
    
    def print_summary(self):
        """Print a human-readable summary of synthesis results."""
        if not self.synthesis_results:
            print("No synthesis results available.")
            return
        
        results = self.synthesis_results
        
        print("\n" + "="*60)
        print("SYNTHESIS SUMMARY")
        print("="*60)
        
        print(f"\nTotal Items Analyzed: {results['total_items']}")
        
        print("\nTop Segments:")
        for segment, data in list(results['segment_insights'].items())[:3]:
            print(f"  - {segment}: {data['count']} items ({data['percentage']}%)")
        
        print("\nTop Themes:")
        for theme, data in list(results['theme_clusters'].items())[:5]:
            print(f"  - {theme}: {data['count']} mentions ({data['percentage']}%)")
        
        print("\nSentiment Distribution:")
        for sentiment, data in results['sentiment_analysis'].items():
            if sentiment != "by_segment":
                print(f"  - {sentiment}: {data['count']} items ({data['percentage']}%)")
        
        print("\nTop Recommendations:")
        for rec in results['recommendations'][:3]:
            print(f"  {rec['priority']}. [{rec['type']}] {rec['title']}")
            print(f"     Rationale: {rec['rationale']}")
        
        print("\n" + "="*60 + "\n")


def main():
    """
    Main function to demonstrate the Synthesizer Agent.
    """
    print("Starting Synthesizer Agent...")
    
    # Load tagged evidence items
    evidence_path = Path("data/tagged_evidence.json")
    if not evidence_path.exists():
        print("Error: Tagged evidence not found. Run tagger_agent.py first.")
        return
    
    with open(evidence_path, 'r') as f:
        evidence_data = json.load(f)
    
    evidence_items = [EvidenceItem(**item) for item in evidence_data]
    print(f"Loaded {len(evidence_items)} tagged evidence items")
    
    # Create synthesizer and synthesize
    synthesizer = SynthesizerAgent()
    results = synthesizer.synthesize(evidence_items)
    
    # Print summary
    synthesizer.print_summary()
    
    # Save results
    synthesizer.save_synthesis()
    
    print("\nSynthesis complete.")


if __name__ == "__main__":
    main()
