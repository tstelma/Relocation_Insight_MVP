import streamlit as st
import pandas as pd
from pathlib import Path


# Page configuration
st.set_page_config(
    page_title="Relocation Insight MVP",
    page_icon="🏠",
    layout="wide"
)

# Data loading
DATA_PATH = Path("data") / "clean" / "all_mvp_insights.csv"

@st.cache_data
def load_insights():
    return pd.read_csv(DATA_PATH)

def main():
    st.title("🏠 Relocation Insight MVP")
    st.markdown("*Explore early financial pressure insights for selected European countries.*")

    # Load data
    try:
        df = load_insights()
    except FileNotFoundError:
        st.error(f"Data file not found: {DATA_PATH}")
        st.info("Please run the MVP pipeline first: `python data_pipeline/run_mvp_pipeline.py`")
        return

    # Country selector
    countries = sorted(df['country_name'].unique())
    selected_country = st.selectbox(
        "Select a country to view insights:",
        countries,
        index=0
    )

    # Filter data for selected country
    country_data = df[df['country_name'] == selected_country]

    if country_data.empty:
        st.warning(f"No data available for {selected_country}")
        return

    st.header(f"📊 Insights for {selected_country}")

    # Country pressure summary
    st.subheader("Country pressure summary")
    total_insights = len(country_data)
    high_pressure_count = country_data["pressure_label"].isin(["High", "Very High"]).sum()
    average_metric_value = country_data["metric_value"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total insights", total_insights)
    col2.metric("High / Very High pressure", high_pressure_count)
    col3.metric(
        "Average metric value",
        f"{average_metric_value:.2f}" if pd.notna(average_metric_value) else "N/A"
    )

    # Display insight cards
    for _, row in country_data.iterrows():
        with st.container():
            # Card header
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.subheader(f"📈 {row['title']}")
            with col2:
                st.caption(f"Category: {row['insight_category'].replace('_', ' ').title()}")
            with col3:
                pressure_color = {
                    'Low': '🟢',
                    'Moderate': '🟡',
                    'High': '🟠',
                    'Very High': '🔴'
                }.get(row['pressure_label'], '⚪')
                st.caption(f"{pressure_color} {row['pressure_label']}")

            # Metric value
            st.metric(
                label="Latest Value",
                value=f"{row['metric_value']:.2f}" if pd.notna(row['metric_value']) else "N/A"
            )

            # Main message
            st.info(row['main_message'])

            # Why it matters
            with st.expander("💡 Why it matters"):
                st.write(row['why_it_matters'])

            # Source and confidence
            col1, col2 = st.columns(2)
            with col1:
                st.caption(f"📊 Source: {row['source']}")
            with col2:
                confidence_icon = "✅" if row['confidence_level'] == "High" else "⚠️"
                st.caption(f"{confidence_icon} Confidence: {row['confidence_level']}")

            st.divider()

    # Raw data table
    st.header("📋 Raw Data")
    st.dataframe(
        country_data,
        use_container_width=True,
        hide_index=True
    )

if __name__ == "__main__":
    main()