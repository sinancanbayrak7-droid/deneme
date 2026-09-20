# Fintables Money Flow Analysis System

Analyze where investment money is flowing in Borsa İstanbul (BIST) using real Fintables data with LLM Council validation to prevent hallucination.

## 🎯 Objective

Understand **sector-based**, **index-based**, and **market-based** money flows by analyzing:

1. **Trading Volume Analysis** - Where is the trading activity concentrated?
2. **Price × Volume Correlation** - Is trading backed by strong conviction or speculation?
3. **Sector Rotation** - Which sectors are gaining/losing money?

## ⚠️ Hallucination Prevention

This system is designed to **prevent hallucination** at every step:

- ✅ **All data from Fintables only** - No outside data sources
- ✅ **Full audit trail** - Every data point traceable to source
- ✅ **Calculation verification** - All formulas are simple and auditable
- ✅ **LLM Council validation** - Multi-perspective validation of results
- ✅ **Anomaly detection** - Suspicious values flagged automatically
- ✅ **Range validation** - All values checked against historical norms

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Fintables Money Flow Analysis             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐       ┌──────────────────┐          │
│  │  Data Collection │       │ Fintables MCP   │          │
│  │  (data_collector)│───────│ Server Tools    │          │
│  └──────────────────┘       └──────────────────┘          │
│           │                                               │
│           ▼                                               │
│  ┌──────────────────┐                                     │
│  │  Analysis Engine │                                     │
│  │ (analysis_engine)│                                     │
│  │                  │                                     │
│  │ • Volume Analysis│                                     │
│  │ • Correlation   │                                     │
│  │ • Rotation      │                                     │
│  └──────────────────┘                                     │
│           │                                               │
│           ▼                                               │
│  ┌──────────────────┐       ┌──────────────────┐         │
│  │  LLM Council     │───────│  Claude Models  │         │
│  │  Validation      │       │  (validation)   │         │
│  │  (validator.py)  │       └──────────────────┘         │
│  └──────────────────┘                                     │
│           │                                               │
│           ▼                                               │
│  ┌──────────────────────────────────────────┐            │
│  │    Report Generator (report_generator)    │            │
│  │                                          │            │
│  │ ├─ CLI Report (text)                    │            │
│  │ └─ Dashboard Data (JSON/Streamlit)      │            │
│  └──────────────────────────────────────────┘            │
│                                                          │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Analysis Metrics

### 1. Trading Volume Analysis
```
Formula: Daily Transaction Value = Close Price × Daily Volume

Output:
- Total transaction value by sector
- Trend (up/down/stable)
- Daily average
- Change percentage
- Anomalies flagged
```

### 2. Price × Volume Correlation
```
Formula: 
- Price Momentum = (Today Close - 30D Ago) / 30D Ago
- Volume Momentum = (Today Volume - 30D Avg) / 30D Avg
- Correlation = Pearson(Price Changes, Volume)

Signals:
- Bullish: High positive correlation (conviction buying)
- Bearish: Negative correlation (weak hands selling)
- Neutral: Low correlation (uncertain)
```

### 3. Sector Rotation
```
Formula: Rotation Index = Sector Performance / Market Performance

Status:
- Money Inflow: Rotation Index > 1.1 (outperforming)
- Money Outflow: Rotation Index < 0.9 (underperforming)
- Neutral: 0.9 ≤ Index ≤ 1.1
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Fintables MCP server configured
- Claude API access (for validation)

### Installation

```bash
# Clone repository
git clone <repo-url>
cd deneme

# Install dependencies
pip install -r requirements.txt
```

### Running Analysis

**Default (90-day analysis):**
```bash
python main.py
```

**Custom period:**
```bash
python main.py --period 180  # 6 months
```

**With debug output:**
```bash
python main.py --debug
```

### Web Dashboard

```bash
# Generate dashboard data
python main.py --dashboard

# Run Streamlit dashboard
streamlit run dashboard.py
```

Then open: http://localhost:8501

## 📁 Project Structure

```
deneme/
├── main.py                 # Orchestration script
├── config.py              # Configuration & constants
├── data_collector.py      # Fintables data fetching
├── analysis_engine.py     # Analysis calculations
├── validator.py           # LLM Council validation
├── report_generator.py    # Report & visualization generation
├── dashboard.py           # Streamlit web dashboard
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── output/
    ├── reports/          # Generated reports
    └── dashboards/       # Dashboard JSON data
```

## 🔍 Data Flow

```
1. DATA COLLECTION
   ├─ Fetch symbol info (sembol_arama)
   ├─ Fetch stock OHLCV (ohlcv)
   ├─ Fetch index data (ohlcv_endeksler)
   ├─ Fetch sector info (kurumsal_bilgi_karti)
   ├─ Fetch disclosures (kap_haberleri)
   └─ Validate: No hallucination sources

2. ANALYSIS
   ├─ Group by sector/index
   ├─ Calculate volume flows
   ├─ Compute correlations
   ├─ Identify rotations
   └─ Detect anomalies

3. VALIDATION (LLM COUNCIL)
   ├─ Source verification
   ├─ Logical consistency check
   ├─ Range validation
   ├─ Temporal continuity check
   └─ Confidence scoring

4. REPORTING
   ├─ Generate CLI report
   ├─ Generate dashboard data
   └─ Save audit trail
```

## 🛡️ Hallucination Prevention Mechanisms

### 1. Source Verification
- Every data point tagged with source: `{"value": 1000, "source": "ohlcv", "date": "2024-01-15"}`
- Audit trail maintained of all data fetches
- No data from outside Fintables

### 2. Calculation Transparency
- All formulas simple and auditable
- Formula: `transaction_value = close_price × volume`
- No black-box calculations

### 3. Anomaly Detection
- Volume spikes >300% flagged
- Price gaps >30% flagged
- Sector rotations >50% daily change flagged
- Missing data detected

### 4. LLM Council Validation
- Multiple validation perspectives
- Questions asked before conclusions
- Issues flagged automatically
- Confidence scores assigned
- Recommendations provided

## 📋 Configuration

Edit `config.py` to customize:

```python
ANALYSIS_PERIOD_DAYS = 90          # Analysis window
VOLUME_ANOMALY_LOWER_BOUND = -0.80 # -80% threshold
VOLUME_ANOMALY_UPPER_BOUND = 3.00  # +300% threshold
LLM_MODEL = "claude-opus-5"        # Validation model
```

## 🧪 Testing

```bash
# Run basic tests
python -m pytest tests/

# Test data collector
python -c "from data_collector import FintablesDataCollector; print(FintablesDataCollector())"

# Test analysis engine
python -c "from analysis_engine import MoneyFlowAnalysisEngine; print(MoneyFlowAnalysisEngine())"
```

## 📊 Output Examples

### CLI Report
```
================================================================================
FINTABLES MONEY FLOW ANALYSIS REPORT
Generated: 2024-01-15 14:30:00
================================================================================

================================================================================
SECTOR-BASED MONEY FLOW ANALYSIS
================================================================================

total_entities: 15
positive_trend_count: 8
negative_trend_count: 7
top_entity: Banking
total_market_volume: ₺2,450,000,000,000
```

### Dashboard
- Interactive charts with Plotly
- Real-time filtering
- Sector rotation visualization
- Validation status panel
- Anomaly alerts

## 🔗 Fintables Integration

Uses the following Fintables MCP tools:

- `sembol_arama` - Symbol verification
- `veri_sorgula` - SQL data queries
- `ohlcv` - Stock OHLCV data
- `ohlcv_endeksler` - Index data
- `kurumsal_bilgi_karti` - Sector classification
- `kap_haberleri` - Official disclosures
- `finansal_beceri_yukle` - Skill schema
- `dokumanlarda_ara` - Document search

## 📝 Notes

- Analysis period: 3 months (90 days)
- Update frequency: Daily
- Output formats: Python script + Web Dashboard
- Validation: LLM Council (Claude models)
- All calculations use only Fintables data

## 🐛 Troubleshooting

**Fintables MCP connection fails:**
```bash
# Check connection
python -c "from mcp import fintables; print('Connected')"

# Or check status
curl -X GET http://localhost:5000/health
```

**Dashboard doesn't load:**
```bash
# Generate data first
python main.py --dashboard

# Check JSON file
cat output/dashboards/dashboard_data.json
```

**Validation errors:**
- Check `output/results.json` for details
- Review validation section in dashboard
- Check data audit trail in logs

## 📚 References

- [Fintables Documentation](https://fintables.com)
- [Borsa İstanbul](https://www.borsaistanbul.com)
- [Claude API](https://anthropic.com)

## 📄 License

MIT License

## ✨ Credits

Generated by [Claude Code](https://claude.ai/code)
Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
