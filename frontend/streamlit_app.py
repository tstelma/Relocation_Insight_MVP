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


def to_ordinal(value: int) -> str:
    if 10 <= value % 100 <= 20:
        suffix = "th"
    elif value % 10 == 1:
        suffix = "st"
    elif value % 10 == 2:
        suffix = "nd"
    elif value % 10 == 3:
        suffix = "rd"
    else:
        suffix = "th"
    return f"{value}{suffix}"


def build_rank_message(rank: int, total: int) -> str:
    if rank == 1:
        return "Lowest pressure among selected countries"
    if rank == total:
        return "Highest pressure among selected countries"
    return f"{to_ordinal(rank)} lowest pressure out of {total} selected countries"


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

    # Calculate relative ranking across all countries by category
    df["relative_rank"] = (
        df.groupby("insight_category")["metric_value"]
        .rank(method="min", ascending=True)
    )
    df["category_count"] = df.groupby("insight_category")["metric_value"].transform("count")
    df["relative_rank_message"] = df.apply(
        lambda row: build_rank_message(int(row["relative_rank"]), int(row["category_count"]))
        if pd.notna(row["relative_rank"]) else "Rank unavailable",
        axis=1,
    )

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
    inflation_value = country_data.loc[
        country_data["insight_category"] == "inflation_pressure",
        "metric_value"
    ].mean()
    housing_value = country_data.loc[
        country_data["insight_category"] == "housing_pressure",
        "metric_value"
    ].mean()
    poverty_value = country_data.loc[
        country_data["insight_category"] == "poverty_pressure",
        "metric_value"
    ].mean()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total insights", total_insights)
    col2.metric("High / Very High pressure", high_pressure_count)
    col3.metric(
        "Inflation value",
        f"{inflation_value:.2f}" if pd.notna(inflation_value) else "N/A"
    )
    col4.metric(
        "Housing burden value",
        f"{housing_value:.2f}" if pd.notna(housing_value) else "N/A"
    )
    col5.metric(
        "Poverty risk value",
        f"{poverty_value:.2f}" if pd.notna(poverty_value) else "N/A"
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
            st.write(row['relative_rank_message'])

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

    # Compare two countries
    st.subheader("Compare two countries")
    compare_col1, compare_col2 = st.columns(2)
    from_country = compare_col1.selectbox(
        "From country",
        countries,
        index=0,
        key="from_country"
    )
    to_country = compare_col2.selectbox(
        "To country",
        countries,
        index=1 if len(countries) > 1 else 0,
        key="to_country"
    )

    def get_metric(country_name: str, category: str) -> float | None:
        values = df.loc[
            (df["country_name"] == country_name) &
            (df["insight_category"] == category),
            "metric_value"
        ]
        return values.mean() if not values.empty else None

    from_inflation = get_metric(from_country, "inflation_pressure")
    to_inflation = get_metric(to_country, "inflation_pressure")
    from_housing = get_metric(from_country, "housing_pressure")
    to_housing = get_metric(to_country, "housing_pressure")
    from_poverty = get_metric(from_country, "poverty_pressure")
    to_poverty = get_metric(to_country, "poverty_pressure")

    comparison_rows = []
    for metric_label, from_value, to_value in [
        ("Inflation pressure", from_inflation, to_inflation),
        ("Housing burden", from_housing, to_housing),
        ("Poverty risk", from_poverty, to_poverty),
    ]:
        if from_value is None or to_value is None:
            difference = None
            better = "Data unavailable"
        else:
            difference = to_value - from_value
            if difference < 0:
                better = to_country
            elif difference > 0:
                better = from_country
            else:
                better = "Equal"

        comparison_rows.append({
            "Metric": metric_label,
            "From country value": f"{from_value:.2f}" if pd.notna(from_value) else "N/A",
            "To country value": f"{to_value:.2f}" if pd.notna(to_value) else "N/A",
            "Difference": f"{difference:.2f}" if difference is not None else "N/A",
            "Better country": better,
        })

    comparison_df = pd.DataFrame(comparison_rows)
    st.table(comparison_df)
    st.write("Lower values suggest lower financial pressure for this metric.")

    # Comparison summary
    st.subheader("Comparison summary")
    inflation_better = comparison_rows[0]["Better country"]
    housing_better = comparison_rows[1]["Better country"]
    poverty_better = comparison_rows[2]["Better country"]
    inflation_diff = None if from_inflation is None or to_inflation is None else abs(to_inflation - from_inflation)
    housing_diff = None if from_housing is None or to_housing is None else abs(to_housing - from_housing)
    poverty_diff = None if from_poverty is None or to_poverty is None else abs(to_poverty - from_poverty)

    if (inflation_diff is not None and housing_diff is not None and poverty_diff is not None and
        inflation_diff < 0.5 and housing_diff < 0.5 and poverty_diff < 0.5):
        tradeoff_label = "No major difference"
    elif (inflation_better == housing_better == poverty_better and
          inflation_better not in ["Equal", "Data unavailable"]):
        tradeoff_label = f"Clear advantage for {inflation_better}"
    else:
        tradeoff_label = "Mixed trade-off"

    st.write(f"**Trade-off label:** {tradeoff_label}")

    if (inflation_better == housing_better == poverty_better and
        inflation_better not in ["Equal", "Data unavailable"]):
        summary_text = f"{inflation_better} shows lower pressure across all tracked indicators."
    else:
        summary_text = "This comparison shows a mixed trade-off across the tracked indicators."

    st.write(summary_text)
    st.info(
        "This MVP currently compares inflation pressure, housing burden, and poverty risk. "
        "It does not yet include salary levels, taxes, career opportunities, language, culture, lifestyle preferences, healthcare, "
        "or personal circumstances."
    )

    # Raw data table
    st.header("📋 Raw Data")
    st.dataframe(
        country_data,
        use_container_width=True,
        hide_index=True
    )

if __name__ == "__main__":
    main()