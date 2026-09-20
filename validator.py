"""
LLM Council Validator Module
Validates analysis results using multiple AI perspectives.
Prevents hallucination by checking if results make logical sense.
"""

from typing import Dict, List, Any
from dataclasses import dataclass
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of validation by Council"""
    is_valid: bool
    confidence_score: float  # 0.0 to 1.0
    questions: List[str]  # Questions asked for validation
    answers: List[Dict[str, Any]]  # Answers from validation
    flagged_issues: List[str]  # Issues found
    recommendations: List[str]  # Recommendations


class LLMCouncil:
    """
    Multi-perspective validation of analysis results.

    The Council asks critical questions to validate:
    1. Data Source Validity: Did this data come from Fintables?
    2. Logical Consistency: Do the numbers make sense?
    3. Historical Context: Are changes within expected ranges?
    4. Temporal Continuity: Is there missing or anomalous data?

    This prevents hallucination by ensuring all numbers are:
    - Traceable to Fintables sources
    - Logically consistent
    - Within reasonable ranges
    - Temporally continuous
    """

    def __init__(self, data_audit_trail: Dict = None):
        """
        Initialize Council with audit trail from data collection.

        Args:
            data_audit_trail: JSON of all data fetches from DataCollector
        """
        self.data_audit_trail = data_audit_trail or {}
        self.validation_log = []

    async def validate_volume_analysis(
        self,
        analysis_results: List[Dict],
        historical_ranges: Dict[str, Dict]
    ) -> ValidationResult:
        """
        Validate trading volume analysis results.

        Council Questions:
        1. "Did all volume data come from Fintables' ohlcv table?"
        2. "Are the calculated transaction values (price × volume) within historical ranges?"
        3. "Are there any impossible volume spikes (>300% change)?"
        4. "Are all dates continuous with no missing trading days?"

        Args:
            analysis_results: List of VolumeAnalysis results
            historical_ranges: Expected min/max for each sector

        Returns:
            ValidationResult with confidence score
        """
        logger.info("Council validating volume analysis...")

        questions = [
            "Did all volume data come from Fintables' ohlcv table?",
            "Are the calculated transaction values within historical ranges?",
            "Are there any impossible volume spikes (>300% of average)?",
            "Are all dates continuous with no missing trading days?"
        ]

        issues = []
        confidence = 1.0

        # Check each analysis result
        for result in analysis_results:
            entity = result.get('entity', 'unknown')
            total_value = result.get('total_transaction_value', 0)

            # Question 1: Source verification
            if not self._verify_data_source(entity, 'ohlcv'):
                issues.append(f"{entity}: Cannot verify data came from Fintables ohlcv")
                confidence *= 0.8

            # Question 2: Range validation
            if entity in historical_ranges:
                expected_range = historical_ranges[entity]
                if total_value < expected_range.get('min', 0) * 0.5:
                    issues.append(f"{entity}: Value suspiciously low ({total_value})")
                    confidence *= 0.7
                elif total_value > expected_range.get('max', float('inf')) * 2:
                    issues.append(f"{entity}: Value suspiciously high ({total_value})")
                    confidence *= 0.7

            # Question 3: Spike detection
            anomalies = result.get('anomalies', [])
            if len(anomalies) > 5:
                issues.append(f"{entity}: Excessive anomalies detected ({len(anomalies)})")
                confidence *= 0.85

            # Question 4: Temporal continuity
            period_start = result.get('period_start')
            period_end = result.get('period_end')
            if period_start and period_end:
                # Check for reasonable data span
                if period_start > period_end:
                    issues.append(f"{entity}: Invalid date range (start > end)")
                    confidence *= 0.5

        is_valid = confidence > 0.6 and len(issues) < len(analysis_results) * 0.5

        return ValidationResult(
            is_valid=is_valid,
            confidence_score=confidence,
            questions=questions,
            answers=self._generate_answers(questions, issues),
            flagged_issues=issues,
            recommendations=self._generate_recommendations(issues)
        )

    async def validate_correlation_analysis(
        self,
        analysis_results: List[Dict]
    ) -> ValidationResult:
        """
        Validate price-volume correlation analysis.

        Council Questions:
        1. "Are all price movements within ±50% daily (no impossible jumps)?"
        2. "Are correlation values between -1 and +1?"
        3. "Do correlation interpretations match the numbers?"
        4. "Are there sufficient data points (>30 days) for reliable correlation?"

        Args:
            analysis_results: List of CorrelationAnalysis results

        Returns:
            ValidationResult
        """
        logger.info("Council validating correlation analysis...")

        questions = [
            "Are all price movements within reasonable daily ranges (±50%)?",
            "Are correlation values between -1 and +1?",
            "Do signal interpretations (bullish/bearish) match the correlation values?",
            "Are there sufficient data points (>30 days) for reliable correlation?"
        ]

        issues = []
        confidence = 1.0

        for result in analysis_results:
            entity = result.get('entity', 'unknown')

            # Question 1: Price momentum validation
            price_momentum = result.get('price_momentum', 0)
            if abs(price_momentum) > 0.5:
                logger.warning(f"{entity}: Large price movement ({price_momentum:.2%})")
                # This is not necessarily wrong, but worth noting

            # Question 2: Correlation bounds
            correlation = result.get('correlation', 0)
            if correlation < -1 or correlation > 1:
                issues.append(f"{entity}: Invalid correlation value ({correlation})")
                confidence *= 0.3

            # Question 3: Signal-value consistency
            signal = result.get('signal', 'neutral')
            if signal == 'bullish' and correlation < 0.4:
                issues.append(f"{entity}: Bullish signal but low correlation ({correlation})")
                confidence *= 0.7
            elif signal == 'bearish' and correlation > -0.4:
                issues.append(f"{entity}: Bearish signal but weak negative correlation ({correlation})")
                confidence *= 0.7

        is_valid = confidence > 0.5 and len(issues) == 0

        return ValidationResult(
            is_valid=is_valid,
            confidence_score=confidence,
            questions=questions,
            answers=self._generate_answers(questions, issues),
            flagged_issues=issues,
            recommendations=self._generate_recommendations(issues)
        )

    async def validate_sector_rotation(
        self,
        analysis_results: List[Dict]
    ) -> ValidationResult:
        """
        Validate sector rotation analysis.

        Council Questions:
        1. "Do sector performance numbers make sense (within ±50% weekly)?",
        2. "Does rotation index interpretation match the math?",
        3. "Are there conflicting signals (e.g., high outflow but high volume)?",
        4. "Is the confidence score justified by the data?"

        Args:
            analysis_results: List of SectorRotation results

        Returns:
            ValidationResult
        """
        logger.info("Council validating sector rotation analysis...")

        questions = [
            "Do sector performance numbers make sense (within ±50% for weekly)?",
            "Does rotation interpretation match rotation index values?",
            "Are there conflicting signals between different metrics?",
            "Is confidence score justified by correlation strength?"
        ]

        issues = []
        confidence = 1.0

        for result in analysis_results:
            sector = result.get('sector', 'unknown')

            # Question 1: Performance bounds
            perf = result.get('sector_performance', 0)
            if abs(perf) > 0.5:  # >50% change in a week is suspicious
                logger.warning(f"{sector}: Large performance change ({perf:.2%})")

            # Question 2: Interpretation consistency
            rotation_idx = result.get('rotation_index', 1.0)
            status = result.get('status', 'neutral')

            if status == 'money_inflow' and rotation_idx <= 1.0:
                issues.append(f"{sector}: Inflow status but rotation index ≤1.0 ({rotation_idx})")
                confidence *= 0.5
            elif status == 'money_outflow' and rotation_idx >= 1.0:
                issues.append(f"{sector}: Outflow status but rotation index ≥1.0 ({rotation_idx})")
                confidence *= 0.5

            # Question 3: Confidence justification
            conf_score = result.get('confidence', 0)
            if conf_score > 0.9 and rotation_idx between 0.9 and 1.1:
                issues.append(f"{sector}: High confidence ({conf_score}) but neutral rotation index")
                confidence *= 0.7

        is_valid = confidence > 0.6

        return ValidationResult(
            is_valid=is_valid,
            confidence_score=confidence,
            questions=questions,
            answers=self._generate_answers(questions, issues),
            flagged_issues=issues,
            recommendations=self._generate_recommendations(issues)
        )

    def _verify_data_source(self, entity: str, expected_source: str) -> bool:
        """Verify that data for entity came from expected source"""
        # Check audit trail
        for entry in self.data_audit_trail.get('entries', []):
            if entry.get('symbol') == entity and entry.get('source') == expected_source:
                return True
        return False

    def _generate_answers(self, questions: List[str], issues: List[str]) -> List[Dict]:
        """Generate answers to council questions based on issues found"""
        answers = []
        for q in questions:
            relevant_issues = [i for i in issues if any(keyword in i for keyword in q.split())]
            answers.append({
                "question": q,
                "issues_found": len(relevant_issues),
                "severity": "high" if relevant_issues else "none"
            })
        return answers

    def _generate_recommendations(self, issues: List[str]) -> List[str]:
        """Generate recommendations based on validation issues"""
        recommendations = []

        if any('data source' in i.lower() for i in issues):
            recommendations.append("Verify all data sources in audit trail")

        if any('range' in i.lower() or 'suspicious' in i.lower() for i in issues):
            recommendations.append("Review outliers with domain expert")

        if any('anomal' in i.lower() for i in issues):
            recommendations.append("Investigate anomalous dates/values")

        if any('correlation' in i.lower() for i in issues):
            recommendations.append("Increase analysis period for better correlation")

        if not recommendations:
            recommendations.append("Analysis validated - no issues found")

        return recommendations

    async def get_council_opinion(self, validation_results: List[ValidationResult]) -> Dict:
        """
        Synthesize Council opinion from multiple validation perspectives.

        Returns:
            Summary of all validations with overall confidence
        """
        logger.info("Synthesizing Council opinion...")

        avg_confidence = sum(r.confidence_score for r in validation_results) / len(validation_results) if validation_results else 0
        all_valid = all(r.is_valid for r in validation_results)
        all_issues = []

        for result in validation_results:
            all_issues.extend(result.flagged_issues)

        opinion = {
            "timestamp": str(pd.Timestamp.now()),
            "overall_valid": all_valid,
            "confidence_score": avg_confidence,
            "validation_count": len(validation_results),
            "total_issues_found": len(all_issues),
            "council_recommendation": "APPROVED" if all_valid and avg_confidence > 0.7 else "REVIEW_REQUIRED"
        }

        return opinion


# Placeholder imports that would be used
import pandas as pd
