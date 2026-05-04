import streamlit as st
import pandas as pd
from pathlib import Path


# Page configuration
st.set_page_config(
    page_title="Relocation Insight MVP",
    layout="wide"
)

# Data loading
DATA_PATH = Path("data") / "clean" / "all_mvp_insights.csv"
TIMESERIES_DATA_PATH = Path("data") / "clean" / "all_mvp_timeseries.csv"

INDICATOR_LABELS = {
    "inflation_pressure": "Inflation pressure",
    "housing_pressure": "Housing pressure",
    "poverty_pressure": "Poverty pressure",
    "income_capacity": "Income capacity",
}

METRIC_EXPLANATIONS = {
    "inflation_pressure": {
        "definition": "Annual price growth. Lower values usually mean more stable prices.",
        "rule": "Lower inflation = less price pressure.",
    },
    "housing_pressure": {
        "definition": "Share of people spending over 40% of income on housing.",
        "rule": "Lower housing overburden = lower housing stress.",
    },
    "poverty_pressure": {
        "definition": "Share of people below 60% of national median income.",
        "rule": "Lower poverty risk = lower social pressure.",
    },
    "income_capacity": {
        "definition": "Median equivalised net income adjusted for purchasing power.",
        "rule": "Higher PPS income = stronger local purchasing power.",
    },
}

@st.cache_data
def load_insights():
    return pd.read_csv(DATA_PATH)


@st.cache_data
def load_timeseries():
    if not TIMESERIES_DATA_PATH.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(TIMESERIES_DATA_PATH)
    except (pd.errors.EmptyDataError, pd.errors.ParserError, OSError):
        return pd.DataFrame()


def apply_visual_style() -> None:
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1180px;
        }
        div[data-testid="stMetric"] {
            background: var(--secondary-background-color, rgba(128, 128, 128, 0.08));
            border: 1px solid rgba(128, 128, 128, 0.24);
            border-radius: 8px;
            padding: 0.55rem 0.75rem;
            color: var(--text-color, inherit);
        }
        div[data-testid="stMetric"] * {
            color: inherit;
        }
        div[data-testid="stAlert"] {
            border-radius: 8px;
        }
        h1, h2, h3 {
            letter-spacing: 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


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


def render_metric_explanation(category: str) -> None:
    explanation = METRIC_EXPLANATIONS.get(category)
    if explanation is None:
        return

    if hasattr(st, "popover"):
        with st.popover("What is this?"):
            st.write(explanation["definition"])
            st.caption(explanation["rule"])
    else:
        with st.expander("What is this?", expanded=False):
            st.write(explanation["definition"])
            st.caption(explanation["rule"])


def make_compact_message(message: str, max_length: int = 130) -> str:
    if pd.isna(message):
        return ""

    text = str(message).strip()
    if not text:
        return ""

    first_sentence = text.split(". ")[0].strip()
    if first_sentence and not first_sentence.endswith("."):
        first_sentence = f"{first_sentence}."

    if len(first_sentence) <= max_length:
        return first_sentence

    return f"{first_sentence[: max_length - 3].rstrip()}..."


def build_quick_overview(high_pressure_count: int) -> str:
    if high_pressure_count == 0:
        return "No elevated pressure signals detected"
    if high_pressure_count == 1:
        return "1 elevated pressure signal detected"
    return f"{high_pressure_count} elevated pressure signals detected"


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


def get_trend_unit(category: str) -> str:
    if category == "income_capacity":
        return "PPS"
    return "percent"


def format_period_for_display(value) -> str:
    if pd.isna(value):
        return ""

    text = str(value).strip()
    if not text:
        return ""

    year_match = pd.Series([text]).str.extract(r"(\d{4})", expand=False).iloc[0]
    if pd.notna(year_match):
        return str(year_match)

    return text


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
        st.caption("Data unavailable")
        return

    metric_label = get_metric_label(best['insight_category'])
    metric_val = format_metric_value(best['insight_category'], best["metric_value"])
    pressure = best['pressure_label']
    
    st.metric(metric_label, metric_val)
    render_metric_explanation(best["insight_category"])
    st.caption(f"Key pressure signal: {pressure}")
    st.caption(
        f"{metric_label} is the strongest pressure signal because it has the highest pressure level "
        f"among the tracked pressure indicators for this country."
    )


def render_income_capacity_signal(country_data: pd.DataFrame) -> None:
    row = country_data.loc[country_data["insight_category"] == "income_capacity"]
    if row.empty:
        return

    row = row.iloc[0]
    metric_val = format_metric_value(row['insight_category'], row["metric_value"])
    level = row['pressure_label']
    
    st.metric("Income capacity", metric_val)
    render_metric_explanation("income_capacity")
    st.caption(f"Capacity signal: {level}")
    st.caption("Higher values indicate stronger local purchasing power.")


def render_research_checklist(country_data: pd.DataFrame) -> None:
    best = get_key_risk_driver(country_data)

    if best is None:
        checklist = [
            "Estimate net salary",
            "Check city rents",
            "Review jobs and healthcare",
        ]
    else:
        category = best["insight_category"]
        if category == "housing_pressure":
            checklist = [
                "Check city rents",
                "Review lease rules",
                "Estimate rent after salary",
            ]
        elif category == "inflation_pressure":
            checklist = [
                "Check recent inflation",
                "Compare food and energy costs",
                "Review wage growth",
            ]
        elif category == "poverty_pressure":
            checklist = [
                "Check job security",
                "Review social support",
                "Compare regional inequality",
            ]
        else:
            checklist = [
                "Estimate net salary",
                "Check city rents",
                "Review jobs and healthcare",
            ]

    st.markdown("\n".join(f"- {item}" for item in checklist))


def render_data_freshness_note(country_data: pd.DataFrame) -> None:
    periods = [
        format_period_for_display(value)
        for value in country_data["time_period"].dropna().unique()
        if format_period_for_display(value)
    ]
    if not periods:
        st.markdown("*Latest data period used: unavailable*")
        return

    unique_periods = sorted(set(periods), key=lambda value: int(value) if value.isdigit() else value)
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


def render_pressure_signals(country_data: pd.DataFrame) -> None:
    categories = [
        "inflation_pressure",
        "housing_pressure",
        "poverty_pressure",
    ]
    cols = st.columns(3)
    for idx, category in enumerate(categories):
        row = country_data.loc[country_data["insight_category"] == category]
        if row.empty:
            continue
        row = row.iloc[0]
        metric_label = get_metric_label(category)
        metric_val = format_metric_value(category, row["metric_value"])
        with cols[idx]:
            with st.container(border=True):
                st.metric(metric_label, metric_val)
                render_metric_explanation(category)
                st.caption(f"Pressure signal: {row['pressure_label']}")


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


def render_historical_trends(timeseries_df: pd.DataFrame, selected_country: str) -> None:
    st.header("Historical trends")
    st.caption(
        "Historical charts are shown for context only. Trend interpretation will be added later with data-quality checks."
    )

    if timeseries_df.empty:
        st.info("Historical trend data is not available yet. Run the MVP pipeline to create all_mvp_timeseries.csv.")
        return

    required_columns = {
        "country_name",
        "indicator",
        "time_period",
        "metric_value",
        "unit",
    }
    missing_columns = required_columns - set(timeseries_df.columns)
    if missing_columns:
        st.warning("Historical trend data is unavailable because the time-series file has an unexpected schema.")
        return

    countries = sorted(timeseries_df["country_name"].dropna().unique())
    if not countries:
        st.info("Historical trend data is empty.")
        return

    default_country_index = countries.index(selected_country) if selected_country in countries else 0
    available_indicators = [
        indicator
        for indicator in INDICATOR_LABELS
        if indicator in set(timeseries_df["indicator"].dropna())
    ]

    if not available_indicators:
        st.info("No historical indicators are available.")
        return

    trend_col_country, trend_col_indicator = st.columns(2)
    with trend_col_country:
        trend_country = st.selectbox(
            "Country",
            countries,
            index=default_country_index,
            key="trend_country",
        )

    with trend_col_indicator:
        selected_label = st.selectbox(
            "Indicator",
            [INDICATOR_LABELS[indicator] for indicator in available_indicators],
            key="trend_indicator",
        )

    trend_indicator = next(
        indicator
        for indicator in available_indicators
        if INDICATOR_LABELS[indicator] == selected_label
    )

    chart_df = timeseries_df.loc[
        (timeseries_df["country_name"] == trend_country) &
        (timeseries_df["indicator"] == trend_indicator),
        ["time_period", "metric_value", "unit"],
    ].copy()

    if chart_df.empty:
        st.info("No historical rows are available for this country and indicator.")
        return

    chart_df["time_period"] = pd.to_numeric(chart_df["time_period"], errors="coerce")
    chart_df["metric_value"] = pd.to_numeric(chart_df["metric_value"], errors="coerce")
    chart_df = chart_df.dropna(subset=["time_period"]).sort_values("time_period")

    if chart_df.empty or chart_df["metric_value"].dropna().empty:
        st.info("Historical rows exist, but metric values are missing for this selection.")
        return

    unit = get_trend_unit(trend_indicator)
    st.caption(f"Unit: {unit}")
    st.line_chart(
        chart_df,
        x="time_period",
        y="metric_value",
        use_container_width=True,
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

    st.header("Country Profile")

    col_left, col_right = st.columns([3, 1])
    with col_left:
        st.subheader(selected_country)
        st.markdown(f"**Overall assessment:** {overall_pressure}")
    with col_right:
        render_country_profile_export(country_data, selected_country)

    st.markdown("#### Key signals")
    render_pressure_signals(country_data)

    col_key, col_income, col_next = st.columns([1, 1, 1.2])
    with col_key:
        st.markdown("#### Key risk driver")
        render_key_risk_driver(country_data)

    with col_income:
        st.markdown("#### Income capacity")
        render_income_capacity_signal(country_data)

    with col_next:
        st.markdown("#### Suggested next checks")
        render_research_checklist(country_data)

    interpretation_map = {
        "Generally low pressure": "All tracked indicators are low, suggesting a stable financial profile.",
        "Price-stable, social risk visible": "Prices are relatively stable, but poverty risk is showing some social pressure.",
        "Housing stress despite price stability": "Housing costs are high even though inflation is not the main source of pressure.",
        "Price pressure, housing less severe": "Inflation is high while housing pressure remains more moderate.",
        "Social vulnerability despite manageable costs": "Poverty risk is high even though prices and housing pressure are not extreme.",
        "Broad pressure risk": "Multiple indicators show high pressure, suggesting broad financial stress.",
        "Uneven pressure profile": "The country shows a mixed profile across inflation, housing, and poverty pressures."
    }

    with st.expander("Profile interpretation", expanded=False):
        st.write(interpretation_map.get(overall_pressure, "This country has a mixed pressure profile across the tracked indicators."))

    render_data_freshness_note(country_data)


def render_detailed_insights(country_data: pd.DataFrame) -> None:
    st.header("Detailed indicator insights")
    st.caption("Compact signal cards. Open a card note for context and source details.")

    card_columns = st.columns(2)
    for idx, (_, row) in enumerate(country_data.iterrows()):
        metric_label = get_metric_label(row["insight_category"])
        metric_value = format_metric_value(row["insight_category"], row["metric_value"])
        category_label = row["insight_category"].replace("_", " ").title()
        compact_message = make_compact_message(row["main_message"])

        with card_columns[idx % 2]:
            with st.container(border=True):
                top_left, top_right = st.columns([1.5, 1])
                with top_left:
                    st.markdown(f"**{metric_label}**")
                    st.caption(category_label)
                with top_right:
                    st.markdown(f"**{row['pressure_label']}**")
                    st.caption("Signal label")

                st.metric("Value", metric_value)
                render_metric_explanation(row["insight_category"])

                if compact_message:
                    st.caption(compact_message)

                st.caption(f"{row['source']} | {row['confidence_level']} confidence")

                with st.expander("More context", expanded=False):
                    st.write(row["why_it_matters"])
                    st.caption(row["relative_rank_message"])


def main():
    apply_visual_style()

    st.title("Relocation Insight MVP")
    st.caption("Early-stage research signals for selected European countries, based on current MVP indicators.")

    # Load data
    try:
        df = load_insights()
    except FileNotFoundError:
        st.error(f"Data file not found: {DATA_PATH}")
        st.info("Please run the MVP pipeline first: `python data_pipeline/run_mvp_pipeline.py`")
        return

    timeseries_df = load_timeseries()

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

    high_pressure_count = country_data["pressure_label"].isin(["High", "Very High"]).sum()
    high_pressure_text = build_quick_overview(high_pressure_count)
    st.caption(f"Quick overview: {high_pressure_text}")
    st.divider()
    render_country_profile(country_data, selected_country)
    st.divider()

    render_detailed_insights(country_data)
    st.divider()

    render_historical_trends(timeseries_df, selected_country)
    st.divider()

    # Compare two countries
    st.header("Country comparison")
    
    # Country selectors
    comp_col1, comp_col2 = st.columns(2)
    with comp_col1:
        from_country = st.selectbox(
            "From country",
            countries,
            index=0,
            key="from_country"
        )
    with comp_col2:
        to_country = st.selectbox(
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
    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True,
    )
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

    st.markdown(f"**Trade-off label:** {tradeoff_label}")

    if (inflation_better == housing_better == poverty_better == income_better and
        inflation_better not in ["Equal", "Data unavailable"]):
        summary_text = f"{inflation_better} shows better pressure and income capacity across the tracked indicators."
    else:
        summary_text = "This comparison shows a mixed trade-off across the tracked indicators."

    st.write(summary_text)
    render_comparison_verdict(comparison_df, from_country, to_country)
    st.divider()

    st.header("Methodology / Disclaimer")
    render_methodology_notes()
    with st.expander("MVP limitations", expanded=False):
        st.write(
            "This MVP currently compares inflation pressure, housing burden, poverty risk, and income capacity. "
            "It does not yet include salary levels, taxes, career opportunities, language, culture, lifestyle preferences, healthcare, "
            "or personal circumstances."
        )

    with st.expander("Raw data", expanded=False):
        st.dataframe(
            country_data,
            use_container_width=True,
            hide_index=True
        )

if __name__ == "__main__":
    main()
