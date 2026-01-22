"""
Planner Agent
Generates research plan JSON including quotas, sources, and stop conditions.
"""
import json
import sys
from pathlib import Path
from typing import Dict, Any, List

# Add parent directory to path to import schemas
sys.path.insert(0, str(Path(__file__).parent.parent))

from schemas.evidence_item import ResearchPlan, ProductHypothesis


class PlannerAgent:
    """
    Planner Agent generates comprehensive research plans for market research.
    """
    
    def __init__(self, topic: str = None):
        """
        Initialize the Planner Agent.
        
        Args:
            topic: Research topic (default: Billboard player rankings research)
        """
        self.topic = topic or "Billboard-style soccer player rankings app - product de-risking research"
    
    def create_plan(self, custom_config: Dict[str, Any] = None) -> ResearchPlan:
        """
        Create a research plan based on the topic and configuration.
        
        Args:
            custom_config: Optional custom configuration to override defaults
            
        Returns:
            ResearchPlan object
        """
        # Default plan configuration for Billboard player rankings research
        default_config = {
            "research_topic": self.topic,
            "target_segments": [
                "Potential",
                "Casual",
                "Engaged",
                "Bettor",
                "Fantasy"
            ],
            "product_hypothesis": {
                "product_name": "Billboard-style soccer player rankings app",
                "goal": "Drive repeat engagement, trust, sharing, and decision support (watch/fantasy/betting) for 18-30 fans",
                "in_scope_concepts": [
                    "player rankings",
                    "player comparison",
                    "follow players",
                    "who to watch",
                    "form",
                    "momentum",
                    "rank movement",
                    "fantasy decisions",
                    "betting decisions",
                    "debate",
                    "shareable takes",
                    "player narratives",
                    "team selection based on players",
                    "overrated",
                    "underrated",
                    "ballon d'or",
                    "player of the week",
                    "power ranking"
                ],
                "out_of_scope_concepts": [
                    "equipment",
                    "training",
                    "boots",
                    "cleats",
                    "coaching drills",
                    "fitness plans",
                    "academy training",
                    "how to play",
                    "youth training",
                    "shin guards",
                    "jerseys",
                    "balls"
                ],
                "required_outputs": [
                    "primary habit moment",
                    "trust model requirements",
                    "share artifact spec",
                    "V1 wedge segment",
                    "do-not-build list"
                ]
            },
            "sources": {
                "reddit": {
                    "subreddits": ["soccer", "FantasyPL", "SoccerBetting", "footballtactics", "PremierLeague"],
                    "time_filter": "year",
                    "sort": "top"
                },
                "youtube": {
                    "search_terms": [
                        "player rankings 2024",
                        "best players right now",
                        "fantasy football tips",
                        "soccer betting analysis",
                        "player comparison debate",
                        "overrated underrated players"
                    ],
                    "max_results": 30
                },
                "app_store": {
                    "apps": ["FotMob", "OneFootball", "ESPN Fantasy", "The Athletic", "SofaScore"],
                    "review_count": 300
                },
                "media": {
                    "websites": [
                        "theringer.com",
                        "theathletic.com",
                        "espn.com",
                        "reddit.com/r/soccer"
                    ],
                    "article_count": 20
                }
            },
            "quotas": {
                "reddit": 150,
                "youtube": 30,
                "app_store": 300,
                "media": 20,
                "total": 500
            },
            "stop_conditions": {
                "max_total_items": 500,
                "time_limit_hours": 48,
                "min_items_per_source": 20
            },
            "keywords": [
                "player rankings",
                "best players",
                "player comparison",
                "fantasy football",
                "betting tips",
                "player stats",
                "form guide",
                "player ratings",
                "tier list",
                "top players",
                "overrated",
                "underrated",
                "power rankings"
            ],
            "filters": {
                "min_engagement": 5,
                "language": "en",
                "exclude_spam": True,
                "recency_months": 12
            }
        }
        
        # Merge custom config if provided
        if custom_config:
            config = self._merge_configs(default_config, custom_config)
        else:
            config = default_config
        
        # Create and validate the research plan
        plan = ResearchPlan(**config)
        return plan
    
    def _merge_configs(self, default: Dict, custom: Dict) -> Dict:
        """
        Deep merge custom config into default config.
        """
        result = default.copy()
        for key, value in custom.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result
    
    def save_plan(self, plan: ResearchPlan, output_path: str = "data/research_plan.json"):
        """
        Save the research plan to a JSON file.
        
        Args:
            plan: ResearchPlan object to save
            output_path: Path to save the plan
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(plan.model_dump(), f, indent=2, default=str)
        
        print(f"✓ Research plan saved to {output_path}")
        return output_path
    
    def load_plan(self, plan_path: str) -> ResearchPlan:
        """
        Load a research plan from a JSON file.
        
        Args:
            plan_path: Path to the plan JSON file
            
        Returns:
            ResearchPlan object
        """
        with open(plan_path, 'r') as f:
            plan_data = json.load(f)
        
        return ResearchPlan(**plan_data)
    
    def print_plan_summary(self, plan: ResearchPlan):
        """
        Print a human-readable summary of the research plan.
        """
        print("\n" + "="*60)
        print("RESEARCH PLAN SUMMARY")
        print("="*60)
        print(f"\nTopic: {plan.research_topic}")
        print(f"\nTarget Segments: {', '.join(plan.target_segments)}")
        print(f"\nSources Configured: {', '.join(plan.sources.keys())}")
        print(f"\nCollection Quotas:")
        for source, quota in plan.quotas.items():
            print(f"  - {source}: {quota} items")
        print(f"\nStop Conditions:")
        for condition, value in plan.stop_conditions.items():
            print(f"  - {condition}: {value}")
        print(f"\nKeywords: {', '.join(plan.keywords[:10])}...")
        print("\n" + "="*60 + "\n")


def main():
    """
    Main function to demonstrate the Planner Agent.
    """
    print("Starting Planner Agent...")
    
    # Create planner
    planner = PlannerAgent(topic="Billboard-style soccer player rankings app - product de-risking research")
    
    # Generate research plan
    plan = planner.create_plan()
    
    # Print summary
    planner.print_plan_summary(plan)
    
    # Save plan to file
    output_path = planner.save_plan(plan)
    
    print(f"Plan generation complete. Saved to {output_path}")
    
    return plan


if __name__ == "__main__":
    main()
