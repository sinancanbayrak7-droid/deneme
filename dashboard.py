"""
Streamlit Web Dashboard
Interactive visualization of money flow analysis results.

Run with: streamlit run dashboard.py
"""

import streamlit as st
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# Configure page
st.set_page_config(
    page_title="BIST Money Flow Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .positive {
        color: #00cc66;
    }
    .negative {
        color: #cc0000;
    }
    .neutral {
        color: #999999;
    }
</style>
""", unsafe_allow_html=True)


class DashboardApp:
    """Streamlit Dashboard Application"""

    def __init__(self):
        self.data_file = "output/dashboards/dashboard_data.json"
        self.dashboard_data = None
        self.load_data()

    def load_data(self):
        """Load dashboard data from JSON"""
        data_path = Path(self.data_file)

        if data_path.exists():
            with open(data_path, 'r', encoding='utf-8') as f:
                self.dashboard_data = json.load(f)
        else:
            st.warning(f"Dashboard data not found. Run `python main.py --dashboard` first.")
            self.dashboard_data = None

    def render_header(self):
        """Render dashboard header"""
        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            st.title("📊 BIST Money Flow Analysis")

        with col3:
            if self.dashboard_data:
                generated_at = self.dashboard_data.get('metadata', {}).get('generated_at', 'Unknown')
                st.caption(f"Updated: {generated_at}")

    def render_sidebar(self):
        """Render sidebar with filters and controls"""
        with st.sidebar:
            st.header("⚙️ Controls")

            # Time period selector
            st.subheader("Analysis Period")
            period = st.selectbox(
                "Select period",
                ["3 months", "6 months", "12 months", "Custom"]
            )

            # Entity type filter
            st.subheader("Entity Type")
            entity_type = st.multiselect(
                "Show data for:",
                ["Sectors", "Indices", "Market"],
                default=["Sectors"]
            )

            # Analysis type filter
            st.subheader("Analysis Type")
            analysis_types = st.multiselect(
                "Include analyses:",
                ["Volume", "Correlation", "Rotation", "All"],
                default=["All"]
            )

            # Validation settings
            st.subheader("Validation")
            show_validation = st.checkbox("Show validation details", value=True)

            return {
                "period": period,
                "entity_types": entity_type,
                "analysis_types": analysis_types,
                "show_validation": show_validation
            }

    def render_overview_metrics(self):
        """Render overview metrics"""
        st.header("📈 Market Overview")

        if not self.dashboard_data:
            st.error("No data available")
            return

        # Get market metrics from first section if available
        sections = self.dashboard_data.get('sections', [])
        market_section = next((s for s in sections if s['title'] == 'Overall Market Overview'), None)

        if market_section:
            metrics = market_section.get('content', {}).get('metrics', {})

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Total Market Volume",
                    f"₺{metrics.get('total_volume', 0)/1e9:.2f}B",
                    f"+{metrics.get('volume_change', 0):.1f}%"
                )

            with col2:
                st.metric(
                    "Daily Avg Volume",
                    f"₺{metrics.get('daily_average_volume', 0)/1e9:.2f}B"
                )

            with col3:
                trend = metrics.get('market_trend', 'Neutral')
                trend_color = '🟢' if trend == 'Up' else ('🔴' if trend == 'Down' else '🟡')
                st.metric("Market Trend", f"{trend_color} {trend}")

            with col4:
                st.metric(
                    "Active Sectors",
                    metrics.get('active_sectors', 'N/A')
                )

    def render_volume_analysis(self):
        """Render trading volume analysis"""
        st.header("💰 Trading Volume Analysis")

        if not self.dashboard_data:
            return

        sections = self.dashboard_data.get('sections', [])
        vol_section = next((s for s in sections if 'Volume' in s['title']), None)

        if not vol_section:
            st.info("No volume analysis data available")
            return

        results = vol_section.get('content', {}).get('results', [])

        if not results:
            st.info("No volume data to display")
            return

        # Create volume comparison chart
        vol_data = pd.DataFrame([
            {
                'entity': r.get('entity', 'N/A'),
                'volume': r.get('total_transaction_value', 0),
                'trend': r.get('trend', 'stable')
            }
            for r in results
        ])

        vol_data = vol_data.sort_values('volume', ascending=False).head(10)

        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(
                vol_data,
                x='entity',
                y='volume',
                color='trend',
                title='Top 10 Entities by Trading Volume',
                color_discrete_map={'up': '#00cc66', 'down': '#cc0000', 'stable': '#999999'}
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Volume trend
            trend_summary = vol_data['trend'].value_counts()
            fig2 = go.Figure(data=[
                go.Pie(
                    labels=trend_summary.index,
                    values=trend_summary.values,
                    marker=dict(colors=['#00cc66', '#cc0000', '#999999'])
                )
            ])
            fig2.update_layout(title="Volume Trends Distribution")
            st.plotly_chart(fig2, use_container_width=True)

        # Table view
        st.subheader("Detailed Volume Data")
        st.dataframe(
            vol_data.sort_values('volume', ascending=False),
            use_container_width=True
        )

    def render_correlation_analysis(self):
        """Render price-volume correlation analysis"""
        st.header("🔗 Price × Volume Correlation")

        if not self.dashboard_data:
            return

        sections = self.dashboard_data.get('sections', [])
        corr_section = next((s for s in sections if 'Correlation' in s['title']), None)

        if not corr_section:
            st.info("No correlation analysis data available")
            return

        results = corr_section.get('content', {}).get('results', [])
        summary = corr_section.get('content', {}).get('summary', {})

        if not results:
            st.info("No correlation data to display")
            return

        # Show signal summary
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Bullish Signals", summary.get('bullish_count', 0))
        with col2:
            st.metric("Bearish Signals", summary.get('bearish_count', 0))
        with col3:
            st.metric("Neutral", summary.get('neutral_count', 0))
        with col4:
            st.metric("Avg Confidence", f"{summary.get('average_confidence', 0):.2f}")

        # Create correlation scatter
        corr_data = pd.DataFrame([
            {
                'entity': r.get('entity', 'N/A'),
                'price_momentum': r.get('price_momentum', 0),
                'volume_momentum': r.get('volume_momentum', 0),
                'signal': r.get('signal', 'neutral'),
                'confidence': r.get('confidence', 0)
            }
            for r in results
        ])

        fig = px.scatter(
            corr_data,
            x='price_momentum',
            y='volume_momentum',
            color='signal',
            size='confidence',
            hover_name='entity',
            title='Price vs Volume Momentum',
            color_discrete_map={'bullish': '#00cc66', 'bearish': '#cc0000', 'neutral': '#999999'}
        )
        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        fig.add_vline(x=0, line_dash="dash", line_color="gray", opacity=0.5)

        st.plotly_chart(fig, use_container_width=True)

    def render_sector_rotation(self):
        """Render sector rotation analysis"""
        st.header("🔄 Sector Rotation")

        if not self.dashboard_data:
            return

        sections = self.dashboard_data.get('sections', [])
        rotation_section = next((s for s in sections if 'Rotation' in s['title']), None)

        if not rotation_section:
            st.info("No rotation analysis data available")
            return

        results = rotation_section.get('content', {}).get('results', [])
        inflows = rotation_section.get('content', {}).get('inflow_sectors', [])
        outflows = rotation_section.get('content', {}).get('outflow_sectors', [])

        # Money flow summary
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("💹 Money Inflows")
            inflow_data = pd.DataFrame([
                {
                    'sector': r.get('sector', 'N/A'),
                    'rotation_index': r.get('rotation_index', 1)
                }
                for r in inflows
            ]).head(5)

            if not inflow_data.empty:
                st.dataframe(inflow_data, use_container_width=True)
            else:
                st.info("No money inflows detected")

        with col2:
            st.subheader("📉 Money Outflows")
            outflow_data = pd.DataFrame([
                {
                    'sector': r.get('sector', 'N/A'),
                    'rotation_index': r.get('rotation_index', 1)
                }
                for r in outflows
            ]).head(5)

            if not outflow_data.empty:
                st.dataframe(outflow_data, use_container_width=True)
            else:
                st.info("No money outflows detected")

        # Rotation heatmap
        if results:
            rotation_data = pd.DataFrame([
                {
                    'sector': r.get('sector', 'N/A'),
                    'rotation': r.get('rotation_index', 1),
                    'status': r.get('status', 'neutral')
                }
                for r in results
            ]).sort_values('rotation', ascending=False)

            fig = px.bar(
                rotation_data,
                x='sector',
                y='rotation',
                color='status',
                title='Sector Rotation Index',
                color_discrete_map={
                    'money_inflow': '#00cc66',
                    'money_outflow': '#cc0000',
                    'neutral': '#999999'
                }
            )
            fig.axhline(y=1.0, line_dash="dash", line_color="black", opacity=0.3)
            st.plotly_chart(fig, use_container_width=True)

    def render_validation(self):
        """Render validation results"""
        st.header("✅ Data Validation & Council Review")

        if not self.dashboard_data:
            st.error("No validation data available")
            return

        sections = self.dashboard_data.get('sections', [])
        validation_section = next(
            (s for s in sections if 'Validation' in s['title']),
            None
        )

        if not validation_section:
            st.info("No validation section found")
            return

        content = validation_section.get('content', {})
        council_opinion = content.get('council_opinion', {})

        # Council opinion summary
        col1, col2, col3 = st.columns(3)

        with col1:
            recommendation = council_opinion.get('council_recommendation', 'UNKNOWN')
            status_color = '🟢' if recommendation == 'APPROVED' else '🔴'
            st.metric("Council Status", f"{status_color} {recommendation}")

        with col2:
            conf_score = council_opinion.get('confidence_score', 0)
            st.metric("Confidence Score", f"{conf_score*100:.1f}%")

        with col3:
            issues = council_opinion.get('total_issues_found', 0)
            st.metric("Issues Found", issues)

        # Hallucination check
        st.subheader("🛡️ Hallucination Prevention")

        col1, col2 = st.columns(2)

        with col1:
            hallucination_status = content.get('hallucination_check', 'UNKNOWN')
            if hallucination_status == 'PASSED':
                st.success(f"✓ {hallucination_status}")
            else:
                st.error(f"✗ {hallucination_status}")

        with col2:
            data_integrity = content.get('data_integrity', 'UNKNOWN')
            if data_integrity == 'VERIFIED':
                st.success(f"✓ Data Integrity: {data_integrity}")
            else:
                st.warning(f"⚠ Data Integrity: {data_integrity}")

        # Recommendations
        if 'recommendations' in council_opinion:
            st.subheader("Recommendations")
            for i, rec in enumerate(council_opinion['recommendations'], 1):
                st.info(f"{i}. {rec}")

    def run(self):
        """Run the dashboard"""
        self.render_header()

        # Sidebar controls
        filters = self.render_sidebar()

        # Main content tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Overview",
            "Volume Analysis",
            "Correlation",
            "Sector Rotation",
            "Validation"
        ])

        with tab1:
            self.render_overview_metrics()

        with tab2:
            self.render_volume_analysis()

        with tab3:
            self.render_correlation_analysis()

        with tab4:
            self.render_sector_rotation()

        with tab5:
            self.render_validation()

        # Footer
        st.divider()
        st.caption(
            "🤖 Generated by Fintables Money Flow Analysis System | "
            "Data Source: Fintables MCP | "
            "Validation: LLM Council"
        )


if __name__ == "__main__":
    app = DashboardApp()
    app.run()
