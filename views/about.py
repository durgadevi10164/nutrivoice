"""
about.py
--------
Static About page explaining the project and its future development plan.
"""

import streamlit as st


def render_about():
    st.markdown("## About NutriVoice")
    st.markdown(
        """
        <div class="nv-card">
        <p>
        <strong>NutriVoice</strong> is a student project focused on developing an accessible
        nutrition assistance platform for rural pregnant women and children.
        </p>
        <p>
        The future system will provide personalized nutrition guidance through AI and
        voice-based interaction, including support for local languages such as Tamil.
        </p>
        <p>
        For this current version, only <strong>profile management</strong> and the
        foundation of the system are implemented — no AI recommendations, voice input,
        or speech-to-text are active yet.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='nv-section-label'>Planned Development Roadmap</div>", unsafe_allow_html=True)
    roadmap = [
        ("Phase 1 — Current", "Professional UI, profile creation, SQLite storage, profile editing."),
        ("Phase 2", "Voice input: microphone → speech-to-text → user question."),
        ("Phase 3", "Nutrition knowledge base: profile + question → relevant nutrition information."),
        ("Phase 4", "AI recommendation: profile + nutrition data + question → personalized guidance."),
        ("Phase 5", "Voice output: AI response → text-to-speech → spoken answer."),
        ("Phase 6", "Local language support, including Tamil."),
    ]
    for title, desc in roadmap:
        st.markdown(
            f"""
            <div class="nv-card">
                <h3>{title}</h3>
                <p>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="nv-notice">
        Privacy note: this prototype does not provide medical diagnosis and does not collect
        unnecessary medical information. It is intended for demonstration and project review
        purposes only.
        </div>
        """,
        unsafe_allow_html=True,
    )
