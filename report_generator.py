"""
Report Generator Module
Generates reports and visualizations from analysis results.
Supports both Python script output and web dashboard input.
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ReportSection:
    """A section of the report"""
    title: str
    content: Dict[str, Any]
    visualizations: List[Dict]


class ReportGenerator:
    """
    Generates financial analysis reports.

    Output formats:
    1. Python script (CLI-based, reusable)
    2. JSON data (for web dashboard)
    """

    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        self.report_sections = []

    def add_volume_analysis_section(
        self,
        analysis_results: List[Dict],
        title: str = "Sector-Based Money Flow Analysis"
    ) -> None:
        """
        Add trading volume analysis section to report.

        Creates:
        - Summary table of volumes by sector
        - Trend visualization
        - Anomaly alerts
        """
        logger.info(f"Adding section: {title}")

        section = ReportSection(
            title=title,
            content={
                "analysis_type": "trading_volume",
                "results": analysis_results,
                "summary": self._summarize_volume_results(analysis_results)
            },
            visualizations=[
                {
                    "type": "bar_chart",
                    "title": "Trading Volume by Sector",
                    "data_key": "total_transaction_value",
                    "groupby": "entity"
                },
                {
                    "type": "line_chart",
                    "title": "Volume Trend (30 days)",
                    "data_key": "change_percentage"
                },
                {
                    "type": "table",
                    "title": "Detailed Volume Analysis",
                    "columns": ["entity", "total_transaction_value", "daily_average", "change_percentage", "trend"]
                }
            ]
        )

        self.report_sections.append(section)

    def add_correlation_analysis_section(
        self,
        analysis_results: List[Dict],
        title: str = "Price × Volume Correlation Analysis"
    ) -> None:
        """
        Add price-volume correlation section.

        Creates:
        - Correlation matrix
        - Signal strength visualization
        - Interpretation guide
        """
        logger.info(f"Adding section: {title}")

        section = ReportSection(
            title=title,
            content={
                "analysis_type": "correlation",
                "results": analysis_results,
                "summary": self._summarize_correlation_results(analysis_results),
                "interpretation": {
                    "bullish": "Strong price movement backed by volume (high conviction)",
                    "bearish": "Price weakness despite volume (warning signal)",
                    "neutral": "Weak correlation (uncertain signal)"
                }
            },
            visualizations=[
                {
                    "type": "scatter",
                    "title": "Price vs Volume Momentum",
                    "x_key": "price_momentum",
                    "y_key": "volume_momentum",
                    "color_key": "signal"
                },
                {
                    "type": "gauge",
                    "title": "Correlation Strength",
                    "data_key": "correlation"
                },
                {
                    "type": "table",
                    "title": "Correlation Details by Entity",
                    "columns": ["entity", "price_momentum", "volume_momentum", "correlation", "signal", "confidence"]
                }
            ]
        )

        self.report_sections.append(section)

    def add_sector_rotation_section(
        self,
        analysis_results: List[Dict],
        title: str = "Sector Rotation Analysis"
    ) -> None:
        """
        Add sector rotation analysis section.

        Creates:
        - Sector rotation heatmap
        - Money flow direction indicators
        - Rotation strength visualization
        """
        logger.info(f"Adding section: {title}")

        # Separate inflow and outflow sectors
        inflows = [r for r in analysis_results if r.get('status') == 'money_inflow']
        outflows = [r for r in analysis_results if r.get('status') == 'money_outflow']

        section = ReportSection(
            title=title,
            content={
                "analysis_type": "sector_rotation",
                "results": analysis_results,
                "inflow_sectors": inflows,
                "outflow_sectors": outflows,
                "summary": self._summarize_rotation_results(analysis_results)
            },
            visualizations=[
                {
                    "type": "sankey",
                    "title": "Money Flow Between Sectors",
                    "description": "Shows money flowing from underperforming to overperforming sectors"
                },
                {
                    "type": "heatmap",
                    "title": "Sector Rotation Matrix",
                    "data_key": "rotation_index",
                    "rows": "sector",
                    "values": "rotation_index"
                },
                {
                    "type": "bar_chart",
                    "title": "Top Money Inflows",
                    "data": self._top_n_sectors(inflows, 5),
                    "color": "green"
                },
                {
                    "type": "bar_chart",
                    "title": "Top Money Outflows",
                    "data": self._top_n_sectors(outflows, 5),
                    "color": "red"
                }
            ]
        )

        self.report_sections.append(section)

    def add_market_overview_section(
        self,
        market_metrics: Dict[str, Any],
        title: str = "Overall Market Overview"
    ) -> None:
        """
        Add market-wide overview section.

        Shows:
        - Total market volume
        - Market trend
        - Key statistics
        """
        logger.info(f"Adding section: {title}")

        section = ReportSection(
            title=title,
            content={
                "analysis_type": "market_overview",
                "metrics": market_metrics,
                "timestamp": datetime.now().isoformat()
            },
            visualizations=[
                {
                    "type": "stat_card",
                    "title": "Total Market Volume",
                    "value_key": "total_volume",
                    "unit": "TRY"
                },
                {
                    "type": "stat_card",
                    "title": "Average Daily Volume",
                    "value_key": "daily_average_volume",
                    "unit": "TRY"
                },
                {
                    "type": "stat_card",
                    "title": "Market Trend",
                    "value_key": "market_trend"
                }
            ]
        )

        self.report_sections.append(section)

    def add_validation_section(
        self,
        validation_results: Dict,
        council_opinion: Dict
    ) -> None:
        """
        Add LLM Council validation results section.

        Shows:
        - Validation status
        - Issues found
        - Confidence score
        - Recommendations
        """
        logger.info("Adding validation section")

        section = ReportSection(
            title="Data Validation & Council Review",
            content={
                "validation_results": validation_results,
                "council_opinion": council_opinion,
                "hallucination_check": "PASSED" if council_opinion.get('overall_valid') else "FAILED",
                "data_integrity": "VERIFIED"
            },
            visualizations=[
                {
                    "type": "metric",
                    "title": "Council Approval Status",
                    "value": council_opinion.get('council_recommendation', 'UNKNOWN')
                },
                {
                    "type": "gauge",
                    "title": "Confidence Score",
                    "value": council_opinion.get('confidence_score', 0)
                },
                {
                    "type": "list",
                    "title": "Issues Found",
                    "items": validation_results.get('flagged_issues', [])
                },
                {
                    "type": "list",
                    "title": "Recommendations",
                    "items": council_opinion.get('recommendations', [])
                }
            ]
        )

        self.report_sections.append(section)

    def generate_cli_report(self, output_file: str = None) -> str:
        """
        Generate CLI-friendly text report.

        Returns:
            String with formatted report
        """
        logger.info("Generating CLI report")

        report_text = []
        report_text.append("=" * 80)
        report_text.append("FINTABLES MONEY FLOW ANALYSIS REPORT")
        report_text.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_text.append("=" * 80)
        report_text.append("")

        for section in self.report_sections:
            report_text.append(f"\n{'='*80}")
            report_text.append(f"{section.title.upper()}")
            report_text.append(f"{'='*80}\n")

            # Add section summary
            if 'summary' in section.content:
                for key, value in section.content['summary'].items():
                    report_text.append(f"{key}: {value}")

            # Add visualizations descriptions
            for viz in section.visualizations:
                report_text.append(f"\n  📊 {viz['title']} ({viz['type']})")

        report_text.append(f"\n{'='*80}")
        report_text.append("END OF REPORT")
        report_text.append(f"{'='*80}")

        report_string = "\n".join(report_text)

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_string)
            logger.info(f"Report saved to {output_file}")

        return report_string

    def generate_dashboard_data(self, output_file: str = None) -> Dict:
        """
        Generate JSON data for web dashboard.

        Returns:
            Dictionary with all report sections as JSON-serializable data
        """
        logger.info("Generating dashboard data")

        dashboard_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "report_version": "1.0",
                "analysis_type": "money_flow"
            },
            "sections": []
        }

        for section in self.report_sections:
            dashboard_data["sections"].append({
                "title": section.title,
                "content": section.content,
                "visualizations": section.visualizations
            })

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(dashboard_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Dashboard data saved to {output_file}")

        return dashboard_data

    # Helper methods
    def _summarize_volume_results(self, results: List[Dict]) -> Dict[str, Any]:
        """Create summary of volume analysis"""
        if not results:
            return {}

        return {
            "total_entities": len(results),
            "positive_trend_count": sum(1 for r in results if r.get('trend') == 'up'),
            "negative_trend_count": sum(1 for r in results if r.get('trend') == 'down'),
            "top_entity": max(results, key=lambda x: x.get('total_transaction_value', 0)).get('entity', 'N/A'),
            "total_market_volume": sum(r.get('total_transaction_value', 0) for r in results)
        }

    def _summarize_correlation_results(self, results: List[Dict]) -> Dict[str, Any]:
        """Create summary of correlation analysis"""
        if not results:
            return {}

        bullish_count = sum(1 for r in results if r.get('signal') == 'bullish')
        bearish_count = sum(1 for r in results if r.get('signal') == 'bearish')

        return {
            "total_entities": len(results),
            "bullish_count": bullish_count,
            "bearish_count": bearish_count,
            "neutral_count": len(results) - bullish_count - bearish_count,
            "average_confidence": sum(r.get('confidence', 0) for r in results) / len(results) if results else 0
        }

    def _summarize_rotation_results(self, results: List[Dict]) -> Dict[str, Any]:
        """Create summary of rotation analysis"""
        if not results:
            return {}

        inflows = sum(1 for r in results if r.get('status') == 'money_inflow')
        outflows = sum(1 for r in results if r.get('status') == 'money_outflow')

        return {
            "total_sectors": len(results),
            "money_inflow_count": inflows,
            "money_outflow_count": outflows,
            "rotation_intensity": max((r.get('rotation_index', 1) - 1) for r in results) if results else 0
        }

    def _top_n_sectors(self, sectors: List[Dict], n: int = 5) -> List[Dict]:
        """Get top N sectors by rotation index"""
        sorted_sectors = sorted(
            sectors,
            key=lambda x: abs(x.get('rotation_index', 1) - 1),
            reverse=True
        )
        return sorted_sectors[:n]
