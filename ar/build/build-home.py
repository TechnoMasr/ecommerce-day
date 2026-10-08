#!/usr/bin/env python3
"""Build ar/index.html (Arabic Home) from index.html.

The Arabic page keeps the English page's layout, CSS and scripts; this
script swaps the text, sets lang/dir, fixes paths for the ar/ folder and
adds the right-to-left overrides. Re-run it after changing index.html so
the two pages stay in step:  python3 ar/build/build-home.py
Every replacement must match exactly once, so a changed English line
stops the build instead of being skipped silently.
"""
import pathlib
import re
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parents[2]
src = (ROOT / "index.html").read_text(encoding="utf-8")
s = src


def rep(old, new, count=1):
    global s
    found = s.count(old)
    if found != count:
        raise SystemExit(f"expected {count} match(es), found {found}: {old[:90]!r}")
    s = s.replace(old, new)


VENUE = "مركز إبداع مصر الرقمية (كريتيفا)، الجيزة"
WA_AR = "https://wa.me/201505437979?text=" + urllib.parse.quote(
    "مرحباً، محتاج مساعدة بخصوص يوم التجارة الإلكترونية 2026"
)

# ---------- <head> ----------
rep('<html lang="en">', '<html lang="ar" dir="rtl">')
rep(
    "<title>ECommerce Day 2026 | TrafficMENA</title>",
    "<title>يوم التجارة الإلكترونية 2026 | TrafficMENA</title>\n"
    '    <!-- Arabic preview: hidden from search engines until the team signs off -->\n'
    '    <meta name="robots" content="noindex, nofollow" />',
)
rep(
    'content="ECommerce Day powered by TrafficMENA. 5 November 2026, Creativa Innovation Hub, Giza."',
    f'content="يوم التجارة الإلكترونية من TrafficMENA. 5 نوفمبر 2026، {VENUE}."',
)
# Arabic font next to Manrope (Latin words and numbers) and JetBrains Mono
rep(
    "family=Manrope:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap",
    "family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap",
    count=2,
)
# Scripts and assets live one level up
rep('<script src="ecd-analytics.js', '<script src="../ecd-analytics.js')
rep(
    '<script src="../ecd-analytics.js?v=20261008a"></script>',
    '<script src="../ecd-analytics.js?v=20261008a"></script>\n'
    '    <!-- Arabic mode for the shared components (must load before them) -->\n'
    '    <script src="../ecd-i18n.js?v=20261008d"></script>',
)
for name in ["navbar.js", "ecd-whatsapp.js", "footer.js", "prices.js", "ecd-api.js", "ecd-content.js", "tickets-section.js"]:
    rep(f'<script src="{name}', f'<script src="../{name}')
s = s.replace('"assets/', '"../assets/')
s = s.replace(" assets/hero-home-", " ../assets/hero-home-")
s = s.replace("imagesrcset=\"../assets/hero-home-480.webp 480w, assets/", "imagesrcset=\"../assets/hero-home-480.webp 480w, ../assets/")
s = re.sub(r"(\d+w), assets/", r"\1, ../assets/", s)

# ---------- right-to-left + Arabic type ----------
RTL_CSS = """
      /* ============ ARABIC (RTL) ============ */
      body {
        font-family:
          "IBM Plex Sans Arabic",
          "Manrope",
          system-ui,
          -apple-system,
          sans-serif;
        line-height: 1.7;
      }
      /* Letter-spacing and capitals break Arabic letters: labels use the
         Arabic face at a readable size instead of mono capitals. */
      .eyebrow,
      .badge,
      .countdown-label,
      .mono-eyebrow,
      .partner-tile span,
      .cmp-table thead th,
      .cd-block .u {
        font-family: "IBM Plex Sans Arabic", "Manrope", sans-serif;
        letter-spacing: 0;
        text-transform: none;
      }
      .eyebrow {
        font-size: 14px;
        font-weight: 600;
      }
      .badge {
        font-size: 13px;
      }
      .cmp-table thead th {
        font-size: 13px;
      }
      .hero-title {
        font-size: clamp(40px, 7.4vw, 84px);
        line-height: 1.25;
        letter-spacing: 0;
      }
      .section-title,
      .hero-text h2,
      .final-cta-title {
        letter-spacing: 0;
        line-height: 1.4;
      }
      .hero-media-float {
        left: auto;
        right: -6px;
      }
      .cmp-table th,
      .cmp-table td,
      .faq-item button {
        text-align: right;
      }
      .faq-answer ul {
        padding-left: 0;
        padding-right: 20px;
      }
      /* Arrows point in the reading direction */
      .ecd-flip {
        transform: scaleX(-1);
      }
      /* The logo strip runs the other way */
      @keyframes marqueeScrollRtl {
        from {
          transform: translateX(0);
        }
        to {
          transform: translateX(50%);
        }
      }
      .marquee {
        animation-name: marqueeScrollRtl;
      }
      /* English names and roles from the admin panel keep their own order */
      .speaker-name,
      .speaker-role {
        unicode-bidi: plaintext;
        text-align: right;
      }
    </style>"""
rep("    </style>\n  </head>", RTL_CSS + "\n  </head>")

# ---------- HERO ----------
rep('<div class="eyebrow">Powered by TrafficMENA</div>', '<div class="eyebrow">بتنظيم TrafficMENA</div>')
rep('<h1 class="hero-title">ECOMMERCE DAY</h1>', '<h1 class="hero-title">يوم التجارة الإلكترونية</h1>')
rep("              5 November 2026\n            </span>\n            <span class=\"badge\">", "              5 نوفمبر 2026\n            </span>\n            <span class=\"badge\">")
rep("              Creativa Innovation Hub, Giza\n            </span>\n            <span class=\"badge badge-green\">",
    f"              {VENUE}\n            </span>\n            <span class=\"badge badge-green\">")
rep("              Where MENA Ecommerce Meets Global Minds\n", "              خبرات المنطقة والعالم في مكان واحد\n")
rep("<h2>Step Into the Ecommerce Growth Ecosystem</h2>", "<h2>يوم كامل مع من يصنعون نمو التجارة الإلكترونية</h2>")
rep("""                Learn from MENA and global leaders through real decisions,
                expert sessions, and focused workshops.<br />
                Network with the operators, platforms, and partners shaping
                ecommerce growth.""",
    """                تعلم من قيادات في المنطقة ومن خارجها عبر قرارات حقيقية
                اتخذوها بأنفسهم، وجلسات مع خبراء، وورش عمل مركزة.<br />
                وتعرف على أصحاب المتاجر والمنصات والشركاء الذين يحركون السوق.""")
rep("""                <a href="tickets.html" class="btn btn-primary btn-lg">
                  Get Your Ticket
                  <svg""",
    """                <a href="tickets.html" data-ar-link class="btn btn-primary btn-lg">
                  احجز تذكرتك
                  <svg
                    class="ecd-flip\"""")
rep("""                <a href="agenda.html" class="link-underline"
                  >Explore the Experience</a
                >""",
    """                <a href="agenda.html" data-ar-link class="link-underline"
                  >اكتشف تفاصيل اليوم</a
                >""")
# Countdown left out of the Arabic page until the user decides (hard rule 9: no countdowns).
s = re.sub(
    r"\n              <div class=\"countdown\" id=\"countdown\" aria-live=\"polite\">[\s\S]*?<div class=\"countdown-blocks\" id=\"countdownBlocks\"></div>\n              </div>\n",
    "\n",
    s,
    count=1,
)
if 'id="countdown"' in s:
    raise SystemExit("countdown block still present")
rep('alt="Aerial view of the venue plaza with the TrafficMENA mark"', 'alt="صورة من أعلى لساحة المكان وعليها شعار TrafficMENA"')
rep('<div class="float-title">Real Operators</div>', '<div class="float-title">أصحاب تجربة فعلية</div>')
rep('<div class="float-sub">Not theory, not recycled slides</div>', '<div class="float-sub">لا كلام نظري ولا شرائح مكررة</div>')

# ---------- SPONSORS ----------
rep('<div class="eyebrow">Our Sponsors</div>', '<div class="eyebrow">رعاتنا</div>')
rep("""            The Sponsors Behind ECommerce Day
          </h2>""", """            الرعاة الداعمون ليوم التجارة الإلكترونية
          </h2>""")
rep("""            Meet the platforms, partners, and enablers supporting ecommerce
            across the region.""", """            منصات وشركات وجهات تدعم التجارة الإلكترونية في المنطقة، وتقف خلف
            هذا اليوم.""")
rep('<p class="sr-only" id="sponsorsStatus">Sponsors will be announced soon.</p>', '<p class="sr-only" id="sponsorsStatus">سيعلن عن الرعاة قريباً.</p>')
rep("""            <a href="become-a-sponsor.html" class="btn btn-primary"
              >Become a Sponsor</a
            >""", """            <a href="become-a-sponsor.html" data-ar-link class="btn btn-primary"
              >كن راعياً</a
            >""")

# ---------- SPEAKERS ----------
rep('<div class="eyebrow">Proven in Practice</div>', '<div class="eyebrow">خبرة من أرض الواقع</div>')
rep("""            Meet the Leaders Behind the Decisions
          </h2>""", """            تعرف على من اتخذوا القرارات بأنفسهم
          </h2>""")
rep("""            Learn from experts building, growing, and operating ecommerce
            businesses across MENA and global markets.""", """            خبراء يبنون متاجر إلكترونية ويديرونها ويكبرونها، في المنطقة وفي
            أسواق عالمية.""")
rep('aria-label="Speaker carousel"', 'aria-label="شريط المتحدثين"')
# In right-to-left, "previous" sits on the right and points right.
rep("""                aria-label="Previous speakers"
              >
                <svg""", """                aria-label="المتحدثون السابقون"
              >
                <svg
                  class="ecd-flip\"""")
rep("""                aria-label="Next speakers"
              >
                <svg""", """                aria-label="المتحدثون التاليون"
              >
                <svg
                  class="ecd-flip\"""")
rep("""            <a href="speakers.html" class="btn btn-outline-dark"
              >Meet All Speakers</a
            >""", """            <a href="speakers.html" data-ar-link class="btn btn-outline-dark"
              >كل المتحدثين</a
            >""")

# ---------- COMMUNITY ----------
rep('<div class="eyebrow">Community</div>', '<div class="eyebrow">المجتمع</div>')
rep('<h2 class="section-title" data-reveal>Our Community Partners</h2>', '<h2 class="section-title" data-reveal>شركاء المجتمع</h2>')
rep("""            <a href="become-a-sponsor.html" class="btn btn-primary"
              >Become a Partner</a
            >""", """            <a href="become-a-sponsor.html" data-ar-link class="btn btn-primary"
              >كن شريكاً</a
            >""")

# ---------- EXPERIENCE ----------
rep('<div class="eyebrow">One Day. The Whole Business.</div>', '<div class="eyebrow">يوم واحد. والصورة كاملة.</div>')
rep("""                See What Moves Ecommerce Forward
              </h2>""", """                اعرف ما الذي يدفع التجارة الإلكترونية للأمام
              </h2>""")
rep("""                Understand how decisions connect across the entire ecommerce
                business.""", """                افهم كيف ترتبط القرارات ببعضها في كل جزء من المتجر.""")
rep("""                ECommerce Day powered by TrafficMENA brings together the
                leaders, experts, and operators shaping ecommerce across Egypt
                and the Gulf.""", """                يجمع يوم التجارة الإلكترونية من TrafficMENA القيادات والخبراء
                وأصحاب التجربة الذين يشكلون السوق في مصر والخليج.""")
rep("""                Across two stages and focused workshops, you will explore the
                decisions, challenges, and experience behind real growth.""", """                على مسرحين وفي ورش عمل مركزة، ستقترب من القرارات والتحديات
                والتجارب التي صنعت نمواً حقيقياً.""")
rep("""              <a href="agenda.html" class="btn btn-primary"
                >View the Agenda</a
              >""", """              <a href="agenda.html" data-ar-link class="btn btn-primary"
                >شاهد الأجندة</a
              >""")

# ---------- COMPARE ----------
rep('<div class="eyebrow">Beyond Online Learning</div>', '<div class="eyebrow">أكثر من دورة أونلاين</div>')
rep("""            One Experience. Multiple Expert Perspectives.
          </h2>""", """            تجربة واحدة. وزوايا نظر كثيرة.
          </h2>""")
rep("""            Access live expertise, regional context, and the wider business
            picture.""", """            خبرة حية، وسياق السوق في منطقتنا، وصورة أوسع للعمل كله.""")
rep("<th>The Experience</th>", "<th>التجربة</th>")
rep('<th class="col-day">ECommerce Day</th>', '<th class="col-day">يوم التجارة الإلكترونية</th>')
rep("<th>A Typical Online Course</th>", "<th>دورة أونلاين معتادة</th>")
rep('aria-label="Compare experience"', 'aria-label="مقارنة التجربة"')
rep("""              <button role="tab" id="tabDay" aria-selected="true">
                ECommerce Day
              </button>""", """              <button role="tab" id="tabDay" aria-selected="true">
                يوم التجارة الإلكترونية
              </button>""")
rep("""              <button role="tab" id="tabCourse" aria-selected="false">
                Online Course
              </button>""", """              <button role="tab" id="tabCourse" aria-selected="false">
                دورة أونلاين
              </button>""")
rep("""            ECommerce Day connects the expertise, functions, and decisions that
            online learning often explores separately.""", """            يربط يوم التجارة الإلكترونية بين خبرات وأقسام وقرارات تتناولها
            الدورات أونلاين عادة كل واحدة على حدة.""")

# ---------- OUTCOMES ----------
rep('<div class="eyebrow">What You Take Back</div>', '<div class="eyebrow">ما ترجع به</div>')
rep("""            Turn Expert Experience Into Better Business Decisions
          </h2>""", """            حول خبرة غيرك إلى قرارات أفضل في عملك
          </h2>""")
rep("""            Build sharper priorities and a clearer view of what drives
            profitable growth.""", """            أولويات أوضح، وفهم أدق لما يصنع نمواً مربحاً.""")
rep('<a href="tickets.html" class="btn btn-primary">Choose Your Pass</a>', '<a href="tickets.html" data-ar-link class="btn btn-primary">اختر تذكرتك</a>')

# ---------- MEDIA ----------
rep('<div class="eyebrow">Proof From the Community</div>', '<div class="eyebrow">من المجتمع نفسه</div>')
rep("""            The Experience Speaks for Itself
          </h2>""", """            التجربة تتكلم عن نفسها
          </h2>""")
rep("""            Explore real events, feedback, and moments from the TrafficMENA
            community.""", """            فعاليات حقيقية وآراء ولحظات من مجتمع TrafficMENA.""")
rep('aria-label="Media wall"', 'aria-label="آراء الحضور بالصور والفيديو"')
rep('<div class="eyebrow">TrafficMENA in Numbers</div>', '<div class="eyebrow">TrafficMENA بالأرقام</div>')

# ---------- LIGHTBOX ----------
rep('aria-label="Media preview"', 'aria-label="معاينة"')
rep('<h3 class="mono-eyebrow">Media preview</h3>', '<h3 class="mono-eyebrow">معاينة</h3>')
rep('aria-label="Close preview"', 'aria-label="إغلاق المعاينة"')

# ---------- FAQ ----------
rep('<div class="eyebrow">Before You Book</div>', '<div class="eyebrow">قبل أن تحجز</div>')
rep('<h2 class="section-title" data-reveal>Everything You Need to Know</h2>', '<h2 class="section-title" data-reveal>كل ما تحتاج معرفته</h2>')
rep("""            Clear answers about the event, tickets, and access.""", """            إجابات واضحة عن اليوم والتذاكر والدخول.""")

# ---------- FINAL CTA ----------
rep('<div class="eyebrow">Access the Ecommerce Ecosystem</div>', '<div class="eyebrow">سوق التجارة الإلكترونية كله في يوم</div>')
rep('<h2 class="final-cta-title">Be Where Ecommerce Decisions Connect</h2>', '<h2 class="final-cta-title">كن حيث تلتقي قرارات التجارة الإلكترونية</h2>')
rep("""            Access the leaders and expertise shaping growth across every
            business function.""", """            قابل القيادات والخبرات التي تصنع النمو في كل قسم من أقسام العمل.""")
rep("              5 November 2026\n            </span>\n            <span>", "              5 نوفمبر 2026\n            </span>\n            <span>")
rep("              Creativa Innovation Hub, Giza\n            </span>\n          </div>", f"              {VENUE}\n            </span>\n          </div>")
rep('<a href="tickets.html" class="btn btn-primary">Get Your Ticket</a>', '<a href="tickets.html" data-ar-link class="btn btn-primary">احجز تذكرتك</a>')
rep("""            <a href="become-a-sponsor.html" class="btn btn-outline-dark"
              >Become a Partner</a
            >""", """            <a href="become-a-sponsor.html" data-ar-link class="btn btn-outline-dark"
              >كن شريكاً</a
            >""")

# ---------- floating bits ----------
rep('aria-label="Back to top"', 'aria-label="العودة إلى الأعلى"')
rep("""        ECommerce Day, 5 Nov 2026
        <span class="price-fj" data-suffix=" EGP">[Final Price] EGP</span>""",
    """        يوم التجارة الإلكترونية، 5 نوفمبر 2026
        <span class="price-fj" data-suffix=" جنيه">[السعر النهائي] جنيه</span>""")
rep('<a href="tickets.html" class="btn btn-primary">Get Ticket</a>', '<a href="tickets.html" data-ar-link class="btn btn-primary">احجز تذكرتك</a>')

# ---------- DATA (inline script) ----------
def block(start, end):
    i = s.index(start)
    j = s.index(end, i) + len(end)
    return i, j

def replace_block(start, end, new):
    global s
    i, j = block(start, end)
    s = s[:i] + new + s[j:]

replace_block("        var featureData = [", "        ];\n", """        var featureData = [
          {
            title: "مسرحان على مدار اليوم",
            line: "نقاشات تغطي كل أطراف السوق، لا قسماً واحداً.",
            svg: '<rect x="9" y="2" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v4M9 22h6"/>',
          },
          {
            title: "جلسات يقودها خبراء",
            line: "حالات حقيقية وقرارات ودروس من التنفيذ.",
            svg: '<path d="M9 18h6M10 22h4M12 2a6 6 0 0 0-4 10.4c.7.6 1 1.4 1 2.3v.3h6v-.3c0-.9.3-1.7 1-2.3A6 6 0 0 0 12 2Z"/>',
          },
          {
            title: "ورش عمل مركزة",
            line: "تطبيق عملي لمن يريد أن يتعمق أكثر.",
            svg: '<path d="M14.7 6.3a4 4 0 0 1 5.6 5.6l-8 8L7 21l1.1-5.3 8-8Z"/><path d="M9 15l-2 2"/>',
          },
          {
            title: "السوق كله في مكان واحد",
            line: "قيادات وأصحاب متاجر ومنصات ووكالات وجهات داعمة.",
            svg: '<circle cx="12" cy="5" r="2.3"/><circle cx="5" cy="19" r="2.3"/><circle cx="19" cy="19" r="2.3"/><path d="M12 7.3V13M12 13l-5.6 4M12 13l5.6 4"/>',
          },
        ];
""")

replace_block("        var cmpData = [", "        ];\n", """        var cmpData = [
          {
            f: "النطاق",
            day: "تخصصات متعددة في التجارة الإلكترونية",
            course: "موضوع واحد غالباً",
          },
          {
            f: "زاوية النظر",
            day: "قيادات وأصحاب تجربة من كل أطراف السوق",
            course: "مدرب واحد غالباً",
          },
          {
            f: "سياق السوق",
            day: "واقع السوق في مصر والخليج",
            course: "أمثلة عامة",
          },
          {
            f: "المحتوى",
            day: "قرارات وحالات حقيقية، وثمن كل قرار",
            course: "محتوى تعليمي منظم",
          },
          {
            f: "التفاعل",
            day: "أسئلة ونقاشات مباشرة",
            course: "تفاعل محدود",
          },
          {
            f: "العلاقات",
            day: "خبراء ومنصات وشركاء محتملون",
            course: "تعلم فردي في الأساس",
          },
        ];
""")

replace_block("        var outcomeData = [", "        ];\n", """        var outcomeData = [
          {
            num: "01",
            title: "اربط محركات النمو ببعضها",
            line: "شاهد كيف يؤثر جذب العملاء والتحويل والاحتفاظ بالعملاء والتشغيل وتجربة العميل كل منها في الآخر.",
            svg: '<circle cx="12" cy="5" r="2.3"/><circle cx="5" cy="19" r="2.3"/><circle cx="19" cy="19" r="2.3"/><path d="M12 7.3V13M12 13l-5.6 4M12 13l5.6 4"/>',
          },
          {
            num: "02",
            title: "وازن بين الخيارات بذكاء",
            line: "تعرف كيف يوازن أصحاب الخبرة بين النمو والتكلفة والسرعة وتوقعات العملاء.",
            svg: '<path d="M4 6h16M4 12h10M4 18h7"/><circle cx="17" cy="12" r="2"/><circle cx="9" cy="18" r="2"/>',
          },
          {
            num: "03",
            title: "اعثر على مواضع التعطيل",
            line: "اعرف الأسئلة التي تكشف فجوات الأداء والفرص الضائعة.",
            svg: '<circle cx="10" cy="10" r="7"/><path d="M21 21l-4.3-4.3"/>',
          },
          {
            num: "04",
            title: "شاهد الأثر على العمل كله",
            line: "افهم كيف تؤثر قرارات كل فريق في باقي الشركة.",
            svg: '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r="1"/>',
          },
          {
            num: "05",
            title: "طبق خبرة حقيقية",
            line: "خذ دروس السوق وطوعها لعملك وفريقك ومرحلة نموك.",
            svg: '<path d="M13 2 4 14h6l-1 8 9-12h-6l1-8Z"/>',
          },
          {
            num: "06",
            title: "ابن علاقات تفيدك",
            line: "قابل قيادات ومتخصصين ومنصات ووكالات وشركاء محتملين.",
            svg: '<circle cx="9" cy="8" r="3"/><path d="M2 20c0-3.3 3-6 7-6s7 2.7 7 6"/><circle cx="17" cy="9" r="2.4"/><path d="M15.5 14c2.9.3 5.5 2.6 5.5 6"/>',
          },
        ];
""")

rep('{ n: 3000, suffix: "+", label: "Community Members" }', '{ n: 3000, suffix: "+", label: "عضو في المجتمع" }')
rep('{ n: 80, suffix: "+", label: "Speakers and Practitioners" }', '{ n: 80, suffix: "+", label: "متحدث وخبير" }')
rep('{ n: 90, suffix: "+", label: "Sessions" }', '{ n: 90, suffix: "+", label: "جلسة" }')
rep('{ n: 400, suffix: "+", label: "Learning Hours" }', '{ n: 400, suffix: "+", label: "ساعة تعلم" }')
rep('{ n: 13, suffix: "", label: "MENA Countries" }', '{ n: 13, suffix: "", label: "دولة في المنطقة" }')
rep('{ n: 10, suffix: "+", label: "Professional Disciplines" }', '{ n: 10, suffix: "+", label: "تخصص مهني" }')

rep('''        var WA_URL =
          "https://wa.me/201505437979?text=I%20need%20help%20for%20Ecommerce%20Day%202026";''',
    f'''        var WA_URL =
          "{WA_AR}";''')

replace_block("        var faqData = [", "        ];\n", """        var faqData = [
          {
            q: "ما يوم التجارة الإلكترونية؟",
            a: [
              {
                p: "فعالية حضورية ليوم واحد من تنظيم TrafficMENA، تجمع المؤسسين والمتخصصين وأصحاب المتاجر ومقدمي الخدمات وشركات التكنولوجيا العاملين في التجارة الإلكترونية.",
              },
              {
                p: "يغطي اليوم رحلة التجارة الإلكترونية كاملة: جذب العملاء، والتحويل، والاحتفاظ بالعملاء، والتشغيل، والشحن، وتجربة العميل، ونمو العمل.",
              },
            ],
          },
          {
            q: "ما الذي يجعل التجربة مفيدة؟",
            a: [
              {
                p: "يجمع اليوم أطرافاً مختلفة من سوق التجارة الإلكترونية في مكان واحد.",
              },
              {
                p: "فيه مسرحان، وورش عمل متخصصة، وحالات حقيقية من شركات، وجلسات يقودها خبراء، وفرص للتعارف، وشركات تقدم خدمات وتكنولوجيا للتجارة الإلكترونية.",
              },
              {
                p: "وبدلاً من التركيز على قناة تسويق واحدة، يربط اليوم بين القرارات التي تؤثر في رحلة العميل والطلب من أولها لآخرها.",
              },
            ],
          },
          {
            q: "من يناسبه الحضور؟",
            a: [
              { p: "صممنا اليوم لـ:" },
              {
                ul: [
                  "مؤسسي المتاجر الإلكترونية وأصحابها.",
                  "مديري التجارة الإلكترونية.",
                  "متخصصي التسويق والنمو.",
                  "مشتري الإعلانات (Media Buyers) وفرق جذب العملاء.",
                  "متخصصي CRO وتجربة العميل.",
                  "فرق الاحتفاظ بالعملاء وCRM.",
                  "فرق التشغيل والشحن.",
                  "فرق المنتج والتكنولوجيا.",
                  "الوكالات ومقدمي خدمات التجارة الإلكترونية.",
                  "من يخطط لبدء متجر إلكتروني أو تكبيره.",
                ],
              },
            ],
          },
          {
            q: "هل اليوم للمسوقين فقط؟",
            a: [
              { p: "لا." },
              {
                p: "التسويق جزء من التجربة، لكن اليوم يغطي أيضاً CRO والاحتفاظ بالعملاء وتجربة العميل والتشغيل والشحن والتكنولوجيا وإدارة العمل ونمو التجارة الإلكترونية.",
              },
            ],
          },
          {
            q: "هل يناسب المبتدئين؟",
            a: [
              { p: "نعم." },
              {
                p: "في البرنامج جلسات لمن يدخل المجال حديثاً، ومحتوى أكثر تخصصاً لأصحاب الخبرة والمديرين وأصحاب الأعمال.",
              },
              {
                p: "ويختار كل حاضر الجلسات والورش الأقرب لدوره ومستوى خبرته.",
              },
            ],
          },
          {
            q: "متى وأين يقام اليوم؟",
            a: [
              {
                p: "يقام يوم التجارة الإلكترونية في 5 نوفمبر 2026 في مركز إبداع مصر الرقمية (كريتيفا)، الجيزة.",
              },
              {
                p: "سنرسل العنوان الكامل والخريطة وتعليمات الدخول والمواصلات للحضور المؤكدين قبل الفعالية.",
              },
            ],
          },
          {
            q: "متى يبدأ اليوم؟",
            a: [
              {
                p: "يبدأ التسجيل الساعة 10:00 صباحاً، ويبدأ برنامج المسرح الساعة 10:30 صباحاً.",
              },
              {
                p: "ننصحك بالوصول مبكراً لتنهي التسجيل وتتعرف على المكان قبل أول جلسة.",
              },
            ],
          },
          {
            q: "متى ينتهي اليوم؟",
            a: [
              { p: "من المقرر أن ينتهي اليوم نحو الساعة 7:00 مساءً." },
              {
                p: "وستجد مواعيد الجلسات والورش بالتفصيل في الأجندة.",
              },
            ],
          },
          {
            q: "هل تحتاج الورش إلى حجز مسبق؟",
            a: [
              { p: "نعم." },
              {
                p: "في اليوم أكثر من 15 ورشة عمل موزعة على 3 مسارات أساسية في التجارة الإلكترونية.",
              },
              {
                p: "يفتح حجز الورش لحاملي التذكرة الشاملة (All Access Pass) قبل الفعالية بـ 7-10 أيام، وسنعلن طريقة الحجز.",
              },
              {
                p: "نؤكد الحجوزات حسب الأماكن المتاحة. ولا يمكن حجز أكثر من 5 ورش، ولا حجز ورشتين في الوقت نفسه.",
              },
            ],
          },
          {
            q: "كيف أستلم المحتوى بعد الفعالية؟",
            a: [
              {
                p: "نرسل المحتوى المرفق بتذكرتك بالبريد الإلكتروني بعد الفعالية. ويحصل حاملو التذكرة الشاملة أيضاً على ملفات ونماذج الورش (Workshop Templates & Files).",
              },
            ],
          },
          {
            q: "هل الجلسات عملية؟",
            a: [
              {
                p: "يجمع البرنامج بين جلسات استراتيجية وحالات حقيقية من شركات ونقاشات مع خبراء وورش عمل مركزة.",
              },
              {
                p: "هدفنا أن تخرج بأفكار قابلة للتطبيق ونقاط واضحة. ويختلف شكل كل جلسة حسب المتحدث والموضوع ونوع الجلسة.",
              },
            ],
          },
          {
            q: "كيف تختارون المتحدثين؟",
            a: [
              {
                p: "نختار المتحدثين حسب خبرتهم، وصلتها بموضوعات اليوم، وقدرتهم على مشاركة معرفة مفيدة وأمثلة حقيقية وآراء مبنية على تجربة.",
              },
              {
                p: "الأولوية للخبرة المهنية والتجربة العملية، لا للعروض الترويجية.",
              },
            ],
          },
          {
            q: "متى تعلنون المتحدثين والأجندة؟",
            a: [
              {
                p: "نعلن المتحدثين والجلسات المؤكدة تباعاً مع اكتمال البرنامج.",
              },
              {
                p: "وننشر الأجندة كاملة، بمواعيد الجلسات وجداول الورش، قبل الفعالية.",
              },
            ],
          },
          {
            q: "هل هناك فرص للتعارف؟",
            a: [
              { p: "نعم." },
              {
                p: "يمكنك التعرف على الحضور طوال اليوم في منطقة المعرض (Expo Area) ومساحات التعارف وأوقات الاستراحة والمساحات المشتركة.",
              },
              {
                p: "التعارف مفتوح وعفوي. ولا تشمل التذكرة ترتيب مقابلات أو لقاءات مضمونة مع حضور بعينهم.",
              },
            ],
          },
          {
            q: "هل يمكنني استرداد ثمن التذكرة أو نقلها لشخص آخر؟",
            a: [
              {
                p: "يمكنك استرداد المبلغ كاملاً حتى نهاية يوم 30 أكتوبر 2026، أي قبل الفعالية بخمسة أيام.",
              },
              {
                p: "لطلب الاسترداد، راسلنا على info@trafficmena.com قبل الموعد من البريد الإلكتروني الذي حجزت به.",
              },
              {
                p: "لا نقبل الطلبات بعد هذا التاريخ. والتذاكر غير قابلة للتحويل، ولا يمكن نقلها لحاضر آخر.",
              },
              {
                p: "يعود المبلغ المسترد بوسيلة الدفع الأصلية نفسها.",
              },
              { contact: "للمساعدة، تواصل معنا على" },
            ],
          },
          {
            q: "هل هناك فرص رعاية؟",
            a: [
              { p: "نعم." },
              {
                p: "نوفر فرص شراكة ورعاية لمنصات التجارة الإلكترونية ومزودي التكنولوجيا وشركات الخدمات والوكالات وشركات الشحن ومزودي الدفع، وكل شركة تخدم سوق التجارة الإلكترونية.",
              },
              {
                p: "زر صفحة كن راعياً، أو تواصل معنا لتعرف الفرص المتاحة.",
              },
              { contact: "لاستفسارات الرعاية:" },
            ],
          },
        ];
""")

# Inline script strings
rep('html: "<span>Loading partners…</span>",', 'html: "<span>جار تحميل الشركاء...</span>",')
rep('line.appendChild(document.createTextNode(" or "));', 'line.appendChild(document.createTextNode(" أو "));')
rep('"aria-label": "Chat with us on WhatsApp (opens in a new tab)",', '"aria-label": "تواصل معنا على واتساب (يفتح في نافذة جديدة)",')
rep('wa.innerHTML = WA_ICON + "<span>WhatsApp</span>";', 'wa.innerHTML = WA_ICON + "<span>واتساب</span>";')
rep('{ key: "highlights", name: "Past Reviews" },', '{ key: "highlights", name: "آراء سابقة" },')
rep('{ key: "videos", name: "Video Reviews" },', '{ key: "videos", name: "آراء بالفيديو" },')
rep('''                  "Open attendee review " + (i + 1) + " of " + reviewShots.length,''',
    '''                  "افتح رأي الحضور رقم " + (i + 1) + " من " + reviewShots.length,''')
rep('alt: "Attendee review from a past TrafficMENA event",', 'alt: "رأي أحد الحضور في فعالية سابقة لـ TrafficMENA",')
rep('''                      "Video review from a past TrafficMENA event (" +
                      vNum +
                      " of " +''', '''                      "رأي بالفيديو من فعالية سابقة لـ TrafficMENA (" +
                      vNum +
                      " من " +''')
# The countdown markup is gone; its script returns early on the missing element.
rep('var labels = ["Days", "Hours", "Mins", "Secs"];', 'var labels = ["يوم", "ساعة", "دقيقة", "ثانية"];')

out = ROOT / "ar" / "index.html"
out.write_text(s, encoding="utf-8")
print("wrote", out, len(s), "bytes")
