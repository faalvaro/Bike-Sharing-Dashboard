import streamlit as st


def load_css():
    st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;600;700&display=swap');

    html, body, [class*="css"]{
        font-family:'DM Sans', sans-serif;
    }

    /* Main Container */
    .main .block-container{
        max-width:1450px;
        padding-top:2rem;
        padding-bottom:2rem;
        padding-left:2rem;
        padding-right:2rem;
    }

    /* Background */
    .stApp{
        background:#0f1117;
        color:#e8eaf0;
    }

    /* Sidebar */
    section[data-testid="stSidebar"]{
        width:270px !important;
        background:#16181f;
        border-right:1px solid #2a2d3a;
    }

    section[data-testid="stSidebar"] > div{
        width:270px !important;
    }

    [data-testid="stSidebar"] > div:first-child{
        padding-top:24px;
        padding-left:18px;
        padding-right:18px;
    }

    /* KPI Cards */
    .kpi-grid{
        display:grid;
        grid-template-columns:repeat(4, 1fr);
        gap:20px;
        margin-bottom:28px;
    }

    .kpi-card{
        background:linear-gradient(135deg, #1e2130 0%, #252840 100%);
        border:1px solid #2e3250;
        border-radius:16px;
        padding:22px;
        position:relative;
        overflow:hidden;
        transition:all .25s ease;
        cursor:pointer;
    }

    .kpi-card:hover{
        transform:translateY(-4px);
        box-shadow:0 12px 30px rgba(99,102,241,.18);
    }

    .kpi-card::before{
        content:'';
        position:absolute;
        left:0;
        right:0;
        top:0;
        height:3px;
        background:var(--accent);
        border-radius:16px 16px 0 0;
    }

    .kpi-label{
        font-size:11px;
        letter-spacing:1.5px;
        text-transform:uppercase;
        color:#6b7280;
        font-weight:600;
        margin-bottom:8px;
    }

    .kpi-value{
        font-family:'Space Mono', monospace;
        font-size:34px;
        font-weight:700;
        color:#ffffff;
        line-height:1;
        margin-bottom:4px;
    }

    .kpi-sub{
        color:#4b5563;
        font-size:12px;
    }

    /* Section Header */
    .section-header{
        font-family:'Space Mono', monospace;
        font-size:15px;
        letter-spacing:3px;
        text-transform:uppercase;
        color:#6366f1;
        margin:32px 0 16px;
        display:flex;
        align-items:center;
        gap:10px;
        font-weight:700;
    }

    .section-header::after{
        content:'';
        flex:1;
        height:1px;
        background:linear-gradient(to right, #6366f1, transparent);
    }

    /* Insight Box */
    .insight-box{
        background:linear-gradient(135deg, #1a1f35, #1e2240);
        border-left:4px solid #6366f1;
        border-radius:0 12px 12px 0;
        padding:18px 22px;
        margin-top:18px;
        color:#9ca3af;
        font-size:14px;
        line-height:1.6;
    }

    .insight-box strong{
        color:#ffffff;
    }

    /* Chart Container */
    .chart-container{
        background:#16181f;
        border:1px solid #2a2d3a;
        border-radius:16px;
        padding:20px;
        box-shadow:0 10px 25px rgba(0,0,0,.18);
    }

    </style>
    """, unsafe_allow_html=True)