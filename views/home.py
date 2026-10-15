"""
home.py
-------
Renders the Home page. Shows a marketing-style hero + feature cards to a
first-time visitor with no profile, and a personalized dashboard once a
profile exists.
"""

import streamlit as st
from database.models import USER_TYPE_PREGNANT


def render_home():
    profile = st.session_state.get("profile")

    if profile:
        _render_dashboard(profile)
    else:
        _render_hero_and_features()

    _render_coming_soon()


def _render_hero_and_features():
    st.markdown(
        """
        <div class="nv-hero">
            <h1>Smart Nutrition Support for <span class="nv-highlight">Better Health</span></h1>
            <p>NutriVoice is an AI-based voice nutrition assistant designed to provide simple,
            accessible and personalized nutrition support.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        if st.button("Create Your Profile", type="primary", use_container_width=True):
            st.session_state.page = "Create Profile"
            st.rerun()
    with col2:
        if st.button("Learn More", use_container_width=True):
            st.session_state.page = "About"
            st.rerun()

    st.markdown("<div class='nv-section-label'>Why NutriVoice</div>", unsafe_allow_html=True)
    features = [
        ("🎯", "Personalized", "Nutrition support can be tailored to your own profile information."),
        ("♿", "Accessible", "Designed with simple, easy-to-follow interaction for different types of users."),
        ("🌾", "Rural-Friendly", "Built with rural users and accessibility challenges in mind."),
        ("🎤", "Voice Ready", "Voice-based interaction is planned for a future version of NutriVoice."),
    ]
    cols = st.columns(4)
    for col, (icon, title, desc) in zip(cols, features):
        with col:
            st.markdown(
                f"""
                <div class="nv-card">
                    <h3>{icon} {title}</h3>
                    <p>{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_dashboard(profile: dict):
    st.markdown(f"### Welcome back, {profile['full_name'].split(' ')[0]} 👋")
    st.markdown("Your NutriVoice profile is ready.")
    st.write("")

    cols = st.columns(4)
    with cols[0]:
        _summary_card("Age", f"{profile['age']} yrs")
    with cols[1]:
        _summary_card("Weight", f"{profile['weight']} kg")
    with cols[2]:
        _summary_card("User Type", profile["user_type"])
    with cols[3]:
        if profile["user_type"] == USER_TYPE_PREGNANT:
            _summary_card("Pregnancy Month", str(profile.get("pregnancy_month") or "—"))
        else:
            _summary_card("Child Age", str(profile.get("child_age") or "—"))

    st.write("")
    if st.button("View My Profile"):
        st.session_state.page = "My Profile"
        st.rerun()


def _summary_card(label: str, value: str):
    st.markdown(
        f"""
        <div class="nv-card" style="text-align:center;">
            <p style="font-size:0.78rem; text-transform:uppercase; letter-spacing:0.4px;">{label}</p>
            <h3 style="font-size:1.4rem; margin-top:4px;">{value}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_coming_soon():
    st.markdown("<div class='nv-section-label'>Coming Soon</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(
            """
            <div class="nv-card">
                <span class="nv-badge">Coming Soon</span>
                <h3>🧠 AI Nutrition Assistant</h3>
                <p>Ask nutrition questions and receive personalized guidance based on your profile.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.write("")
        st.write("")
        if st.button("Nutrition Assistant", use_container_width=True):
            st.info("Nutrition Assistant will be available in the next version.")

    st.write("")
    future_cols = st.columns(4)
    future_features = [
        ("🎤", "Voice Nutrition Assistant"),
        ("🌐", "Local Language Support"),
        ("🍎", "Personalized Food Recommendations"),
        ("📊", "Nutrition Tracking"),
    ]
    for col, (icon, title) in zip(future_cols, future_features):
        with col:
            st.markdown(
                f"""
                <div class="nv-card" style="text-align:center;">
                    <span class="nv-badge">Coming Soon</span>
                    <h3>{icon} {title}</h3>
                </div>
                """,
                unsafe_allow_html=True,
            )
