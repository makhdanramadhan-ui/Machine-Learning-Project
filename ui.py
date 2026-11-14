from __future__ import annotations

import base64
import math
from pathlib import Path
from urllib.parse import quote

LIGHT = {
    "canvas": "#F6F7F9",
    "surface": "#FFFFFF",
    "recess": "#EFF2F6",
    "ink": "#0F172A",
    "ink2": "#334155",
    "muted": "#5B6779",
    "rule": "#D3D9E3",
    "rule-soft": "#E5E9F0",
    "accent": "#1D4ED8",
    "accent-ink": "#FFFFFF",
    "accent-hi": "#1E40AF",
    "accent-soft": "#E3EBFD",
    "safe": "#0F766E",
    "safe-soft": "#DCF1EE",
    "mid": "#B45309",
    "mid-soft": "#FCEBD3",
    "high": "#BE123C",
    "high-soft": "#FBE1E7",
    "neutral": "#8A97AB",
    "shadow": "rgba(15, 23, 42, .10)",
}

DARK = {
    "canvas": "#0B1120",
    "surface": "#111827",
    "recess": "#1E293B",
    "ink": "#F8FAFC",
    "ink2": "#CBD5E1",
    "muted": "#94A3B8",
    "rule": "#2C3A50",
    "rule-soft": "#1F2B3E",
    "accent": "#60A5FA",
    "accent-ink": "#0B1120",
    "accent-hi": "#93C5FD",
    "accent-soft": "#1A2B4D",
    "safe": "#2DD4BF",
    "safe-soft": "#0F2E2E",
    "mid": "#FBBF24",
    "mid-soft": "#33270E",
    "high": "#FB7185",
    "high-soft": "#3A1522",
    "neutral": "#64748B",
    "shadow": "rgba(0, 0, 0, .45)",
}

THEMES = {"Terang": LIGHT, "Gelap": DARK}

_PATHS = {
    "target": '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3"/>'
              '<path d="M12 1v4M12 19v4M1 12h4M19 12h4"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "upload": '<path d="M12 16V4M7 9l5-5 5 5"/><path d="M4 16v3a1 1 0 0 0 1 1h14'
              'a1 1 0 0 0 1-1v-3"/>',
    "download": '<path d="M12 4v12M7 11l5 5 5-5"/><path d="M4 16v3a1 1 0 0 0 1 1h14'
                'a1 1 0 0 0 1-1v-3"/>',
    "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "linechart": '<path d="M3 20h18"/><path d="M4 16l5-5 4 3 7-8"/>',
    "search": '<circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5"/>',
    "check": '<path d="M4 12.5l5 5L20 6.5"/>',
    "alert": '<path d="M12 3l9.5 17H2.5L12 3z"/><path d="M12 10v4M12 17.5v.01"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.01"/>',
    "doc": '<path d="M14 3H7a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1V7z"/>'
          '<path d="M14 3v4h4"/>',
    "grid": '<rect x="3" y="3" width="7.5" height="7.5"/><rect x="13.5" y="3" width="7.5" height="7.5"/>'
            '<rect x="3" y="13.5" width="7.5" height="7.5"/><rect x="13.5" y="13.5" width="7.5" height="7.5"/>',
    "layers": '<path d="M12 3l9 5-9 5-9-5 9-5z"/><path d="M3 13l9 5 9-5"/>',
    "flag": '<path d="M5 21V4M5 5h11l-2 4 2 4H5"/>',
    "phone": '<rect x="7" y="2.5" width="10" height="19" rx="2"/><path d="M11 18.5h2"/>',
    "wifi": '<path d="M2.5 9a14 14 0 0 1 19 0M5.5 12.5a9.5 9.5 0 0 1 13 0M8.7 16a5 5 0 0 1 6.6 0"/>'
            '<path d="M12 19.5v.01"/>',
    "receipt": '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6"/>',
    "cube": '<path d="M12 2.5l8.5 4.5v10L12 21.5 3.5 17V7z"/><path d="M3.5 7L12 11.5 20.5 7M12 11.5v10"/>',
    "scale": '<path d="M12 3v18M5 21h14"/><path d="M5 7h14"/><path d="M5 7l-3 7a3.2 3.2 0 0 0 6 0zM19 7l-3 7a3.2 3.2 0 0 0 6 0z"/>',
}


def icon(name: str, size: int = 16, cls: str = "") -> str:
    body = _PATHS[name]
    return (f'<svg class="ico {cls}" width="{size}" height="{size}" viewBox="0 0 24 24" '
            f'fill="none" stroke="currentColor" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>')


def icon_uri(name: str) -> str:
    body = _PATHS[name]
    raw = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
           f'stroke="black" stroke-width="1.7" stroke-linecap="round" '
           f'stroke-linejoin="round">{body}</svg>')
    return "url(\"data:image/svg+xml,%s\")" % quote(raw, safe="")


_BASE_CSS = r"""
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"], .stApp {
    font-family: 'Archivo', 'Segoe UI', system-ui, -apple-system, sans-serif;
    font-feature-settings: 'tnum' 1, 'cv05' 1;
    font-variant-numeric: tabular-nums;
}
[data-testid="stAppViewContainer"] { background: var(--canvas); }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { opacity: .6; }
section[data-testid="stSidebar"] { display: none; }
[data-testid="stMainBlockContainer"] { padding: 2.9rem 2.4rem 3rem; max-width: 1440px; }
[data-testid="stMain"] { background: transparent; }
[data-testid="stVerticalBlock"] { gap: .7rem; }

.stMarkdown p { line-height: 1.6; }
html body [data-testid="stMarkdownContainer"],
html body [data-testid="stCaptionContainer"],
html body [data-testid="stWidgetLabel"] p,
html body label p,
html body [data-testid="stMarkdownContainer"] p,
html body [data-testid="stMarkdownContainer"] span,
html body [data-testid="stMarkdownContainer"] div,
html body [data-testid="stMarkdownContainer"] li,
html body [data-testid="stMarkdownContainer"] td,
html body [data-testid="stMarkdownContainer"] th,
html body [data-testid="stMarkdownContainer"] h1,
html body [data-testid="stMarkdownContainer"] h2,
html body [data-testid="stMarkdownContainer"] h3,
html body [data-testid="stMarkdownContainer"] h4,
html body [data-testid="stCaptionContainer"] p {
    font-family: 'Archivo', 'Segoe UI', system-ui, -apple-system, sans-serif !important; }
html body [data-testid="stMarkdownContainer"] .mono,
html body [data-testid="stMarkdownContainer"] .mono * ,
html body [data-testid="stMarkdownContainer"] .rb-meta,
html body [data-testid="stMarkdownContainer"] .rb-meta *,
html body [data-testid="stMarkdownContainer"] .risk-chip,
html body [data-testid="stMarkdownContainer"] .sheet-foot,
html body [data-testid="stMarkdownContainer"] .scale-tick,
html body [data-testid="stMarkdownContainer"] .scale-marker-val,
html body [data-testid="stMarkdownContainer"] .cb-val,
html body [data-testid="stMarkdownContainer"] .bench-scale span {
    font-family: 'JetBrains Mono', ui-monospace, monospace !important; }
html body code, html body pre, html body [data-testid="stCode"], html body .stCode {
    font-family: 'JetBrains Mono', ui-monospace, monospace !important; }
html body .stMarkdown h1, html body .stMarkdown h2, html body .stMarkdown h3,
html body .stMarkdown h4 { color: var(--ink) !important; letter-spacing: -0.015em; }
html body .stMarkdown p, html body .stMarkdown li { color: var(--ink2); }
html body .stMarkdown th { color: var(--ink) !important; font-weight: 600 !important; }
html body .stMarkdown td { color: var(--ink2) !important; }
html body .stMarkdown th, html body .stMarkdown td {
    background: transparent !important; border-bottom: 1px solid var(--rule-soft) !important;
    padding: .45rem .6rem !important; font-size: .82rem !important; }
html body .stMarkdown tr:last-child td { border-bottom: none !important; }
html body [data-testid="stCaptionContainer"] { color: var(--muted) !important; }
html body [data-testid="stWidgetLabel"] p, html body label p { color: var(--muted) !important; }
html body code { background: var(--accent-soft) !important; color: var(--ink) !important;
    border-radius: 4px; padding: 0 .25em; }
html body pre { background: var(--recess) !important; color: var(--ink) !important;
    border: 1px solid var(--rule-soft) !important; border-radius: 8px; }
html body pre code { background: transparent !important; color: inherit; padding: 0; }

html body [data-testid="stMarkdownContainer"]:has(> div, > section, > h3.sec-title, > svg) {
    margin-bottom: 0 !important; }

/* ---- kepala aplikasi ---- */
.brand { display: flex; align-items: center; gap: .95rem; min-width: 0; }
.brand-frame { flex: none; width: 52px; height: 52px; border-radius: 12px; padding: 5px;
    background: var(--surface); border: 1px solid var(--rule); display: grid; place-items: center; }
.brand-frame img { width: 100%; height: 100%; object-fit: contain; display: block;
    border-radius: 7px; }
.app-title { font-size: 1.45rem; font-weight: 700; letter-spacing: -0.02em; color: var(--ink);
    line-height: 1.2; }
.app-sub { margin: .25rem 0 0; font-size: .86rem; color: var(--muted) !important;
    max-width: 78ch; line-height: 1.5; }
.st-key-topbar { padding-bottom: .15rem; }

/* ---- pita ringkasan model ---- */
.ribbon { border: 1px solid var(--rule); border-radius: 14px; background: var(--surface);
    overflow: hidden; }
.rb-main { display: grid; grid-template-columns: minmax(0, 1.25fr) repeat(4, minmax(0, 1fr)); }
.rb-model, .kpi { padding: .85rem 1.15rem .9rem; min-width: 0;
    border-right: 1px solid var(--rule-soft); }
.kpi:last-child { border-right: none; }
.rb-model { display: flex; flex-direction: column; justify-content: center; gap: .55rem;
    background: var(--accent-soft); }
.rb-badge { align-self: flex-start; font-size: 1.05rem; font-weight: 650; color: var(--ink);
    letter-spacing: -0.01em; white-space: nowrap; }
.rb-model-sub { font-size: .78rem; color: var(--ink2) !important; line-height: 1.45; }
.kpi-key { display: block; font-size: .74rem; font-weight: 600; color: var(--muted);
    letter-spacing: .01em; margin-bottom: .3rem; }
.kpi-val { display: block; font-size: 1.7rem; font-weight: 700; color: var(--ink);
    letter-spacing: -0.03em; line-height: 1.1; font-variant-numeric: tabular-nums; }
.kpi-cap { display: block; font-size: .76rem; color: var(--muted); margin-top: .32rem;
    line-height: 1.4; }
.rb-meta { display: flex; flex-wrap: wrap; gap: .3rem 1.5rem; padding: .62rem 1.15rem;
    background: var(--recess); border-top: 1px solid var(--rule-soft); }
.rb-meta span { font-size: .68rem; color: var(--muted); white-space: nowrap; }
.rb-meta b { color: var(--ink); font-weight: 600; margin-left: .35rem; }

/* ---- tab: lintasan pil ---- */
div[role="tablist"] { display: flex !important; width: fit-content !important; gap: 4px; padding: 4px; border-bottom: none !important;
    background: var(--recess); border: 1px solid var(--rule-soft); border-radius: 14px;
    margin-bottom: 1rem; max-width: 100%; overflow-x: auto; scrollbar-width: none; }
div[role="tablist"]::-webkit-scrollbar { display: none; }
div[data-testid="stTabs"] > div[data-orientation] { border-bottom: none !important;
    box-shadow: none !important; }
div[data-testid="stTab"] { font-family: 'Archivo', sans-serif !important;
    font-size: .84rem !important; font-weight: 600 !important; letter-spacing: -0.005em;
    color: var(--muted) !important; background: transparent !important;
    padding: .5rem 1rem !important; margin: 0 !important; border-radius: 10px !important;
    white-space: nowrap; transition: color .15s ease, background-color .15s ease; }
div[data-testid="stTab"] p { font-size: inherit !important; font-weight: inherit !important;
    color: inherit !important; letter-spacing: inherit !important; }
div[data-testid="stTab"] p::before { content: ""; display: inline-block;
    width: 15px; height: 15px; margin-right: .5rem; vertical-align: -2.5px;
    background: currentColor; -webkit-mask: var(--tabicon) center/contain no-repeat;
    mask: var(--tabicon) center/contain no-repeat; }
div[data-testid="stTab"][aria-selected="true"] { color: var(--ink) !important;
    background: var(--surface) !important;
    box-shadow: 0 1px 2px var(--shadow), 0 3px 8px var(--shadow); }
div[data-testid="stTab"] .react-aria-SelectionIndicator { display: none !important; }
div[data-testid="stTab"]:hover { color: var(--ink) !important; }
div[data-testid="stTab"]:focus-visible { outline: 2px solid var(--accent); outline-offset: 1px; }
div[data-testid="stTabs"] > div:first-child::after { display: none; }

/* ---- judul bagian ---- */
html body .stMarkdown h3.sec-title, .sec-title { display: flex; align-items: center; gap: .55rem; font-size: 1.04rem;
    font-weight: 650; letter-spacing: -0.015em; color: var(--ink); margin: 0 0 .1rem; }
html body .stMarkdown h3.sec-title { font-size: 1.04rem !important; font-weight: 650 !important;
    padding: 0 !important; margin: 0 0 .1rem !important; line-height: 1.35 !important; }
.sec-title .ico { color: var(--accent); flex: none; }
.sec-note { font-size: .84rem; color: var(--muted) !important; margin: .2rem 0 .4rem;
    max-width: 82ch; line-height: 1.55; }
.sub-head { display: flex; align-items: center; gap: .55rem; font-size: .9rem; font-weight: 650;
    color: var(--ink); letter-spacing: -0.01em; padding-top: 1rem; margin-top: .45rem;
    border-top: 1px solid var(--rule-soft); }
.sub-head.first { border-top: none; padding-top: 0; margin-top: 0; }
.sub-head .ico { color: var(--accent); flex: none; }
.sub-head { margin-bottom: .45rem; }
.sub-head small { margin-left: auto; font-size: .72rem; font-weight: 500; color: var(--muted); }

/* ---- panel: satu bingkai, hook lewat key ---- */
[class*="st-key-panel"] { border: 1px solid var(--rule); border-radius: 14px;
    background: var(--surface); padding: 1.2rem 1.35rem 1.3rem; }
div[data-testid="stExpander"] { border: 1px solid var(--rule) !important;
    border-radius: 12px !important; background: var(--surface) !important;
    box-shadow: none !important; overflow: hidden; }
div[data-testid="stExpander"] details { border: none !important; background: transparent !important; }
div[data-testid="stExpander"] summary { font-size: .86rem !important; font-weight: 600 !important;
    color: var(--ink) !important; background: transparent !important; padding: .7rem 1rem !important; }
div[data-testid="stExpander"] summary:hover { background: var(--recess) !important; }
div[data-testid="stExpander"] summary svg { color: var(--muted); }
[class*="st-key-panel"] div[data-testid="stExpander"] { background: var(--canvas) !important; }

/* ---- kontrol ---- */
label p, [data-testid="stWidgetLabel"] p { font-size: .76rem !important;
    font-weight: 550 !important; color: var(--muted) !important;
    letter-spacing: 0; margin-bottom: .15rem !important; }
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stTextInput"] input {
    background: var(--surface) !important; color: var(--ink) !important;
    border: 1px solid var(--rule) !important; border-radius: 8px !important;
    font-size: .86rem !important; box-shadow: none !important; min-height: 2.5rem; }
html body [data-testid="stSelectbox"] [data-baseweb="select"] div,
html body [data-testid="stSelectbox"] input,
html body [data-testid="stNumberInput"] input,
html body [data-testid="stTextInput"] input {
    font-family: 'Archivo', 'Segoe UI', system-ui, sans-serif !important; }
div[data-testid="stSelectbox"]:hover > div > div,
div[data-testid="stNumberInputContainer"]:hover { border-color: var(--neutral) !important; }
div[data-testid="stNumberInputContainer"] {
    background: var(--surface) !important; border: 1px solid var(--rule) !important;
    border-radius: 8px !important; box-shadow: none !important; overflow: hidden;
    min-height: 2.5rem; }
div[data-testid="stNumberInput"] input {
    background: transparent !important; color: var(--ink) !important;
    border: none !important; box-shadow: none !important; font-size: .86rem !important;
    font-variant-numeric: tabular-nums; }
[data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] {
    background: var(--surface) !important; color: var(--ink2) !important;
    border-color: var(--rule) !important; }
[data-testid="stNumberInputStepUp"] svg, [data-testid="stNumberInputStepDown"] svg {
    fill: var(--ink2) !important; }
[data-testid="stNumberInputStepUp"]:hover, [data-testid="stNumberInputStepDown"]:hover {
    background: var(--accent-soft) !important; color: var(--ink) !important; }
div[data-testid="stSelectbox"] div[data-baseweb="select"] div,
div[data-testid="stSelectbox"] div[data-baseweb="select"] span,
div[data-testid="stSelectbox"] [role="combobox"] { color: var(--ink) !important; }
div[data-testid="stSelectbox"] [aria-disabled="true"],
div[data-testid="stSelectbox"] [disabled] { opacity: .62; }
div[data-testid="stSelectbox"] > div > div:focus-within,
div[data-testid="stNumberInputContainer"]:focus-within,
div[data-testid="stTextInput"] input:focus {
    border-color: var(--accent) !important; outline: none !important;
    box-shadow: 0 0 0 3px var(--accent-soft) !important; }
div[data-testid="stSelectbox"] svg { fill: var(--muted); }
div[data-testid="stSelectboxVirtualDropdown"] {
    background: var(--surface) !important; color: var(--ink) !important;
    border: 1px solid var(--rule) !important; border-radius: 10px !important; }
div[data-testid="stSelectboxVirtualDropdown"] [role="listbox"],
div[data-testid="stSelectboxVirtualDropdown"] [role="presentation"] {
    background: transparent !important; color: var(--ink) !important; }
div[data-testid="stSelectboxVirtualDropdown"] [role="option"] {
    font-size: .86rem !important; color: var(--ink) !important; }
div[data-testid="stSelectboxVirtualDropdown"] [role="option"][aria-selected="true"],
div[data-testid="stSelectboxVirtualDropdown"] [role="option"]:hover {
    background: var(--accent-soft) !important; color: var(--ink) !important; }
div[data-baseweb="popover"] > div, div[data-testid="stPopoverBody"], div[role="tooltip"] {
    background: var(--surface) !important; color: var(--ink) !important;
    border: 1px solid var(--rule) !important; }
div[role="tooltip"] * { color: var(--ink) !important; }

/* ---- tombol ---- */
.stButton > button, .stDownloadButton > button {
    border-radius: 10px !important; font-family: 'Archivo', sans-serif !important;
    font-size: .88rem !important; font-weight: 650 !important; min-height: 2.75rem;
    letter-spacing: -0.005em; box-shadow: none !important;
    border: 1px solid var(--rule) !important; background: var(--surface) !important;
    color: var(--ink) !important; transition: background .15s ease, border-color .15s ease; }
.stButton > button:hover, .stDownloadButton > button:hover {
    border-color: var(--accent) !important; background: var(--accent-soft) !important; }
.stButton > button[kind="primary"], .stDownloadButton > button[kind="primary"] {
    background: var(--accent) !important; color: var(--accent-ink) !important;
    border-color: var(--accent) !important; }
.stButton > button[kind="primary"] *, .stDownloadButton > button[kind="primary"] * {
    color: var(--accent-ink) !important; }
.stButton > button[kind="primary"]:hover, .stDownloadButton > button[kind="primary"]:hover {
    background: var(--accent-hi) !important; border-color: var(--accent-hi) !important; }
.stButton > button[kind="primary"]:hover *, .stDownloadButton > button[kind="primary"]:hover * {
    color: var(--accent-ink) !important; }
.stButton > button:active, .stDownloadButton > button:active { transform: translateY(1px); }
.stButton > button:focus-visible, .stDownloadButton > button:focus-visible {
    outline: 2px solid var(--accent) !important; outline-offset: 2px !important; }
.stButton > button:disabled { opacity: .45 !important; }

[data-testid="stFileUploaderDropzone"] { background: var(--recess) !important;
    border: 1.5px dashed var(--neutral) !important; border-radius: 12px !important;
    color: var(--ink2) !important; }
[data-testid="stFileUploaderDropzone"]:hover { border-color: var(--accent) !important; }
[data-testid="stFileUploaderDropzone"] * { color: var(--ink2); }
[data-testid="stFileUploaderDropzone"] small { color: var(--muted) !important; }
[data-testid="stFileUploaderDropzone"] button {
    background: var(--surface) !important; color: var(--ink) !important;
    border: 1px solid var(--rule) !important; border-radius: 8px !important; }
[data-testid="stFileUploaderDropzone"] button * { color: var(--ink) !important; }
[data-testid="stFileUploaderDropzone"] button:hover { border-color: var(--accent) !important; }
[data-testid="stFileUploaderFile"] * { color: var(--ink2) !important; }

/* ---- pengalih tema ---- */
div[data-testid="stButtonGroup"] { background: var(--recess) !important;
    border: 1px solid var(--rule-soft) !important; border-radius: 12px !important;
    padding: 3px !important; gap: 3px !important; width: 100% !important; }
div[data-testid="stButtonGroup"] button { font-family: 'Archivo', sans-serif !important;
    font-size: .8rem !important; font-weight: 600 !important; border-radius: 9px !important;
    color: var(--muted) !important; background: transparent !important;
    border: 1px solid transparent !important; box-shadow: none !important; min-height: 2.2rem; }
div[data-testid="stButtonGroup"] button:hover { color: var(--ink) !important; }
div[data-testid="stButtonGroup"] button[aria-checked="true"],
div[data-testid="stButtonGroup"] button[data-checked="true"],
div[data-testid="stButtonGroup"] button[aria-pressed="true"] {
    background: var(--surface) !important; color: var(--ink) !important;
    box-shadow: 0 1px 2px var(--shadow), 0 2px 6px var(--shadow) !important; }

/* ---- snapshot pelanggan ---- */
.snap { border: 1px solid var(--rule); border-radius: 14px; background: var(--surface);
    padding: .85rem 1.15rem .95rem; }
.snap-head { display: flex; align-items: center; justify-content: space-between; gap: .6rem;
    margin-bottom: .75rem; }
html body .stMarkdown h4 { font-size: .95rem !important; padding: 0 !important;
    margin: 0 0 .3rem !important; line-height: 1.3 !important; color: var(--ink) !important; }
.snap-head h4 { margin: 0; display: flex; align-items: center; gap: .5rem; font-size: .95rem;
    font-weight: 650; color: var(--ink); }
.snap-head h4 .ico { color: var(--accent); }
.snap-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: .6rem;
    margin: 0 0 .8rem; }
.snap-grid div { background: var(--recess); border-radius: 10px; padding: .45rem .7rem;
    min-width: 0; }
.snap-grid dt { font-size: .7rem; color: var(--muted); font-weight: 550; margin: 0 0 .15rem; }
.snap-grid dd { margin: 0; font-size: .9rem; font-weight: 650; color: var(--ink);
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.bench-head { display: flex; align-items: baseline; justify-content: space-between; gap: .6rem;
    margin-bottom: .55rem; }
.bench-head span { font-size: .76rem; color: var(--muted); font-weight: 550; }
.bench-head b { font-size: 1.2rem; color: var(--ink); font-weight: 700; letter-spacing: -0.02em; }
.bench-track { position: relative; height: 10px; border-radius: 999px; background: var(--recess);
    border: 1px solid var(--rule-soft); }
.bench-iqr { position: absolute; top: -1px; bottom: -1px; border-radius: 999px;
    background: var(--accent-soft); border: 1px solid var(--accent); opacity: .9; }
.bench-med { position: absolute; top: -4px; bottom: -4px; width: 2px; background: var(--ink2);
    transform: translateX(-1px); }
.bench-pin { position: absolute; top: 50%; width: 16px; height: 16px; border-radius: 50%;
    background: var(--ink); border: 3px solid var(--surface); transform: translate(-50%, -50%);
    box-shadow: 0 0 0 1px var(--ink); }
.bench-pin.out { background: var(--high); box-shadow: 0 0 0 1px var(--high); }
.bench-scale { display: flex; justify-content: space-between; margin-top: .45rem; }
.bench-scale span { font-size: .66rem; color: var(--muted); }
.bench-note { margin: .55rem 0 0; font-size: .78rem; color: var(--ink2) !important; line-height: 1.45; }

/* ---- keadaan siap ---- */
.ready { border: 1px dashed var(--neutral); border-radius: 14px; background: var(--surface);
    padding: 1.05rem 1.15rem 1.1rem; }
.ready h4 { margin: 0 0 .7rem; display: flex; align-items: center; gap: .5rem; font-size: .95rem;
    font-weight: 650; color: var(--ink); }
.ready h4 .ico { color: var(--accent); }
.ready-text { margin: 0 0 .75rem; font-size: .82rem; color: var(--muted) !important; line-height: 1.5; }
.band-list { display: grid; gap: .45rem; }
.band-row { display: flex; align-items: center; gap: .6rem; font-size: .82rem; color: var(--ink2); }
.band-row .risk-chip { min-width: 4.9rem; text-align: center; }

/* ---- vonis + gauge ---- */
.verdict { border: 1px solid var(--rule); border-radius: 14px; background: var(--surface);
    padding: .9rem 1.15rem 1rem; }
.verdict-gauge { width: 100%; max-width: 330px; margin: 0 auto; }
.verdict-gauge svg { width: 100%; height: auto; display: block; overflow: visible; }
.g-band { fill: none; stroke-width: 14; stroke-linecap: butt; opacity: .26; }
.g-val { fill: none; stroke-width: 14; stroke-linecap: round; }
.g-low { stroke: var(--safe); } .g-mid { stroke: var(--mid); } .g-high { stroke: var(--high); }
.g-tick { stroke: var(--ink); stroke-width: 2; }
.g-label { fill: var(--muted); font-size: 10.5px; font-weight: 600; }
.g-num { fill: var(--ink); font-size: 36px; font-weight: 700; letter-spacing: -0.03em;
    font-variant-numeric: tabular-nums; }
.g-cap { fill: var(--muted); font-size: 10.5px; font-weight: 550; }
.verdict-meta { display: flex; align-items: center; justify-content: center; gap: .7rem;
    flex-wrap: wrap; margin-top: .35rem; }
.risk-chip { display: inline-flex; align-items: center; font-size: .68rem;
    font-weight: 600; letter-spacing: .08em; text-transform: uppercase; padding: .3rem .6rem;
    border-radius: 999px; }
.risk-low { background: var(--safe-soft); color: var(--safe); }
.risk-mid { background: var(--mid-soft); color: var(--mid); }
.risk-high { background: var(--high-soft); color: var(--high); }
.verdict-decision { font-size: .86rem; color: var(--ink2) !important; }
.verdict-decision b { color: var(--ink); font-weight: 700; }
.verdict-decision b.hot { color: var(--high); }
.verdict-sub { text-align: center; font-size: .76rem; color: var(--muted) !important;
    margin-top: .25rem; }

/* ---- skala probabilitas terkalibrasi ---- */
.scale { border: 1px solid var(--rule); border-radius: 14px; background: var(--surface);
    padding: .9rem 1.15rem .8rem; }
.scale-head { display: flex; justify-content: space-between; align-items: baseline;
    margin-bottom: 1.9rem; gap: 1rem; flex-wrap: wrap; }
.scale-title { font-size: .84rem; font-weight: 650; color: var(--ink) !important; }
.scale-note { font-size: .72rem; color: var(--muted) !important; }
.scale-track { position: relative; height: 12px; border-radius: 999px; display: flex;
    overflow: visible; }
.scale-seg { height: 100%; }
.seg-low { background: var(--safe); flex: none; border-radius: 999px 0 0 999px; opacity: .85; }
.seg-mid { background: var(--mid); flex: none; opacity: .85; }
.seg-high { background: var(--high); flex: 1; border-radius: 0 999px 999px 0; opacity: .85; }
.scale-marker { position: absolute; top: -6px; bottom: -6px; width: 3px; background: var(--ink);
    transform: translateX(-1.5px); border-radius: 2px; }
.scale-marker-val { position: absolute; top: -1.7rem; left: 50%; transform: translateX(-50%);
    font-size: .7rem; font-weight: 600; color: var(--ink); white-space: nowrap;
    background: var(--surface); border: 1px solid var(--rule); border-radius: 6px;
    padding: .1rem .38rem; }
.scale-ticks { position: relative; height: 1.1rem; margin-top: .55rem; }
.scale-tick { position: absolute; transform: translateX(-50%); font-size: .62rem;
    color: var(--muted); white-space: nowrap; }
.scale-tick.hard { color: var(--ink2); font-weight: 600; }
.scale-tick:first-child { transform: translateX(0); }
.scale-tick:last-child { transform: translateX(-100%); }

/* ---- kontribusi fitur ---- */
.contrib { border: 1px solid var(--rule); border-radius: 14px; background: var(--surface);
    padding: .95rem 1.15rem 1rem; }
.contrib h4 { margin: 0 0 .15rem; display: flex; align-items: center; gap: .5rem; font-size: .95rem;
    font-weight: 650; color: var(--ink); }
.contrib h4 .ico { color: var(--accent); }
.contrib-note { margin: 0 0 .7rem; font-size: .76rem; color: var(--muted) !important;
    line-height: 1.5; }
.cb-group { font-size: .72rem; font-weight: 650; color: var(--muted); margin: .65rem 0 .3rem;
    display: flex; align-items: center; gap: .4rem; }
.cb-group i { width: 8px; height: 8px; border-radius: 2px; }
.cb-group.up i { background: var(--high); } .cb-group.down i { background: var(--safe); }
.cb-row { margin-bottom: .5rem; }
.cb-label { display: flex; justify-content: space-between; gap: .6rem; font-size: .8rem;
    color: var(--ink2); margin-bottom: .2rem; }
.cb-val { font-size: .72rem; color: var(--muted); white-space: nowrap; }
.cb-track { display: grid; grid-template-columns: 1fr 1fr; height: 8px; position: relative; }
.cb-track::after { content: ""; position: absolute; left: 50%; top: -2px; bottom: -2px; width: 1px;
    background: var(--neutral); }
.cb-neg, .cb-pos { position: relative; background: var(--recess); }
.cb-neg { border-radius: 999px 0 0 999px; display: flex; justify-content: flex-end; }
.cb-pos { border-radius: 0 999px 999px 0; }
.cb-neg i, .cb-pos i { display: block; height: 100%; }
.cb-neg i { background: var(--safe); border-radius: 999px 0 0 999px; }
.cb-pos i { background: var(--high); border-radius: 0 999px 999px 0; }

/* ---- saran ---- */
.rec-list { border: 1px solid var(--rule); border-radius: 14px; background: var(--surface);
    padding: .3rem 1.15rem; }
.rec { display: flex; gap: .75rem; padding: .75rem 0; border-bottom: 1px solid var(--rule-soft);
    font-size: .84rem; color: var(--ink2) !important; line-height: 1.5; }
.rec:last-child { border-bottom: none; }
.rec-rank { flex: none; width: 24px; height: 24px; border-radius: 50%; display: grid;
    place-items: center; background: var(--accent-soft); color: var(--accent);
    font-size: .74rem; font-weight: 700; margin-top: .05rem; }
.rec b { color: var(--ink); font-weight: 650; }

/* ---- matriks konfusi ---- */
.cm { display: grid; grid-template-columns: auto minmax(0, 1fr) minmax(0, 1fr); gap: 4px;
    margin: .2rem 0 .5rem; }
.cm-axis { font-size: .7rem; font-weight: 600; color: var(--muted); display: flex;
    align-items: center; justify-content: center; text-align: center; padding: .15rem .3rem; }
.cm-axis.row { writing-mode: vertical-rl; transform: rotate(180deg); }
.cm-cell { padding: .8rem .95rem .85rem; border-radius: 10px; background: var(--recess);
    border: 1px solid var(--rule-soft); min-width: 0; }
.cm-cell.ok { background: var(--safe-soft); border-color: transparent; }
.cm-cell.bad { background: var(--high-soft); border-color: transparent; }
.cm-key { display: block; font-size: .72rem; font-weight: 650; color: var(--ink2); margin-bottom: .2rem; }
.cm-val { display: block; font-size: 1.7rem; font-weight: 700; letter-spacing: -0.03em;
    color: var(--ink); font-variant-numeric: tabular-nums; line-height: 1.1; }
.cm-pct { display: block; font-size: .76rem; font-weight: 600; color: var(--ink2);
    font-variant-numeric: tabular-nums; margin-top: .1rem; }
.cm-desc { display: block; font-size: .72rem; color: var(--muted) !important; margin-top: .25rem;
    line-height: 1.35; }

/* ---- strip ringkasan ---- */
.summary-strip { display: grid; grid-template-columns: repeat(var(--n, 4), minmax(0, 1fr));
    border: 1px solid var(--rule); border-radius: 14px; overflow: hidden; background: var(--surface); }
.summary-strip > div { padding: .85rem 1.1rem; border-right: 1px solid var(--rule-soft);
    min-width: 0; }
.summary-strip > div:last-child { border-right: none; }
.summary-strip .kpi-val { font-size: 1.6rem; }
.summary-strip .kpi-val.hot { color: var(--high); }
.summary-strip .kpi-val.ok { color: var(--safe); }

/* ---- kartu model ---- */
.model-strip { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: .8rem; }
.model-card { border: 1px solid var(--rule); border-radius: 14px; background: var(--surface);
    padding: .9rem 1.05rem 1rem; min-width: 0; }
.model-card.sel { border-color: var(--accent); background: var(--accent-soft); }
.mc-head { display: flex; align-items: center; justify-content: space-between; gap: .5rem;
    margin-bottom: .65rem; }
.mc-name { font-size: .95rem; font-weight: 650; color: var(--ink); }
.mc-tag { font-size: .66rem; font-weight: 650; padding: .2rem .5rem; border-radius: 999px;
    background: var(--accent); color: var(--accent-ink); white-space: nowrap; }
.mc-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .5rem .8rem; }
.mc-grid span { display: block; font-size: .7rem; color: var(--muted); font-weight: 550; }
.mc-grid b { display: block; font-size: 1.1rem; font-weight: 700; color: var(--ink);
    letter-spacing: -0.02em; font-variant-numeric: tabular-nums; }

/* ---- galeri EDA ---- */
.fig-note { font-size: .82rem; color: var(--ink2) !important; line-height: 1.55;
    background: var(--recess); border-radius: 10px; padding: .7rem .85rem; margin-top: .4rem; }
[data-testid="stImage"] img { border: 1px solid var(--rule-soft); border-radius: 10px;
    background: #FFFFFF; display: block; }
[data-testid="stImage"] { margin: 0; }
.doc-links { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .8rem; }
.doc-link { display: flex; align-items: center; gap: .75rem; padding: .85rem 1rem;
    border: 1px solid var(--rule); border-radius: 12px; background: var(--surface);
    text-decoration: none !important; color: var(--ink) !important; font-size: .86rem;
    font-weight: 600; transition: border-color .15s ease, background-color .15s ease; }
.doc-link:hover { border-color: var(--accent); background: var(--accent-soft); }
.doc-link .ico { color: var(--accent); flex: none; }

/* ---- tabel dan grafik ---- */
[data-testid="stDataFrame"] { border: 1px solid var(--rule); border-radius: 10px;
    overflow: hidden; }
[data-testid="stDataFrameResizable"] { border: none !important; }
[data-testid="stVegaLiteChart"] { background: transparent; }
.chart-title { font-size: .86rem; font-weight: 650; color: var(--ink); margin: 0 0 .1rem; }
.chart-sub { font-size: .76rem; color: var(--muted) !important; margin: 0 0 .3rem; line-height: 1.45; }

/* ---- pesan ---- */
[data-testid="stAlert"] { border-radius: 10px !important; border: 1px solid var(--rule) !important;
    background: var(--surface) !important; font-size: .85rem !important; }
[data-testid="stAlertContainer"] { background: transparent !important; color: var(--ink2) !important; }
[data-testid="stAlertContainer"] * { color: var(--ink2) !important; }
div[data-testid="stAlert"][data-baseweb="callout"][kind="error"],
div[data-testid="stAlert"][kind="error"] { border-color: var(--high) !important;
    background: var(--high-soft) !important; }
div[data-testid="stAlert"][data-baseweb="callout"][kind="warning"],
div[data-testid="stAlert"][kind="warning"] { border-color: var(--mid) !important;
    background: var(--mid-soft) !important; }
div[data-testid="stAlert"][kind="info"], div[data-testid="stAlert"][kind="success"] {
    border-color: var(--accent) !important; background: var(--accent-soft) !important; }

/* ---- gerak ---- */
.scale-marker { animation: marker-in .5s cubic-bezier(.16, .84, .44, 1) both; }
@keyframes marker-in { from { opacity: 0; transform: translateX(-1.5px) scaleY(.35); }
    to { opacity: 1; transform: translateX(-1.5px) scaleY(1); } }
.g-val { stroke-dasharray: 400; stroke-dashoffset: 0;
    animation: g-in .7s cubic-bezier(.16, .84, .44, 1) both; }
@keyframes g-in { from { stroke-dashoffset: 400; } to { stroke-dashoffset: 0; } }
.ribbon, .snap, .verdict, .scale, .contrib, .model-card, .rec-list,
div[data-testid="stExpander"], [class*="st-key-panel"] {
    transition: background-color .2s ease, border-color .2s ease, color .2s ease; }
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation-duration: .001ms !important;
        animation-iteration-count: 1 !important; transition-duration: .001ms !important; } }

/* ---- footer ---- */
.sheet-foot { margin-top: 2rem; padding-top: .85rem; border-top: 1px solid var(--rule);
    font-size: .7rem; letter-spacing: .02em; color: var(--muted) !important; }

/* ---- layar kecil ---- */
@media (max-width: 1100px) {
    .rb-main { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .rb-model { grid-column: 1 / -1; border-right: none; border-bottom: 1px solid var(--rule-soft); }
    .kpi:nth-child(3), .kpi:nth-child(5) { border-right: none; }
    .kpi:nth-child(n+4) { border-top: 1px solid var(--rule-soft); }
    .model-strip { grid-template-columns: 1fr; }
}
@media (max-width: 900px) {
    [data-testid="stMainBlockContainer"] { padding: 3rem .9rem 2rem; }
    .app-title { font-size: 1.2rem; }
    .summary-strip { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .summary-strip > div:nth-child(2n) { border-right: none; }
    .summary-strip > div:nth-child(n+3) { border-top: 1px solid var(--rule-soft); }
    .doc-links { grid-template-columns: 1fr; }
    [class*="st-key-panel"] { padding: 1rem 1rem 1.1rem; }
    div[data-testid="stTab"] { padding: .5rem .7rem !important; font-size: .78rem !important; }
}
@media (max-width: 640px) {
    .kpi-val { font-size: 1.5rem; }
    .snap-grid { grid-template-columns: 1fr; }
    .brand-frame { width: 44px; height: 44px; }
    .rb-meta { gap: .3rem 1rem; }
    div[data-testid="stTab"] p::before { margin-right: .3rem; }
}

/* ---- fokus & aksesibilitas ---- */
::selection { background: var(--accent); color: var(--accent-ink); }
a { color: var(--accent) !important; text-underline-offset: 3px; }
a:hover { text-decoration-thickness: 2px; }
*:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
"""


TAB_ICONS = ("user", "upload", "chart", "search")

_FONT_FILES = (
    ("Archivo", "archivo-latin.woff2", "400 700"),
    ("JetBrains Mono", "jetbrains-mono-latin.woff2", "400 700"),
)
_FONT_CSS_CACHE = []
_BRAND_CACHE = []


def font_face_css() -> str:
    if _FONT_CSS_CACHE:
        return _FONT_CSS_CACHE[0]
    base = Path(__file__).resolve().parent / "static" / "fonts"
    blocks = []
    for family, filename, weight in _FONT_FILES:
        path = base / filename
        if not path.exists():
            continue
        encoded = base64.b64encode(path.read_bytes()).decode("ascii")
        blocks.append(
            "@font-face{font-family:" + family + ";"
            "src:url(data:font/woff2;base64," + encoded + ") format('woff2');"
            "font-weight:" + weight + ";font-style:normal;font-display:swap;}")
    css = "<style>\n%s\n</style>" % "\n".join(blocks)
    _FONT_CSS_CACHE.append(css)
    return css


def brand_mark_uri() -> str:
    if _BRAND_CACHE:
        return _BRAND_CACHE[0]
    path = Path(__file__).resolve().parent / "assets" / "brand-mark.png"
    uri = ""
    if path.exists():
        uri = "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode("ascii")
    _BRAND_CACHE.append(uri)
    return uri


def _tab_icon_css() -> str:
    return "\n".join(
        'div[role="tablist"] > div:nth-child(%d) { --tabicon: %s; }' % (i, icon_uri(name))
        for i, name in enumerate(TAB_ICONS, start=1)
    )


def build_css(theme: str) -> str:
    tokens = THEMES[theme]
    root = "\n".join("  --%s: %s;" % (k, v) for k, v in tokens.items())
    streamlit_vars = (
        "--background-color: %(canvas)s;"
        "--text-color: %(ink)s;"
        "--text-color-light: %(ink2)s;"
        "--primary-color: %(accent)s;"
        "--secondary-background-color: %(surface)s;"
        "--border-color: %(rule)s;"
        "--font-family-body: 'Archivo', 'Segoe UI', system-ui, sans-serif;"
        "--font-family: 'Archivo', 'Segoe UI', system-ui, sans-serif;"
        "--font-family-code: 'JetBrains Mono', ui-monospace, monospace;"
    ) % tokens
    body = "\n".join(line for line in _BASE_CSS.splitlines() if line.strip())
    tabs = _tab_icon_css()
    if theme == "Gelap":
        tabs += '\n[data-testid="stDataFrameResizable"] { filter: invert(.92) hue-rotate(180deg); }'
    return (
        "<style>\n:root {\n%s\n}\n"
        "html body, html body [data-testid=\"stAppViewContainer\"] {\n%s\n}\n"
        "%s\n%s\n</style>"
    ) % (root, streamlit_vars, body, tabs)


def header_bar(title: str, subtitle: str) -> str:
    uri = brand_mark_uri()
    img = '<img src="%s" alt="Logo Kelompok 12" />' % uri if uri else ""
    return (
        '<div class="brand"><span class="brand-frame">%s</span>'
        '<div><div class="app-title">%s</div><div class="app-sub">%s</div></div></div>'
    ) % (img, title, subtitle)


def model_ribbon(model_label: str, kpis, meta) -> str:
    parts = [
        '<section class="ribbon" aria-label="Ringkasan model">',
        '<div class="rb-main"><div class="rb-model">'
        '<span class="rb-badge">%s</span>'
        '<span class="rb-model-sub">Model aplikasi dengan probabilitas terkalibrasi, '
        'diuji pada data uji.</span></div>' % model_label,
    ]
    for key, value, caption in kpis:
        parts.append('<div class="kpi"><span class="kpi-key">%s</span>'
                     '<span class="kpi-val">%s</span><span class="kpi-cap">%s</span></div>'
                     % (key, value, caption))
    parts.append('</div><div class="rb-meta">')
    for key, value in meta:
        parts.append("<span>%s<b>%s</b></span>" % (key, value))
    parts.append("</div></section>")
    return "".join(parts)


def _inline_code(text: str) -> str:
    parts = text.split("`")
    return "".join(("<code>%s</code>" % part) if i % 2 else part for i, part in enumerate(parts))


def section(title: str, icon_name: str, note: str = "") -> str:
    note = _inline_code(note)
    head = '<h3 class="sec-title">%s %s</h3>' % (icon(icon_name), title)
    if note:
        return head + '<div class="sec-note">%s</div>' % note
    return head


def sub_head(title: str, icon_name: str, hint: str = "", first: bool = False) -> str:
    small = "<small>%s</small>" % hint if hint else ""
    return '<div class="sub-head%s">%s<span>%s</span>%s</div>' % (
        " first" if first else "", icon(icon_name, 17), title, small)


def risk_chip(level: str) -> str:
    slug = {"RENDAH": "low", "SEDANG": "mid", "TINGGI": "high"}.get(level, "low")
    return '<span class="risk-chip risk-%s">%s</span>' % (slug, level)


def _arc(cx: float, cy: float, r: float, p0: float, p1: float) -> str:
    def point(p):
        angle = math.pi * p
        return cx - r * math.cos(angle), cy - r * math.sin(angle)

    x0, y0 = point(p0)
    x1, y1 = point(p1)
    return "M%.2f %.2f A%g %g 0 0 1 %.2f %.2f" % (x0, y0, r, r, x1, y1)


def risk_gauge(prob: float, threshold: float, high: float, level: str) -> str:
    cx, cy, r = 130.0, 120.0, 92.0
    p = max(0.0, min(1.0, prob))
    cls = {"RENDAH": "g-low", "SEDANG": "g-mid", "TINGGI": "g-high"}.get(level, "g-low")

    def tick(pos, label, dy=0):
        angle = math.pi * pos
        ca, sa = math.cos(angle), math.sin(angle)
        x_in, y_in = cx - (r - 11) * ca, cy - (r - 11) * sa
        x_out, y_out = cx - (r + 10) * ca, cy - (r + 10) * sa
        x_lab, y_lab = cx - (r + 22) * ca, cy - (r + 22) * sa + 3 + dy
        anchor = "end" if ca > 0.25 else ("start" if ca < -0.25 else "middle")
        return (
            '<line class="g-tick" x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"/>'
            '<text class="g-label" x="%.2f" y="%.2f" text-anchor="%s">%s</text>'
            % (x_in, y_in, x_out, y_out, x_lab, y_lab, anchor, label))

    value_arc = ""
    if p > 0:
        value_arc = '<path class="g-val %s" d="%s"/>' % (cls, _arc(cx, cy, r, 0, p))
    svg = (
        '<svg viewBox="0 0 260 150" role="img" aria-label="Probabilitas churn %s, threshold %s">'
        '<path class="g-band g-low" d="%s"/>'
        '<path class="g-band g-mid" d="%s"/>'
        '<path class="g-band g-high" d="%s"/>'
        '%s%s%s'
        '<text class="g-num" x="130" y="108" text-anchor="middle">%s</text>'
        '<text class="g-cap" x="130" y="126" text-anchor="middle">probabilitas churn</text>'
        '<text class="g-label" x="%.2f" y="%.2f" text-anchor="middle">0%%</text>'
        '<text class="g-label" x="%.2f" y="%.2f" text-anchor="middle">100%%</text>'
        '</svg>'
    ) % (
        fmt_pct(prob), fmt_pct(threshold),
        _arc(cx, cy, r, 0, threshold), _arc(cx, cy, r, threshold, high), _arc(cx, cy, r, high, 1),
        value_arc, tick(threshold, fmt_pct(threshold)), tick(high, fmt_pct(high)),
        fmt_num(p * 100) + "%",
        cx - r, cy + 20, cx + r, cy + 20,
    )
    return svg


def verdict(prob: float, threshold: float, high: float, level: str, pred: int) -> str:
    decision = "CHURN" if pred == 1 else "TETAP"
    return (
        '<div class="verdict"><div class="verdict-gauge">%s</div>'
        '<div class="verdict-meta">%s<span class="verdict-decision">Keputusan model: '
        '<b class="%s">%s</b></span></div>'
        '<div class="verdict-sub">Probabilitas churn terkalibrasi</div></div>'
    ) % (risk_gauge(prob, threshold, high, level), risk_chip(level),
         "hot" if pred == 1 else "", decision)


def calibrated_scale(prob: float, threshold: float, high: float) -> str:
    lo_pct = threshold * 100
    hi_pct = high * 100
    mid_pct = hi_pct - lo_pct
    value = max(0.0, min(100.0, prob * 100))
    return (
        '<div class="scale">'
        '<div class="scale-head"><span class="scale-title">Skala risiko terkalibrasi</span>'
        '<span class="scale-note">Threshold %s · batas kategori tinggi %s</span></div>'
        '<div class="scale-track">'
        '<div class="scale-seg seg-low" style="width:%s%%"></div>'
        '<div class="scale-seg seg-mid" style="width:%s%%"></div>'
        '<div class="scale-seg seg-high"></div>'
        '<div class="scale-marker" style="left:%s%%">'
        '<span class="scale-marker-val">%s</span></div>'
        '</div>'
        '<div class="scale-ticks">'
        '<span class="scale-tick" style="left:0%%">0%%</span>'
        '<span class="scale-tick hard" style="left:%s%%">threshold %s</span>'
        '<span class="scale-tick" style="left:%s%%">%s</span>'
        '<span class="scale-tick" style="left:100%%">100%%</span>'
        '</div></div>'
    ) % (fmt_pct(threshold), fmt_pct(high),
         css_num(lo_pct), css_num(mid_pct), css_num(value),
         fmt_num(value) + "%",
         css_num(lo_pct), fmt_pct(threshold), css_num(hi_pct), fmt_pct(high))


def snapshot(contract: str, internet: str, tenure: str, charge: float, ref: dict,
             charge_text: str, status: str, outside: bool, low_text: str, high_text: str,
             med_text: str) -> str:
    span = max(ref["max"] - ref["min"], 1e-9)

    def pos(value):
        return max(0.0, min(100.0, (value - ref["min"]) / span * 100))

    q1, q3 = pos(ref["q1"]), pos(ref["q3"])
    return (
        '<div class="snap"><div class="snap-head"><h4>%s Ringkasan Pelanggan</h4>'
        '</div>'
        '<dl class="snap-grid"><div><dt>Kontrak</dt><dd>%s</dd></div>'
        '<div><dt>Layanan internet</dt><dd>%s</dd></div>'
        '<div><dt>Lama berlangganan</dt><dd>%s</dd></div></dl>'
        '<div class="bench-head"><span>Tagihan bulanan dibanding data latih</span><b>%s</b></div>'
        '<div class="bench-track" role="img" aria-label="Posisi tagihan terhadap rentang data latih">'
        '<div class="bench-iqr" style="left:%s%%;width:%s%%"></div>'
        '<div class="bench-med" style="left:%s%%"></div>'
        '<div class="bench-pin%s" style="left:%s%%"></div></div>'
        '<div class="bench-scale"><span>%s</span><span>median %s</span><span>%s</span></div>'
        '<div class="bench-note">%s</div></div>'
    ) % (icon("user", 17), contract, internet, tenure, charge_text,
         css_num(q1), css_num(max(q3 - q1, 1.0)), css_num(pos(ref["median"])),
         " out" if outside else "", css_num(pos(charge)),
         low_text, med_text, high_text, status)


def ready_state(threshold: float, high: float) -> str:
    return (
        '<div class="ready"><h4>%s Aturan Klasifikasi Risiko</h4>'
        '<div class="band-list">'
        '<div class="band-row">%s<span>di bawah %s: model memprediksi TETAP</span></div>'
        '<div class="band-row">%s<span>%s sampai di bawah %s: diprediksi CHURN</span></div>'
        '<div class="band-row">%s<span>%s ke atas: diprediksi CHURN dengan risiko tinggi</span></div>'
        '</div></div>'
    ) % (icon("target", 17),
         risk_chip("RENDAH"), fmt_pct(threshold),
         risk_chip("SEDANG"), fmt_pct(threshold), fmt_pct(high),
         risk_chip("TINGGI"), fmt_pct(high))


def contributions(ups, downs, scale_max: float, note: str) -> str:
    def row(label, value):
        width = abs(value) / scale_max * 100 if scale_max else 0
        width = max(2.0, min(100.0, width))
        pos_i = '<i style="width:%s%%"></i>' % css_num(width) if value > 0 else ""
        neg_i = '<i style="width:%s%%"></i>' % css_num(width) if value < 0 else ""
        sign = "+" if value > 0 else "−"
        return (
            '<div class="cb-row"><div class="cb-label"><span>%s</span>'
            '<span class="cb-val">%s%s</span></div>'
            '<div class="cb-track"><div class="cb-neg">%s</div><div class="cb-pos">%s</div></div></div>'
            % (label, sign, fmt_num(abs(value)), neg_i, pos_i))

    out = ['<div class="contrib"><h4>%s Faktor Utama Pelanggan Ini</h4>'
           '<div class="contrib-note">%s</div>' % (icon("scale", 17), note)]
    if ups:
        out.append('<div class="cb-group up"><i></i>Mendorong risiko churn naik</div>')
        out.extend(row(label, value) for label, value in ups)
    if downs:
        out.append('<div class="cb-group down"><i></i>Menurunkan risiko churn</div>')
        out.extend(row(label, value) for label, value in downs)
    out.append("</div>")
    return "".join(out)


def recommendation(rank: int, label: str, text: str) -> str:
    return '<div class="rec"><span class="rec-rank">%d</span><span><b>%s:</b> %s</span></div>' % (
        rank, label, text)


def rec_list(items) -> str:
    return '<div class="rec-list">%s</div>' % "".join(items)


def confusion_matrix(metrics, total: int | None = None) -> str:
    tn, fp, fn, tp = (int(metrics[k]) for k in ("TN", "FP", "FN", "TP"))
    total = total or (tn + fp + fn + tp)

    def cell(key, value, desc, cls):
        pct = value / total * 100 if total else 0
        return ('<div class="cm-cell %s"><span class="cm-key">%s</span>'
                '<span class="cm-val">%s</span>'
                '<span class="cm-pct">%s%% data uji</span>'
                '<span class="cm-desc">%s</span></div>'
                % (cls, key, count(value), fmt_num(pct, 1), desc))

    return (
        '<div class="cm"><span></span>'
        '<span class="cm-axis">Prediksi TETAP</span><span class="cm-axis">Prediksi CHURN</span>'
        '<span class="cm-axis row">Aktual TETAP</span>%s%s'
        '<span class="cm-axis row">Aktual CHURN</span>%s%s</div>'
    ) % (
        cell("TN", tn, "Tetap, diprediksi tetap", "ok"),
        cell("FP", fp, "Tetap, ditandai churn", "bad"),
        cell("FN", fn, "Churn yang terlewat", "bad"),
        cell("TP", tp, "Churn, terdeteksi", "ok"),
    )


def summary_strip(cells) -> str:
    out = ['<div class="summary-strip" style="--n:%d">' % len(cells)]
    for cell in cells:
        key, value = cell[0], cell[1]
        extra = cell[2] if len(cell) > 2 else ""
        caption = cell[3] if len(cell) > 3 else ""
        cap = '<span class="kpi-cap">%s</span>' % caption if caption else ""
        out.append('<div><span class="kpi-key">%s</span>'
                   '<span class="kpi-val %s">%s</span>%s</div>' % (key, extra, value, cap))
    out.append("</div>")
    return "".join(out)


def model_strip(cards) -> str:
    out = ['<div class="model-strip">']
    for name, selected, rows in cards:
        tag = '<span class="mc-tag">Terpilih</span>' if selected else ""
        grid = "".join("<div><span>%s</span><b>%s</b></div>" % (k, v) for k, v in rows)
        out.append('<div class="model-card%s"><div class="mc-head"><span class="mc-name">%s</span>%s</div>'
                   '<div class="mc-grid">%s</div></div>' % (" sel" if selected else "", name, tag, grid))
    out.append("</div>")
    return "".join(out)


def chart_head(title: str, sub: str = "") -> str:
    sub_html = '<div class="chart-sub">%s</div>' % sub if sub else ""
    return '<div class="chart-title">%s</div>%s' % (title, sub_html)


def note_card(text: str) -> str:
    return '<div class="fig-note">%s</div>' % text


def doc_links(items) -> str:
    return '<div class="doc-links">%s</div>' % "".join(
        '<a class="doc-link" href="%s" target="_blank" rel="noopener">%s<span>%s</span></a>'
        % (url, icon("doc", 18), label) for label, url in items)


def style_chart(chart, tok):
    return chart.configure(
        background="rgba(0,0,0,0)",
        font="Archivo",
        view={"stroke": None},
        axis={"labelColor": tok["muted"], "titleColor": tok["ink2"], "gridColor": tok["rule-soft"],
              "domainColor": tok["rule"], "tickColor": tok["rule"], "labelFont": "Archivo",
              "titleFont": "Archivo", "labelFontSize": 11, "titleFontSize": 11,
              "titleFontWeight": 600, "titlePadding": 8},
        legend={"labelColor": tok["ink2"], "titleColor": tok["ink2"], "labelFont": "Archivo",
                "titleFont": "Archivo", "labelFontSize": 11, "titleFontSize": 11,
                "orient": "bottom", "symbolType": "square", "title": None, "padding": 4},
        title={"color": tok["ink"], "font": "Archivo"},
    )


def count(value) -> str:
    return f"{int(value):,}".replace(",", ".")


def fmt_num(value: float, places: int = 2) -> str:
    return ("%.*f" % (places, float(value))).replace(".", ",")


def fmt_pct(value: float) -> str:
    return ("%.0f%%" % (float(value) * 100)).replace(".", ",")


def css_num(value: float) -> str:
    return ("%g" % float(value))
