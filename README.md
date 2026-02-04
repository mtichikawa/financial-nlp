# Financial Report NLP Parser

Automated extraction and analysis of financial data from SEC filings.

## Features

- **Metric Extraction** - Revenue, earnings, assets, liabilities
- **Sentiment Analysis** - MD&A section analysis
- **Entity Recognition** - Companies, dates, amounts
- **Risk Factor Detection** - Automated risk identification
- **Financial Ratios** - Profit margin, ROA, debt/equity
- **Visualizations** - Charts and dashboards

## Quick Start

```bash
pip install -r requirements.txt
python examples/quick_analysis.py
```

## Usage

```python
from src.parser import SECFilingParser

parser = SECFilingParser()
results = parser.parse_filing(filing_text, ticker='AAPL', filing_type='10-K')

# Get metrics
print(results['metrics'])

# Get sentiment
print(results['sentiment'])

# Generate report
report = parser.generate_report(results)
```

## Code Structure

- `src/parser.py` (550+ lines) - Complete parsing system
- `src/visualizations.py` (300+ lines) - Chart generation
- `examples/quick_analysis.py` - Demo script

## What's Extracted

- Revenue, net income, EPS, assets, liabilities
- Profit margins, ROA, debt ratios
- Sentiment scores (positive/negative/uncertainty)
- Risk factors
- Key entities (companies, dates, amounts)

## What I Learned

- SEC filing structure and formats
- Financial NLP and domain-specific extraction
- Regex patterns for financial data
- Sentiment analysis for financial text

Contact: Mike Ichikawa - projects.ichikawa@gmail.com

# 2026-02-01
# 2026-02-01
# 2026-02-04