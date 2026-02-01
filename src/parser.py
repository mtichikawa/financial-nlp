'''
Financial Report NLP Parser
Extract and analyze financial data from SEC filings
'''

import re
import json
from typing import Dict, List, Tuple, Optional
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET


class FinancialMetricExtractor:
    '''Extract financial metrics from text'''
    
    def __init__(self):
        self.patterns = self._load_patterns()
        
    def _load_patterns(self) -> Dict[str, re.Pattern]:
        '''Compiled regex patterns for financial metrics'''
        return {
            'revenue': re.compile(
                r'(?:revenue|sales|net\s+sales).*?[\$\s]+([\d,\.]+)\s*(?:million|billion)?',
                re.IGNORECASE
            ),
            'net_income': re.compile(
                r'net\s+income.*?[\$\s]+([\d,\.]+)\s*(?:million|billion)?',
                re.IGNORECASE
            ),
            'earnings_per_share': re.compile(
                r'earnings\s+per\s+share.*?[\$\s]+([\d,\.]+)',
                re.IGNORECASE
            ),
            'gross_profit': re.compile(
                r'gross\s+profit.*?[\$\s]+([\d,\.]+)\s*(?:million|billion)?',
                re.IGNORECASE
            ),
            'operating_income': re.compile(
                r'operating\s+income.*?[\$\s]+([\d,\.]+)\s*(?:million|billion)?',
                re.IGNORECASE
            ),
            'total_assets': re.compile(
                r'total\s+assets.*?[\$\s]+([\d,\.]+)\s*(?:million|billion)?',
                re.IGNORECASE
            ),
            'total_liabilities': re.compile(
                r'total\s+liabilities.*?[\$\s]+([\d,\.]+)\s*(?:million|billion)?',
                re.IGNORECASE
            ),
            'cash_and_equivalents': re.compile(
                r'cash\s+(?:and\s+)?(?:cash\s+)?equivalents.*?[\$\s]+([\d,\.]+)\s*(?:million|billion)?',
                re.IGNORECASE
            ),
            'stockholders_equity': re.compile(
                r'(?:stockholders|shareholders)\s+equity.*?[\$\s]+([\d,\.]+)\s*(?:million|billion)?',
                re.IGNORECASE
            )
        }
        
    def extract_metrics(self, text: str) -> Dict[str, float]:
        '''Extract all financial metrics from text'''
        metrics = {}
        
        for metric_name, pattern in self.patterns.items():
            match = pattern.search(text)
            if match:
                value_str = match.group(1).replace(',', '')
                try:
                    value = float(value_str)
                    
                    # Check for billion/million multiplier
                    context = text[max(0, match.start()-50):match.end()+20]
                    if 'billion' in context.lower():
                        value *= 1000  # Convert to millions
                        
                    metrics[metric_name] = value
                except ValueError:
                    pass
                    
        return metrics
        
    def calculate_ratios(self, metrics: Dict[str, float]) -> Dict[str, float]:
        '''Calculate financial ratios from extracted metrics'''
        ratios = {}
        
        # Profit margin
        if 'net_income' in metrics and 'revenue' in metrics:
            if metrics['revenue'] > 0:
                ratios['profit_margin'] = (metrics['net_income'] / metrics['revenue']) * 100
                
        # Return on assets
        if 'net_income' in metrics and 'total_assets' in metrics:
            if metrics['total_assets'] > 0:
                ratios['return_on_assets'] = (metrics['net_income'] / metrics['total_assets']) * 100
                
        # Debt to equity
        if 'total_liabilities' in metrics and 'stockholders_equity' in metrics:
            if metrics['stockholders_equity'] > 0:
                ratios['debt_to_equity'] = metrics['total_liabilities'] / metrics['stockholders_equity']
                
        # Current ratio (simplified - needs current assets/liabilities)
        if 'cash_and_equivalents' in metrics and 'total_liabilities' in metrics:
            if metrics['total_liabilities'] > 0:
                ratios['cash_ratio'] = metrics['cash_and_equivalents'] / metrics['total_liabilities']
                
        return ratios


class SentimentAnalyzer:
    '''Analyze sentiment in financial text (MD&A, risk factors)'''
    
    def __init__(self):
        self.lexicons = self._load_lexicons()
        
    def _load_lexicons(self) -> Dict[str, List[str]]:
        '''Financial sentiment lexicons'''
        return {
            'positive': [
                'growth', 'increase', 'improved', 'strong', 'positive',
                'gain', 'profit', 'success', 'opportunity', 'favorable',
                'expand', 'efficient', 'excellent', 'robust', 'momentum',
                'outperform', 'exceeded', 'innovative', 'competitive'
            ],
            'negative': [
                'decline', 'decrease', 'loss', 'weak', 'negative',
                'risk', 'challenge', 'concern', 'adverse', 'difficult',
                'uncertainty', 'volatile', 'impairment', 'litigation',
                'default', 'breach', 'deteriorate', 'unsuccessful'
            ],
            'uncertainty': [
                'may', 'could', 'might', 'uncertain', 'estimate',
                'believe', 'expect', 'anticipate', 'subject to',
                'depends', 'varies', 'fluctuate'
            ]
        }
        
    def analyze_text(self, text: str) -> Dict:
        '''Analyze sentiment of text'''
        text_lower = text.lower()
        words = text_lower.split()
        
        counts = {
            'positive': 0,
            'negative': 0,
            'uncertainty': 0
        }
        
        # Count sentiment words
        for category, lexicon in self.lexicons.items():
            for word in lexicon:
                counts[category] += text_lower.count(word)
                
        # Calculate scores
        total = sum(counts.values())
        if total == 0:
            scores = {cat: 0.0 for cat in counts.keys()}
            overall = 0.5
        else:
            scores = {cat: count/total for cat, count in counts.items()}
            overall = (scores['positive'] - scores['negative'] + 1) / 2  # Normalize to 0-1
            
        return {
            'counts': counts,
            'scores': scores,
            'overall_sentiment': overall,
            'sentiment_label': self._label_sentiment(overall)
        }
        
    def _label_sentiment(self, score: float) -> str:
        '''Convert score to label'''
        if score > 0.6:
            return 'Positive'
        elif score < 0.4:
            return 'Negative'
        else:
            return 'Neutral'


class EntityExtractor:
    '''Extract named entities (companies, people, locations)'''
    
    def __init__(self):
        self.patterns = self._load_patterns()
        
    def _load_patterns(self) -> Dict[str, re.Pattern]:
        '''Entity extraction patterns'''
        return {
            'company': re.compile(r'\b(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:Inc\.|Corp\.|LLC|Ltd\.)', re.IGNORECASE),
            'date': re.compile(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}', re.IGNORECASE),
            'money': re.compile(r'\$[\d,]+(?:\.\d{2})?'),
            'percentage': re.compile(r'\d+(?:\.\d+)?%')
        }
        
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        '''Extract all entities from text'''
        entities = {}
        
        for entity_type, pattern in self.patterns.items():
            matches = pattern.findall(text)
            entities[entity_type] = list(set(matches))  # Unique matches
            
        return entities


class SECFilingParser:
    '''Complete SEC filing parser'''
    
    def __init__(self):
        self.metric_extractor = FinancialMetricExtractor()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.entity_extractor = EntityExtractor()
        
    def parse_filing(self, text: str, ticker: str = None, filing_type: str = '10-K') -> Dict:
        '''
        Parse complete SEC filing
        
        Args:
            text: Filing text content
            ticker: Company ticker symbol
            filing_type: Type of filing (10-K, 10-Q, etc.)
            
        Returns:
            Parsed filing data
        '''
        print(f'\n📄 Parsing {filing_type} filing...')
        
        # Extract sections
        sections = self._extract_sections(text)
        
        # Extract financial metrics
        print('  Extracting financial metrics...')
        metrics = self.metric_extractor.extract_metrics(text)
        ratios = self.metric_extractor.calculate_ratios(metrics)
        
        # Analyze sentiment
        print('  Analyzing sentiment...')
        mda_text = sections.get('mda', text[:5000])  # First 5000 chars if no section
        sentiment = self.sentiment_analyzer.analyze_text(mda_text)
        
        # Extract entities
        print('  Extracting entities...')
        entities = self.entity_extractor.extract_entities(text)
        
        # Extract risk factors
        print('  Identifying risk factors...')
        risks = self._extract_risk_factors(text)
        
        result = {
            'ticker': ticker,
            'filing_type': filing_type,
            'parsed_date': datetime.now().isoformat(),
            'metrics': metrics,
            'ratios': ratios,
            'sentiment': sentiment,
            'entities': entities,
            'risks': risks,
            'sections': {k: len(v) for k, v in sections.items()}
        }
        
        print('  ✅ Parsing complete')
        
        return result
        
    def _extract_sections(self, text: str) -> Dict[str, str]:
        '''Extract major sections from filing'''
        sections = {}
        
        # MD&A section
        mda_match = re.search(
            r'(?:ITEM\s+7|Management.{0,50}Discussion).{0,100}?(.{1,10000}?)(?:ITEM\s+8|Financial\s+Statements)',
            text,
            re.IGNORECASE | re.DOTALL
        )
        if mda_match:
            sections['mda'] = mda_match.group(1)
            
        # Risk factors
        risk_match = re.search(
            r'(?:ITEM\s+1A|Risk\s+Factors).{0,100}?(.{1,10000}?)(?:ITEM\s+1B|ITEM\s+2)',
            text,
            re.IGNORECASE | re.DOTALL
        )
        if risk_match:
            sections['risk_factors'] = risk_match.group(1)
            
        return sections
        
    def _extract_risk_factors(self, text: str) -> List[str]:
        '''Extract risk factor sentences'''
        risk_keywords = ['risk', 'uncertainty', 'adverse', 'challenge', 'concern']
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        
        risks = []
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in risk_keywords):
                if len(sentence.strip()) > 50:  # Meaningful length
                    risks.append(sentence.strip())
                    
        return risks[:10]  # Top 10 risks
        
    def generate_report(self, parsed_data: Dict) -> str:
        '''Generate human-readable report'''
        report = []
        
        report.append(f"Financial Analysis Report")
        report.append(f"{'='*60}")
        report.append(f"Ticker: {parsed_data.get('ticker', 'N/A')}")
        report.append(f"Filing: {parsed_data.get('filing_type', 'N/A')}")
        report.append(f"")
        
        # Metrics
        if parsed_data.get('metrics'):
            report.append("Financial Metrics (in millions):")
            report.append("-" * 40)
            for metric, value in parsed_data['metrics'].items():
                report.append(f"  {metric.replace('_', ' ').title()}: ${value:,.1f}M")
            report.append("")
            
        # Ratios
        if parsed_data.get('ratios'):
            report.append("Financial Ratios:")
            report.append("-" * 40)
            for ratio, value in parsed_data['ratios'].items():
                if 'margin' in ratio or 'return' in ratio:
                    report.append(f"  {ratio.replace('_', ' ').title()}: {value:.2f}%")
                else:
                    report.append(f"  {ratio.replace('_', ' ').title()}: {value:.2f}")
            report.append("")
            
        # Sentiment
        if parsed_data.get('sentiment'):
            sent = parsed_data['sentiment']
            report.append("Sentiment Analysis:")
            report.append("-" * 40)
            report.append(f"  Overall: {sent['sentiment_label']} ({sent['overall_sentiment']:.2f})")
            report.append(f"  Positive mentions: {sent['counts']['positive']}")
            report.append(f"  Negative mentions: {sent['counts']['negative']}")
            report.append(f"  Uncertainty mentions: {sent['counts']['uncertainty']}")
            report.append("")
            
        # Top risks
        if parsed_data.get('risks'):
            report.append("Key Risk Factors:")
            report.append("-" * 40)
            for i, risk in enumerate(parsed_data['risks'][:3], 1):
                report.append(f"  {i}. {risk[:100]}...")
            report.append("")
            
        return "\n".join(report)
        
    def save_results(self, parsed_data: Dict, filepath: str):
        '''Save parsed results to JSON'''
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(parsed_data, f, indent=2)
            
        print(f'  ✅ Saved results to {filepath}')


class MockSECFetcher:
    '''Mock SEC filing fetcher (for demo)'''
    
    @staticmethod
    def fetch_filing(ticker: str, filing_type: str = '10-K') -> str:
        '''Generate mock SEC filing text'''
        return f"""
        UNITED STATES SECURITIES AND EXCHANGE COMMISSION
        Washington, D.C. 20549
        
        FORM {filing_type}
        ANNUAL REPORT PURSUANT TO SECTION 13 OR 15(d) 
        OF THE SECURITIES EXCHANGE ACT OF 1934
        
        For the fiscal year ended December 31, 2023
        
        {ticker} Corporation
        
        ITEM 1A. RISK FACTORS
        
        Our business faces significant risks and uncertainties. Market conditions may 
        adversely affect our operations. Competition in our industry remains intense.
        Regulatory changes could impact our business model. Economic downturns may 
        decrease demand for our products and services.
        
        ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS
        
        Overview
        
        We experienced strong growth in fiscal year 2023. Revenue increased 15% to 
        $2.5 billion, driven by robust demand in our core markets. Net income improved 
        to $450 million, reflecting operational efficiencies and favorable market conditions.
        
        Financial Highlights:
        - Revenue: $2,500 million
        - Gross Profit: $1,200 million  
        - Operating Income: $580 million
        - Net Income: $450 million
        - Earnings Per Share: $8.50
        - Total Assets: $5,600 million
        - Total Liabilities: $2,100 million
        - Stockholders Equity: $3,500 million
        - Cash and Equivalents: $800 million
        
        Our positive momentum continued throughout the year. We believe market 
        opportunities remain favorable. However, uncertainties in the global economy 
        may impact future results. We anticipate continued growth but remain cautious 
        about potential challenges.
        
        ITEM 8. FINANCIAL STATEMENTS
        [Financial statements would follow]
        """


def demo():
    '''Comprehensive demonstration'''
    print('Financial Report NLP Parser - Demo')
    print('=' * 60)
    
    # Fetch mock filing
    print('\n📥 Fetching SEC filing...')
    fetcher = MockSECFetcher()
    filing_text = fetcher.fetch_filing('AAPL', '10-K')
    print('  ✅ Filing retrieved')
    
    # Parse filing
    parser = SECFilingParser()
    results = parser.parse_filing(filing_text, ticker='AAPL', filing_type='10-K')
    
    # Generate report
    print('\n📊 Generating report...')
    report = parser.generate_report(results)
    print('\n' + report)
    
    # Save results
    parser.save_results(results, 'results/aapl_10k_analysis.json')
    
    print('\n✅ Demo complete!')


if __name__ == '__main__':
    demo()
