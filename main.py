"""
Main Pipeline
Orchestrates all agents in the Agentic AI Market-Research System.
"""
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from scripts.planner_agent import PlannerAgent
from scripts.collector_agent import CollectorAgent
from scripts.extractor_agent import ExtractorAgent
from scripts.tagger_agent import TaggerAgent
from scripts.synthesizer_agent import SynthesizerAgent
from scripts.report_generator import ReportGenerator


def print_banner():
    """Print system banner."""
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║   Agentic AI Market-Research System                      ║
    ║   Billboard Player Rankings - Product De-Risking         ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)


def run_pipeline(use_mock_data: bool = True):
    """
    Run the complete market research pipeline.
    
    Args:
        use_mock_data: If True, use mock data instead of real APIs
    """
    print_banner()
    
    print("\n" + "="*60)
    print("STEP 1: PLANNING")
    print("="*60)
    
    # Step 1: Generate research plan
    planner = PlannerAgent(topic="Billboard-style soccer player rankings app - product de-risking research")
    plan = planner.create_plan()
    planner.print_plan_summary(plan)
    plan_path = planner.save_plan(plan)
    
    print("\n" + "="*60)
    print("STEP 2: DATA COLLECTION")
    print("="*60)
    
    # Step 2: Collect data
    collector = CollectorAgent(plan, use_mock_data=use_mock_data)
    raw_items = collector.collect_all()
    raw_data_path = collector.save_raw_data()
    
    print("\n" + "="*60)
    print("STEP 3: DATA EXTRACTION & NORMALIZATION")
    print("="*60)
    
    # Step 3: Extract and normalize
    extractor = ExtractorAgent()
    evidence_items = extractor.extract_all(raw_items)
    evidence_path = extractor.save_evidence()
    
    print("\n" + "="*60)
    print("STEP 4: DATA TAGGING & CLASSIFICATION")
    print("="*60)
    
    # Step 4: Tag and classify
    tagger = TaggerAgent()
    tagged_items = tagger.tag_all(evidence_items)
    tagged_path = tagger.save_tagged_items(tagged_items)
    
    print("\n" + "="*60)
    print("STEP 5: SYNTHESIS & ANALYSIS")
    print("="*60)
    
    # Step 5: Synthesize and analyze
    synthesizer = SynthesizerAgent(research_plan=plan)
    synthesis_results = synthesizer.synthesize(tagged_items)
    synthesizer.print_summary()
    synthesis_path = synthesizer.save_synthesis()
    
    print("\n" + "="*60)
    print("STEP 6: REPORT GENERATION")
    print("="*60)
    
    # Step 6: Generate report
    generator = ReportGenerator()
    generator.generate_full_report(
        synthesis_path=synthesis_path,
        evidence_path=tagged_path,
        report_path="REPORT.md",
        csv_path="evidence.csv"
    )
    
    print("\n" + "="*60)
    print("PIPELINE COMPLETE")
    print("="*60)
    
    print("\n✓ All steps completed successfully!")
    print("\nGenerated outputs:")
    print(f"  1. Research Plan: {plan_path}")
    print(f"  2. Raw Data: {raw_data_path}")
    print(f"  3. Evidence Items: {evidence_path}")
    print(f"  4. Tagged Evidence: {tagged_path}")
    print(f"  5. Synthesis Results: {synthesis_path}")
    print(f"  6. Final Report: REPORT.md")
    print(f"  7. Evidence CSV: evidence.csv")
    
    print("\n" + "="*60)
    print("Next steps:")
    print("  - Review REPORT.md for insights and recommendations")
    print("  - Analyze evidence.csv for detailed evidence data")
    print("  - Customize agents for specific research needs")
    print("="*60 + "\n")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run the Agentic AI Market-Research System"
    )
    parser.add_argument(
        "--real-data",
        action="store_true",
        help="Use real APIs instead of mock data (requires API credentials)"
    )
    
    args = parser.parse_args()
    
    use_mock_data = not args.real_data
    
    if not use_mock_data:
        print("WARNING: Real data mode requires API credentials.")
        print("Make sure to set up .env file with necessary API keys.")
        response = input("Continue? (y/n): ")
        if response.lower() != 'y':
            print("Exiting.")
            return
    
    run_pipeline(use_mock_data=use_mock_data)


if __name__ == "__main__":
    main()
