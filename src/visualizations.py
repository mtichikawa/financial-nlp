'''
Financial Data Visualization
'''

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import Dict, List


class FinancialVisualizer:
    '''Visualize financial analysis results'''
    
    def __init__(self, output_dir: str = 'assets'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def plot_metrics_comparison(self, 
                               metrics: Dict[str, float],
                               title: str = 'Financial Metrics',
                               save: bool = True) -> str:
        '''Plot financial metrics as bar chart'''
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Filter and sort metrics
        sorted_metrics = sorted(metrics.items(), key=lambda x: x[1], reverse=True)
        names = [m[0].replace('_', ' ').title() for m, v in sorted_metrics]
        values = [v for m, v in sorted_metrics]
        
        colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(names)))
        bars = ax.barh(names, values, color=colors, edgecolor='black', linewidth=1.5)
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2,
                   f'${width:,.0f}M',
                   ha='left', va='center', fontsize=10, fontweight='bold')
        
        ax.set_xlabel('Amount (Millions)', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        
        if save:
            filepath = self.output_dir / 'metrics_comparison.png'
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            return str(filepath)
        else:
            plt.show()
            return None
            
    def plot_sentiment_breakdown(self,
                                sentiment: Dict,
                                save: bool = True) -> str:
        '''Visualize sentiment analysis'''
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Counts pie chart
        counts = sentiment['counts']
        colors = ['#2ecc71', '#e74c3c', '#f39c12']
        ax1.pie(counts.values(), labels=counts.keys(), autopct='%1.1f%%',
               colors=colors, startangle=90)
        ax1.set_title('Sentiment Word Distribution', fontsize=12, fontweight='bold')
        
        # Scores bar chart
        scores = sentiment['scores']
        categories = list(scores.keys())
        values = list(scores.values())
        
        ax2.bar(categories, values, color=colors, edgecolor='black', linewidth=2)
        ax2.set_ylabel('Score', fontsize=11)
        ax2.set_title('Sentiment Scores', fontsize=12, fontweight='bold')
        ax2.set_ylim(0, max(values) * 1.2 if values else 1)
        ax2.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for i, v in enumerate(values):
            ax2.text(i, v + 0.01, f'{v:.2f}', 
                    ha='center', va='bottom', fontweight='bold')
        
        plt.suptitle(f'Overall Sentiment: {sentiment["sentiment_label"]}',
                    fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        if save:
            filepath = self.output_dir / 'sentiment_analysis.png'
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            return str(filepath)
        else:
            plt.show()
            return None
            
    def plot_financial_ratios(self,
                             ratios: Dict[str, float],
                             save: bool = True) -> str:
        '''Visualize financial ratios'''
        fig, ax = plt.subplots(figsize=(10, 6))
        
        names = [r.replace('_', ' ').title() for r in ratios.keys()]
        values = list(ratios.values())
        
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12'][:len(names)]
        bars = ax.bar(names, values, color=colors, edgecolor='black', linewidth=2)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height,
                   f'{height:.2f}',
                   ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        ax.set_ylabel('Ratio Value', fontsize=12)
        ax.set_title('Key Financial Ratios', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        plt.xticks(rotation=15, ha='right')
        plt.tight_layout()
        
        if save:
            filepath = self.output_dir / 'financial_ratios.png'
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            return str(filepath)
        else:
            plt.show()
            return None
            
    def create_dashboard(self,
                        parsed_data: Dict,
                        save: bool = True) -> str:
        '''Create comprehensive analysis dashboard'''
        fig = plt.figure(figsize=(16, 10))
        
        # 2x2 layout
        ax1 = plt.subplot(2, 2, 1)
        ax2 = plt.subplot(2, 2, 2)
        ax3 = plt.subplot(2, 2, 3)
        ax4 = plt.subplot(2, 2, 4)
        
        # 1. Top metrics
        metrics = parsed_data.get('metrics', {})
        if metrics:
            top_metrics = dict(list(sorted(metrics.items(), key=lambda x: x[1], reverse=True))[:5])
            names = [m.replace('_', ' ').title() for m in top_metrics.keys()]
            values = list(top_metrics.values())
            
            ax1.barh(names, values, color='steelblue', edgecolor='black')
            ax1.set_xlabel('Amount ($M)')
            ax1.set_title('Top Financial Metrics', fontweight='bold')
            ax1.grid(axis='x', alpha=0.3)
            
        # 2. Sentiment
        sentiment = parsed_data.get('sentiment', {})
        if sentiment and 'counts' in sentiment:
            counts = sentiment['counts']
            ax2.pie(counts.values(), labels=counts.keys(), autopct='%1.1f%%',
                   colors=['#2ecc71', '#e74c3c', '#f39c12'])
            ax2.set_title('Sentiment Distribution', fontweight='bold')
            
        # 3. Ratios
        ratios = parsed_data.get('ratios', {})
        if ratios:
            names = [r.replace('_', ' ').title() for r in ratios.keys()]
            values = list(ratios.values())
            ax3.bar(names, values, color='coral', edgecolor='black')
            ax3.set_ylabel('Ratio')
            ax3.set_title('Financial Ratios', fontweight='bold')
            ax3.tick_params(axis='x', rotation=15)
            ax3.grid(axis='y', alpha=0.3)
            
        # 4. Summary text
        ax4.axis('off')
        summary = [
            f"Company: {parsed_data.get('ticker', 'N/A')}",
            f"Filing: {parsed_data.get('filing_type', 'N/A')}",
            "",
            "Key Findings:",
            f"• Sentiment: {sentiment.get('sentiment_label', 'N/A')}",
            f"• Metrics Extracted: {len(metrics)}",
            f"• Ratios Calculated: {len(ratios)}",
            f"• Risk Factors: {len(parsed_data.get('risks', []))}",
        ]
        
        ax4.text(0.1, 0.9, '\n'.join(summary),
                verticalalignment='top',
                fontfamily='monospace',
                fontsize=12)
        
        plt.suptitle('Financial Analysis Dashboard',
                    fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        if save:
            filepath = self.output_dir / 'analysis_dashboard.png'
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            return str(filepath)
        else:
            plt.show()
            return None


def demo():
    '''Demo visualizations'''
    print('Financial Visualization Demo')
    print('=' * 50)
    
    # Mock data
    metrics = {
        'revenue': 2500,
        'net_income': 450,
        'gross_profit': 1200,
        'total_assets': 5600,
        'cash': 800
    }
    
    sentiment = {
        'counts': {'positive': 45, 'negative': 18, 'uncertainty': 12},
        'scores': {'positive': 0.6, 'negative': 0.24, 'uncertainty': 0.16},
        'sentiment_label': 'Positive'
    }
    
    ratios = {
        'profit_margin': 18.0,
        'return_on_assets': 8.04,
        'debt_to_equity': 0.6
    }
    
    viz = FinancialVisualizer()
    
    print('\nGenerating visualizations...')
    viz.plot_metrics_comparison(metrics)
    print('  ✅ Metrics chart')
    
    viz.plot_sentiment_breakdown(sentiment)
    print('  ✅ Sentiment analysis')
    
    viz.plot_financial_ratios(ratios)
    print('  ✅ Financial ratios')
    
    parsed_data = {
        'ticker': 'AAPL',
        'filing_type': '10-K',
        'metrics': metrics,
        'sentiment': sentiment,
        'ratios': ratios,
        'risks': ['Risk 1', 'Risk 2', 'Risk 3']
    }
    viz.create_dashboard(parsed_data)
    print('  ✅ Dashboard')
    
    print('\n✅ All visualizations saved!')


if __name__ == '__main__':
    demo()
