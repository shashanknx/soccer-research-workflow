# Market Research Report: Billboard-style soccer player rankings app — Product De-risking Research

**Generated on:** {{ generated_at }}

---

## Executive Summary

**Purpose:** De-risk product requirements for a Billboard-style player rankings app (rank, follow, compare, share) targeting 18–30 year-old fans.

**Primary decisions this report must unlock:**
1) Primary habit moment
2) Trust model requirements (explainability + transparency)
3) Share artifact specification (growth loop)
4) V1 wedge segment
5) Do-not-build list (churn drivers)

**Dataset:**
- Total evidence items: {{ totals.total_items }}
- Sources: {{ totals.sources | join(", ") }}
- Time window: {{ totals.time_window }}

### EXECUTIVE DECISIONS (REQUIRED):

- **Primary habit moment:** {{ exec_decisions.primary_habit_moment }}
- **Trust model:** {{ exec_decisions.trust_model }}
- **Share artifact:** {{ exec_decisions.share_artifact }}
- **V1 wedge segment:** {{ exec_decisions.v1_wedge }}
- **Do-not-build list:** {{ exec_decisions.do_not_build }}

---

## Data Collection Overview

| Source | Items | % |
|--------|------:|--:|
{% for s in totals.source_breakdown %}
| {{ s.source }} | {{ s.count }} | {{ s.percentage }}% |
{% endfor %}

**Coverage quality:**
- Reddit: {{ totals.coverage.reddit }} items
- YouTube: {{ totals.coverage.youtube }} items
- App Reviews: {{ totals.coverage.app_reviews }} items
- Media Articles: {{ totals.coverage.media }} items

---

## RQ1 — Where do fans already go during the moments we want to own?

**Decision unlocked:** Primary habit moment + notification strategy

### Decision Table

| Moment | Platform(s) today | Content type | Player-centric? | Ranking-like? | Product implication |
|--------|-------------------|--------------|-----------------|---------------|---------------------|
{% for row in rq1.decision_table %}
| {{ row.moment }} | {{ row.platforms }} | {{ row.content_type }} | {{ row.player_centric }} | {{ row.ranking_like }} | {{ row.implication }} |
{% endfor %}

### Findings

{% for finding in rq1.findings %}
- {{ finding }}
{% endfor %}

### DECISION STATEMENT

{{ rq1.decision }}

### Confidence and Open Risks

- **Confidence:** {{ rq1.confidence }}
- **Known uncertainties:** {{ rq1.risks }}

### Evidence Snapshot

{% for item in rq1.evidence %}
{{ loop.index }}. **{{ item.title }}** ({{ item.source }}) — {{ item.quote }}  
   _Implication: {{ item.implication }}_
{% endfor %}

---

## RQ2 — What makes rankings feel credible vs annoying?

**Decision unlocked:** Trust + explainability requirements

### Decision Table

| Trust trigger | Evidence source | Frequency | User quote | Design requirement |
|---------------|-----------------|-----------|------------|-------------------|
{% for row in rq2.decision_table %}
| {{ row.trigger }} | {{ row.source }} | {{ row.frequency }} | {{ row.quote }} | {{ row.requirement }} |
{% endfor %}

### Findings

{% for finding in rq2.findings %}
- {{ finding }}
{% endfor %}

### DECISION STATEMENT

{{ rq2.decision }}

### Confidence and Open Risks

- **Confidence:** {{ rq2.confidence }}
- **Known uncertainties:** {{ rq2.risks }}

### Evidence Snapshot

{% for item in rq2.evidence %}
{{ loop.index }}. **{{ item.title }}** ({{ item.source }}) — {{ item.quote }}  
   _Implication: {{ item.implication }}_
{% endfor %}

---

## RQ3 — What content do fans actually share?

**Decision unlocked:** Share artifact specification / growth loop

### Decision Table

| Content type | Share platform | Share trigger | Virality signal | Growth implication |
|--------------|----------------|---------------|-----------------|-------------------|
{% for row in rq3.decision_table %}
| {{ row.content_type }} | {{ row.platform }} | {{ row.trigger }} | {{ row.virality }} | {{ row.implication }} |
{% endfor %}

### Findings

{% for finding in rq3.findings %}
- {{ finding }}
{% endfor %}

### DECISION STATEMENT

{{ rq3.decision }}

### Confidence and Open Risks

- **Confidence:** {{ rq3.confidence }}
- **Known uncertainties:** {{ rq3.risks }}

### Evidence Snapshot

{% for item in rq3.evidence %}
{{ loop.index }}. **{{ item.title }}** ({{ item.source }}) — {{ item.quote }}  
   _Implication: {{ item.implication }}_
{% endfor %}

---

## RQ4 — Which segment should V1 optimize for?

**Decision unlocked:** V1 wedge segment

### Decision Table

| Segment | Size signal | Engagement | Pain point | Substitutes | V1 fit score |
|---------|-------------|------------|------------|-------------|--------------|
{% for row in rq4.decision_table %}
| {{ row.segment }} | {{ row.size }} | {{ row.engagement }} | {{ row.pain }} | {{ row.substitutes }} | {{ row.fit_score }} |
{% endfor %}

### Findings

{% for finding in rq4.findings %}
- {{ finding }}
{% endfor %}

### DECISION STATEMENT

{{ rq4.decision }}

### Confidence and Open Risks

- **Confidence:** {{ rq4.confidence }}
- **Known uncertainties:** {{ rq4.risks }}

### Evidence Snapshot

{% for item in rq4.evidence %}
{{ loop.index }}. **{{ item.title }}** ({{ item.source }}) — {{ item.quote }}  
   _Implication: {{ item.implication }}_
{% endfor %}

---

## RQ5 — What causes churn even if users like rankings?

**Decision unlocked:** Do-not-build list

### Decision Table

| Churn driver | Evidence count | User signal | Avoidance strategy |
|--------------|----------------|-------------|--------------------|
{% for row in rq5.decision_table %}
| {{ row.driver }} | {{ row.count }} | {{ row.signal }} | {{ row.strategy }} |
{% endfor %}

### Findings

{% for finding in rq5.findings %}
- {{ finding }}
{% endfor %}

### DECISION STATEMENT

{{ rq5.decision }}

### Confidence and Open Risks

- **Confidence:** {{ rq5.confidence }}
- **Known uncertainties:** {{ rq5.risks }}

### Evidence Snapshot

{% for item in rq5.evidence %}
{{ loop.index }}. **{{ item.title }}** ({{ item.source }}) — {{ item.quote }}  
   _Implication: {{ item.implication }}_
{% endfor %}

---

## V1 Product Blueprint

### Core Loop

{{ blueprint.core_loop }}

### Surfaces & Mechanics

| Surface | Primary mechanic | Target segment | Rationale |
|---------|------------------|----------------|-----------|
{% for row in blueprint.surfaces %}
| {{ row.surface }} | {{ row.mechanic }} | {{ row.segment }} | {{ row.rationale }} |
{% endfor %}

### Do-Not-Build List (V1 Exclusions)

{% for item in blueprint.do_not_build %}
- **{{ item.feature }}** — {{ item.rationale }}
{% endfor %}

---

## Appendix: Quality Assurance

### Coverage Validation

- Reddit posts + comments: {{ qa.reddit_coverage }} (target: 180)
- YouTube videos: {{ qa.youtube_coverage }} (target: 30)
- App reviews: {{ qa.app_review_coverage }} (target: 300)
- Media articles: {{ qa.media_coverage }} (target: 20)

### Evidence Quality

- Total evidence items analyzed: {{ qa.total_items }}
- Items dropped (out of scope): {{ qa.dropped_count }}
- Deduplication rate: {{ qa.dedup_rate }}%

### Validation Checklist

{% for check in qa.validation_checks %}
- [{{ 'x' if check.passed else ' ' }}] {{ check.name }}
{% endfor %}

---

## Appendix: Complete Evidence Dataset

A complete CSV file containing all {{ totals.total_items }} evidence items with tags and classifications is available as `evidence.csv`.

### CSV Columns

- **id**: Unique identifier
- **source**: Data source platform
- **source_type**: Type of content
- **title**: Content title
- **content**: Main text content
- **author**: Content author
- **published_at**: Publication timestamp
- **collected_at**: Collection timestamp
- **engagement_total**: Total engagement score
- **segment**: User segment classification
- **moment**: User moment classification
- **job**: Job-to-be-done classification
- **themes**: Identified themes (comma-separated)
- **sentiment**: Sentiment classification
- **source_url**: Original URL

---

*This report was generated by the Agentic AI Market-Research System — RQ-Driven Decision Framework*
