"""
Analysis Engine Module
Calculates money flows by sector, index, and market.
Implements the three analysis metrics:
1. Trading Volume Analysis
2. Price x Volume Correlation
3. Sector Rotation
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class VolumeAnalysis:
    """Trading volume analysis results"""
    entity: str  # Sector, index, or market name
    entity_type: str  # "sector", "index", or "market"
    period_start: str
    period_end: str
    total_transaction_value: float  # Sum of (close_price × volume)
    daily_average: float
    change_percentage: float  # vs previous period
    trend: str  # "up", "down", "stable"
    anomalies: List[Dict]  # Flagged unusual values


@dataclass
class CorrelationAnalysis:
    """Price × Volume correlation analysis"""
    entity: str
    entity_type: str
    price_momentum: float  # (today_close - 30d_ago_close) / 30d_ago_close
    volume_momentum: float  # (today_volume - 30d_avg_volume) / 30d_avg_volume
    correlation: float  # -1.0 to 1.0
    signal: str  # "bullish", "risky", "neutral"
    confidence: float  # 0.0 to 1.0


@dataclass
class SectorRotation:
    """Sector rotation analysis"""
    sector: str
    period: str  # "weekly", "monthly"
    sector_performance: float
    market_performance: float
    rotation_index: float  # sector_perf / market_perf
    status: str  # "money_inflow", "money_outflow", "neutral"
    confidence: float


class MoneyFlowAnalysisEngine:
    """
    Analyzes where money is flowing in BIST markets.

    Three main analysis types:
    1. Volume Analysis: Where is the trading activity?
    2. Correlation Analysis: Is trading backed by strong conviction?
    3. Sector Rotation: Which sectors are gaining/losing money?
    """

    def __init__(self, analysis_period_days: int = 90):
        self.analysis_period_days = analysis_period_days
        self.short_term_window = 30  # days
        self.long_term_window = 90   # days
        self.results = {}

    def analyze_trading_volumes(
        self,
        data: pd.DataFrame,
        groupby_column: str
    ) -> List[VolumeAnalysis]:
        """
        Analyze trading volumes by sector, index, or across market.

        Formula:
            Daily Transaction Value = Close Price × Daily Volume
            Total = Sum of Daily Transaction Values

        Args:
            data: DataFrame with columns: date, close_price, volume, groupby_column
            groupby_column: "sector", "index", or "symbol"

        Returns:
            List of VolumeAnalysis results
        """
        logger.info(f"Analyzing trading volumes grouped by: {groupby_column}")

        results = []

        # Group data by sector/index
        grouped = data.groupby(groupby_column)

        for entity, group_data in grouped:
            # Calculate transaction value
            group_data = group_data.copy()
            group_data['transaction_value'] = group_data['close_price'] * group_data['volume']

            # Sort by date
            group_data = group_data.sort_values('date')

            # Split into current and previous periods
            today = pd.Timestamp.now()
            cutoff = today - timedelta(days=self.short_term_window)

            current_period = group_data[group_data['date'] >= cutoff]
            previous_period = group_data[
                (group_data['date'] < cutoff) &
                (group_data['date'] >= cutoff - timedelta(days=self.short_term_window))
            ]

            if len(current_period) == 0:
                logger.warning(f"Insufficient data for {entity}")
                continue

            # Calculate metrics
            total_value = current_period['transaction_value'].sum()
            daily_avg = current_period['transaction_value'].mean()

            prev_total = previous_period['transaction_value'].sum()
            change_pct = ((total_value - prev_total) / prev_total * 100) if prev_total > 0 else 0

            # Determine trend
            if change_pct > 10:
                trend = "up"
            elif change_pct < -10:
                trend = "down"
            else:
                trend = "stable"

            # Detect anomalies
            anomalies = self._detect_volume_anomalies(current_period)

            analysis = VolumeAnalysis(
                entity=str(entity),
                entity_type=groupby_column,
                period_start=str(current_period['date'].min()),
                period_end=str(current_period['date'].max()),
                total_transaction_value=total_value,
                daily_average=daily_avg,
                change_percentage=change_pct,
                trend=trend,
                anomalies=anomalies
            )
            results.append(analysis)

        return results

    def analyze_price_volume_correlation(
        self,
        data: pd.DataFrame,
        groupby_column: str
    ) -> List[CorrelationAnalysis]:
        """
        Analyze correlation between price movements and volume.

        High correlation = Strong conviction (bullish)
        Low correlation = Speculation/weak signal

        Formula:
            Price Momentum = (Today Close - 30D Ago Close) / 30D Ago Close
            Volume Momentum = (Today Volume - 30D Avg Volume) / 30D Avg Volume
            Correlation = Pearson correlation of price changes and volume

        Args:
            data: DataFrame with columns: date, close_price, volume, groupby_column
            groupby_column: "sector", "index", or "symbol"

        Returns:
            List of CorrelationAnalysis results
        """
        logger.info(f"Analyzing price-volume correlation grouped by: {groupby_column}")

        results = []
        grouped = data.groupby(groupby_column)

        for entity, group_data in grouped:
            group_data = group_data.copy()
            group_data = group_data.sort_values('date')

            if len(group_data) < self.short_term_window:
                logger.warning(f"Insufficient data for correlation analysis: {entity}")
                continue

            # Calculate price momentum
            latest_close = group_data['close_price'].iloc[-1]
            thirty_days_ago_idx = max(0, len(group_data) - self.short_term_window)
            close_30d_ago = group_data['close_price'].iloc[thirty_days_ago_idx]
            price_momentum = (latest_close - close_30d_ago) / close_30d_ago if close_30d_ago != 0 else 0

            # Calculate volume momentum
            latest_volume = group_data['volume'].iloc[-1]
            avg_volume_30d = group_data.iloc[thirty_days_ago_idx:]['volume'].mean()
            volume_momentum = (latest_volume - avg_volume_30d) / avg_volume_30d if avg_volume_30d > 0 else 0

            # Calculate correlation
            price_changes = group_data['close_price'].pct_change()
            volume_normalized = group_data['volume'] / group_data['volume'].mean()

            # Remove NaN values for correlation
            valid_data = pd.DataFrame({
                'price': price_changes,
                'volume': volume_normalized
            }).dropna()

            if len(valid_data) > 1:
                correlation = valid_data['price'].corr(valid_data['volume'])
            else:
                correlation = 0.0

            # Determine signal
            if abs(correlation) > 0.6:
                if correlation > 0:
                    signal = "bullish"  # Price up with volume
                    confidence = abs(correlation)
                else:
                    signal = "bearish"  # Price up but volume down
                    confidence = abs(correlation)
            else:
                signal = "neutral"
                confidence = abs(correlation)

            analysis = CorrelationAnalysis(
                entity=str(entity),
                entity_type=groupby_column,
                price_momentum=price_momentum,
                volume_momentum=volume_momentum,
                correlation=correlation,
                signal=signal,
                confidence=confidence
            )
            results.append(analysis)

        return results

    def analyze_sector_rotation(
        self,
        sector_data: pd.DataFrame,
        market_data: pd.DataFrame,
        period: str = "weekly"
    ) -> List[SectorRotation]:
        """
        Analyze sector rotation - which sectors are gaining/losing money.

        Formula:
            Sector Performance = Sum(Close[today] - Close[period_ago]) / Sum(Close[period_ago])
            Market Performance = Same but for entire market
            Rotation Index = Sector Performance / Market Performance

        Interpretation:
            > 1.0 = Money flowing INTO sector (outperforming)
            < 1.0 = Money flowing OUT OF sector (underperforming)

        Args:
            sector_data: DataFrame with sector OHLCV data
            market_data: DataFrame with total market OHLCV data
            period: "weekly" or "monthly"

        Returns:
            List of SectorRotation results
        """
        logger.info(f"Analyzing sector rotation (period: {period})")

        if period == "weekly":
            lookback_days = 7
        else:  # monthly
            lookback_days = 30

        results = []

        # Get unique sectors
        sectors = sector_data['sector'].unique()

        for sector in sectors:
            sector_subset = sector_data[sector_data['sector'] == sector]
            sector_subset = sector_subset.sort_values('date')

            if len(sector_subset) < lookback_days:
                continue

            # Calculate sector performance
            sector_close_today = sector_subset['close_price'].iloc[-1]
            sector_close_period_ago = sector_subset['close_price'].iloc[-lookback_days]
            sector_perf = (sector_close_today - sector_close_period_ago) / sector_close_period_ago if sector_close_period_ago > 0 else 0

            # Calculate market performance
            market_subset = market_data.sort_values('date')
            if len(market_subset) < lookback_days:
                continue

            market_close_today = market_subset['close_price'].iloc[-1]
            market_close_period_ago = market_subset['close_price'].iloc[-lookback_days]
            market_perf = (market_close_today - market_close_period_ago) / market_close_period_ago if market_close_period_ago > 0 else 0

            # Calculate rotation index
            if market_perf != 0:
                rotation_idx = sector_perf / market_perf
            else:
                rotation_idx = 1.0

            # Determine status
            if rotation_idx > 1.1:
                status = "money_inflow"
                confidence = min(rotation_idx - 1.0, 1.0)
            elif rotation_idx < 0.9:
                status = "money_outflow"
                confidence = min(1.0 - rotation_idx, 1.0)
            else:
                status = "neutral"
                confidence = 0.5

            rotation = SectorRotation(
                sector=str(sector),
                period=period,
                sector_performance=sector_perf,
                market_performance=market_perf,
                rotation_index=rotation_idx,
                status=status,
                confidence=confidence
            )
            results.append(rotation)

        # Sort by rotation index (strongest inflows first)
        results.sort(key=lambda x: x.rotation_index, reverse=True)

        return results

    def _detect_volume_anomalies(self, data: pd.DataFrame) -> List[Dict]:
        """
        Detect anomalous volume values.

        Anomaly = Value outside [-80%, +300%] of historical average
        """
        anomalies = []

        if len(data) < 2:
            return anomalies

        volumes = data['volume'].values
        mean_volume = np.mean(volumes)
        std_volume = np.std(volumes)

        lower_bound = mean_volume * 0.2  # -80% threshold
        upper_bound = mean_volume * 4.0   # +300% threshold

        for idx, row in data.iterrows():
            if row['volume'] < lower_bound or row['volume'] > upper_bound:
                anomalies.append({
                    "date": str(row['date']),
                    "volume": row['volume'],
                    "expected_range": f"[{lower_bound:.0f}, {upper_bound:.0f}]",
                    "deviation_percent": ((row['volume'] - mean_volume) / mean_volume * 100)
                })

        return anomalies
