# Agentic AI Market-Research System

A comprehensive market research pipeline for analyzing soccer equipment and training preferences using AI agents.

## Overview

This system implements a complete agentic workflow for market research, featuring specialized agents that work together to collect, analyze, and synthesize data from multiple sources including Reddit, YouTube, app stores, and media outlets.

## System Architecture

The system consists of five specialized agents:

1. **Planner Agent** (`scripts/planner_agent.py`)
   - Generates comprehensive research plans with quotas, sources, and stop conditions
   - Configures data collection parameters

2. **Collector Agent** (`scripts/collector_agent.py`)
   - Fetches data from multiple sources (Reddit, YouTube, app stores, media)
   - Supports both real API integration and mock data for testing

3. **Extractor Agent** (`scripts/extractor_agent.py`)
   - Normalizes collected data into standardized EvidenceItem schema
   - Extracts engagement metrics and metadata

4. **Tagger Agent** (`scripts/tagger_agent.py`)
   - Classifies data into segments, moments, jobs-to-be-done, themes, and sentiment
   - Uses keyword-based rules and pattern matching

5. **Synthesizer Agent** (`scripts/synthesizer_agent.py`)
   - Aggregates evidence and clusters themes
   - Generates product recommendations based on analysis

## Project Structure

```
soccer-research-workflow/
├── main.py                      # Main pipeline orchestrator
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── REPORT.md                    # Generated research report (output)
├── evidence.csv                 # Complete evidence dataset (output)
├── schemas/
│   ├── __init__.py
│   └── evidence_item.py         # Pydantic schemas (EvidenceItem, ResearchPlan)
├── scripts/
│   ├── planner_agent.py         # Research plan generation
│   ├── collector_agent.py       # Data collection
│   ├── extractor_agent.py       # Data normalization
│   ├── tagger_agent.py          # Data classification
│   ├── synthesizer_agent.py     # Analysis and synthesis
│   └── report_generator.py      # Report generation
├── templates/
│   └── report_template.md       # Jinja2 template for reports
└── data/                        # Intermediate data files (generated)
    ├── research_plan.json
    ├── raw_collected_data.json
    ├── evidence_items.json
    ├── tagged_evidence.json
    └── synthesis_results.json
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/shashanknx/soccer-research-workflow.git
cd soccer-research-workflow
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start (Mock Data)

Run the complete pipeline with mock data:

```bash
python main.py
```

This will:
- Generate a research plan
- Collect mock data from various sources
- Normalize and tag the data
- Perform synthesis and analysis
- Generate `REPORT.md` and `evidence.csv`

### Run Individual Agents

You can also run agents individually:

```bash
# 1. Generate research plan
python scripts/planner_agent.py

# 2. Collect data
python scripts/collector_agent.py

# 3. Extract and normalize
python scripts/extractor_agent.py

# 4. Tag and classify
python scripts/tagger_agent.py

# 5. Synthesize and analyze
python scripts/synthesizer_agent.py

# 6. Generate report
python scripts/report_generator.py
```

### Use Real Data Sources

To use real API data (requires API credentials):

```bash
python main.py --real-data
```

**Note:** Real data mode requires setting up API credentials for Reddit (PRAW), YouTube, etc. Create a `.env` file with your API keys.

## Output Files

### REPORT.md

A comprehensive Markdown report containing:
- Executive summary
- Data collection overview
- Segment analysis
- User moments and jobs-to-be-done
- Theme clustering
- Sentiment analysis
- Top evidence items
- Product recommendations

### evidence.csv

A CSV file with all collected and tagged evidence items, including:
- Source information
- Content and metadata
- Engagement metrics
- Classifications (segment, moment, job, themes, sentiment)

## Schemas

### EvidenceItem

Normalized schema for all collected data:
- Unique ID and source information
- Content (title, text, author)
- Timestamps (collected, published)
- Engagement metrics (upvotes, views, likes, etc.)
- Tags (segment, moment, job, themes, sentiment)
- Platform-specific metadata

### ResearchPlan

Configuration for data collection:
- Research topic and target segments
- Source configurations
- Collection quotas
- Stop conditions
- Keywords and filters

## Customization

### Add New Sources

Extend `CollectorAgent` to add new data sources:

```python
def collect_new_source(self):
    # Implement data collection logic
    items = []
    # ...
    return items
```

### Modify Classification Rules

Update tagging rules in `TaggerAgent`:

```python
self.segment_rules = {
    "new_segment": ["keyword1", "keyword2", ...]
}
```

### Customize Report Template

Edit `templates/report_template.md` to modify report structure and content.

## Dependencies

- **pydantic**: Schema validation
- **requests**: HTTP requests
- **praw**: Reddit API
- **beautifulsoup4**: Web scraping
- **pandas**: Data manipulation
- **Jinja2**: Template rendering
- **python-dotenv**: Environment configuration

## Development

### Testing

Each agent can be tested independently by running its script:

```bash
python scripts/planner_agent.py
```

### Mock Data

By default, the system uses mock data for testing. This allows you to:
- Test the complete pipeline without API credentials
- Develop and debug agents quickly
- Demonstrate the system functionality

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Contact

For questions or support, please open an issue in the GitHub repository.
