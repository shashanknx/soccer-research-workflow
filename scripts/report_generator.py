"""
Report Generator
Generates Markdown REPORT.md with evidence.csv appendix.
"""
import sys
import json
import csv
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from jinja2 import Template

# Add parent directory to path to import schemas
sys.path.insert(0, str(Path(__file__).parent.parent))

from schemas.evidence_item import EvidenceItem


class ReportGenerator:
    """
    Report Generator creates comprehensive markdown reports and CSV data exports.
    """
    
    def __init__(self, template_path: str = "templates/report_template.md", use_rq_template: bool = False):
        """
        Initialize the Report Generator.
        
        Args:
            template_path: Path to Jinja2 template file
            use_rq_template: If True, use RQ-driven template
        """
        if use_rq_template:
            template_path = "templates/report_rq_template.md"
        self.template_path = Path(template_path)
        self.template = self._load_template()
        self.use_rq_template = use_rq_template
    
    def _load_template(self) -> Template:
        """Load the Jinja2 template."""
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template not found: {self.template_path}")
        
        with open(self.template_path, 'r') as f:
            template_content = f.read()
        
        return Template(template_content)
    
    def generate_report(
        self,
        synthesis_results: Dict[str, Any],
        evidence_items: List[EvidenceItem],
        output_path: str = "REPORT.md"
    ) -> str:
        """
        Generate the markdown report.
        
        Args:
            synthesis_results: Results from synthesizer agent
            evidence_items: List of all evidence items
            output_path: Path to save the report
            
        Returns:
            Path to generated report
        """
        print("\nGenerating report...")
        
        # Prepare template context
        context = self._prepare_context(synthesis_results, evidence_items)
        
        # Render template
        report_content = self.template.render(**context)
        
        # Save report
        output_file = Path(output_path)
        with open(output_file, 'w') as f:
            f.write(report_content)
        
        print(f"✓ Report generated: {output_path}")
        
        return str(output_file)
    
    def _prepare_context(
        self,
        synthesis_results: Dict[str, Any],
        evidence_items: List[EvidenceItem]
    ) -> Dict[str, Any]:
        """
        Prepare context for template rendering.
        
        Args:
            synthesis_results: Synthesis results dictionary
            evidence_items: List of evidence items
            
        Returns:
            Context dictionary for template
        """
        # Check if using RQ-driven synthesis
        if "rq1" in synthesis_results:
            # RQ-driven context (new format)
            from datetime import datetime
            context = {
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "totals": synthesis_results.get("totals", {}),
                "exec_decisions": synthesis_results.get("exec_decisions", {}),
                "rq1": synthesis_results.get("rq1", {}),
                "rq2": synthesis_results.get("rq2", {}),
                "rq3": synthesis_results.get("rq3", {}),
                "rq4": synthesis_results.get("rq4", {}),
                "rq5": synthesis_results.get("rq5", {}),
                "blueprint": synthesis_results.get("blueprint", {}),
                "qa": synthesis_results.get("qa", {})
            }
            return context
        
        # Legacy context (old format)
        # Get unique sources
        sources = list(synthesis_results.get("sources_analyzed", {}).keys())
        sources_str = ", ".join(s.title() for s in sources)
        
        # Count classifications
        segments = set(item.segment for item in evidence_items if item.segment)
        moments = set(item.moment for item in evidence_items if item.moment)
        jobs = set(item.job for item in evidence_items if item.job)
        themes = set(theme for item in evidence_items for theme in item.themes)
        
        context = {
            "research_topic": synthesis_results.get("research_topic", "Billboard-style soccer player rankings app - product de-risking research"),
            "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_items": synthesis_results.get("total_items", 0),
            "sources": sources_str,
            "sources_analyzed": synthesis_results.get("sources_analyzed", {}),
            "segment_insights": synthesis_results.get("segment_insights", {}),
            "moment_insights": synthesis_results.get("moment_insights", {}),
            "job_insights": synthesis_results.get("job_insights", {}),
            "theme_clusters": synthesis_results.get("theme_clusters", {}),
            "sentiment_analysis": synthesis_results.get("sentiment_analysis", {}),
            "top_evidence": synthesis_results.get("top_evidence", []),
            "recommendations": synthesis_results.get("recommendations", []),
            "top_recommendations": synthesis_results.get("recommendations", [])[:3],
            "segment_count": len(segments),
            "moment_count": len(moments),
            "job_count": len(jobs),
            "theme_count": len(themes)
        }
        
        return context
    
    def generate_csv(
        self,
        evidence_items: List[EvidenceItem],
        output_path: str = "evidence.csv"
    ) -> str:
        """
        Generate CSV file with all evidence items.
        
        Args:
            evidence_items: List of evidence items
            output_path: Path to save the CSV file
            
        Returns:
            Path to generated CSV
        """
        print("\nGenerating evidence CSV...")
        
        output_file = Path(output_path)
        
        # Define CSV columns
        fieldnames = [
            "id",
            "source",
            "source_type",
            "source_url",
            "title",
            "content",
            "author",
            "published_at",
            "collected_at",
            "engagement_total",
            "engagement_details",
            "segment",
            "moment",
            "job",
            "themes",
            "sentiment",
            "metadata"
        ]
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for item in evidence_items:
                row = {
                    "id": item.id,
                    "source": item.source,
                    "source_type": item.source_type,
                    "source_url": item.source_url,
                    "title": item.title or "",
                    "content": item.content,
                    "author": item.author or "",
                    "published_at": item.published_at.isoformat() if item.published_at else "",
                    "collected_at": item.collected_at.isoformat() if item.collected_at else "",
                    "engagement_total": item.engagement_metrics.get("total_engagement", 0),
                    "engagement_details": json.dumps(item.engagement_metrics),
                    "segment": item.segment or "",
                    "moment": item.moment or "",
                    "job": item.job or "",
                    "themes": ", ".join(item.themes),
                    "sentiment": item.sentiment or "",
                    "metadata": json.dumps(item.metadata)
                }
                writer.writerow(row)
        
        print(f"✓ CSV generated: {output_path}")
        print(f"  Total rows: {len(evidence_items)}")
        
        return str(output_file)
    
    def generate_full_report(
        self,
        synthesis_path: str = "data/synthesis_results.json",
        evidence_path: str = "data/tagged_evidence.json",
        report_path: str = "REPORT.md",
        csv_path: str = "evidence.csv"
    ):
        """
        Generate both markdown report and CSV file.
        
        Args:
            synthesis_path: Path to synthesis results JSON
            evidence_path: Path to tagged evidence JSON
            report_path: Output path for markdown report
            csv_path: Output path for CSV file
        """
        # Load synthesis results
        with open(synthesis_path, 'r') as f:
            synthesis_results = json.load(f)
        
        # Load evidence items
        with open(evidence_path, 'r') as f:
            evidence_data = json.load(f)
        
        evidence_items = [EvidenceItem(**item) for item in evidence_data]
        
        # Generate report and CSV
        self.generate_report(synthesis_results, evidence_items, report_path)
        self.generate_csv(evidence_items, csv_path)
        
        print("\n✓ Full report generation complete!")
        print(f"  - Markdown report: {report_path}")
        print(f"  - Evidence CSV: {csv_path}")


def main():
    """
    Main function to demonstrate the Report Generator.
    """
    print("Starting Report Generator...")
    
    # Check if required files exist
    synthesis_path = Path("data/synthesis_results.json")
    evidence_path = Path("data/tagged_evidence.json")
    
    if not synthesis_path.exists():
        print("Error: Synthesis results not found. Run synthesizer_agent.py first.")
        return
    
    if not evidence_path.exists():
        print("Error: Tagged evidence not found. Run tagger_agent.py first.")
        return
    
    # Generate report
    generator = ReportGenerator()
    generator.generate_full_report()
    
    print("\nReport generation complete!")


if __name__ == "__main__":
    main()
