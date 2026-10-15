"""
app.py
------
NutriVoice — Version 1 (Profile Management Foundation)

This is the only file Streamlit runs directly. It handles:
  - page configuration and CSS loading
  - database initialization
  - top header + sidebar navigation
  - routing to the correct view (Home / Create Profile / Edit Profile /
    My Profile / About / Success)

The AI nutrition engine, voice input, speech-to-text, and Tamil voice
support are intentionally NOT implemented in this version — see the
'Coming Soon' sections on the Home page and the About page for the
planned roadmap.
"""

import os
import streamlit as st

from database.database import init_db, get_latest_user
from views import home, profile, about

st.set_page_config(
    page_title="NutriVoice — AI-Based Voice Nutrition Assistant",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_css():
    css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "style.css")
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def init_session_state():
    if "page" not in st.session_state:
        st.session_state.page = "Home"
    if "profile" not in st.session_state:
        # Restore the most recently saved profile from the database, if any.
        # This is a single-profile demo prototype (no login system yet),
        # so "the profile" simply means the latest row in the table.
        latest = get_latest_user()
        st.session_state.profile = latest
        st.session_state.profile_id = latest["id"] if latest else None


def _nav_button(label, key, target_page, active_pages, use_container_width=True, force_primary=False):
    """
    Render a single nav button that turns green ("selected") whenever the
    current page is in active_pages, so header and sidebar navigation both
    show which section the user is on.
    """
    is_active = st.session_state.page in active_pages
    button_type = "primary" if (is_active or force_primary) else "secondary"
    clicked = st.button(label, key=key, type=button_type, use_container_width=use_container_width)
    if clicked:
        st.session_state.page = target_page
        st.rerun()


def render_header():
    has_profile = st.session_state.profile is not None
    my_profile_target = "My Profile" if has_profile else "Create Profile"

    left, nav1, nav2, nav3, nav4 = st.columns([2, 1, 1, 1, 1.2])

    with left:
        st.markdown(
            """
            <div>
                <div class="nv-logo">🥗 NutriVoice</div>
                <div class="nv-tagline">AI-Based Voice Nutrition Assistant</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with nav1:
        st.write("")
        _nav_button("Home", "nav_home", "Home", {"Home"})
    with nav2:
        st.write("")
        _nav_button("My Profile", "nav_profile", my_profile_target, {"My Profile", "Edit Profile", "Success"})
    with nav3:
        st.write("")
        _nav_button("About", "nav_about", "About", {"About"})
    with nav4:
        st.write("")
        # Create Profile is the primary call-to-action, so it stays green
        # even when it isn't the active page.
        _nav_button("Create Profile", "nav_create", "Create Profile", {"Create Profile"}, force_primary=True)

    st.markdown("<hr style='margin-top:0.5rem; margin-bottom:1.5rem; border-color:#E2E8F0;'>", unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown("### 🥗 NutriVoice")
        st.write("")

        has_profile = st.session_state.profile is not None
        my_profile_target = "My Profile" if has_profile else "Create Profile"

        _nav_button("🏠 Home", "sb_home", "Home", {"Home"})
        _nav_button("👤 My Profile", "sb_profile", my_profile_target, {"My Profile", "Edit Profile", "Success"})
        _nav_button("ℹ️ About", "sb_about", "About", {"About"})

        st.write("")
        st.markdown("**Profile Status**")
        if st.session_state.profile:
            st.markdown('<span class="nv-status-ok">● Profile Completed</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="nv-status-warn">● Profile Not Created</span>', unsafe_allow_html=True)


def route():
    page = st.session_state.page
    if page == "Home":
        home.render_home()
    elif page == "Create Profile":
        profile.render_form(mode="create")
    elif page == "Edit Profile":
        profile.render_form(mode="edit")
    elif page == "My Profile":
        profile.render_view()
    elif page == "Success":
        profile.render_success()
    elif page == "About":
        about.render_about()
    else:
        home.render_home()


def main():
    init_db()
    init_session_state()
    load_css()
    render_header()
    render_sidebar()
    route()


if __name__ == "__main__":
    main()
