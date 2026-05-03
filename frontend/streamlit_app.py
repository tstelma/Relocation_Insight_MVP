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


def build_rank_message(category: str, rank: int, total: int) -> str:
    if category == "income_capacity":
        if rank == 1:
            return "Highest income capacity among selected countries"
        if rank == total:
            return "Lowest income capacity among selected countries"
        return f"{to_ordinal(rank)} highest income capacity out of {total} selected countries"

    if rank == 1:
        return "Lowest pressure among selected countries"
    if rank == total:
        return "Highest pressure among selected countries"
    return f"{to_ordinal(rank)} lowest pressure out of {total} selected countries"


def get_metric_label(category: str) -> str:
    """Map insight category to human-readable metric label."""
    labels = {
        "inflation_pressure": "Annual inflation rate",
        "housing_pressure": "Housing overburden rate",
        "poverty_pressure": "At-risk-of-poverty rate",
        "income_capacity": "Income capacity"
    }
    return labels.get(category, category.replace("_", " ").title())


def format_percentage(value: float | None) -> str:
    """Format value as percentage string."""
    if pd.isna(value):
        return "N/A"
    return f"{value:.2f}%"


def format_metric_value(category: str, value: float | None) -> str:
    if pd.isna(value):
        return "N/A"
    if category == "income_capacity":
        return f"{value:,.0f} PPS"
    return format_percentage(value)


def is_higher_better(category: str) -> bool:
    return category == "income_capacity"


def get_overall_pressure(country_data: pd.DataFrame) -> str:
    inflation_label = country_data.loc[
        country_data["insight_category"] == "inflation_pressure",
        "pressure_label"
    ].values[0] if len(country_data[country_data["insight_category"] == "inflation_pressure"]) > 0 else None

    housing_label = country_data.loc[
        country_data["insight_category"] == "housing_pressure",
        "pressure_label"
    ].values[0] if len(country_data[country_data["insight_category"] == "housing_pressure"]) > 0 else None

    poverty_label = country_data.loc[
        country_data["insight_category"] == "poverty_pressure",
        "pressure_label"
    ].values[0] if len(country_data[country_data["insight_category"] == "poverty_pressure"]) > 0 else None

    if all([inflation_label == "Low", housing_label == "Low", poverty_label == "Low"]):
        return "Generally low pressure"
    if (inflation_label in ["Low", "Moderate"] and housing_label == "Low" and 
            poverty_label in ["Moderate", "High", "Very High"]):
        return "Price-stable, social risk visible"
    if (inflation_label in ["Low", "Moderate"] and housing_label in ["High", "Very High"]):
        return "Housing stress despite price stability"
    if (inflation_label in ["High", "Very High"] and housing_label in ["Low", "Moderate"]):
        return "Price pressure, housing less severe"
    if (poverty_label in ["High", "Very High"] and inflation_label in ["Low", "Moderate"] and
            housing_label in ["Low", "Moderate"]):
        return "Social vulnerability despite manageable costs"
    if country_data["pressure_label"].isin(["High", "Very High"]).sum() >= 2:
        return "Broad pressure risk"
    return "Uneven pressure profile"


def get_key_risk_driver(country_data: pd.DataFrame):
    pressure_categories = {"inflation_pressure", "housing_pressure", "poverty_pressure"}
    severity_map = {
        "Low": 1,
        "Moderate": 2,
        "High": 3,
        "Very High": 4,
    }
    candidates = []
    for _, row in country_data.iterrows():
        if row["insight_category"] not in pressure_categories:
            continue
        severity = severity_map.get(row["pressure_label"])
        if severity is None:
            continue
        metric_value = row["metric_value"] if pd.notna(row["metric_value"]) else float("-inf")
        candidates.append((severity, metric_value, row))

    if not candidates:
        return None

    return max(candidates, key=lambda entry: (entry[0], entry[1]))[2]


def render_key_risk_driver(country_data: pd.DataFrame) -> None:
    best = get_key_risk_driver(country_data)
    if best is None:
        st.markdown("**Key risk driver:** Data unavailable")
        return

    st.markdown("**Key risk driver**")
    st.markdown(f"**{get_metric_label(best['insight_category'])}**")
    st.write(format_metric_value(best['insight_category'], best["metric_value"]))
    st.caption(f"{best['pressure_label']} • {best.get('relative_rank_message', '')}")

    explanations = {
        "Low": "This indicator is the strongest signal, but the pressure level remains low.",
        "Moderate": "This indicator shows moderate pressure and should be monitored.",
        "High": "This indicator is a high pressure signal and may be a key relocation concern.",
        "Very High": "This indicator is the strongest risk driver, suggesting significant pressure.",
    }
    st.write(explanations.get(best["pressure_label"], "This is the leading pressure signal for this country."))


def render_income_capacity_signal(country_data: pd.DataFrame) -> None:
    row = country_data.loc[country_data["insight_category"] == "income_capacity"]
    if row.empty:
        return

    row = row.iloc[0]
    st.markdown("**Supporting income capacity signal**")
    st.markdown(f"**{get_metric_label(row['insight_category'])}**")
    st.write(format_metric_value(row['insight_category'], row["metric_value"]))
    st.caption(f"{row['pressure_label']} income capacity • {row.get('relative_rank_message', '')}")
    st.write(
        "Higher income capacity suggests stronger local purchasing power and a better starting point for relocation decisions."
    )


def render_research_checklist(country_data: pd.DataFrame) -> None:
    best = get_key_risk_driver(country_data)
    st.markdown("**Suggested next checks**")

    if best is None:
        checklist = [
            "Review salary after tax and cost of living.",
            "Compare local rent and housing affordability.",
            "Assess job market stability and healthcare access.",
        ]
    else:
        category = best["insight_category"]
        if category == "housing_pressure":
            checklist = [
                "Check city-level rents and rental availability.",
                "Review local deposit and lease rules.",
                "Estimate net salary after rent and housing costs.",
            ]
        elif category == "inflation_pressure":
            checklist = [
                "Review recent monthly inflation trends.",
                "Compare grocery and energy cost changes.",
                "Assess wage growth relative to inflation.",
            ]
        elif category == "poverty_pressure":
            checklist = [
                "Check job security and employment stability.",
                "Review income distribution and social benefits.",
                "Consider regional inequality and local support services.",
            ]
            income_row = country_data.loc[country_data["insight_category"] == "income_capacity"]
            if not income_row.empty and income_row.iloc[0]["pressure_label"] == "Low":
                checklist.append(
                    "Compare local purchasing power and income capacity when median income capacity appears weak."
                )
        else:
            checklist = [
                "Review salary after tax and cost of living.",
                "Compare local rent and housing affordability.",
                "Assess job market stability and healthcare access.",
            ]

    st.markdown("\n".join(f"- {item}" for item in checklist))


def render_data_freshness_note(country_data: pd.DataFrame) -> None:
    periods = [
        str(value).strip()
        for value in country_data["time_period"].dropna().unique()
        if str(value).strip()
    ]
    if not periods:
        st.markdown("*Latest data period used: unavailable*")
        return

    unique_periods = sorted(set(periods))
    latest_period = unique_periods[-1]
    if len(unique_periods) > 1:
        st.markdown(f"*Latest data period used: {latest_period}. Some indicators may use earlier available periods.*")
    else:
        st.markdown(f"*Latest data period used: {latest_period}*")


def render_country_profile_export(country_data: pd.DataFrame, selected_country: str) -> None:
    if country_data.empty:
        st.info("No country profile data available to export.")
        return

    csv_bytes = country_data.to_csv(index=False).encode("utf-8")
    safe_name = "".join(
        ch if ch.isalnum() or ch in {" ", "-", "_"} else "_"
        for ch in selected_country
    ).strip().lower().replace(" ", "_")
    filename = f"{safe_name}_relocation_pressure_profile.csv"

    st.download_button(
        label="Export selected country profile",
        data=csv_bytes,
        file_name=filename,
        mime="text/csv",
    )


def render_methodology_notes() -> None:
    with st.expander("Methodology notes"):
        st.write(
            "Inflation pressure uses annual inflation rate from Eurostat HICP. "
            "Housing pressure uses housing overburden rate from Eurostat SILC. "
            "Poverty pressure uses at-risk-of-poverty rate from Eurostat SILC."
        )
        st.write(
            "Income capacity uses median equivalised net income from Eurostat ilc_di03, expressed in PPS. "
            "Higher income capacity values are better, unlike the cost pressure indicators."
        )
        st.write(
            "Pressure labels are simplified MVP categories for early-stage signals only, "
            "not detailed economic diagnostics. Country comparisons are signals, not full relocation recommendations."
        )


def render_comparison_verdict(comparison_df: pd.DataFrame, country_a: str, country_b: str) -> None:
    if comparison_df.empty:
        st.write("_Comparison verdict: insufficient data for a directional signal based only on the current MVP indicators._")
        return

    a_wins = (comparison_df["Better country"] == country_a).sum()
    b_wins = (comparison_df["Better country"] == country_b).sum()
    valid_rows = comparison_df[comparison_df["Better country"].isin([country_a, country_b, "Equal"])]

    if valid_rows.empty:
        st.write("_Comparison verdict: insufficient data for a directional signal based only on the current MVP indicators._")
        return

    if a_wins > b_wins:
        verdict = f"{country_a} has an overall MVP advantage across the available indicators."
    elif b_wins > a_wins:
        verdict = f"{country_b} has an overall MVP advantage across the available indicators."
    else:
        verdict = "The comparison is mixed across the available indicators."

    st.write(f"**Comparison verdict:** {verdict} _This is directional only and based only on the current MVP indicators._")


def render_country_profile(country_data: pd.DataFrame, selected_country: str) -> None:
    overall_pressure = get_overall_pressure(country_data)

    st.subheader("Country Profile")
    st.markdown(f"**{selected_country}**")
    st.markdown(f"**Overall pressure snapshot:** {overall_pressure}")
    render_country_profile_export(country_data, selected_country)
    render_key_risk_driver(country_data)
    render_income_capacity_signal(country_data)
    render_research_checklist(country_data)
    render_data_freshness_note(country_data)
    render_methodology_notes()

    indicator_categories = [
        "inflation_pressure",
        "housing_pressure",
        "poverty_pressure",
        "income_capacity",
    ]
    cols = st.columns(4)

    for idx, category in enumerate(indicator_categories):
        row = country_data.loc[country_data["insight_category"] == category]
        if row.empty:
            continue
        row = row.iloc[0]
        with cols[idx]:
            st.markdown(f"**{get_metric_label(category)}**")
            st.write(format_metric_value(category, row["metric_value"]))
            caption_label = row['pressure_label']
            if category == "income_capacity":
                caption_label = f"{caption_label} income capacity"
            st.caption(f"{caption_label} • {row['relative_rank_message']}")

    interpretation_map = {
        "Generally low pressure": "All tracked indicators are low, suggesting a stable financial profile.",
        "Price-stable, social risk visible": "Prices are relatively stable, but poverty risk is showing some social pressure.",
        "Housing stress despite price stability": "Housing costs are high even though inflation is not the main source of pressure.",
        "Price pressure, housing less severe": "Inflation is high while housing pressure remains more moderate.",
        "Social vulnerability despite manageable costs": "Poverty risk is high even though prices and housing pressure are not extreme.",
        "Broad pressure risk": "Multiple indicators show high pressure, suggesting broad financial stress.",
        "Uneven pressure profile": "The country shows a mixed profile across inflation, housing, and poverty pressures."
    }
    st.write(interpretation_map.get(overall_pressure, "This country has a mixed pressure profile across the tracked indicators."))


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
    def rank_group(group: pd.DataFrame) -> pd.Series:
        ascending = group.name != "income_capacity"
        return group["metric_value"].rank(method="min", ascending=ascending)

    df["relative_rank"] = df.groupby("insight_category", group_keys=False).apply(rank_group)
    df["category_count"] = df.groupby("insight_category")["metric_value"].transform("count")
    df["relative_rank_message"] = df.apply(
        lambda row: build_rank_message(
            row["insight_category"],
            int(row["relative_rank"]),
            int(row["category_count"]),
        ) if pd.notna(row["relative_rank"]) else "Rank unavailable",
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
    st.divider()

    # Country pressure summary
    st.subheader("Country pressure snapshot")
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

    # Calculate overall pressure snapshot
    # Extract pressure labels for each category
    inflation_label = country_data.loc[
        country_data["insight_category"] == "inflation_pressure",
        "pressure_label"
    ].values[0] if len(country_data[country_data["insight_category"] == "inflation_pressure"]) > 0 else None

    housing_label = country_data.loc[
        country_data["insight_category"] == "housing_pressure",
        "pressure_label"
    ].values[0] if len(country_data[country_data["insight_category"] == "housing_pressure"]) > 0 else None

    poverty_label = country_data.loc[
        country_data["insight_category"] == "poverty_pressure",
        "pressure_label"
    ].values[0] if len(country_data[country_data["insight_category"] == "poverty_pressure"]) > 0 else None

    # Apply pattern-based rules for overall pressure snapshot
    if all([inflation_label == "Low", housing_label == "Low", poverty_label == "Low"]):
        overall_pressure = "Generally low pressure"
    elif (inflation_label in ["Low", "Moderate"] and housing_label == "Low" and 
          poverty_label in ["Moderate", "High", "Very High"]):
        overall_pressure = "Price-stable, social risk visible"
    elif (inflation_label in ["Low", "Moderate"] and housing_label in ["High", "Very High"]):
        overall_pressure = "Housing stress despite price stability"
    elif (inflation_label in ["High", "Very High"] and housing_label in ["Low", "Moderate"]):
        overall_pressure = "Price pressure, housing less severe"
    elif (poverty_label in ["High", "Very High"] and inflation_label in ["Low", "Moderate"] and
          housing_label in ["Low", "Moderate"]):
        overall_pressure = "Social vulnerability despite manageable costs"
    elif country_data["pressure_label"].isin(["High", "Very High"]).sum() >= 2:
        overall_pressure = "Broad pressure risk"
    else:
        overall_pressure = "Uneven pressure profile"

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

    st.divider()
    render_country_profile(country_data, selected_country)
    st.divider()

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
                label=get_metric_label(row['insight_category']),
                value=format_metric_value(row['insight_category'], row['metric_value'])
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
    st.subheader("Country comparison")
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
    from_income_capacity = get_metric(from_country, "income_capacity")
    to_income_capacity = get_metric(to_country, "income_capacity")

    comparison_rows = []
    for metric_label, category, from_value, to_value in [
        ("Annual inflation rate", "inflation_pressure", from_inflation, to_inflation),
        ("Housing overburden rate", "housing_pressure", from_housing, to_housing),
        ("At-risk-of-poverty rate", "poverty_pressure", from_poverty, to_poverty),
        ("Income capacity", "income_capacity", from_income_capacity, to_income_capacity),
    ]:
        if from_value is None or to_value is None:
            difference = None
            better = "Data unavailable"
        else:
            difference = to_value - from_value
            if difference == 0:
                better = "Equal"
            else:
                higher_is_better = is_higher_better(category)
                if (difference > 0) == higher_is_better:
                    better = to_country
                else:
                    better = from_country

        comparison_rows.append({
            "Metric": metric_label,
            "From country value": format_metric_value(category, from_value),
            "To country value": format_metric_value(category, to_value),
            "Difference": (
                f"{difference:+.2f}%" if difference is not None and category != "income_capacity"
                else f"{difference:+,.0f} PPS" if difference is not None
                else "N/A"
            ),
            "Better country": better,
        })

    comparison_df = pd.DataFrame(comparison_rows)
    st.table(comparison_df)
    st.caption("Lower values indicate lower pressure; higher values indicate stronger income capacity.")
    st.divider()

    # Comparison summary
    st.subheader("Comparison summary and verdict")
    inflation_better = comparison_rows[0]["Better country"]
    housing_better = comparison_rows[1]["Better country"]
    poverty_better = comparison_rows[2]["Better country"]
    income_better = comparison_rows[3]["Better country"]
    inflation_diff = None if from_inflation is None or to_inflation is None else abs(to_inflation - from_inflation)
    housing_diff = None if from_housing is None or to_housing is None else abs(to_housing - from_housing)
    poverty_diff = None if from_poverty is None or to_poverty is None else abs(to_poverty - from_poverty)
    income_diff = None if from_income_capacity is None or to_income_capacity is None else abs(to_income_capacity - from_income_capacity)

    if (inflation_diff is not None and housing_diff is not None and poverty_diff is not None and income_diff is not None and
        inflation_diff < 0.5 and housing_diff < 0.5 and poverty_diff < 0.5 and income_diff < 500):
        tradeoff_label = "No major difference"
    elif (inflation_better == housing_better == poverty_better == income_better and
          inflation_better not in ["Equal", "Data unavailable"]):
        tradeoff_label = f"Clear advantage for {inflation_better}"
    else:
        tradeoff_label = "Mixed trade-off"

    st.write(f"**Trade-off label:** {tradeoff_label}")

    if (inflation_better == housing_better == poverty_better == income_better and
        inflation_better not in ["Equal", "Data unavailable"]):
        summary_text = f"{inflation_better} shows better pressure and income capacity across the tracked indicators."
    else:
        summary_text = "This comparison shows a mixed trade-off across the tracked indicators."

    st.write(summary_text)
    render_comparison_verdict(comparison_df, from_country, to_country)
    st.info(
        "This MVP currently compares inflation pressure, housing burden, and poverty risk. "
        "It does not yet include salary levels, taxes, career opportunities, language, culture, lifestyle preferences, healthcare, "
        "or personal circumstances."
    )
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