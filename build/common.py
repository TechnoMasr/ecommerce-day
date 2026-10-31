"""Shared steps for building the Arabic pages from the English pages.

Arabic is the main site (user decision, 12 Oct 2026): the English pages
live in en/ and are the source; each build-<page>.py reads en/<page>,
calls these helpers, swaps the text with rep()/replace_block() (each must
match exactly once, so a changed English line stops the build) and writes
the Arabic page to the site root as <page>.  Run from anywhere:
    python3 build/build-home.py   (and the other build-*.py)
"""
import pathlib
import re
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parents[1]

I18N_TAG = "ecd-i18n.js?v=20261031a"
SITE_TAG = '<script src="ecd-site.js?v=20261029a"></script>'
BASE_URL = "https://www.trafficmena.com/ecommerce-day/"

VENUE = "مركز إبداع مصر الرقمية (كريتيفا)، الجيزة"
WA_TEXT = "مرحباً، محتاج مساعدة بخصوص يوم التجارة الإلكترونية 2026"
WA_AR = "https://wa.me/201505437979?text=" + urllib.parse.quote(WA_TEXT)
WA_EN = "https://wa.me/201505437979?text=I%20need%20help%20for%20Ecommerce%20Day%202026"
WA_ARIA_EN = 'aria-label="Chat with us on WhatsApp (opens in a new tab)"'
WA_ARIA_AR = 'aria-label="تواصل معنا على واتساب (يفتح في نافذة جديدة)"'


ARABIC_FONT = '"IBM Plex Sans Arabic", "Manrope", system-ui, -apple-system, sans-serif'


def keep_names_together(s):
    """English pass names in brackets must not break across lines in RTL text."""
    for name in ["(All Access Pass)", "(Standard Pass)"]:
        s = s.replace(name, name.replace(" ", "\u00a0"))
    # "المسرح 1" / "المسرح 2" (Stage 1 / Stage 2) stay on one line too
    s = re.sub(r"المسرح ([12])(?![0-9])", "المسرح\u00a0\\1", s)
    # "القاعة 1/2/3" (Room 1/2/3, 29 Oct 2026) too
    s = re.sub(r"القاعة ([123])(?![0-9])", "القاعة\u00a0\\1", s)
    return s


def finish_arabic(s):
    """From an English page in en/ to the Arabic page at the site root:
    shared files one level up become root paths, the canonical URL is the
    Arabic one, pages without an Arabic copy open in English (en/), and
    ecd-i18n.js loads right after ecd-site.js."""
    # Every "../" in the English pages points from en/ to a root file.
    s = s.replace("../", "")
    s = s.replace(f'<link rel="canonical" href="{BASE_URL}en/', f'<link rel="canonical" href="{BASE_URL}')
    s = re.sub(r"""(["'])(become-a-sponsor|faq|policy)\.html""", r"\1en/\2.html", s)
    if s.count(SITE_TAG) != 1:
        raise SystemExit("ecd-site.js tag not found once")
    s = s.replace(
        SITE_TAG,
        SITE_TAG + "\n    <!-- Arabic strings for the shared components (must load before them) -->\n"
        f'    <script src="{I18N_TAG}"></script>',
    )
    return keep_names_together(s)


class Page:
    def __init__(self, name):
        self.name = name
        self.s = (ROOT / "en" / name).read_text(encoding="utf-8")

    def rep(self, old, new, count=1):
        found = self.s.count(old)
        if found != count:
            raise SystemExit(f"[{self.name}] expected {count} match(es), found {found}: {old[:100]!r}")
        self.s = self.s.replace(old, new)

    def text(self, en, ar, count=1):
        """Replace a text node by its content (whitespace-insensitive), keeping
        the surrounding tags and indentation. Matches must equal `count`."""
        import html as _html
        norm = lambda t: re.sub(r"\s+", " ", _html.unescape(t)).strip()
        target = norm(en)
        hits = 0

        def sub(m):
            nonlocal hits
            if norm(m.group(1)) == target:
                hits += 1
                inner = m.group(1)
                lead = inner[: len(inner) - len(inner.lstrip())]
                trail = inner[len(inner.rstrip()):]
                return ">" + lead + ar + trail + "<"
            return m.group(0)

        self.s = re.sub(r">([^<>]*)<", sub, self.s)
        if hits != count:
            raise SystemExit(f"[{self.name}] text {en[:80]!r}: expected {count}, found {hits}")

    def replace_block(self, start, end, new):
        i = self.s.index(start)
        j = self.s.index(end, i) + len(end)
        self.s = self.s[:i] + new + self.s[j:]

    def head(self, title_en, title_ar, desc_en=None, desc_ar=None):
        """lang/dir, Arabic title and description, Arabic font."""
        self.rep('<html lang="en">', '<html lang="ar" dir="rtl">')
        self.rep(f"<title>{title_en}</title>", f"<title>{title_ar}</title>")
        if desc_en:
            self.rep(f'content="{desc_en}"', f'content="{desc_ar}"')
        # Arabic face first in every Google Fonts request
        self.s = re.sub(
            r"https://fonts\.googleapis\.com/css2\?family=",
            "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=",
            self.s,
        )

    def breadcrumb_schema(self, items):
        """Swap the BreadcrumbList JSON-LD names/URLs for the Arabic ones.
        items: list of (english_name, arabic_name, arabic_url_or_None)."""
        for en, ar, url in items:
            self.rep(f'"name": "{en}"', f'"name": "{ar}"')
        # Arabic trail URLs are the root pages (the English ones are in en/)
        self.s = self.s.replace(f'"item": "{BASE_URL}en/', f'"item": "{BASE_URL}')

    def whatsapp_links(self):
        """Arabic message and label on every inline WhatsApp link."""
        self.s = self.s.replace(WA_EN, WA_AR)
        self.s = self.s.replace(WA_ARIA_EN, WA_ARIA_AR)
        self.s = self.s.replace("<span>WhatsApp</span>", "<span>واتساب</span>")

    def add_css(self, css):
        i = self.s.rindex("    </style>\n  </head>")
        self.s = self.s[:i] + css.rstrip() + "\n" + self.s[i:]

    def write(self):
        # Arabic reads "7 إلى 10 أيام"; a "7-10" range also breaks badly at line ends in RTL
        self.s = self.s.replace("بـ 7-10 أيام", "بـ 7 إلى 10 أيام").replace("بـ\n                7-10 أيام", "بـ\n                7 إلى 10 أيام")
        self.s = self.s.replace("، 7-10 أيام", "، 7 إلى 10 أيام")
        self.s = finish_arabic(self.s)
        out = ROOT / self.name
        out.write_text(self.s, encoding="utf-8")
        print("wrote", out, len(self.s), "bytes")
