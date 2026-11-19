"""
UI Header and Scientific Disclaimer Component.
Strictly professional design with zero emojis.
"""

import streamlit as st


def render_disclaimer_banner():
    """Persistent disclaimer banner strictly following scientific wording rules."""
    st.info(
        "Proti IQ Screening Engine: Ranks which crops to lab-test first. "
        "Scores represent similarity-based likelihoods, not empirical measurements. "
        "Lab validation is the required next step."
    )


def render_app_header(title: str, subtitle: str = ""):
    """Standardized clean header across all pages."""
    st.title(f"Proti IQ - {title}")
    if subtitle:
        st.caption(subtitle)
    render_disclaimer_banner()
