'''Quick Financial Analysis'''
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
from parser import SECFilingParser, MockSECFetcher

# Fetch and parse
fetcher = MockSECFetcher()
filing = fetcher.fetch_filing('AAPL', '10-K')

parser = SECFilingParser()
results = parser.parse_filing(filing, 'AAPL', '10-K')

# Show report
print(parser.generate_report(results))
