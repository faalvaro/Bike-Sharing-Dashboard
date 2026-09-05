import streamlit as st

from charts import (
    plot_hourly_rentals,
    plot_monthly_trend,
    plot_season_total,
    plot_user_type_monthly,
    plot_weather_average,
    plot_weekday_heatmap,
)
from components import (
    render_data_preview,
    render_footer,
    render_header,
    render_kpi_cards,
    render_section_header,
    render_sidebar,
)
from style import load_css
from utils import (
    CUACA_MAP,
    MUSIM_MAP,
    filter_data,
    get_kpi_metrics,
    load_data,
    prepare_data,
)


# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ── MAIN APP ───────────────────────────────────────────────────────────────────
def main():
    load_css()

    try:
        days_df, hours_df = load_data()
    except FileNotFoundError as error:
        st.error(
            "❌ Data file not found. Please make sure `day.csv` and `hour.csv` "
            "are available inside the `data/` folder."
        )
        st.caption(f"Detail: {error}")
        st.stop()

    days_df, hours_df = prepare_data(days_df, hours_df)

    filters = render_sidebar(
        season_options=list(MUSIM_MAP.values()),
        weather_options=list(CUACA_MAP.values()),
    )

    flt_days, flt_hours = filter_data(
        days_df=days_df,
        hours_df=hours_df,
        selected_years=filters["selected_years"],
        selected_seasons=filters["selected_seasons"],
        selected_weather=filters["selected_weather"],
        selected_hour=filters["selected_hour"],
    )

    if flt_days.empty or flt_hours.empty:
        st.warning("⚠️ The selected filters do not match any data.")
        st.stop()

    render_header()

    kpi_metrics = get_kpi_metrics(
        flt_days=flt_days,
        flt_hours=flt_hours,
    )

    render_kpi_cards(kpi_metrics)

    render_section_header("01 — Daily & Weekly Pattern")

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        plot_hourly_rentals(flt_hours)

    with col2:
        plot_weekday_heatmap(flt_hours)

    render_section_header("02 — Monthly Trend & User Segmentation")

    col3, col4 = st.columns([1, 1], gap="large")

    with col3:
        plot_monthly_trend(flt_days)

    with col4:
        plot_user_type_monthly(flt_days)

    render_section_header("03 — Weather & Season Impact")

    col5, col6 = st.columns([1, 1], gap="large")

    with col5:
        plot_weather_average(flt_hours)

    with col6:
        plot_season_total(flt_days)

    render_section_header("04 — Data Preview")

    render_data_preview(
        flt_days=flt_days,
        flt_hours=flt_hours,
    )

    render_footer()


if __name__ == "__main__":
    main()