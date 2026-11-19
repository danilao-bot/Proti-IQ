"""
UI Badges for Confidence Levels and Screening Flags.
Uses color-blind-safe styling and accessible contrast without emojis.
"""

import streamlit as st


def render_confidence_badge(level: str):
    """Render High, Medium, or Low confidence badge with accessible colors."""
    colors = {
        "High": ("#166534", "#dcfce7", "[High Confidence]"),
        "Medium": ("#854d0e", "#fef9c3", "[Medium Confidence]"),
        "Low": ("#991b1b", "#fee2e2", "[Low Confidence]"),
    }
    fg, bg, label = colors.get(level, ("#374151", "#f3f4f6", f"[{level}]"))

    st.markdown(
        f'<span style="background-color: {bg}; color: {fg}; padding: 3px 8px; '
        f'border-radius: 4px; font-weight: 600; font-size: 0.82rem; border: 1px solid {fg}40;">'
        f'{label}</span>',
        unsafe_allow_html=True,
    )


def render_screening_flags(flags: list):
    """Render screening badges for allergens and anti-nutritional factors."""
    if not flags:
        st.markdown(
            '<span style="color: #6b7280; font-size: 0.82rem; font-style: italic;">'
            'No screening flags detected in UniProt annotations</span>',
            unsafe_allow_html=True,
        )
        return

    badge_htmls = []
    for f in flags:
        badge_htmls.append(
            f'<span style="background-color: #ffedd5; color: #9a3412; padding: 2px 8px; '
            f'border-radius: 4px; font-size: 0.8rem; font-weight: 500; margin-right: 6px; border: 1px solid #fdba74;">'
            f'FLAG: {f}</span>'
        )
    st.markdown(" ".join(badge_htmls), unsafe_allow_html=True)
