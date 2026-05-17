"""Shared branding/styling helpers for Isaac Maya's demo collection.

Uses st.html() for reliable CSS/HTML injection (st.markdown with unsafe_allow_html
gets sanitized in some Streamlit Cloud configurations).
"""

from __future__ import annotations

import streamlit as st

ACCENT = "#818cf8"
ACCENT_2 = "#22d3ee"
SURFACE = "#151823"
BG = "#0b0d12"
INK = "#e6e7eb"
MUTED = "#9aa0b4"

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"]  {{
  font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
  letter-spacing: -0.01em;
}}
code, pre, kbd, samp {{
  font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, monospace !important;
}}
.stApp {{
  background:
    radial-gradient(1200px 600px at 10% -10%, rgba(129,140,248,0.10), transparent 60%),
    radial-gradient(800px 400px at 90% 0%, rgba(34,211,238,0.08), transparent 60%),
    {BG} !important;
}}
.im-hero {{
  margin: -1rem 0 2rem 0;
  padding: 2.2rem 2.4rem 2rem;
  border-radius: 18px;
  background: linear-gradient(135deg, rgba(129,140,248,0.18), rgba(34,211,238,0.08) 50%, rgba(255,255,255,0.02));
  border: 1px solid rgba(129,140,248,0.25);
  box-shadow: 0 10px 30px rgba(0,0,0,0.35);
}}
.im-hero .im-kicker {{
  display: inline-block; font-size: 0.78rem; font-weight: 600;
  letter-spacing: 0.12em; text-transform: uppercase; color: {ACCENT_2};
  margin-bottom: 0.6rem;
}}
.im-hero h1 {{
  margin: 0 0 0.6rem 0 !important; font-size: clamp(2.0rem, 4vw, 3.0rem) !important;
  font-weight: 800 !important; letter-spacing: -0.03em;
  background: linear-gradient(180deg, #ffffff 0%, #c8cbe0 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}}
.im-hero .im-tagline {{
  color: {INK}; font-size: 1.1rem; font-weight: 400; margin: 0 0 1.1rem 0; max-width: 60ch;
}}
.im-hero .im-badges {{ display: flex; flex-wrap: wrap; gap: 0.5rem; }}
.im-hero .im-badge {{
  display: inline-block; font-size: 0.78rem; font-weight: 500;
  padding: 4px 10px; border-radius: 999px;
  background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.12); color: {INK};
}}
.im-section {{
  display: flex; align-items: center; gap: 0.7rem; margin: 2.4rem 0 1.0rem 0;
}}
.im-section .im-bar {{
  width: 4px; height: 28px; border-radius: 4px;
  background: linear-gradient(180deg, {ACCENT}, {ACCENT_2});
}}
.im-section h2 {{
  margin: 0 !important; font-size: 1.35rem !important; font-weight: 700 !important;
  color: {INK}; letter-spacing: -0.02em;
}}
[data-testid="stExpander"] {{
  background: {SURFACE}; border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px; overflow: hidden; margin-bottom: 0.7rem;
}}
[data-testid="stExpander"] summary {{ padding: 0.85rem 1.0rem; font-weight: 600; }}
.stButton > button {{
  border-radius: 10px !important; border: 1px solid rgba(255,255,255,0.12) !important;
  font-weight: 600 !important;
  transition: transform 0.06s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}}
.stButton > button:hover {{
  border-color: {ACCENT} !important; box-shadow: 0 0 0 3px rgba(129,140,248,0.18);
  transform: translateY(-1px);
}}
.stButton > button[kind="primary"] {{
  background: linear-gradient(135deg, {ACCENT}, #6366f1) !important;
  color: white !important; border: 0 !important;
}}
[data-testid="stMetric"] {{
  background: {SURFACE}; border: 1px solid rgba(255,255,255,0.06);
  border-radius: 12px; padding: 0.9rem 1.0rem;
}}
[data-testid="stFileUploaderDropzone"] {{
  background: {SURFACE}; border: 2px dashed rgba(129,140,248,0.35) !important;
  border-radius: 12px !important;
}}
[data-testid="stDataFrame"] {{
  border-radius: 10px; overflow: hidden; border: 1px solid rgba(255,255,255,0.06);
}}
#MainMenu {{ visibility: hidden; }}
header[data-testid="stHeader"] {{ background: transparent; }}
footer {{ visibility: hidden; }}
.im-footer {{
  margin-top: 3rem; padding: 1.6rem 1.8rem; border-radius: 14px;
  background: linear-gradient(135deg, rgba(129,140,248,0.10), rgba(34,211,238,0.06));
  border: 1px solid rgba(255,255,255,0.08);
  display: flex; flex-wrap: wrap; gap: 1.4rem; align-items: center; justify-content: space-between;
}}
.im-footer .im-name {{ font-weight: 700; font-size: 1.05rem; color: {INK}; }}
.im-footer .im-name span {{ color: {MUTED}; font-weight: 400; }}
.im-footer .im-links {{ display: flex; gap: 1.0rem; flex-wrap: wrap; }}
.im-footer a {{
  color: {ACCENT_2} !important; text-decoration: none; font-weight: 500;
  border-bottom: 1px dashed rgba(34,211,238,0.45); padding-bottom: 1px;
}}
.im-footer a:hover {{ color: white !important; border-bottom-color: white; }}
</style>
"""


def _inject(html: str) -> None:
    """Inject HTML reliably across Streamlit versions.

    Prefers st.html (Streamlit 1.33+) which bypasses markdown sanitization.
    Falls back to st.markdown with unsafe_allow_html for older versions.
    """
    fn = getattr(st, "html", None)
    if callable(fn):
        fn(html)
    else:
        st.markdown(html, unsafe_allow_html=True)


def apply_branding() -> None:
    """Inject fonts + CSS. Call once near the top of app.py, after st.set_page_config."""
    _inject(CSS)


def hero(title: str, tagline: str, kicker: str = "", badges: list[str] | None = None) -> None:
    """Render the branded hero block."""
    badge_html = ""
    if badges:
        badge_html = '<div class="im-badges">' + "".join(
            f'<span class="im-badge">{b}</span>' for b in badges
        ) + '</div>'
    kicker_html = f'<div class="im-kicker">{kicker}</div>' if kicker else ""
    _inject(
        f'<div class="im-hero">{kicker_html}'
        f'<h1>{title}</h1>'
        f'<p class="im-tagline">{tagline}</p>'
        f'{badge_html}</div>'
    )


def section(title: str) -> None:
    """Section divider with an accent bar."""
    _inject(
        f'<div class="im-section"><div class="im-bar"></div><h2>{title}</h2></div>'
    )


def footer(repo_slug: str) -> None:
    """Standard contact footer."""
    _inject(
        '<div class="im-footer">'
        '<div class="im-name">Isaac Maya <span>· QA · Agentic AI · Data Quality</span></div>'
        '<div class="im-links">'
        '<a href="mailto:theisaacmaya@icloud.com">📧 Email</a>'
        '<a href="https://linkedin.com/in/isaac-maya" target="_blank">💼 LinkedIn</a>'
        f'<a href="https://github.com/isaac-maya/{repo_slug}" target="_blank">🔗 Source</a>'
        '<a href="https://isaac-maya.github.io/essays/" target="_blank">📝 Essays</a>'
        '</div></div>'
    )
