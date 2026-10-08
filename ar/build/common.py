"""Shared steps for building the Arabic pages in ar/ from the English pages.

Each build-<page>.py reads the English page, calls these helpers, swaps
the text with rep()/replace_block() (each must match exactly once, so a
changed English line stops the build) and writes ar/<page>.html.
"""
import pathlib
import re
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parents[2]

I18N_TAG = "../ecd-i18n.js?v=20261008e"

VENUE = "مركز إبداع مصر الرقمية (كريتيفا)، الجيزة"
WA_TEXT = "مرحباً، محتاج مساعدة بخصوص يوم التجارة الإلكترونية 2026"
WA_AR = "https://wa.me/201505437979?text=" + urllib.parse.quote(WA_TEXT)
WA_EN = "https://wa.me/201505437979?text=I%20need%20help%20for%20Ecommerce%20Day%202026"
WA_ARIA_EN = 'aria-label="Chat with us on WhatsApp (opens in a new tab)"'
WA_ARIA_AR = 'aria-label="تواصل معنا على واتساب (يفتح في نافذة جديدة)"'

SHARED_SCRIPTS = [
    "navbar.js", "breadcrumbs.js", "ecd-whatsapp.js", "footer.js", "prices.js",
    "ecd-api.js", "ecd-content.js", "tickets-section.js",
]

ARABIC_FONT = '"IBM Plex Sans Arabic", "Manrope", system-ui, -apple-system, sans-serif'


class Page:
    def __init__(self, name):
        self.name = name
        self.s = (ROOT / name).read_text(encoding="utf-8")

    def rep(self, old, new, count=1):
        found = self.s.count(old)
        if found != count:
            raise SystemExit(f"[{self.name}] expected {count} match(es), found {found}: {old[:100]!r}")
        self.s = self.s.replace(old, new)

    def replace_block(self, start, end, new):
        i = self.s.index(start)
        j = self.s.index(end, i) + len(end)
        self.s = self.s[:i] + new + self.s[j:]

    def head(self, title_en, title_ar, desc_en=None, desc_ar=None):
        """lang/dir, Arabic title + noindex, Arabic font, ../ paths, ecd-i18n.js."""
        self.rep('<html lang="en">', '<html lang="ar" dir="rtl">')
        self.rep(
            f"<title>{title_en}</title>",
            f"<title>{title_ar}</title>\n"
            "    <!-- Arabic preview: hidden from search engines until the team signs off -->\n"
            '    <meta name="robots" content="noindex, nofollow" />',
        )
        if desc_en:
            self.rep(f'content="{desc_en}"', f'content="{desc_ar}"')
        # Arabic face first in every Google Fonts request
        self.s = re.sub(
            r"https://fonts\.googleapis\.com/css2\?family=",
            "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=",
            self.s,
        )
        self.rep('<script src="ecd-analytics.js', '<script src="../ecd-analytics.js')
        tag = re.search(r'<script src="\.\./ecd-analytics\.js\?v=[0-9a-z]+"></script>', self.s).group(0)
        self.rep(
            tag,
            tag + "\n    <!-- Arabic mode for the shared components (must load before them) -->\n"
            f'    <script src="{I18N_TAG}"></script>',
        )
        for name in SHARED_SCRIPTS:
            self.s = self.s.replace(f'<script src="{name}', f'<script src="../{name}')
        self.s = self.s.replace('"assets/', '"../assets/')
        self.s = re.sub(r"(\d+w), assets/", r"\1, ../assets/", self.s)

    def breadcrumb_schema(self, items):
        """Swap the BreadcrumbList JSON-LD names/URLs for the Arabic ones.
        items: list of (english_name, arabic_name, arabic_url_or_None)."""
        for en, ar, url in items:
            self.rep(f'"name": "{en}"', f'"name": "{ar}"')
        self.s = self.s.replace(
            '"item": "https://www.trafficmena.com/ecommerce-day/"',
            '"item": "https://www.trafficmena.com/ecommerce-day/ar/"',
        )
        self.s = re.sub(
            r'"item": "https://www\.trafficmena\.com/ecommerce-day/([a-z-]+\.html)"',
            r'"item": "https://www.trafficmena.com/ecommerce-day/ar/\1"',
            self.s,
        )

    def whatsapp_links(self):
        """Arabic message and label on every inline WhatsApp link."""
        self.s = self.s.replace(WA_EN, WA_AR)
        self.s = self.s.replace(WA_ARIA_EN, WA_ARIA_AR)
        self.s = self.s.replace("<span>WhatsApp</span>", "<span>واتساب</span>")

    def add_css(self, css):
        i = self.s.rindex("    </style>\n  </head>")
        self.s = self.s[:i] + css.rstrip() + "\n" + self.s[i:]

    def write(self):
        out = ROOT / "ar" / self.name
        out.write_text(self.s, encoding="utf-8")
        print("wrote", out, len(self.s), "bytes")
