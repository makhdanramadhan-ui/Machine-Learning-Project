"""Sistem visual aplikasi: token, ikon garis, dan komponen markup.

Dunia visual: lembar gambar teknik. Kertas, hairline, satu tinta biru teknis,
angka tabular, dan title block yang membawa identitas model. Tanpa gradien,
tanpa kaca, tanpa emoji.
"""
from __future__ import annotations

# --------------------------------------------------------------------------
# Token
# --------------------------------------------------------------------------
# Ramp nada: satu skala abu dari kertas ke tinta. Tingkat risiko dibaca dari
# posisi pada ramp, bukan dari warna lalu lintas; itu sebabnya satu-satunya
# warna di seluruh aplikasi adalah tinta biru aksen.
LIGHT = {
    "paper": "#F7F6F2",
    "sheet": "#FFFFFF",
    "ink": "#16181A",
    "ink2": "#3C3F45",
    "muted": "#6B6A64",
    "rule": "#C9C4B8",
    "rule-soft": "#E3E0D8",
    "accent": "#1F4FD8",
    "accent-ink": "#FFFFFF",
    "accent-soft": "#E4EAFB",
    "danger": "#B3272D",
    "ramp1": "#EDEBE4",
    "ramp2": "#D9D6CD",
    "ramp4": "#C2BEB3",
    "ramp6": "#9C988D",
    "ramp8": "#6E6A61",
    "ramp10": "#3A3833",
    "band-low-bg": "#EDEBE4",
    "band-low-fg": "#16181A",
    "band-mid-bg": "#C2BEB3",
    "band-mid-fg": "#16181A",
    "band-high-bg": "#16181A",
    "band-high-fg": "#FFFFFF",
}

DARK = {
    "paper": "#14161A",
    "sheet": "#1B1E23",
    "ink": "#E9E7E2",
    "ink2": "#C6C4BE",
    "muted": "#8E8C86",
    "rule": "#33373E",
    "rule-soft": "#262A30",
    "accent": "#7E9BFF",
    "accent-ink": "#14161A",
    "accent-soft": "#1E2740",
    "danger": "#E8746F",
    "ramp1": "#232830",
    "ramp2": "#2E333C",
    "ramp4": "#454B54",
    "ramp6": "#6E747D",
    "ramp8": "#9DA3AB",
    "ramp10": "#D2D0CA",
    "band-low-bg": "#232830",
    "band-low-fg": "#E9E7E2",
    "band-mid-bg": "#454B54",
    "band-mid-fg": "#E9E7E2",
    "band-high-bg": "#E9E7E2",
    "band-high-fg": "#14161A",
}

THEMES = {"Terang": LIGHT, "Gelap": DARK}

# --------------------------------------------------------------------------
# Ikon garis: satu keluarga, stroke 1.5, 24x24, tanpa isian
# --------------------------------------------------------------------------
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
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2'
           'M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M19.1 4.9l-1.4 1.4M6.3 17.7l-1.4 1.4"/>',
    "moon": '<path d="M20 14.5A8.5 8.5 0 1 1 9.5 4a6.8 6.8 0 0 0 10.5 10.5z"/>',
    "check": '<path d="M4 12.5l5 5L20 6.5"/>',
    "alert": '<path d="M12 3l9.5 17H2.5L12 3z"/><path d="M12 10v4M12 17.5v.01"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.01"/>',
    "chevron": '<path d="M6 9l6 6 6-6"/>',
    "play": '<path d="M7 4.5l12 7.5-12 7.5z"/>',
    "reset": '<path d="M3 12a9 9 0 1 0 3-6.7"/><path d="M3 4v5h5"/>',
    "doc": '<path d="M14 3H7a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1V7z"/>'
          '<path d="M14 3v4h4"/>',
    "grid": '<rect x="3" y="3" width="7.5" height="7.5"/><rect x="13.5" y="3" width="7.5" height="7.5"/>'
            '<rect x="3" y="13.5" width="7.5" height="7.5"/><rect x="13.5" y="13.5" width="7.5" height="7.5"/>',
    "layers": '<path d="M12 3l9 5-9 5-9-5 9-5z"/><path d="M3 13l9 5 9-5"/>',
    "flag": '<path d="M5 21V4M5 5h11l-2 4 2 4H5"/>',
}


def icon(name: str, size: int = 16, cls: str = "") -> str:
    """Kembalikan SVG ikon garis seukuran dan sefamily."""
    body = _PATHS[name]
    return (f'<svg class="ico {cls}" width="{size}" height="{size}" viewBox="0 0 24 24" '
            f'fill="none" stroke="currentColor" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>')


def icon_uri(name: str) -> str:
    """URL data untuk ikon, dipakai sebagai mask CSS pada tab."""
    body = _PATHS[name]
    raw = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
           f'stroke="black" stroke-width="1.5" stroke-linecap="round" '
           f'stroke-linejoin="round">{body}</svg>')
    from urllib.parse import quote

    return "url(\"data:image/svg+xml,%s\")" % quote(raw, safe="")


# --------------------------------------------------------------------------
# CSS
# --------------------------------------------------------------------------
_BASE_CSS = r"""
/* ---- huruf: di-host sendiri, bukan stylesheet pihak ketiga ---- */
@font-face {
    font-family: 'Archivo';
    src: url('/app/static/fonts/archivo-latin.woff2') format('woff2'),
         url('/static/fonts/archivo-latin.woff2') format('woff2');
    font-weight: 400 700; font-style: normal; font-display: swap;
}
@font-face {
    font-family: 'JetBrains Mono';
    src: url('/app/static/fonts/jetbrains-mono-latin.woff2') format('woff2'),
         url('/static/fonts/jetbrains-mono-latin.woff2') format('woff2');
    font-weight: 400 700; font-style: normal; font-display: swap;
}

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"], .stApp {
    font-family: 'Archivo', 'Segoe UI', system-ui, -apple-system, sans-serif;
    font-feature-settings: 'tnum' 1, 'cv05' 1;
}
html body, html body [data-testid="stAppViewContainer"], html body [data-testid="stApp"],
html body .stApp {
    font-family: 'Archivo', 'Segoe UI', system-ui, -apple-system, sans-serif !important;
}
html body code, html body pre, html body [data-testid="stCode"], html body .stCode,
html body .stMarkdown pre {
    font-family: 'JetBrains Mono', ui-monospace, monospace !important;
}
[data-testid="stAppViewContainer"] {
    background: var(--paper);
}
[data-testid="stHeader"] { background: var(--paper); }
[data-testid="stToolbar"] { opacity: .55; }
section[data-testid="stSidebar"] { display: none; }
[data-testid="stMainBlockContainer"] { padding: 3.5rem 2.6rem 3rem; max-width: 1440px; }
[data-testid="stMain"] { background: transparent; }
[data-testid="stVerticalBlock"] { gap: .55rem; }

/* ---- tipografi dasar ---- */
p, span, div, label, li, td, th { letter-spacing: -0.005em; }
.stMarkdown p { line-height: 1.6; }
html body .stMarkdown h1, html body .stMarkdown h2, html body .stMarkdown h3,
html body .stMarkdown h4, html body .stMarkdown h5, html body .stMarkdown h6 {
    color: var(--ink) !important; letter-spacing: -0.018em; }
html body .stMarkdown p, html body .stMarkdown li { color: var(--ink2); }
html body .stCaptionContainer, html body [data-testid="stCaptionContainer"] {
    color: var(--muted) !important; }
html body [data-testid="stWidgetLabel"] p, html body label p { color: var(--muted) !important; }

/* Streamlit memasang huruf tema sendiri pada isi markdown dan label widget.
   Tanpa aturan ini Archivo hanya dimuat tapi tidak dipakai, dan teks aplikasi
   jatuh ke huruf bawaan Streamlit. */
html body [data-testid="stMarkdownContainer"],
html body [data-testid="stCaptionContainer"],
html body [data-testid="stWidgetLabel"] p,
html body label p {
    font-family: 'Archivo', 'Segoe UI', system-ui, -apple-system, sans-serif !important; }
html body [data-testid="stMarkdownContainer"] p,
html body [data-testid="stMarkdownContainer"] span,
html body [data-testid="stMarkdownContainer"] div,
html body [data-testid="stMarkdownContainer"] li,
html body [data-testid="stMarkdownContainer"] h1,
html body [data-testid="stMarkdownContainer"] h2,
html body [data-testid="stMarkdownContainer"] h3,
html body [data-testid="stMarkdownContainer"] h4,
html body [data-testid="stMarkdownContainer"] h5,
html body [data-testid="stMarkdownContainer"] h6,
html body [data-testid="stCaptionContainer"] p {
    font-family: 'Archivo', 'Segoe UI', system-ui, -apple-system, sans-serif !important; }
/* Mono hanya untuk hal yang diukur, jadi specifisitasnya di atas aturan umum. */
html body [data-testid="stMarkdownContainer"] .tb-key,
html body [data-testid="stMarkdownContainer"] .tb-strip span,
html body [data-testid="stMarkdownContainer"] .cm-key,
html body [data-testid="stMarkdownContainer"] .risk-chip,
html body [data-testid="stMarkdownContainer"] .scale-seg span,
html body [data-testid="stMarkdownContainer"] .scale-marker-val,
html body [data-testid="stMarkdownContainer"] .scale-tick,
html body [data-testid="stMarkdownContainer"] .sheet-foot {
    font-family: 'JetBrains Mono', ui-monospace, monospace !important; }
code, pre, .stCode, [data-testid="stCode"] { font-family: 'JetBrains Mono', ui-monospace, monospace; }
.num { font-variant-numeric: tabular-nums; }

/* ---- kepala aplikasi ---- */
.app-head { display: flex; align-items: flex-start; justify-content: space-between;
            gap: 2rem; margin-bottom: 1.1rem; }
.app-title { font-size: 1.32rem; font-weight: 700; letter-spacing: -0.022em; color: var(--ink); }
.app-sub { margin-top: .32rem; font-size: .875rem; color: var(--muted) !important; max-width: 72ch;
           line-height: 1.55; }
.head-tools { display: flex; align-items: center; gap: .6rem; }

/* ---- title block ---- */
.title-block { border: 1px solid var(--rule); border-radius: 8px; overflow: hidden;
               background: var(--sheet); margin-bottom: 1.1rem; }
.tb-grid { display: grid; grid-template-columns: repeat(9, minmax(0, 1fr)); }
.tb-cell { padding: .6rem .75rem .62rem; border-right: 1px solid var(--rule-soft);
           border-bottom: 1px solid var(--rule-soft); min-width: 0; }
.tb-cell:last-child { border-right: none; }
.tb-key { display: block; font-family: 'JetBrains Mono', monospace; font-size: .625rem;
          font-weight: 500; letter-spacing: .11em; text-transform: uppercase;
          color: var(--muted); margin-bottom: .2rem; }
.tb-val { display: block; font-size: 1.02rem; font-weight: 600; color: var(--ink);
          font-variant-numeric: tabular-nums; letter-spacing: -0.015em;
          white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.tb-val.sm { font-size: .8rem; font-weight: 600; }
.tb-strip { display: flex; flex-wrap: wrap; gap: 0 1.5rem; padding: .5rem .75rem;
            border-top: 1px solid var(--rule-soft); background: var(--paper); }
.tb-strip span { font-family: 'JetBrains Mono', monospace; font-size: .625rem;
                 letter-spacing: .1em; text-transform: uppercase; color: var(--muted); }
.tb-strip b { color: var(--ink); font-weight: 600; margin-left: .34rem;
              font-variant-numeric: tabular-nums; }

/* ---- rail tab ---- */
div[role="tablist"] { gap: .35rem; border-bottom: 1px solid var(--rule);
                      margin-bottom: 1.1rem; }
div[data-testid="stTab"] { font-family: 'Archivo', sans-serif !important;
    font-size: .82rem !important; font-weight: 600 !important; letter-spacing: -0.01em;
    color: var(--muted) !important; background: transparent !important;
    padding: .5rem 0 .55rem !important; margin-right: 1.35rem !important;
    transition: color .12s ease; }
div[data-testid="stTab"] p { font-size: inherit !important; font-weight: inherit !important;
    color: inherit !important; letter-spacing: inherit !important; }
div[data-testid="stTab"] p::before { content: ""; display: inline-block;
    width: 15px; height: 15px; margin-right: .45rem; vertical-align: -2px;
    background: currentColor; -webkit-mask: var(--tabicon) center/contain no-repeat;
    mask: var(--tabicon) center/contain no-repeat; }
div[data-testid="stTab"][aria-selected="true"] { color: var(--ink) !important; }
div[data-testid="stTab"] .react-aria-SelectionIndicator { background: var(--ink) !important;
    height: 2px !important; }
div[data-testid="stTab"]:hover { color: var(--ink2) !important; }
div[data-testid="stTab"]:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }

/* ---- judul bagian ---- */
.sec-title { display: flex; align-items: center; gap: .5rem; font-size: 1rem;
             font-weight: 650; letter-spacing: -0.018em; color: var(--ink);
             margin: 0 0 .1rem; }
.sec-title .ico { color: var(--accent); flex: none; }
.sec-note { font-size: .82rem; color: var(--muted) !important; margin: .15rem 0 .5rem;
            max-width: 78ch; line-height: 1.55; }

/* ---- panel ---- */
div[data-testid="stVerticalBlockBorderWrapper"] { border: 1px solid var(--rule) !important;
    border-radius: 8px !important; background: var(--sheet) !important;
    box-shadow: none !important; padding: 1.1rem 1.25rem 1.15rem !important; }
div[data-testid="stExpander"] { border: 1px solid var(--rule) !important;
    border-radius: 8px !important; background: var(--sheet) !important;
    box-shadow: none !important; }
div[data-testid="stExpander"] summary { font-size: .84rem !important;
    font-weight: 600 !important; color: var(--ink2) !important; }

/* ---- kontrol ---- */
label p, [data-testid="stWidgetLabel"] p { font-size: .74rem !important;
    font-weight: 500 !important; color: var(--muted) !important;
    letter-spacing: .005em; margin-bottom: .18rem !important; }
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stTextInput"] input,
div[data-testid="stFileUploader"] {
    background: var(--sheet) !important; color: var(--ink) !important;
    border: 1px solid var(--rule) !important; border-radius: 6px !important;
    font-size: .85rem !important; box-shadow: none !important; }
html body [data-testid="stSelectbox"] [data-baseweb="select"] div,
html body [data-testid="stSelectbox"] input,
html body [data-testid="stNumberInput"] input,
html body [data-testid="stTextInput"] input {
    font-family: 'Archivo', 'Segoe UI', system-ui, -apple-system, sans-serif !important; }
div[data-testid="stNumberInputContainer"] {
    background: var(--sheet) !important; border: 1px solid var(--rule) !important;
    border-radius: 6px !important; box-shadow: none !important; }
div[data-testid="stNumberInput"] input {
    background: transparent !important; color: var(--ink) !important;
    border: none !important; border-radius: 6px 0 0 6px !important;
    box-shadow: none !important; font-size: .85rem !important; }
div[data-testid="stNumberInputStepUp"], div[data-testid="stNumberInputStepDown"] {
    background: transparent !important; color: var(--muted) !important; }
div[data-testid="stNumberInputStepUp"] svg, div[data-testid="stNumberInputStepDown"] svg {
    fill: var(--muted) !important; }
div[data-testid="stNumberInputStepUp"]:hover, div[data-testid="stNumberInputStepDown"]:hover {
    color: var(--ink) !important; }
div[data-testid="stSelectbox"] div[data-baseweb="select"] div,
div[data-testid="stSelectbox"] div[data-baseweb="select"] span,
div[data-testid="stSelectbox"] [data-testid="stMarkdownContainer"] p,
div[data-testid="stSelectbox"] [role="combobox"] {
    color: var(--ink) !important; }
div[data-testid="stSelectbox"] > div > div > div:last-child,
div[data-testid="stSelectbox"] [data-baseweb="select"] > div:last-child { color: var(--ink) !important; }
div[data-testid="stSelectbox"] > div > div:focus-within,
div[data-testid="stNumberInputContainer"]:focus-within,
div[data-testid="stTextInput"] input:focus {
    border-color: var(--accent) !important; outline: none !important;
    box-shadow: 0 0 0 2px var(--accent-soft) !important; }
div[data-testid="stSelectbox"] svg { fill: var(--muted); }
div[data-baseweb="popover"] > div { background: var(--sheet) !important; }
div[data-baseweb="menu"] { background: var(--sheet) !important;
    border: 1px solid var(--rule) !important; }
div[role="option"] { font-size: .85rem !important; color: var(--ink) !important; }
div[data-testid="stNumberInputStepUp"], div[data-testid="stNumberInputStepDown"] {
    background: var(--sheet) !important; color: var(--muted) !important;
    border-color: var(--rule) !important; }
div[data-testid="stNumberInputStepUp"]:hover, div[data-testid="stNumberInputStepDown"]:hover {
    background: var(--accent-soft) !important; color: var(--ink) !important; }

/* ---- tombol ---- */
.stButton > button, .stDownloadButton > button {
    border-radius: 6px !important; font-family: 'Archivo', sans-serif !important;
    font-size: .84rem !important; font-weight: 600 !important;
    letter-spacing: -0.005em; box-shadow: none !important;
    border: 1px solid var(--rule) !important; background: var(--sheet) !important;
    color: var(--ink) !important; transition: background .12s ease, border-color .12s ease; }
.stButton > button:hover, .stDownloadButton > button:hover {
    border-color: var(--ink2) !important; background: var(--paper) !important; }
.stButton > button[kind="primary"], .stDownloadButton > button[kind="primary"] {
    background: var(--ink) !important; color: var(--paper) !important;
    border-color: var(--ink) !important; }
.stButton > button[kind="primary"]:hover { background: var(--ink2) !important;
    border-color: var(--ink2) !important; color: var(--paper) !important; }
.stButton > button:focus-visible, .stDownloadButton > button:focus-visible {
    outline: 2px solid var(--accent) !important; outline-offset: 2px !important; }
.stButton > button:disabled { opacity: .45 !important; }
.btn { display: inline-flex; align-items: center; gap: .45rem; }

/* ---- pengalih tema ---- */
div[data-testid="stButtonGroup"] { background: var(--sheet) !important;
    border: 1px solid var(--rule) !important; border-radius: 6px !important;
    padding: 2px !important; gap: 0 !important; width: 100% !important; }
div[data-testid="stButtonGroup"] button { font-family: 'Archivo', sans-serif !important;
    font-size: .72rem !important; font-weight: 600 !important; border-radius: 4px !important;
    color: var(--muted) !important; letter-spacing: -0.005em;
    background: transparent !important; border: 1px solid transparent !important;
    box-shadow: none !important; }
div[data-testid="stButtonGroup"] button:hover { color: var(--ink) !important;
    background: var(--paper) !important; }
div[data-testid="stButtonGroup"] button[aria-checked="true"],
div[data-testid="stButtonGroup"] button[data-checked="true"],
div[data-testid="stButtonGroup"] button[aria-pressed="true"] {
    background: var(--accent-soft) !important; color: var(--ink) !important;
    border-color: var(--accent) !important; }

/* ---- blok vonis ---- */
.verdict { border: 1px solid var(--rule); border-radius: 8px; background: var(--sheet);
           padding: 1rem 1.15rem 1.05rem; margin: .2rem 0 .9rem; }
.verdict-head { display: flex; align-items: center; gap: .7rem; flex-wrap: wrap;
                margin-bottom: .45rem; }
.risk-chip { font-family: 'JetBrains Mono', monospace; font-size: .66rem; font-weight: 600;
             letter-spacing: .1em; text-transform: uppercase; padding: .28rem .5rem;
             border-radius: 4px; }
.risk-low { background: var(--band-low-bg); color: var(--band-low-fg); }
.risk-mid { background: var(--band-mid-bg); color: var(--band-mid-fg); }
.risk-high { background: var(--band-high-bg); color: var(--band-high-fg); }
.verdict-decision { font-size: .84rem; color: var(--ink2) !important; }
.verdict-decision b { color: var(--ink); }
.verdict-figure { font-size: 2.5rem; font-weight: 700; letter-spacing: -0.032em;
                  color: var(--ink); font-variant-numeric: tabular-nums; line-height: 1.05; }
.verdict-figure .unit { font-size: 1.15rem; font-weight: 600; color: var(--muted);
                         margin-left: .08em; letter-spacing: -0.01em; }
.verdict-sub { font-size: .8rem; color: var(--muted) !important; margin-top: .18rem; }

/* ---- skala probabilitas terkalibrasi ---- */
.scale { border: 1px solid var(--rule); border-radius: 8px; background: var(--sheet);
         padding: .85rem 1rem .7rem; margin-bottom: .85rem; }
.scale-head { display: flex; justify-content: space-between; align-items: baseline;
              margin-bottom: 1.7rem; gap: 1rem; }
.scale-title { font-size: .78rem; font-weight: 600; color: var(--ink) !important; }
.scale-note { font-size: .72rem; color: var(--muted) !important; }
.scale-track { position: relative; height: 26px; border: 1px solid var(--rule);
               border-radius: 4px; overflow: visible; display: flex; }
.scale-seg { height: 100%; display: flex; align-items: center; justify-content: flex-start;
            padding-left: .55rem; }
.scale-seg span { font-family: 'JetBrains Mono', monospace; font-size: .58rem;
                  letter-spacing: .11em; text-transform: uppercase; }
.seg-low { background: var(--band-low-bg); color: var(--band-low-fg); flex: none; }
.seg-mid { background: var(--band-mid-bg); color: var(--band-mid-fg); flex: none; }
.seg-high { background: var(--band-high-bg); color: var(--band-high-fg); flex: 1; }
.scale-marker { position: absolute; top: -6px; bottom: -6px; width: 2px;
                background: var(--ink); transform: translateX(-1px); }
.scale-marker::after { content: ""; position: absolute; top: -4px; left: -3px;
    width: 8px; height: 8px; background: var(--ink); border-radius: 50%; }
.scale-marker-val { position: absolute; top: -1.5rem; left: 50%; transform: translateX(-50%);
    font-family: 'JetBrains Mono', monospace; font-size: .68rem; font-weight: 600;
    color: var(--ink); white-space: nowrap; background: var(--sheet);
    border: 1px solid var(--rule); border-radius: 3px; padding: .1rem .32rem; }
.scale-ticks { position: relative; height: 1rem; margin-top: .3rem; }
.scale-tick { position: absolute; transform: translateX(-50%); font-family: 'JetBrains Mono',
              monospace; font-size: .58rem; letter-spacing: .08em; color: var(--muted);
              white-space: nowrap; }
.scale-tick.hard { color: var(--ink2); font-weight: 600; }
.scale-tick:first-child { transform: translateX(-8%); }
.scale-tick:last-child { transform: translateX(-92%); }

/* ---- matriks konfusi ---- */
.cm { display: grid; grid-template-columns: 1fr 1fr; border: 1px solid var(--rule);
      border-radius: 8px; overflow: hidden; background: var(--sheet); margin: .3rem 0 .6rem; }
.cm-cell { padding: .6rem .85rem .7rem; border-right: 1px solid var(--rule-soft);
           border-bottom: 1px solid var(--rule-soft); }
.cm-cell:nth-child(2n) { border-right: none; }
.cm-cell:nth-child(n+3) { border-bottom: none; }
.cm-key { display: block; font-family: 'JetBrains Mono', monospace; font-size: .6rem;
          letter-spacing: .12em; text-transform: uppercase; color: var(--muted);
          margin-bottom: .22rem; }
.cm-val { display: block; font-size: 1.55rem; font-weight: 650; letter-spacing: -0.025em;
          color: var(--ink); font-variant-numeric: tabular-nums; line-height: 1.15; }
.cm-desc { display: block; font-size: .76rem; color: var(--muted) !important; margin-top: .12rem; }
.cm-cell.hit { background: var(--ramp1); }

/* ---- daftar saran ---- */
.rec { display: flex; gap: .6rem; padding: .62rem .1rem; border-bottom: 1px solid var(--rule-soft);
       font-size: .85rem; color: var(--ink2) !important; line-height: 1.5; }
.rec:last-child { border-bottom: none; }
.rec .ico { color: var(--accent); flex: none; margin-top: .12rem; }
.rec b { color: var(--ink); font-weight: 600; }

/* ---- strip ringkasan ---- */
.summary-strip { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr));
                  border: 1px solid var(--rule); border-radius: 8px; overflow: hidden;
                  background: var(--sheet); margin: .3rem 0 .8rem; }
.summary-strip > div { padding: .62rem .8rem; border-right: 1px solid var(--rule-soft); }
.summary-strip > div:last-child { border-right: none; }

/* ---- plate gambar EDA ---- */
[data-testid="stImage"] img { border: 1px solid var(--rule); border-radius: 8px;
    background: #FFFFFF; display: block; }
[data-testid="stImage"] { margin: .5rem 0 .2rem; }
.plate-cap { font-size: .78rem; color: var(--muted) !important; padding: .5rem .05rem .55rem;
             line-height: 1.5; }

/* ---- tabel ---- */
[data-testid="stDataFrame"] { border: 1px solid var(--rule); border-radius: 8px;
                              overflow: hidden; }
[data-testid="stDataFrameResizable"] { border: none !important; }

/* ---- pesan ---- */
[data-testid="stAlert"] { border-radius: 6px !important; border: 1px solid var(--rule) !important;
                          background: var(--sheet) !important; font-size: .85rem !important; }
[data-testid="stAlertContainer"] { background: var(--sheet) !important; color: var(--ink2) !important; }
div[data-testid="stAlert"][data-baseweb="callout"][kind="error"],
div[data-testid="stAlert"][data-baseweb="callout"][kind="success"] {
    border-color: var(--danger) !important; }
div[data-testid="stAlert"][data-baseweb="callout"][kind="warning"] { border-left: 3px solid var(--ramp8) !important; }

/* ---- footer ---- */
.sheet-foot { margin-top: 2.2rem; padding-top: .85rem; border-top: 1px solid var(--rule);
              font-family: 'JetBrains Mono', monospace; font-size: .625rem;
              letter-spacing: .06em; color: var(--muted) !important; }

/* ---- layar kecil ---- */
@media (max-width: 900px) {
    [data-testid="stMainBlockContainer"] { padding: 1rem .9rem 2rem; }
    .app-head { flex-direction: column; gap: .8rem; }
    .tb-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .tb-cell { border-bottom: 1px solid var(--rule-soft) !important; }
    .summary-strip { grid-template-columns: 1fr; }
    .summary-strip > div { border-right: none; border-bottom: 1px solid var(--rule-soft); }
    .verdict-figure { font-size: 2.1rem; }
    button[data-baseweb="tab"] { margin-right: .9rem !important; font-size: .78rem !important; }
}
@media (max-width: 640px) {
    .tb-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .scale-seg span { display: none; }
    .cm { grid-template-columns: 1fr; }
    .cm-cell { border-right: none; }
    .cm-cell:nth-child(3) { border-bottom: 1px solid var(--rule-soft); }
}

/* ---- fokus & aksesibilitas ---- */
::selection { background: var(--accent); color: var(--accent-ink); }
a { color: var(--accent) !important; text-underline-offset: 3px; }
a:hover { text-decoration-thickness: 2px; }
*:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
"""


TAB_ICONS = ("user", "upload", "chart", "search")


def _tab_icon_css() -> str:
    """Ikon untuk rail tab, dipasang lewat mask agar tetap satu keluarga garis."""
    return "\n".join(
        'div[role="tablist"] > div:nth-child(%d) { --tabicon: %s; }' % (i, icon_uri(name))
        for i, name in enumerate(TAB_ICONS, start=1)
    )


def build_css(theme: str) -> str:
    """CSS lengkap untuk tema yang dipilih.

    Baris kosong dibuang: markdown Streamlit mengakhiri blok HTML di baris
    kosong, dan stylesheet yang terpotong di tengah membuat halaman kehilangan
    separuh gayanya.
    """
    tokens = THEMES[theme]
    root = "\n".join("  --%s: %s;" % (k, v) for k, v in tokens.items())
    # Variabel tema Streamlit ikut ditulis. Declarasi harus ada di `body`, bukan
    # hanya di `:root`: Streamlit menulis variabel itu pada `body`, dan
    # deklarasi milik elemen yang lebih dekat menang atas nilai warisan.
    streamlit_vars = (
        "--background-color: %(paper)s;"
        "--text-color: %(ink)s;"
        "--text-color-light: %(ink2)s;"
        "--primary-color: %(accent)s;"
        "--secondary-background-color: %(sheet)s;"
        "--border-color: %(rule)s;"
        "--font-family-body: 'Archivo', 'Segoe UI', system-ui, sans-serif;"
        "--font-family: 'Archivo', 'Segoe UI', system-ui, sans-serif;"
        "--font-family-code: 'JetBrains Mono', ui-monospace, monospace;"
    ) % {
        "paper": tokens["paper"], "ink": tokens["ink"], "ink2": tokens["ink2"],
        "accent": tokens["accent"], "sheet": tokens["sheet"], "rule": tokens["rule"],
    }
    body = "\n".join(line for line in _BASE_CSS.splitlines() if line.strip())
    tabs = "\n".join(line for line in _tab_icon_css().splitlines() if line.strip())
    return (
        "<style>\n:root {\n%s\n}\n"
        "html body, html body [data-testid=\"stAppViewContainer\"] {\n%s\n}\n"
        "%s\n%s\n</style>"
    ) % (root, streamlit_vars, body, tabs)


# --------------------------------------------------------------------------
# Komponen markup
# --------------------------------------------------------------------------
def title_block(cells, strip=()) -> str:
    """Title block: deretan sel berhairline yang membawa identitas model.

    cells  : iterable (kunci, nilai) atau (kunci, nilai, kelas-tambahan)
    strip  : iterable (kunci, nilai) untuk baris mikro di bawah blok
    """
    parts = ['<div class="title-block"><div class="tb-grid">']
    for cell in cells:
        key, value = cell[0], cell[1]
        extra = cell[2] if len(cell) > 2 else ""
        parts.append(
            '<div class="tb-cell"><span class="tb-key">%s</span>'
            '<span class="tb-val %s">%s</span></div>' % (key, extra, value))
    parts.append("</div>")
    if strip:
        parts.append('<div class="tb-strip">')
        for key, value in strip:
            parts.append("<span>%s<b>%s</b></span>" % (key, value))
        parts.append("</div>")
    parts.append("</div>")
    return "".join(parts)


def section(title: str, icon_name: str, note: str = "") -> str:
    """Judul bagian dengan ikon garis dan catatan satu baris."""
    head = '<h3 class="sec-title">%s %s</h3>' % (icon(icon_name), title)
    if note:
        return head + '<p class="sec-note">%s</p>' % note
    return head


def risk_chip(level: str) -> str:
    """Chip kategori risiko. Warna berasal dari ramp nada, bukan palet lalu lintas."""
    slug = {"RENDAH": "low", "SEDANG": "mid", "TINGGI": "high"}.get(level, "low")
    return '<span class="risk-chip risk-%s">%s</span>' % (slug, level)


def calibrated_scale(prob: float, threshold: float, high: float) -> str:
    """Skala probabilitas terkalibrasi dengan penanda ambang keputusan.

    Posisi pada ramp adalah besaran; warna hanya langkah dari ramp nada yang
    sama. Angka posisi ditulis dengan titik desimal karena nilainya masuk ke
    inline CSS, bukan ke teks.
    """
    lo_pct = threshold * 100
    hi_pct = high * 100
    mid_pct = hi_pct - lo_pct
    value = max(0.0, min(100.0, prob * 100))
    return (
        '<div class="scale">'
        '<div class="scale-head"><span class="scale-title">Skala risiko terkalibrasi</span>'
        '<span class="scale-note">Ambang keputusan %s · batas kategori tinggi %s</span></div>'
        '<div class="scale-track">'
        '<div class="scale-seg seg-low" style="width:%s%%"><span>Rendah</span></div>'
        '<div class="scale-seg seg-mid" style="width:%s%%"><span>Sedang</span></div>'
        '<div class="scale-seg seg-high"><span>Tinggi</span></div>'
        '<div class="scale-marker" style="left:%s%%">'
        '<span class="scale-marker-val">%s</span></div>'
        '</div>'
        '<div class="scale-ticks">'
        '<span class="scale-tick" style="left:0%%">0%%</span>'
        '<span class="scale-tick hard" style="left:%s%%">%s ambang</span>'
        '<span class="scale-tick" style="left:%s%%">%s</span>'
        '<span class="scale-tick" style="left:100%%">100%%</span>'
        '</div></div>'
    ) % (fmt_pct(threshold), fmt_pct(high),
         css_num(lo_pct), css_num(mid_pct), css_num(value),
         fmt_num(value) + "%",
         css_num(lo_pct), fmt_pct(threshold), css_num(hi_pct), fmt_pct(high))


def confusion_matrix(metrics) -> str:
    """Matriks konfusi sebagai hairline cell, tanpa isian warna lalu lintas."""
    cells = [
        ("TP", metrics["TP"], "Diprediksi churn dan memang churn", "hit"),
        ("TN", metrics["TN"], "Diprediksi tidak churn dan memang tidak churn", "hit"),
        ("FP", metrics["FP"], "Diprediksi churn, ternyata tidak churn", ""),
        ("FN", metrics["FN"], "Churn terlewat", ""),
    ]
    out = ['<div class="cm">']
    for key, value, desc, cls in cells:
        out.append('<div class="cm-cell %s"><span class="cm-key">%s</span>'
                   '<span class="cm-val">%s</span>'
                   '<span class="cm-desc">%s</span></div>' % (cls, key, f"{int(value):,}".replace(",", "."), desc))
    out.append("</div>")
    return "".join(out)


def summary_strip(cells) -> str:
    """Strip ringkasan: label mono di atas, angka tabular di bawah."""
    out = ['<div class="summary-strip">']
    for key, value in cells:
        out.append('<div><span class="tb-key">%s</span>'
                   '<span class="tb-val">%s</span></div>' % (key, value))
    out.append("</div>")
    return "".join(out)


def plate(src: str, caption: str = "") -> str:
    """Gambar yang direkat ke lembar: bingkai hairline dan keterangan."""
    cap = '<div class="plate-cap">%s</div>' % caption if caption else ""
    return '<div class="plate"><img src="%s" alt="Grafik EDA" />%s</div>' % (src, cap)


def recommendation(icon_name: str, label: str, text: str) -> str:
    """Satu saran retensi dengan ikon garis."""
    return '<div class="rec">%s<span><b>%s</b> — %s</span></div>' % (
        icon(icon_name, 15), label, text)


def fmt_num(value: float, places: int = 2) -> str:
    """Angka dengan koma desimal."""
    return ("%.*f" % (places, float(value))).replace(".", ",")


def fmt_pct(value: float) -> str:
    """Persen tanpa desimal, gaya Indonesia."""
    return ("%.0f%%" % (float(value) * 100)).replace(".", ",")


def css_num(value: float) -> str:
    """Angka untuk inline CSS: titik desimal, tanpa nol di belakang koma."""
    return ("%g" % float(value))
