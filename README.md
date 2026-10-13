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

The demo parses a bundled sample 10-K (`MockSECFetcher`). There is no live EDGAR client; pass in filing text you already have.

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

- `src/parser.py` - Regex metric extraction, lexicon sentiment, entity and risk-factor extraction
- `src/visualizations.py` - Chart generation
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

> _Note: sentiment lexicons drift over time as financial vocabulary evolves. The bundled lexicon is a snapshot — for production use, plan to refresh at least annually against recent MD&A samples._
