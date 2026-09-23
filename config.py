"""
Configuration and constants for Fintables Money Flow Analysis
"""

# Analysis Configuration
ANALYSIS_PERIOD_DAYS = 90  # 3 months
UPDATE_FREQUENCY = "daily"

# Time windows for momentum calculation
SHORT_TERM_WINDOW = 30  # days
LONG_TERM_WINDOW = 90   # days

# Fintables Skills to use
FINTABLES_SKILLS = {
    "ohlcv": "Daily OHLCV data for stocks",
    "ohlcv_endeksler": "Index OHLCV data",
    "kurumsal_bilgi_karti": "Company sector classification",
    "kap_haberleri": "Official disclosures",
    "fintables_arastirma": "Sector research and analysis"
}

# Validation thresholds
VOLUME_ANOMALY_LOWER_BOUND = -0.80  # -80% from historical average
VOLUME_ANOMALY_UPPER_BOUND = 3.00   # +300% from historical average
SECTOR_ROTATION_ANOMALY_THRESHOLD = 0.50  # ±50% daily change

# Output paths
OUTPUT_DIR = "output"
DATA_DIR = "data"
REPORTS_DIR = f"{OUTPUT_DIR}/reports"
DASHBOARDS_DIR = f"{OUTPUT_DIR}/dashboards"

# BIST Indices
MAJOR_INDICES = ["BIST 30", "BIST 100", "BIST All", "BIST Industrial"]

# Sector classification codes
BIST_SECTORS = {
    "10": "Finance",
    "20": "Industrial",
    "30": "Technology",
    "40": "Energy",
    "50": "Healthcare",
    "60": "Consumer",
    "70": "Utilities",
    "80": "Telecom",
    "90": "Other"
}

# LLM Configuration for Council Validation
LLM_MODEL = "claude-opus-5"  # For reasoning and validation
LLM_MAX_TOKENS = 2000

# Data validation rules
VALIDATION_RULES = {
    "volume_range": {
        "lower_bound": VOLUME_ANOMALY_LOWER_BOUND,
        "upper_bound": VOLUME_ANOMALY_UPPER_BOUND,
        "description": "Trading volume should be within historical range"
    },
    "price_continuity": {
        "max_gap": 0.30,  # 30% max daily gap
        "description": "Price movements should be continuous (no impossible gaps)"
    },
    "sector_consistency": {
        "threshold": SECTOR_ROTATION_ANOMALY_THRESHOLD,
        "description": "Sector rotation should be gradual"
    },
    "data_completeness": {
        "min_data_points": 50,  # At least 50 days of data
        "description": "Need sufficient historical data for analysis"
    }
}
