'''Quick Financial Analysis'''
import sys
sys.path.append('../src')
from parser import SECFilingParser, MockSECFetcher

# Fetch and parse
fetcher = MockSECFetcher()
filing = fetcher.fetch_filing('AAPL', '10-K')

parser = SECFilingParser()
results = parser.parse_filing(filing, 'AAPL', '10-K')

# Show report
print(parser.generate_report(results))
