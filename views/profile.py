"""
profile.py
----------
Handles three related views:
  - render_form()    : the Create / Edit Profile form
  - render_success()  : the "Profile Created Successfully" screen
  - render_view()      : the read-only "My Profile" dashboard page
"""

import streamlit as st

from database.database import create_user, update_user
from database.models import (
    USER_TYPE_PREGNANT,
    USER_TYPE_CHILD,
    USER_TYPES,
    GENDERS,
    CHILD_GENDERS,
    FOOD_PREFERENCES,
    DIETARY_PREFERENCES,
    LANGUAGES,
)
from utils.bmi import calculate_bmi, bmi_category
from utils.validation import validate_profile_form


def render_form(mode: str = "create"):
    """mode is 'create' or 'edit'."""
    existing = st.session_state.get("profile") if mode == "edit" else None

    st.markdown(f"## {'Edit Profile' if mode == 'edit' else 'Create Your Profile'}")
    st.markdown(
        """
        <div class="nv-notice">
        This prototype collects basic profile information for demonstration purposes.
        Please avoid entering highly sensitive medical information.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='nv-section-label'>Basic Information</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        full_name = st.text_input("Full Name *", value=existing["full_name"] if existing else "")
        age = st.number_input("Age *", min_value=0, max_value=120, step=1,
                               value=existing["age"] if existing else 25)
        gender = st.selectbox("Gender *", GENDERS,
                               index=GENDERS.index(existing["gender"]) if existing and existing["gender"] in GENDERS else 0)
    with c2:
        phone = st.text_input("Phone Number (optional)", value=(existing.get("phone") or "") if existing else "")
        email = st.text_input("Email (optional)", value=(existing.get("email") or "") if existing else "")

    st.markdown("<div class='nv-section-label'>Physical Information</div>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        height = st.number_input("Height (cm) *", min_value=0.0, max_value=300.0, step=0.5,
                                  value=float(existing["height"]) if existing else 160.0)
    with c4:
        weight = st.number_input("Weight (kg) *", min_value=0.0, max_value=400.0, step=0.5,
                                  value=float(existing["weight"]) if existing else 55.0)

    live_bmi = calculate_bmi(weight, height) if height and weight else 0.0
    st.markdown(
        f"""
        <div class="nv-notice">
        Estimated BMI: <strong>{live_bmi if live_bmi else '—'}</strong>
        ({bmi_category(live_bmi)}) — this is an informational value only, not a medical diagnosis.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='nv-section-label'>User Category</div>", unsafe_allow_html=True)
    default_type_index = USER_TYPES.index(existing["user_type"]) if existing and existing.get("user_type") in USER_TYPES else 0
    user_type = st.radio("This profile is for *", USER_TYPES, index=default_type_index, horizontal=True)

    pregnancy_month = None
    child_age = None
    child_gender = None

    if user_type == USER_TYPE_PREGNANT:
        st.markdown("<div class='nv-section-label'>Pregnancy Details</div>", unsafe_allow_html=True)
        pregnancy_month = st.number_input(
            "Pregnancy Month (1-9) *", min_value=0, max_value=9, step=1,
            value=int(existing["pregnancy_month"]) if existing and existing.get("pregnancy_month") else 1,
        )
    else:
        st.markdown("<div class='nv-section-label'>Child Details</div>", unsafe_allow_html=True)
        cc1, cc2 = st.columns(2)
        with cc1:
            child_age = st.number_input(
                "Child Age *", min_value=0, max_value=18, step=1,
                value=int(existing["child_age"]) if existing and existing.get("child_age") else 3,
            )
        with cc2:
            default_child_gender = (
                CHILD_GENDERS.index(existing["child_gender"])
                if existing and existing.get("child_gender") in CHILD_GENDERS else 0
            )
            child_gender = st.selectbox("Child Gender *", CHILD_GENDERS, index=default_child_gender)

    st.markdown("<div class='nv-section-label'>Nutrition Preferences</div>", unsafe_allow_html=True)
    c5, c6 = st.columns(2)
    with c5:
        default_food = FOOD_PREFERENCES.index(existing["food_preference"]) if existing and existing.get("food_preference") in FOOD_PREFERENCES else 0
        food_preference = st.selectbox("Vegetarian / Non-Vegetarian *", FOOD_PREFERENCES, index=default_food)
        default_lang = LANGUAGES.index(existing["preferred_language"]) if existing and existing.get("preferred_language") in LANGUAGES else 0
        preferred_language = st.selectbox("Preferred Language *", LANGUAGES, index=default_lang)
    with c6:
        default_diet = DIETARY_PREFERENCES.index(existing["dietary_preference"]) if existing and existing.get("dietary_preference") in DIETARY_PREFERENCES else 0
        dietary_preference = st.selectbox("Dietary Preference", DIETARY_PREFERENCES, index=default_diet)
        food_allergies = st.text_input("Any food allergies? (optional)",
                                        value=(existing.get("food_allergies") or "") if existing else "")

    st.write("")
    submit_label = "Save Changes" if mode == "edit" else "Create Profile"
    submitted = st.button(submit_label, type="primary")

    if submitted:
        data = {
            "full_name": full_name.strip(),
            "age": int(age),
            "gender": gender,
            "phone": phone.strip() or None,
            "email": email.strip() or None,
            "height": float(height),
            "weight": float(weight),
            "bmi": calculate_bmi(weight, height),
            "user_type": user_type,
            "pregnancy_month": int(pregnancy_month) if user_type == USER_TYPE_PREGNANT else None,
            "child_age": int(child_age) if user_type == USER_TYPE_CHILD else None,
            "child_gender": child_gender if user_type == USER_TYPE_CHILD else None,
            "food_preference": food_preference,
            "dietary_preference": dietary_preference,
            "preferred_language": preferred_language,
            "food_allergies": food_allergies.strip() or None,
        }

        errors = validate_profile_form(data)
        if errors:
            for err in errors:
                st.error(err)
        else:
            if mode == "edit" and existing:
                update_user(existing["id"], data)
                new_id = existing["id"]
            else:
                new_id = create_user(data)

            data["id"] = new_id
            st.session_state.profile = data
            st.session_state.profile_id = new_id
            if mode == "edit":
                st.session_state.page = "My Profile"
            else:
                st.session_state.page = "Success"
            st.rerun()


def render_success():
    profile = st.session_state.get("profile")
    name = profile["full_name"] if profile else "there"

    st.markdown(
        f"""
        <div class="nv-card" style="text-align:center; padding:3rem 2rem;">
            <span class="nv-badge nv-badge-green">Profile Created Successfully</span>
            <h2 style="margin-top:0.6rem;">Welcome to NutriVoice, {name}!</h2>
            <p style="color:#5f6d69;">Your profile has been saved. You're all set to explore NutriVoice.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("View My Profile", type="primary"):
            st.session_state.page = "My Profile"
            st.rerun()
    with col2:
        if st.button("Go to Home"):
            st.session_state.page = "Home"
            st.rerun()


def render_view():
    profile = st.session_state.get("profile")
    if not profile:
        st.warning("You don't have a profile yet.")
        if st.button("Create Your Profile", type="primary"):
            st.session_state.page = "Create Profile"
            st.rerun()
        return

    st.markdown(
        f"""
        <div class="nv-profile-header">
            <div class="nv-avatar">👤</div>
            <div>
                <h2 style="margin-bottom:0;">{profile['full_name']}</h2>
                <span style="color:#5f6d69; font-size:0.9rem;">{profile['user_type']}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='nv-section-label'>Basic Information</div>", unsafe_allow_html=True)
    _row("Name", profile["full_name"])
    _row("Age", f"{profile['age']}")
    _row("Gender", profile["gender"])
    if profile.get("phone"):
        _row("Phone", profile["phone"])
    if profile.get("email"):
        _row("Email", profile["email"])

    st.markdown("<div class='nv-section-label'>Physical Information</div>", unsafe_allow_html=True)
    _row("Height", f"{profile['height']} cm")
    _row("Weight", f"{profile['weight']} kg")
    _row("BMI", f"{profile['bmi']} ({bmi_category(profile['bmi'])}) — informational only")

    st.markdown("<div class='nv-section-label'>Nutrition Profile</div>", unsafe_allow_html=True)
    _row("User Type", profile["user_type"])
    if profile["user_type"] == USER_TYPE_PREGNANT:
        _row("Pregnancy Month", f"{profile.get('pregnancy_month') or '—'}")
    else:
        _row("Child Age", f"{profile.get('child_age') or '—'}")
        _row("Child Gender", profile.get("child_gender") or "—")
    _row("Food Preference", profile.get("food_preference") or "—")
    _row("Dietary Preference", profile.get("dietary_preference") or "—")
    _row("Preferred Language", profile.get("preferred_language") or "—")
    _row("Food Allergies", profile.get("food_allergies") or "None reported")

    st.write("")
    if st.button("Edit Profile", type="primary"):
        st.session_state.page = "Edit Profile"
        st.rerun()


def _row(label: str, value: str):
    st.markdown(
        f"""<div class="nv-row"><span>{label}</span><span>{value}</span></div>""",
        unsafe_allow_html=True,
    )
