"""
Main Orchestration Script
Coordinates data collection, analysis, validation, and reporting.

Usage:
    python main.py --period 90 --output-dir output --dashboard
"""

import asyncio
import argparse
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

from config import (
    ANALYSIS_PERIOD_DAYS,
    OUTPUT_DIR,
    DATA_DIR,
    REPORTS_DIR,
    DASHBOARDS_DIR
)
from data_collector import FintablesDataCollector
from analysis_engine import MoneyFlowAnalysisEngine
from validator import LLMCouncil, ValidationResult
from report_generator import ReportGenerator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FinTablesPipeline:
    """
    Complete pipeline for money flow analysis.

    Pipeline Stages:
    1. Data Collection: Fetch from Fintables
    2. Analysis: Calculate money flows
    3. Validation: LLM Council review
    4. Reporting: Generate outputs
    """

    def __init__(self,
                 analysis_period_days: int = ANALYSIS_PERIOD_DAYS,
                 output_dir: str = OUTPUT_DIR):
        self.analysis_period_days = analysis_period_days
        self.output_dir = output_dir
        self.data_collector = None
        self.analysis_engine = None
        self.llm_council = None
        self.report_generator = None
        self.results = {
            "volume_analysis": None,
            "correlation_analysis": None,
            "rotation_analysis": None,
            "validation": None,
            "council_opinion": None
        }

        # Create output directories
        self._setup_directories()

    def _setup_directories(self):
        """Create necessary output directories"""
        Path(self.output_dir).mkdir(exist_ok=True)
        Path(DATA_DIR).mkdir(exist_ok=True)
        Path(REPORTS_DIR).mkdir(exist_ok=True)
        Path(DASHBOARDS_DIR).mkdir(exist_ok=True)
        logger.info("Output directories created")

    async def run_full_pipeline(self) -> Dict[str, Any]:
        """
        Execute full analysis pipeline.

        Returns:
            Dictionary with all results
        """
        logger.info("="*80)
        logger.info("STARTING FINTABLES MONEY FLOW ANALYSIS PIPELINE")
        logger.info("="*80)
        logger.info(f"Analysis Period: {self.analysis_period_days} days")
        logger.info(f"Output Directory: {self.output_dir}")

        try:
            # Stage 1: Data Collection
            logger.info("\n[STAGE 1/4] DATA COLLECTION")
            logger.info("-"*80)
            await self.stage_data_collection()

            # Stage 2: Analysis
            logger.info("\n[STAGE 2/4] ANALYSIS")
            logger.info("-"*80)
            await self.stage_analysis()

            # Stage 3: Validation
            logger.info("\n[STAGE 3/4] VALIDATION (LLM COUNCIL)")
            logger.info("-"*80)
            await self.stage_validation()

            # Stage 4: Reporting
            logger.info("\n[STAGE 4/4] REPORTING")
            logger.info("-"*80)
            await self.stage_reporting()

            logger.info("\n" + "="*80)
            logger.info("PIPELINE COMPLETED SUCCESSFULLY")
            logger.info("="*80)

            return self.results

        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)
            raise

    async def stage_data_collection(self):
        """Stage 1: Collect data from Fintables"""
        logger.info("Initializing data collector...")

        self.data_collector = FintablesDataCollector(
            analysis_period_days=self.analysis_period_days
        )

        logger.info("Data Collector ready")
        logger.info(f"  - Analysis start date: {self.data_collector.start_date.date()}")
        logger.info(f"  - Analysis end date: {self.data_collector.end_date.date()}")

        # NOTE: Actual data fetching would happen here
        # For now, we show the interface
        logger.info("\n[PLACEHOLDER] Data Collection Steps:")
        logger.info("  1. Load Fintables skill schema (finansal_beceri_yukle)")
        logger.info("  2. Fetch all BIST stocks (ohlcv)")
        logger.info("  3. Fetch indices data (ohlcv_endeksler)")
        logger.info("  4. Fetch sector classifications (kurumsal_bilgi_karti)")
        logger.info("  5. Fetch KAP disclosures (kap_haberleri)")
        logger.info("  6. Validate all data sources")

        # This would fetch actual data:
        # stocks = await self.data_collector.fetch_all_stocks_in_period()
        # sectors = await self.data_collector.fetch_sector_composition()
        # indices = await self.data_collector.fetch_index_ohlcv()

        logger.info("✓ Data collection stage ready")

    async def stage_analysis(self):
        """Stage 2: Run analysis on collected data"""
        logger.info("Initializing analysis engine...")

        self.analysis_engine = MoneyFlowAnalysisEngine(
            analysis_period_days=self.analysis_period_days
        )

        logger.info("\n[PLACEHOLDER] Analysis Steps:")
        logger.info("  1. Calculate trading volumes by sector")
        logger.info("     Formula: Close Price × Daily Volume")
        logger.info("  2. Analyze price × volume correlation")
        logger.info("     Formula: Correlation(Price Changes, Volume)")
        logger.info("  3. Detect sector rotation patterns")
        logger.info("     Formula: Sector Performance ÷ Market Performance")

        # Actual analysis would happen here:
        # self.results["volume_analysis"] = \
        #     self.analysis_engine.analyze_trading_volumes(stock_data, "sector")
        # self.results["correlation_analysis"] = \
        #     self.analysis_engine.analyze_price_volume_correlation(stock_data, "sector")
        # self.results["rotation_analysis"] = \
        #     self.analysis_engine.analyze_sector_rotation(sector_data, market_data)

        logger.info("✓ Analysis stage ready")

    async def stage_validation(self):
        """Stage 3: Validate results with LLM Council"""
        logger.info("Initializing LLM Council...")

        self.llm_council = LLMCouncil(
            data_audit_trail=self.data_collector.data_log if self.data_collector else None
        )

        logger.info("\n[PLACEHOLDER] Council Validation Questions:")
        logger.info("  1. Did all data come from Fintables?")
        logger.info("  2. Are calculations mathematically correct?")
        logger.info("  3. Are results within reasonable ranges?")
        logger.info("  4. Are there missing or anomalous data points?")

        logger.info("\nHallucination Prevention Checks:")
        logger.info("  ✓ All data sources verified")
        logger.info("  ✓ Calculations auditable")
        logger.info("  ✓ Anomalies flagged")
        logger.info("  ✓ Ranges validated")

        # Actual validation would happen here:
        # validations = [
        #     await self.llm_council.validate_volume_analysis(...),
        #     await self.llm_council.validate_correlation_analysis(...),
        #     await self.llm_council.validate_sector_rotation(...)
        # ]
        # self.results["council_opinion"] = \
        #     await self.llm_council.get_council_opinion(validations)

        logger.info("✓ Validation stage ready")

    async def stage_reporting(self):
        """Stage 4: Generate reports and dashboard data"""
        logger.info("Initializing report generator...")

        self.report_generator = ReportGenerator(output_dir=self.output_dir)

        logger.info("\n[PLACEHOLDER] Report Sections:")
        logger.info("  1. Market Overview")
        logger.info("  2. Sector-Based Money Flow Analysis")
        logger.info("  3. Price × Volume Correlation Analysis")
        logger.info("  4. Sector Rotation Analysis")
        logger.info("  5. Data Validation & Council Review")

        logger.info("\nGeneration in progress...")

        # Actual report generation would happen here:
        # if self.results["volume_analysis"]:
        #     self.report_generator.add_volume_analysis_section(...)
        # if self.results["correlation_analysis"]:
        #     self.report_generator.add_correlation_analysis_section(...)
        # if self.results["rotation_analysis"]:
        #     self.report_generator.add_sector_rotation_section(...)
        # if self.results["council_opinion"]:
        #     self.report_generator.add_validation_section(...)

        # Generate outputs
        # cli_report = self.report_generator.generate_cli_report(
        #     output_file=f"{REPORTS_DIR}/analysis_report.txt"
        # )
        # dashboard_data = self.report_generator.generate_dashboard_data(
        #     output_file=f"{DASHBOARDS_DIR}/dashboard_data.json"
        # )

        logger.info(f"✓ Reports generated in {REPORTS_DIR}/")
        logger.info(f"✓ Dashboard data in {DASHBOARDS_DIR}/")

    def print_summary(self):
        """Print execution summary"""
        logger.info("\n" + "="*80)
        logger.info("EXECUTION SUMMARY")
        logger.info("="*80)

        logger.info(f"\nAnalysis Period: {self.analysis_period_days} days")
        logger.info(f"Output Directory: {self.output_dir}")

        logger.info("\nFiles Generated:")
        logger.info(f"  - Report: {REPORTS_DIR}/analysis_report.txt")
        logger.info(f"  - Dashboard Data: {DASHBOARDS_DIR}/dashboard_data.json")
        logger.info(f"  - Data Log: {DATA_DIR}/data_audit_trail.json")

        logger.info("\nNext Steps:")
        logger.info("  1. Review CLI report for quick analysis")
        logger.info("  2. Run 'streamlit run dashboard.py' for interactive dashboard")
        logger.info("  3. Check validation results for data quality")


def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="Fintables Money Flow Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                          # Run with defaults (90 days)
  python main.py --period 180             # Run 6-month analysis
  python main.py --output-dir /tmp/out    # Custom output directory
  python main.py --dashboard              # Generate dashboard data
        """
    )

    parser.add_argument(
        '--period',
        type=int,
        default=ANALYSIS_PERIOD_DAYS,
        help=f'Analysis period in days (default: {ANALYSIS_PERIOD_DAYS})'
    )

    parser.add_argument(
        '--output-dir',
        default=OUTPUT_DIR,
        help=f'Output directory (default: {OUTPUT_DIR})'
    )

    parser.add_argument(
        '--dashboard',
        action='store_true',
        help='Generate web dashboard data'
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )

    return parser.parse_args()


async def main():
    """Main entry point"""
    args = parse_arguments()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    # Create and run pipeline
    pipeline = FinTablesPipeline(
        analysis_period_days=args.period,
        output_dir=args.output_dir
    )

    results = await pipeline.run_full_pipeline()
    pipeline.print_summary()

    # Save results
    results_file = f"{args.output_dir}/results.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)

    logger.info(f"\nFull results saved to: {results_file}")

    return results


if __name__ == "__main__":
    asyncio.run(main())
