import streamlit as st
from textwrap import dedent

from utils import human_number


def render_sidebar(season_options, weather_options):
    with st.sidebar:
        st.title("🚲 Filters")
        st.caption("Explore bike rental trends using the filters below.")
        st.divider()

        selected_years = st.multiselect(
            "📅 Year",
            options=[2011, 2012],
            default=[2011, 2012],
        )

        selected_seasons = st.multiselect(
            "🍃 Season",
            options=season_options,
            default=season_options,
        )

        selected_weather = st.multiselect(
            "🌤 Weather",
            options=weather_options,
            default=weather_options,
        )

        selected_hour = st.slider(
            "⏰ Hour Range",
            0,
            23,
            (0, 23),
        )

        st.divider()
        st.caption("Python • Streamlit • Pandas")

    return {
        "selected_years": selected_years,
        "selected_seasons": selected_seasons,
        "selected_weather": selected_weather,
        "selected_hour": selected_hour,
    }


def render_header():
    html = """
    <div style="margin-bottom:24px;">
        <div style="font-family:'Space Mono', monospace;font-size:32px;font-weight:700;color:#ffffff;line-height:1.2;">
            Bike Sharing <span style="color:#6366f1;">Dashboard</span>
        </div>
        <div style="margin-top:10px;color:#9ca3af;font-size:15px;font-weight:500;">
            Interactive visualization of bike rental patterns from the 2011–2012 dataset.
        </div>
    </div>
    """

    html = html.replace("\n", "").replace("    ", "")

    st.markdown(html, unsafe_allow_html=True)


def render_kpi_cards(metrics):
    total_rentals = metrics["total_rentals"]
    average_daily = metrics["average_daily"]
    casual_percentage = metrics["casual_percentage"]
    registered_percentage = metrics["registered_percentage"]
    peak_hour = metrics["peak_hour"]

    html = f"""
    <div class="kpi-grid">
        <div class="kpi-card" style="--accent:#6366f1;">
            <div class="kpi-label">🚲 Total Rentals</div>
            <div class="kpi-value">{human_number(total_rentals)}</div>
            <div class="kpi-sub">Selected data</div>
        </div>

        <div class="kpi-card" style="--accent:#f59e0b;">
            <div class="kpi-label">📈 Average / Day</div>
            <div class="kpi-value">{average_daily:,.0f}</div>
            <div class="kpi-sub">Average rentals</div>
        </div>

        <div class="kpi-card" style="--accent:#10b981;">
            <div class="kpi-label">👤 Casual Users</div>
            <div class="kpi-value">{casual_percentage}%</div>
            <div class="kpi-sub">Registered: {registered_percentage}%</div>
        </div>

        <div class="kpi-card" style="--accent:#f43f5e;">
            <div class="kpi-label">🕒 Peak Hour</div>
            <div class="kpi-value">{peak_hour:02d}:00</div>
            <div class="kpi-sub">Highest activity</div>
        </div>
    </div>
    """

    html = html.replace("\n", "").replace("    ", "")

    st.markdown(html, unsafe_allow_html=True)


def render_section_header(title):
    st.markdown(
        f'<div class="section-header">{title}</div>',
        unsafe_allow_html=True,
    )


def insight_box(content):
    st.markdown(
        dedent(f"""
        <div class="insight-box">
            💡 <strong>Insight:</strong> {content}
        </div>
        """),
        unsafe_allow_html=True,
    )


def render_data_preview(flt_days, flt_hours):
    tab1, tab2 = st.tabs(["📋 Hourly Data", "📋 Daily Data"])

    with tab1:
        st.dataframe(
            flt_hours[
                [
                    "dteday",
                    "hr",
                    "season",
                    "weathersit",
                    "casual",
                    "registered",
                    "cnt",
                ]
            ].head(50),
            use_container_width=True,
        )

    with tab2:
        st.dataframe(
            flt_days[
                [
                    "dteday",
                    "season",
                    "weathersit",
                    "casual",
                    "registered",
                    "cnt",
                ]
            ].head(50),
            use_container_width=True,
        )


def render_footer():
    st.markdown(
        dedent("""
        <div style="
            text-align:center;
            color:#9ca3af;
            font-size:13px;
            margin-top:50px;
            padding-top:20px;
            border-top:1px solid #1e2130;
        ">
            <b>© 2026 Farhan Ahmad Alvaro</b><br>
            Python • Streamlit • Pandas • Data Visualization • Data Analytics
        </div>
        """),
        unsafe_allow_html=True,
    )