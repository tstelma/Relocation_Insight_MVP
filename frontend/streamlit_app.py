import streamlit as st
import pandas as pd
import html
from pathlib import Path


# Page configuration
st.set_page_config(
    page_title="Relocation Insight MVP",
    layout="wide"
)

# Data loading
APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent
DATA_PATH = PROJECT_ROOT / "data" / "clean" / "all_mvp_insights.csv"
TIMESERIES_DATA_PATH = PROJECT_ROOT / "data" / "clean" / "all_mvp_timeseries.csv"
REQUIRED_DATA_PATHS = (DATA_PATH, TIMESERIES_DATA_PATH)

INSIGHTS_REQUIRED_COLUMNS = {
    "insight_category",
    "country_code",
    "country_name",
    "time_period",
    "metric_value",
    "pressure_label",
    "main_message",
    "why_it_matters",
    "confidence_level",
    "source",
}
TIMESERIES_REQUIRED_COLUMNS = {
    "country_code",
    "country_name",
    "indicator",
    "time_period",
    "metric_value",
    "unit",
    "better_direction",
    "source",
}

INDICATOR_LABELS = {
    "inflation_pressure": "Inflation pressure",
    "housing_pressure": "Housing pressure",
    "poverty_pressure": "Poverty pressure",
    "income_capacity": "Income capacity",
    "net_earnings_capacity": "Net earnings capacity",
    "employment_strength": "Employment strength",
}

PRESSURE_CATEGORIES = {
    "inflation_pressure",
    "housing_pressure",
    "poverty_pressure",
}

CAPACITY_CATEGORIES = {
    "income_capacity",
    "net_earnings_capacity",
}

STRENGTH_CATEGORIES = {
    "employment_strength",
}

HIGHER_IS_BETTER_CATEGORIES = CAPACITY_CATEGORIES | STRENGTH_CATEGORIES

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
    "net_earnings_capacity": {
        "definition": "Annual net earnings for a single person without children earning 100% of average earnings.",
        "rule": "Higher PPS net earnings = stronger working-person earnings capacity.",
    },
    "employment_strength": {
        "definition": "Working-age employment rate for people aged 20-64.",
        "rule": "Higher employment rate = stronger labour-market participation signal.",
    },
}

def get_file_modified_ns(path: Path) -> int | None:
    if not path.exists():
        return None
    return path.stat().st_mtime_ns


@st.cache_data
def load_insights(path: str, modified_ns: int | None):
    return pd.read_csv(path)


@st.cache_data
def load_timeseries(path: str, modified_ns: int | None):
    return pd.read_csv(path)


def format_repo_path(path: Path) -> str:
    try:
        return path.relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def show_data_file_error(missing_paths: list[Path]) -> None:
    st.error("Required CSV data files are missing.")
    st.markdown("\n".join(f"- `{format_repo_path(path)}`" for path in missing_paths))
    st.info(
        "Run `python data_pipeline/run_mvp_pipeline.py` locally, then commit the generated "
        "`data/clean/` CSV files before deploying."
    )


def validate_required_columns(df: pd.DataFrame, required_columns: set[str], file_path: Path) -> bool:
    missing_columns = sorted(required_columns - set(df.columns))
    if not missing_columns:
        return True

    st.error(f"`{format_repo_path(file_path)}` has an unexpected schema.")
    st.markdown("Missing columns: " + ", ".join(f"`{column}`" for column in missing_columns))
    st.info("Regenerate the data with `python data_pipeline/run_mvp_pipeline.py` before deploying.")
    return False


def apply_visual_style() -> None:
    st.markdown(
        """
        <style>
        :root {
            --app-bg: #090f1c;
            --app-bg-2: #0d1424;
            --surface: #111a2c;
            --surface-raised: #151f33;
            --surface-soft: rgba(21, 31, 51, 0.78);
            --border: rgba(148, 163, 184, 0.18);
            --border-strong: rgba(148, 163, 184, 0.28);
            --text-main: #f4f7fb;
            --text-soft: #d3dbe7;
            --text-muted: #aebbd0;
            --text-faint: #8ea0ba;
            --accent: #8b9cff;
            --accent-soft: rgba(139, 156, 255, 0.14);
            --accent-border: rgba(139, 156, 255, 0.34);
            --shadow: 0 18px 52px rgba(0, 0, 0, 0.28);
        }
        .stApp {
            background:
                radial-gradient(circle at 18% 0%, rgba(139, 156, 255, 0.16), transparent 28rem),
                radial-gradient(circle at 88% 12%, rgba(45, 212, 191, 0.08), transparent 22rem),
                linear-gradient(180deg, var(--app-bg) 0%, var(--app-bg-2) 48%, #09111f 100%);
            color: var(--text-main);
        }
        .block-container {
            padding-top: 2.15rem;
            padding-bottom: 3.4rem;
            max-width: 1180px;
        }
        h1 {
            font-size: 2.25rem;
            font-weight: 740;
            margin-bottom: 0.2rem;
            color: var(--text-main);
        }
        h2 {
            font-size: 1.18rem;
            font-weight: 700;
            margin-top: 0.45rem;
            margin-bottom: 0.18rem;
            color: var(--text-main);
        }
        h3 {
            font-size: 0.96rem;
            font-weight: 680;
            margin-bottom: 0.15rem;
            color: var(--text-main);
        }
        h1, h2, h3 {
            letter-spacing: 0;
        }
        p, li, label, span {
            color: inherit;
        }
        div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stMarkdownContainer"] li {
            color: var(--text-soft);
            font-size: 0.95rem;
            line-height: 1.52;
        }
        div[data-testid="stMarkdownContainer"] strong {
            color: var(--text-main);
            font-weight: 700;
        }
        div[data-testid="stCaptionContainer"] {
            color: var(--text-faint);
            font-size: 0.83rem;
            line-height: 1.35;
        }
        div[data-testid="stCaptionContainer"] * {
            color: var(--text-faint);
        }
        div[data-testid="stMetric"] {
            background: rgba(9, 15, 28, 0.5);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 0.58rem 0.72rem;
            color: var(--text-main);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04);
        }
        div[data-testid="stMetric"] * {
            color: var(--text-main);
        }
        div[data-testid="stMetric"] label {
            color: var(--text-muted);
            font-size: 0.78rem;
            font-weight: 620;
        }
        div[data-testid="stMetricValue"] {
            color: var(--text-main);
            font-size: 1.62rem;
            font-weight: 780;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: linear-gradient(180deg, rgba(21, 31, 51, 0.96), rgba(17, 26, 44, 0.96));
            border: 1px solid var(--border);
            border-radius: 16px;
            box-shadow: var(--shadow);
            padding: 0.14rem;
        }
        div[data-testid="stExpander"] {
            background: rgba(9, 15, 28, 0.46);
            border: 1px solid var(--border);
            border-radius: 12px;
            color: var(--text-soft);
        }
        div[data-testid="stAlert"] {
            background: rgba(21, 31, 51, 0.92);
            border: 1px solid var(--border);
            border-radius: 12px;
            color: var(--text-soft);
        }
        hr {
            margin: 1.65rem 0;
            border-color: rgba(148, 163, 184, 0.16);
        }
        div[data-testid="stDownloadButton"] button,
        div[data-testid="stPopover"] button {
            background: var(--accent-soft);
            border: 1px solid var(--accent-border);
            border-radius: 999px;
            color: #c8d0ff;
            font-weight: 620;
            min-height: 2rem;
        }
        div[data-testid="stDownloadButton"] button:hover,
        div[data-testid="stPopover"] button:hover {
            border-color: rgba(139, 156, 255, 0.62);
            color: var(--accent);
            background: rgba(139, 156, 255, 0.2);
        }
        div[data-testid="stSelectbox"] label,
        div[data-testid="stSelectbox"] div {
            color: var(--text-soft);
        }
        div[data-baseweb="select"] > div {
            background: rgba(9, 15, 28, 0.76);
            border-color: var(--border-strong);
            border-radius: 12px;
            color: var(--text-main);
        }
        div[data-testid="stDataFrame"] {
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
        }
        .app-hero {
            padding: 1.25rem 1.35rem;
            margin-bottom: 1rem;
            border: 1px solid var(--border);
            border-radius: 18px;
            background:
                linear-gradient(135deg, rgba(139, 156, 255, 0.12), transparent 42%),
                rgba(17, 26, 44, 0.72);
            box-shadow: var(--shadow);
        }
        .app-kicker {
            color: var(--accent);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            text-transform: uppercase;
            margin: 0 0 0.22rem;
        }
        .app-title {
            color: var(--text-main);
            font-size: 2.15rem;
            font-weight: 780;
            line-height: 1.08;
            margin: 0;
        }
        .app-subtitle {
            color: var(--text-muted);
            font-size: 0.98rem;
            line-height: 1.5;
            max-width: 740px;
            margin: 0.42rem 0 0;
        }
        .section-kicker {
            color: var(--text-faint);
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            margin: 0 0 0.12rem;
        }
        .section-title {
            color: var(--text-main);
            font-size: 1.18rem;
            font-weight: 740;
            line-height: 1.2;
            margin: 0 0 0.2rem;
        }
        .section-subtitle {
            color: var(--text-muted);
            font-size: 0.92rem;
            line-height: 1.45;
            margin: 0 0 0.7rem;
        }
        .signal-text {
            color: var(--text-soft);
            font-size: 0.95rem;
            line-height: 1.45;
            margin: 0.2rem 0 0.55rem;
        }
        .status-pill {
            display: inline-flex;
            align-items: center;
            width: fit-content;
            margin: 0.25rem 0 0.35rem;
            padding: 0.22rem 0.58rem;
            border: 1px solid var(--accent-border);
            border-radius: 999px;
            background: var(--accent-soft);
            color: #dbe2ff;
            font-size: 0.8rem;
            font-weight: 720;
            line-height: 1.2;
        }
        .metadata-text {
            color: var(--text-faint);
            font-size: 0.8rem;
            line-height: 1.35;
            margin-top: 0.35rem;
        }
        .country-profile-card {
            margin-top: 0.55rem;
            padding: 0.9rem 1rem 0.85rem;
            border: 1px solid var(--border);
            border-radius: 16px;
            background:
                linear-gradient(135deg, rgba(139, 156, 255, 0.11), transparent 46%),
                rgba(17, 26, 44, 0.82);
            box-shadow:
                inset 0 1px 0 rgba(255, 255, 255, 0.04),
                0 14px 36px rgba(0, 0, 0, 0.18);
        }
        .country-eyebrow {
            color: var(--text-faint);
            font-size: 0.74rem;
            font-weight: 720;
            letter-spacing: 0.05em;
            margin: 0 0 0.28rem;
            text-transform: uppercase;
        }
        .country-title {
            color: var(--text-main);
            font-size: 3.05rem;
            font-weight: 820;
            letter-spacing: 0;
            line-height: 1.02;
            margin: 0;
            overflow-wrap: anywhere;
        }
        .country-title-flag,
        .top-signal-flag {
            display: inline-block;
            border-radius: 3px;
            object-fit: cover;
            vertical-align: middle;
            box-shadow: 0 0 0 1px rgba(148, 163, 184, 0.24);
        }
        .country-title-flag {
            margin-right: 0.58rem;
            transform: translateY(-0.08rem);
        }
        .top-signal-flag {
            margin-right: 0.34rem;
        }
        .comparison-metric {
            color: var(--text-main);
            font-size: 0.95rem;
            font-weight: 720;
            line-height: 1.25;
            margin-bottom: 0.4rem;
        }
        .comparison-value-label {
            color: var(--text-faint);
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            margin-bottom: 0.12rem;
            text-transform: uppercase;
        }
        .comparison-value-large {
            color: var(--text-main);
            font-size: 1.32rem;
            font-weight: 780;
            line-height: 1.15;
            margin-bottom: 0.35rem;
        }
        .trend-stat-label {
            color: var(--text-faint);
            font-size: 0.72rem;
            font-weight: 720;
            letter-spacing: 0.04em;
            line-height: 1.2;
            margin: 0.2rem 0 0.12rem;
            text-transform: uppercase;
        }
        .trend-stat-value {
            color: var(--text-main);
            font-size: 1rem;
            font-weight: 740;
            line-height: 1.2;
            margin: 0 0 0.25rem;
        }
        .comparison-row {
            display: grid;
            grid-template-columns: 1.2fr 1fr 1fr 0.9fr;
            gap: 0.75rem;
            align-items: center;
            padding: 0.78rem 0;
            border-bottom: 1px solid rgba(148, 163, 184, 0.12);
        }
        .comparison-row:last-child {
            border-bottom: 0;
        }
        .comparison-label {
            color: var(--text-main);
            font-weight: 700;
            font-size: 0.92rem;
        }
        .comparison-value {
            color: var(--text-soft);
            font-size: 0.9rem;
        }
        .comparison-better {
            color: #dbe2ff;
            font-size: 0.86rem;
            font-weight: 700;
        }
        .top-signal-card-title {
            color: var(--text-main);
            font-size: 0.94rem;
            font-weight: 760;
            line-height: 1.2;
            margin: 0 0 0.06rem;
        }
        .top-signal-card-subtitle {
            color: var(--text-faint);
            font-size: 0.74rem;
            line-height: 1.3;
            margin: 0 0 0.22rem;
        }
        .top-signal-row {
            display: grid;
            grid-template-columns: 1.85rem minmax(7rem, 0.78fr) max-content;
            gap: 0.34rem;
            align-items: center;
            max-width: 25rem;
            padding: 0.26rem 0;
            border-bottom: 1px solid rgba(148, 163, 184, 0.12);
        }
        .top-signal-row:last-child {
            border-bottom: 0;
            padding-bottom: 0.05rem;
        }
        .top-signal-rank {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 1.62rem;
            height: 1.62rem;
            border: 1px solid rgba(148, 163, 184, 0.3);
            border-radius: 999px;
            background: rgba(9, 15, 28, 0.46);
            color: var(--text-main);
            font-size: 0.92rem;
            font-weight: 800;
            line-height: 1;
        }
        .top-signal-country {
            color: var(--text-main);
            font-size: 0.96rem;
            font-weight: 800;
            line-height: 1.22;
            overflow-wrap: anywhere;
        }
        .top-signal-value {
            color: var(--text-main);
            font-size: 0.92rem;
            font-weight: 800;
            line-height: 1.2;
            white-space: nowrap;
            text-align: right;
        }
        .top-signal-panel {
            margin-top: 0.1rem;
        }
        .top-signal-panel div[data-testid="stTabs"] button {
            padding: 0.25rem 0.42rem;
            min-height: 1.9rem;
            font-size: 0.78rem;
        }
        @media (max-width: 760px) {
            .app-title {
                font-size: 1.72rem;
            }
            .country-title {
                font-size: 2.35rem;
            }
            .comparison-row {
                grid-template-columns: 1fr;
                gap: 0.2rem;
                padding: 0.9rem 0;
            }
            .top-signal-row {
                grid-template-columns: 1.85rem minmax(0, 1fr) max-content;
                max-width: none;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


FLAG_CODE_OVERRIDES = {
    "EL": "gr",
}

TOP_SIGNAL_CONFIG = [
    ("inflation_pressure", "Inflation", "Lowest inflation pressure", "Lower current inflation ranks first."),
    ("housing_pressure", "Housing", "Lowest housing pressure", "Lower housing overburden ranks first."),
    ("poverty_pressure", "Poverty", "Lowest poverty pressure", "Lower poverty risk ranks first."),
    ("income_capacity", "Income", "Strongest income capacity", "Higher PPS income capacity ranks first."),
    ("net_earnings_capacity", "Net earnings", "Strongest net earnings capacity", "Higher PPS net earnings rank first."),
    ("employment_strength", "Employment", "Strongest employment signal", "Higher working-age employment rate ranks first."),
]

INDICATOR_GLOSSARY = [
    {
        "name": "Inflation pressure",
        "definition": "Annual price growth based on Eurostat HICP.",
        "rule": "Lower inflation usually means less price pressure.",
        "unit": "%",
        "source": "Eurostat HICP",
    },
    {
        "name": "Housing pressure",
        "definition": "Share of people spending more than 40% of income on housing.",
        "rule": "Lower housing overburden usually means lower housing stress.",
        "unit": "%",
        "source": "Eurostat SILC",
    },
    {
        "name": "Poverty pressure",
        "definition": "Share of people below 60% of national median income.",
        "rule": "Lower poverty risk usually means lower social pressure.",
        "unit": "%",
        "source": "Eurostat SILC",
    },
    {
        "name": "Income capacity",
        "definition": "Median equivalised net income adjusted for purchasing power.",
        "rule": "Higher PPS income means stronger local purchasing power.",
        "unit": "PPS",
        "source": "Eurostat ilc_di03",
    },
    {
        "name": "Net earnings capacity",
        "definition": "Annual net earnings for a single person without children earning 100% of average earnings.",
        "rule": "Higher PPS net earnings means stronger working-person earnings capacity.",
        "unit": "PPS",
        "source": "Eurostat earn_nt_net",
    },
    {
        "name": "Employment strength",
        "definition": "Working-age employment rate for people aged 20-64.",
        "rule": "Higher employment rate suggests a stronger labour-market participation signal.",
        "unit": "%",
        "source": "Eurostat lfsi_emp_a",
    },
]


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
    if category == "net_earnings_capacity":
        if rank == 1:
            return "Highest net earnings capacity among selected countries"
        if rank == total:
            return "Lowest net earnings capacity among selected countries"
        return f"{to_ordinal(rank)} highest net earnings capacity out of {total} selected countries"
    if category == "employment_strength":
        if rank == 1:
            return "Highest employment strength among selected countries"
        if rank == total:
            return "Lowest employment strength among selected countries"
        return f"{to_ordinal(rank)} highest employment strength out of {total} selected countries"

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
        "income_capacity": "Income capacity",
        "net_earnings_capacity": "Net earnings capacity",
        "employment_strength": "Employment strength",
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


def make_signal_sentence(row: pd.Series, max_length: int = 92) -> str:
    compact_message = make_compact_message(row.get("main_message", ""), max_length=max_length)
    if compact_message:
        return compact_message

    category = row.get("insight_category", "")
    label = row.get("pressure_label", "signal")
    if category in CAPACITY_CATEGORIES:
        return f"Capacity signal is {label}."
    if category in STRENGTH_CATEGORIES:
        return f"Labour-market signal is {label}."
    return f"Pressure signal is {label}."


def render_signal_sentence(text: str) -> None:
    st.markdown(f'<p class="signal-text">{html.escape(text)}</p>', unsafe_allow_html=True)


def render_status_label(text: str) -> None:
    st.markdown(f'<span class="status-pill">{html.escape(text)}</span>', unsafe_allow_html=True)


def render_metadata(text: str) -> None:
    st.markdown(f'<p class="metadata-text">{html.escape(text)}</p>', unsafe_allow_html=True)


def get_country_code_for_name(df: pd.DataFrame, country_name: str) -> str | None:
    values = df.loc[df["country_name"].eq(country_name), "country_code"].dropna()
    if values.empty:
        return None
    return str(values.iloc[0])


def render_country_title(selected_country: str, country_code: str | None = None) -> None:
    flag_html = get_flag_img_html(country_code, selected_country, css_class="country-title-flag") if country_code else ""
    st.markdown(
        f"""
        <section class="country-profile-card">
            <p class="country-eyebrow">Country profile</p>
            <h2 class="country-title">{flag_html}{html.escape(selected_country)}</h2>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_comparison_value(label: str, value: str) -> None:
    st.markdown(
        f"""
        <p class="comparison-value-label">{html.escape(label)}</p>
        <p class="comparison-value-large">{html.escape(value)}</p>
        """,
        unsafe_allow_html=True,
    )


def render_trend_stat(label: str, value: str) -> None:
    st.markdown(
        f"""
        <p class="trend-stat-label">{html.escape(label)}</p>
        <p class="trend-stat-value">{html.escape(value)}</p>
        """,
        unsafe_allow_html=True,
    )


def get_flag_code(country_code) -> str | None:
    if pd.isna(country_code):
        return None

    code = str(country_code).strip().upper()
    if not code:
        return None
    return FLAG_CODE_OVERRIDES.get(code, code.lower())


def get_flag_img_html(
    country_code,
    country_name: str,
    size: str = "24x18",
    css_class: str = "top-signal-flag",
) -> str:
    flag_code = get_flag_code(country_code)
    if flag_code is None:
        return ""

    width, height = size.split("x", maxsplit=1) if "x" in size else ("24", "18")
    src = f"https://flagcdn.com/{html.escape(size)}/{html.escape(flag_code)}.png"
    alt = f"{country_name} flag"
    return (
        f'<img src="{src}" alt="{html.escape(alt)}" class="{html.escape(css_class)}" '
        f'style="width: {html.escape(width)}px; height: {html.escape(height)}px; '
        'border-radius: 3px; object-fit: cover; vertical-align: middle;" '
        'onerror="this.style.display=\'none\';" />'
    )


def get_rank_marker(rank: int) -> str:
    medals = {
        1: "🥇",
        2: "🥈",
        3: "🥉",
    }
    return medals.get(rank, str(rank))


def render_top_signal_row(row: pd.Series, rank: int, category: str) -> None:
    country = str(row.get("country_name", "Unknown country"))
    value = format_metric_value(category, row.get("metric_value"))
    flag_html = get_flag_img_html(row.get("country_code"), country)

    st.markdown(
        f"""
        <div class="top-signal-row">
            <span class="top-signal-rank">{html.escape(get_rank_marker(rank))}</span>
            <div class="top-signal-country">{flag_html}{html.escape(country)}</div>
            <div class="top-signal-value">{html.escape(value)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_top_signals_by_indicator(df: pd.DataFrame) -> None:
    with st.container(border=True):
        st.markdown(
            """
            <div class="top-signal-panel">
                <p class="top-signal-card-title">Top 5 by indicator</p>
                <p class="top-signal-card-subtitle">Ranks are indicator-specific and do not represent an overall relocation ranking.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        tabs = st.tabs([tab_label for _, tab_label, _, _ in TOP_SIGNAL_CONFIG])
        for tab, (category, _, title, subtitle) in zip(tabs, TOP_SIGNAL_CONFIG):
            with tab:
                category_df = df.loc[
                    df["insight_category"].eq(category) & df["metric_value"].notna()
                ].copy()

                if category_df.empty:
                    top_rows = category_df
                else:
                    top_rows = category_df.sort_values(
                        "metric_value",
                        ascending=not is_higher_better(category),
                    ).head(5)

                st.markdown(
                    f"""
                    <p class="top-signal-card-title">{html.escape(title)}</p>
                    <p class="top-signal-card-subtitle">{html.escape(subtitle)}</p>
                    """,
                    unsafe_allow_html=True,
                )
                if top_rows.empty:
                    st.caption("No current values available.")
                else:
                    for rank, (_, row) in enumerate(top_rows.iterrows(), start=1):
                        render_top_signal_row(row, rank, category)


def render_app_header() -> None:
    st.markdown(
        """
        <section class="app-hero">
            <p class="app-kicker">Relocation decision support</p>
            <h1 class="app-title">Relocation Insight MVP</h1>
            <p class="app-subtitle">
                Compact financial pressure signals for selected European countries.
                Use the profile first, then open details only where you need context.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(title: str, subtitle: str | None = None, kicker: str | None = None) -> None:
    kicker_html = f'<p class="section-kicker">{html.escape(kicker)}</p>' if kicker else ""
    subtitle_html = f'<p class="section-subtitle">{html.escape(subtitle)}</p>' if subtitle else ""
    st.markdown(
        f"""
        <div>
            {kicker_html}
            <h2 class="section-title">{html.escape(title)}</h2>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_indicator_context(category: str, why_it_matters=None, rank_message=None) -> None:
    explanation = METRIC_EXPLANATIONS.get(category)
    has_why = why_it_matters is not None and not pd.isna(why_it_matters)
    has_rank = rank_message is not None and not pd.isna(rank_message)

    if explanation is None and not has_why and not has_rank:
        return

    def write_context() -> None:
        if explanation is not None:
            st.write(explanation["definition"])
            st.caption(explanation["rule"])
        if has_why:
            st.write(why_it_matters)
        if has_rank:
            st.caption(rank_message)

    if hasattr(st, "popover"):
        with st.popover("Details"):
            write_context()
    else:
        with st.expander("Details", expanded=False):
            write_context()


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
    if category in CAPACITY_CATEGORIES:
        return f"{value:,.0f} PPS"
    return format_percentage(value)


def format_change_value(category: str, value: float | None) -> str:
    if pd.isna(value):
        return "N/A"
    if category in CAPACITY_CATEGORIES:
        return f"{value:+,.0f} PPS"
    return f"{value:+.2f} pp"


def get_trend_unit(category: str) -> str:
    if category in CAPACITY_CATEGORIES:
        return "PPS"
    return "percent"


TIME_RANGE_OPTIONS = ["Last 10 years", "Last 20 years", "Full available history"]


def filter_timeseries_by_range(df: pd.DataFrame, selected_range: str) -> pd.DataFrame:
    if selected_range == "Full available history" or df.empty:
        return df

    valid_years = df["time_period"].dropna()
    if valid_years.empty:
        return df

    latest_year = int(valid_years.max())
    years_back = 10 if selected_range == "Last 10 years" else 20
    start_year = latest_year - years_back + 1
    return df.loc[df["time_period"] >= start_year].copy()


def has_large_historical_spike(full_df: pd.DataFrame, recent_df: pd.DataFrame) -> bool:
    full_values = full_df["metric_value"].dropna().abs()
    recent_values = recent_df["metric_value"].dropna().abs()
    if full_values.empty or recent_values.empty:
        return False

    recent_reference = recent_values.quantile(0.95)
    if recent_reference <= 0:
        return False
    return full_values.max() >= recent_reference * 5


def render_outlier_context_note(full_df: pd.DataFrame, recent_df: pd.DataFrame) -> None:
    if has_large_historical_spike(full_df, recent_df):
        render_metadata("Older historical outliers may compress recent variation. Use a shorter time range for recent context.")


def render_trend_unit_note(indicator: str) -> None:
    if indicator in CAPACITY_CATEGORIES:
        render_metadata("Unit: PPS. Absolute changes are shown in PPS.")
    else:
        render_metadata("Unit: percent. Absolute changes are shown in percentage points.")


def get_chart_metric_label(indicator: str) -> str:
    unit = "PPS" if indicator in CAPACITY_CATEGORIES else "%"
    return f"{INDICATOR_LABELS.get(indicator, get_metric_label(indicator))} ({unit})"


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
    return category in HIGHER_IS_BETTER_CATEGORIES


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
    pressure_data = country_data.loc[country_data["insight_category"].isin(PRESSURE_CATEGORIES)]
    if pressure_data["pressure_label"].isin(["High", "Very High"]).sum() >= 2:
        return "Broad pressure risk"
    return "Uneven pressure profile"


def get_key_risk_driver(country_data: pd.DataFrame):
    severity_map = {
        "Low": 1,
        "Moderate": 2,
        "High": 3,
        "Very High": 4,
    }
    candidates = []
    for _, row in country_data.iterrows():
        if row["insight_category"] not in PRESSURE_CATEGORIES:
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
    render_status_label(f"{pressure} pressure")
    render_signal_sentence(make_signal_sentence(best))
    render_indicator_context(
        best["insight_category"],
        (
            f"{metric_label} is the strongest pressure signal because it has the highest pressure level "
            f"among the tracked pressure indicators for this country."
        ),
    )


def render_capacity_signal(country_data: pd.DataFrame, category: str, context_text: str) -> None:
    row = country_data.loc[country_data["insight_category"] == category]
    if row.empty:
        st.caption("Data unavailable")
        return

    row = row.iloc[0]
    metric_label = get_metric_label(category)
    metric_val = format_metric_value(category, row["metric_value"])
    level = row['pressure_label']
    
    st.metric(metric_label, metric_val)
    render_status_label(f"{level} capacity")
    render_signal_sentence(make_signal_sentence(row))
    render_indicator_context(
        category,
        context_text,
    )


def render_income_and_earnings_capacity(country_data: pd.DataFrame) -> None:
    capacity_columns = st.columns(2)
    with capacity_columns[0]:
        render_capacity_signal(
            country_data,
            "income_capacity",
            "Higher values indicate stronger local purchasing power.",
        )
    with capacity_columns[1]:
        render_capacity_signal(
            country_data,
            "net_earnings_capacity",
            "Higher values indicate stronger working-person net earnings capacity.",
        )


def render_employment_strength_signal(country_data: pd.DataFrame) -> None:
    row = country_data.loc[country_data["insight_category"] == "employment_strength"]
    if row.empty:
        st.caption("Data unavailable")
        return

    row = row.iloc[0]
    metric_val = format_metric_value("employment_strength", row["metric_value"])
    level = row["pressure_label"]

    st.metric("Employment strength", metric_val)
    render_status_label(f"{level} signal")
    render_signal_sentence(make_signal_sentence(row))
    render_indicator_context(
        "employment_strength",
        "Higher values indicate a stronger working-age employment signal.",
    )


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
                render_status_label(f"{row['pressure_label']} pressure")
                render_signal_sentence(make_signal_sentence(row, max_length=82))
                render_indicator_context(category)


def render_methodology_notes() -> None:
    with st.expander("Methodology notes"):
        st.write(
            "Inflation pressure uses annual inflation rate from Eurostat HICP. "
            "Housing pressure uses housing overburden rate from Eurostat SILC. "
            "Poverty pressure uses at-risk-of-poverty rate from Eurostat SILC."
        )
        st.write(
            "Income capacity uses median equivalised net income from Eurostat ilc_di03, expressed in PPS. "
            "Net earnings capacity uses annual net earnings from Eurostat earn_nt_net for a single person without children "
            "earning 100% of average earnings, expressed in PPS. Higher capacity values are better, unlike the cost pressure indicators."
        )
        st.write(
            "Employment strength uses the working-age employment rate from Eurostat lfsi_emp_a. "
            "It is a higher-is-better labour-market strength signal, not a cost pressure or income indicator."
        )
        st.write(
            "Pressure labels are simplified MVP categories for early-stage signals only, "
            "not detailed economic diagnostics. Country comparisons are signals, not full relocation recommendations."
        )


def render_indicator_glossary() -> None:
    with st.expander("Indicator glossary", expanded=False):
        search_term = st.text_input(
            "Search indicators",
            placeholder="Try income, housing, poverty...",
            key="indicator_glossary_search",
        ).strip().lower()

        if search_term:
            glossary_rows = [
                item for item in INDICATOR_GLOSSARY
                if search_term in " ".join(str(value).lower() for value in item.values())
            ]
        else:
            glossary_rows = INDICATOR_GLOSSARY

        if not glossary_rows:
            st.caption("No matching indicators.")
            return

        for idx, item in enumerate(glossary_rows):
            if idx > 0:
                st.divider()

            st.markdown(f"**{item['name']}**")
            st.caption(f"Unit: {item['unit']} | Source: {item['source']}")
            st.write(item["definition"])
            render_metadata(item["rule"])


def render_trend_summary_stats(chart_df: pd.DataFrame, indicator: str) -> None:
    valid_df = chart_df.dropna(subset=["time_period", "metric_value"]).copy()
    if len(valid_df) < 2:
        render_metadata("Trend summary needs at least two valid values for the selected series.")
        return

    valid_df = valid_df.sort_values("time_period")
    earliest = valid_df.iloc[0]
    latest = valid_df.iloc[-1]
    earliest_value = float(earliest["metric_value"])
    latest_value = float(latest["metric_value"])
    min_value = float(valid_df["metric_value"].min())
    max_value = float(valid_df["metric_value"].max())
    absolute_change = latest_value - earliest_value
    relative_change = None
    if earliest_value != 0:
        relative_change = (absolute_change / abs(earliest_value)) * 100
    position_label = get_historical_position_label(min_value, max_value, latest_value)

    stat_cols = st.columns(5)
    stats = [
        ("Latest value", format_metric_value(indicator, latest_value)),
        ("Abs. change", format_change_value(indicator, absolute_change)),
        ("Rel. change", f"{relative_change:+.1f}%" if relative_change is not None else "N/A"),
        ("Historical range", f"{format_metric_value(indicator, min_value)} to {format_metric_value(indicator, max_value)}"),
        ("Current position", position_label),
    ]

    for col, (label, value) in zip(stat_cols, stats):
        with col:
            render_trend_stat(label, value)


def get_historical_position_label(min_value: float, max_value: float, latest_value: float) -> str:
    if min_value == max_value:
        return "stable historical range"

    position_ratio = (latest_value - min_value) / (max_value - min_value)
    if position_ratio <= 0.15:
        return "near historical low"
    if position_ratio <= 0.35:
        return "lower range"
    if position_ratio <= 0.65:
        return "middle range"
    if position_ratio <= 0.85:
        return "upper range"
    return "near historical high"


def render_trend_data_quality(chart_df: pd.DataFrame, timeseries_df: pd.DataFrame, indicator: str) -> None:
    valid_df = chart_df.dropna(subset=["time_period", "metric_value"]).copy()
    valid_year_count = valid_df["time_period"].nunique()

    selected_latest_year = None
    missing_year_count = None
    missing_share = None
    if valid_year_count > 0:
        valid_years = sorted(int(year) for year in valid_df["time_period"].dropna().unique())
        selected_latest_year = valid_years[-1]
        observed_year_count = valid_years[-1] - valid_years[0] + 1
        missing_year_count = max(observed_year_count - valid_year_count, 0)
        missing_share = missing_year_count / observed_year_count if observed_year_count else 0

    indicator_df = timeseries_df.loc[timeseries_df["indicator"] == indicator, ["time_period", "metric_value"]].copy()
    indicator_df["time_period"] = pd.to_numeric(indicator_df["time_period"], errors="coerce")
    indicator_df["metric_value"] = pd.to_numeric(indicator_df["metric_value"], errors="coerce")
    indicator_valid_df = indicator_df.dropna(subset=["time_period", "metric_value"])
    overall_latest_year = (
        int(indicator_valid_df["time_period"].max())
        if not indicator_valid_df.empty
        else None
    )

    is_stale = (
        selected_latest_year is not None and
        overall_latest_year is not None and
        selected_latest_year < overall_latest_year
    )

    if valid_year_count < 5:
        quality_label = "Insufficient trend data"
    elif is_stale:
        quality_label = "Stale latest data"
    elif missing_share is not None and missing_share > 0.4:
        quality_label = "Limited trend coverage"
    else:
        quality_label = "Suitable for cautious trend interpretation"

    with st.expander("Data quality details", expanded=False):
        render_status_label(quality_label)
        detail_cols = st.columns(4)
        details = [
            ("Valid years", str(valid_year_count)),
            (
                "Missing coverage",
                (
                    f"{missing_year_count} years ({missing_share:.0%})"
                    if missing_year_count is not None and missing_share is not None
                    else "N/A"
                ),
            ),
            ("Selected latest", str(selected_latest_year) if selected_latest_year is not None else "N/A"),
            ("Indicator latest", str(overall_latest_year) if overall_latest_year is not None else "N/A"),
        ]
        for col, (label, value) in zip(detail_cols, details):
            with col:
                render_trend_stat(label, value)


def build_country_trend_summary(country_df: pd.DataFrame, indicator: str) -> dict:
    valid_df = country_df.dropna(subset=["time_period", "metric_value"]).sort_values("time_period")
    valid_year_count = valid_df["time_period"].nunique()
    if valid_year_count == 0:
        return {
            "latest_year": "N/A",
            "latest_value": "N/A",
            "absolute_change": "N/A",
            "valid_year_count": "0",
            "has_minimum_values": False,
        }

    latest = valid_df.iloc[-1]
    latest_value = float(latest["metric_value"])
    absolute_change = "N/A"
    has_minimum_values = valid_year_count >= 2
    if has_minimum_values:
        earliest = valid_df.iloc[0]
        absolute_change = format_change_value(
            indicator,
            latest_value - float(earliest["metric_value"]),
        )

    return {
        "latest_year": str(int(latest["time_period"])),
        "latest_value": format_metric_value(indicator, latest_value),
        "absolute_change": absolute_change,
        "valid_year_count": str(valid_year_count),
        "has_minimum_values": has_minimum_values,
    }


def render_historical_comparison_summary(
    country_a: str,
    country_b: str,
    country_a_df: pd.DataFrame,
    country_b_df: pd.DataFrame,
    indicator: str,
) -> None:
    summary_a = build_country_trend_summary(country_a_df, indicator)
    summary_b = build_country_trend_summary(country_b_df, indicator)

    if not summary_a["has_minimum_values"] or not summary_b["has_minimum_values"]:
        render_metadata("Coverage note: at least one selected country has fewer than two valid observations.")

    stat_rows = [
        ("Latest year", summary_a["latest_year"], summary_b["latest_year"]),
        ("Latest value", summary_a["latest_value"], summary_b["latest_value"]),
        ("Abs. change", summary_a["absolute_change"], summary_b["absolute_change"]),
        ("Valid years", summary_a["valid_year_count"], summary_b["valid_year_count"]),
    ]

    header_cols = st.columns([1.2, 1, 1])
    with header_cols[0]:
        render_metadata("Measure")
    with header_cols[1]:
        render_metadata(country_a)
    with header_cols[2]:
        render_metadata(country_b)

    for label, country_a_value, country_b_value in stat_rows:
        row_cols = st.columns([1.2, 1, 1])
        with row_cols[0]:
            render_trend_stat(label, "")
        with row_cols[1]:
            render_trend_stat("", country_a_value)
        with row_cols[2]:
            render_trend_stat("", country_b_value)

    render_metadata("Coverage note: missing years remain missing; series are shown on their available years.")


def render_historical_trends(timeseries_df: pd.DataFrame, selected_country: str) -> None:
    render_section_header(
        "Historical trends",
        "Context only. Trend interpretation will be added later with data-quality checks.",
        "Context",
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

    trend_col_indicator, trend_col_country, trend_col_range = st.columns(3)
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

    with trend_col_country:
        trend_country = st.selectbox(
            "Country",
            countries,
            index=default_country_index,
            key="trend_country",
        )
    with trend_col_range:
        selected_range = st.selectbox(
            "Time range",
            TIME_RANGE_OPTIONS,
            index=0,
            key="trend_time_range",
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

    full_chart_df = chart_df.copy()
    chart_df = filter_timeseries_by_range(chart_df, selected_range)
    if chart_df.empty or chart_df["metric_value"].dropna().empty:
        st.info("No valid historical values are available for the selected time range.")
        return

    render_trend_unit_note(trend_indicator)
    chart_label = get_chart_metric_label(trend_indicator)
    display_chart_df = chart_df.rename(columns={"metric_value": chart_label})
    st.line_chart(
        display_chart_df,
        x="time_period",
        y=chart_label,
        width="stretch",
    )
    render_trend_summary_stats(chart_df, trend_indicator)
    render_trend_data_quality(chart_df, timeseries_df, trend_indicator)
    if selected_range == "Full available history":
        recent_df = filter_timeseries_by_range(full_chart_df, "Last 10 years")
        render_outlier_context_note(full_chart_df, recent_df)


def render_compare_historical_trends(timeseries_df: pd.DataFrame, countries: list[str]) -> None:
    render_section_header(
        "Compare historical trends",
        "Two-country historical context for one selected indicator.",
        "Trend comparison",
    )

    if timeseries_df.empty:
        st.info("Historical trend comparison data is not available yet.")
        return

    required_columns = {
        "country_name",
        "indicator",
        "time_period",
        "metric_value",
    }
    missing_columns = required_columns - set(timeseries_df.columns)
    if missing_columns:
        st.warning("Historical trend comparison is unavailable because the time-series file has an unexpected schema.")
        return

    trend_countries = sorted(timeseries_df["country_name"].dropna().unique())
    if not trend_countries:
        st.info("Historical trend comparison data is empty.")
        return

    country_options = [country for country in countries if country in trend_countries] or trend_countries
    available_indicators = [
        indicator
        for indicator in INDICATOR_LABELS
        if indicator in set(timeseries_df["indicator"].dropna())
    ]
    if not available_indicators:
        st.info("No historical indicators are available for comparison.")
        return

    control_indicator, control_a, control_b, control_range = st.columns(4)
    with control_indicator:
        selected_label = st.selectbox(
            "Indicator",
            [INDICATOR_LABELS[indicator] for indicator in available_indicators],
            key="trend_compare_indicator",
        )

    trend_indicator = next(
        indicator
        for indicator in available_indicators
        if INDICATOR_LABELS[indicator] == selected_label
    )

    with control_a:
        country_a = st.selectbox(
            "Country A",
            country_options,
            index=0,
            key="trend_compare_country_a",
        )
    with control_b:
        default_b_index = 1 if len(country_options) > 1 else 0
        country_b = st.selectbox(
            "Country B",
            country_options,
            index=default_b_index,
            key="trend_compare_country_b",
        )
    with control_range:
        selected_range = st.selectbox(
            "Time range",
            TIME_RANGE_OPTIONS,
            index=0,
            key="trend_compare_time_range",
        )

    compare_df = timeseries_df.loc[
        (timeseries_df["country_name"].isin([country_a, country_b])) &
        (timeseries_df["indicator"] == trend_indicator),
        ["country_name", "time_period", "metric_value"],
    ].copy()

    if compare_df.empty:
        st.info("No historical rows are available for this country and indicator selection.")
        return

    compare_df["time_period"] = pd.to_numeric(compare_df["time_period"], errors="coerce")
    compare_df["metric_value"] = pd.to_numeric(compare_df["metric_value"], errors="coerce")
    compare_df = compare_df.dropna(subset=["time_period"]).sort_values(["time_period", "country_name"])
    full_compare_df = compare_df.copy()
    compare_df = filter_timeseries_by_range(compare_df, selected_range)

    chart_df = compare_df.pivot(
        index="time_period",
        columns="country_name",
        values="metric_value",
    ).sort_index()

    if chart_df.empty or chart_df.dropna(how="all").empty:
        st.info("Historical rows exist, but metric values are missing for this comparison.")
        return

    render_trend_unit_note(trend_indicator)
    st.line_chart(chart_df, width="stretch")

    country_a_df = compare_df.loc[compare_df["country_name"] == country_a, ["time_period", "metric_value"]]
    country_b_df = compare_df.loc[compare_df["country_name"] == country_b, ["time_period", "metric_value"]]
    render_historical_comparison_summary(
        country_a,
        country_b,
        country_a_df,
        country_b_df,
        trend_indicator,
    )
    if selected_range == "Full available history":
        recent_df = filter_timeseries_by_range(full_compare_df, "Last 10 years")
        render_outlier_context_note(full_compare_df, recent_df)


def render_comparison_verdict(comparison_df: pd.DataFrame, country_a: str, country_b: str) -> None:
    if comparison_df.empty:
        render_signal_sentence("Comparison verdict: insufficient data for a directional signal based only on the current MVP indicators.")
        return

    a_wins = (comparison_df["Better country"] == country_a).sum()
    b_wins = (comparison_df["Better country"] == country_b).sum()
    valid_rows = comparison_df[comparison_df["Better country"].isin([country_a, country_b, "Equal"])]

    if valid_rows.empty:
        render_signal_sentence("Comparison verdict: insufficient data for a directional signal based only on the current MVP indicators.")
        return

    if a_wins > b_wins:
        verdict = f"{country_a} has an overall MVP advantage across the available indicators."
    elif b_wins > a_wins:
        verdict = f"{country_b} has an overall MVP advantage across the available indicators."
    else:
        verdict = "The comparison is mixed across the available indicators."

    render_signal_sentence(f"Comparison verdict: {verdict} This is directional only and based only on the current MVP indicators.")


def render_comparison_matrix(comparison_rows: list[dict], from_country: str, to_country: str) -> None:
    with st.container(border=True):
        for idx, row in enumerate(comparison_rows):
            if idx > 0:
                st.divider()

            row_cols = st.columns([1.3, 1, 1, 0.9, 0.85])
            better_country = str(row["Better country"])

            with row_cols[0]:
                st.markdown(f"**{row['Metric']}**")
            with row_cols[1]:
                render_metadata(from_country)
                st.markdown(f"### {row['From country value']}")
            with row_cols[2]:
                render_metadata(to_country)
                st.markdown(f"### {row['To country value']}")
            with row_cols[3]:
                render_metadata("Better")
                if better_country in {from_country, to_country, "Equal"}:
                    render_status_label(better_country)
                else:
                    render_metadata(better_country)
            with row_cols[4]:
                render_metadata("Difference")
                st.markdown(f"**{row['Difference']}**")

            with st.expander(f"Details: {row['Metric']}", expanded=False):
                render_metric_explanation(row["Category"])


def render_country_profile(country_data: pd.DataFrame, selected_country: str) -> None:
    st.markdown("#### Key signals")
    render_pressure_signals(country_data)

    col_key, col_income = st.columns([1, 1.55])
    with col_key:
        with st.container(border=True):
            st.markdown("#### Key risk")
            render_key_risk_driver(country_data)

    with col_income:
        with st.container(border=True):
            st.markdown("#### Income & earnings")
            render_income_and_earnings_capacity(country_data)

    with st.container(border=True):
        st.markdown("#### Labour market")
        render_employment_strength_signal(country_data)

    overall_pressure = get_overall_pressure(country_data)
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
    export_col, _ = st.columns([1, 2.4])
    with export_col:
        render_country_profile_export(country_data, selected_country)


def render_detailed_insights(country_data: pd.DataFrame) -> None:
    render_section_header(
        "Indicator details",
        "Compact signal cards. Open details only when you need context.",
        "Drill-down",
    )

    card_columns = st.columns(2)
    for idx, (_, row) in enumerate(country_data.iterrows()):
        metric_label = get_metric_label(row["insight_category"])
        metric_value = format_metric_value(row["insight_category"], row["metric_value"])
        category_label = row["insight_category"].replace("_", " ").title()
        compact_message = make_compact_message(row["main_message"])

        with card_columns[idx % 2]:
            with st.container(border=True):
                top_left, top_right = st.columns([1.35, 1])
                with top_left:
                    st.markdown(f"**{metric_label}**")
                    st.caption(category_label)
                with top_right:
                    render_status_label(str(row["pressure_label"]))

                st.metric("Value", metric_value)

                if compact_message:
                    render_signal_sentence(compact_message)

                render_metadata(f"{row['source']} | {row['confidence_level']} confidence")

                with st.expander("More context", expanded=False):
                    render_metric_explanation(row["insight_category"])
                    st.write(row["why_it_matters"])


def main():
    apply_visual_style()

    render_app_header()

    # Load data
    missing_data_paths = [path for path in REQUIRED_DATA_PATHS if not path.exists()]
    if missing_data_paths:
        show_data_file_error(missing_data_paths)
        return

    try:
        df = load_insights(str(DATA_PATH), get_file_modified_ns(DATA_PATH))
        timeseries_df = load_timeseries(str(TIMESERIES_DATA_PATH), get_file_modified_ns(TIMESERIES_DATA_PATH))
    except (pd.errors.EmptyDataError, pd.errors.ParserError, OSError) as error:
        st.error("Required CSV data files could not be loaded.")
        st.caption(str(error))
        st.info("Regenerate the data with `python data_pipeline/run_mvp_pipeline.py` before deploying.")
        return

    if not validate_required_columns(df, INSIGHTS_REQUIRED_COLUMNS, DATA_PATH):
        return
    if not validate_required_columns(timeseries_df, TIMESERIES_REQUIRED_COLUMNS, TIMESERIES_DATA_PATH):
        return

    # Calculate relative ranking across all countries by category
    def rank_group(group: pd.DataFrame) -> pd.Series:
        ascending = not is_higher_better(group.name)
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

    countries = sorted(df['country_name'].unique())
    selector_col, top_signals_col = st.columns([1, 1.65], vertical_alignment="top")
    with selector_col:
        selected_country = st.selectbox(
            "Country",
            countries,
            index=0
        )
        selected_country_code = get_country_code_for_name(df, selected_country)
        render_country_title(selected_country, selected_country_code)
    with top_signals_col:
        render_top_signals_by_indicator(df)

    # Filter data for selected country
    country_data = df[df['country_name'] == selected_country]

    if country_data.empty:
        st.warning(f"No data available for {selected_country}")
        return

    render_country_profile(country_data, selected_country)
    st.divider()

    render_detailed_insights(country_data)
    st.divider()

    # Compare two countries
    render_section_header(
        "Country comparison",
        "Directional comparison across the current MVP indicators.",
        "Compare",
    )
    
    # Country selectors
    comp_col1, comp_col2, _ = st.columns([1, 1, 1.2])
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
    from_net_earnings_capacity = get_metric(from_country, "net_earnings_capacity")
    to_net_earnings_capacity = get_metric(to_country, "net_earnings_capacity")
    from_employment_strength = get_metric(from_country, "employment_strength")
    to_employment_strength = get_metric(to_country, "employment_strength")

    comparison_rows = []
    for metric_label, category, from_value, to_value in [
        ("Annual inflation rate", "inflation_pressure", from_inflation, to_inflation),
        ("Housing overburden rate", "housing_pressure", from_housing, to_housing),
        ("At-risk-of-poverty rate", "poverty_pressure", from_poverty, to_poverty),
        ("Income capacity", "income_capacity", from_income_capacity, to_income_capacity),
        ("Net earnings capacity", "net_earnings_capacity", from_net_earnings_capacity, to_net_earnings_capacity),
        ("Employment strength", "employment_strength", from_employment_strength, to_employment_strength),
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
            "Category": category,
            "From country value": format_metric_value(category, from_value),
            "To country value": format_metric_value(category, to_value),
            "Difference": format_change_value(category, difference) if difference is not None else "N/A",
            "Better country": better,
        })

    comparison_df = pd.DataFrame(comparison_rows)
    render_comparison_matrix(comparison_rows, from_country, to_country)
    render_metadata("Lower pressure is better; higher income, net earnings, and employment strength are better.")

    with st.expander("Comparison table", expanded=False):
        st.dataframe(
            comparison_df,
            width="stretch",
            hide_index=True,
        )

    # Comparison summary
    st.markdown("#### Summary")
    inflation_better = comparison_rows[0]["Better country"]
    housing_better = comparison_rows[1]["Better country"]
    poverty_better = comparison_rows[2]["Better country"]
    income_better = comparison_rows[3]["Better country"]
    net_earnings_better = comparison_rows[4]["Better country"]
    employment_better = comparison_rows[5]["Better country"]
    inflation_diff = None if from_inflation is None or to_inflation is None else abs(to_inflation - from_inflation)
    housing_diff = None if from_housing is None or to_housing is None else abs(to_housing - from_housing)
    poverty_diff = None if from_poverty is None or to_poverty is None else abs(to_poverty - from_poverty)
    income_diff = None if from_income_capacity is None or to_income_capacity is None else abs(to_income_capacity - from_income_capacity)
    net_earnings_diff = (
        None
        if from_net_earnings_capacity is None or to_net_earnings_capacity is None
        else abs(to_net_earnings_capacity - from_net_earnings_capacity)
    )
    employment_diff = (
        None
        if from_employment_strength is None or to_employment_strength is None
        else abs(to_employment_strength - from_employment_strength)
    )

    if (
        inflation_diff is not None and housing_diff is not None and poverty_diff is not None and
        income_diff is not None and net_earnings_diff is not None and employment_diff is not None and
        inflation_diff < 0.5 and housing_diff < 0.5 and poverty_diff < 0.5 and
        income_diff < 500 and net_earnings_diff < 500 and employment_diff < 0.5
    ):
        tradeoff_label = "No major difference"
    elif (inflation_better == housing_better == poverty_better == income_better == net_earnings_better == employment_better and
          inflation_better not in ["Equal", "Data unavailable"]):
        tradeoff_label = f"Clear advantage for {inflation_better}"
    else:
        tradeoff_label = "Mixed trade-off"

    render_status_label(tradeoff_label)

    if (inflation_better == housing_better == poverty_better == income_better == net_earnings_better == employment_better and
        inflation_better not in ["Equal", "Data unavailable"]):
        summary_text = f"{inflation_better} shows better pressure, capacity, and employment signals across the tracked indicators."
    else:
        summary_text = "This comparison shows a mixed trade-off across the tracked indicators."

    render_signal_sentence(summary_text)
    render_comparison_verdict(comparison_df, from_country, to_country)
    st.divider()

    render_historical_trends(timeseries_df, selected_country)
    st.divider()

    render_compare_historical_trends(timeseries_df, countries)
    st.divider()

    render_section_header(
        "Methodology / Disclaimer",
        "Kept collapsed so methodology does not dominate the main workflow.",
        "Reference",
    )
    render_indicator_glossary()
    render_methodology_notes()
    with st.expander("MVP limitations", expanded=False):
        st.write(
            "This MVP currently compares inflation pressure, housing burden, poverty risk, income capacity, "
            "net earnings capacity, and employment strength. "
            "It does not yet include salary levels, taxes, career opportunities, language, culture, lifestyle preferences, healthcare, "
            "or personal circumstances."
        )

    with st.expander("Raw data", expanded=False):
        st.dataframe(
            country_data,
            width="stretch",
            hide_index=True
        )

if __name__ == "__main__":
    main()
