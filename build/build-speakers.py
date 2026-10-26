#!/usr/bin/env python3
"""Build speakers.html (Arabic, site root) from en/speakers.html.  Run: python3 build/build-speakers.py"""
from common import Page

p = Page("speakers.html")
p.head("TrafficMENA | ECommerce Day 2026 · Speakers", "المتحدثون | يوم التجارة الإلكترونية 2026")
p.breadcrumb_schema([("ECommerce Day", "يوم التجارة الإلكترونية", None), ("Speakers", "المتحدثون", None)])
p.rep(
    """data-trail='[["ECommerce Day", "index.html"], ["Speakers"]]'""",
    """data-trail='[["يوم التجارة الإلكترونية", "index.html"], ["المتحدثون"]]'""",
)

p.add_css("""
      /* ============ ARABIC (RTL) ============ */
      body {
        font-family:
          "IBM Plex Sans Arabic",
          "Manrope",
          system-ui,
          -apple-system,
          sans-serif;
      }
      /* Letter-spacing and capitals break Arabic letters */
      .hero-label span,
      .hero-meta,
      .featured-label span,
      .main-speaker-pill,
      .filter-search label,
      .filter-meta-count,
      .filter-row-label,
      .lineup-progress-label {
        font-family: "IBM Plex Sans Arabic", "Manrope", sans-serif;
        letter-spacing: 0;
        text-transform: none;
      }
      .hero-label span,
      .featured-label span,
      .lineup-progress-label {
        font-size: 14px;
        font-weight: 600;
      }
      .hero-meta {
        font-size: 14px;
      }
      .filter-meta {
        margin-left: 0;
        margin-right: auto;
      }
      .filter-row-label {
        margin-right: 0;
        margin-left: 4px;
      }
      .hero-title,
      .featured-title,
      .cta-inner h2 {
        line-height: 1.35;
        letter-spacing: 0;
      }
      /* English names, roles and companies from the admin panel */
      .speaker-name,
      .speaker-role,
      .speaker-company,
      .main-speaker-name,
      .main-speaker-role,
      .main-speaker-company {
        unicode-bidi: plaintext;
        text-align: right;
      }
      .main-speaker-pill {
        font-size: 13px;
        font-weight: 600;
      }
      /* Speaker list: big heading with a line under it, no small label */
      .featured-title.ar-has-sub {
        margin-bottom: 12px;
      }
      .ar-section-sub {
        font-size: 18px;
        line-height: 1.7;
        color: #4a5563;
        max-width: 60ch;
        margin: 0 0 40px;
      }
      @media (max-width: 768px) {
        .ar-section-sub {
          font-size: 16px;
        }
      }
""")

# ---------- HERO ----------
p.rep("<span>ECommerce Day 2026 Speaker Lineup</span>", "<span>متحدثو يوم التجارة الإلكترونية 2026</span>")
p.rep("""        Meet the Minds Shaping
        <span style="color: #04c44e">Ecommerce</span> Across MENA""",
      """        من يبنون <span style="color: #04c44e">التجارة الإلكترونية</span> في
        المنطقة، ويحكون كيف""")
p.rep("""        Gain practical insight, strengthen your decisions, and build a valuable
        network with founders, business leaders, and specialists across the
        ecommerce ecosystem.""",
      """        مؤسسون وقيادات ومتخصصون من كل جوانب السوق. اسمع كيف يفكرون،
        واسألهم، وابدأ علاقة قد تفيدك بعد اليوم بكثير.""")
p.rep('<a class="btn-primary" href="#featured-speakers">Meet the Experts</a>', '<a class="btn-primary" href="#featured-speakers">تعرف على المتحدثين</a>')
p.rep('<a class="btn-secondary" href="tickets.html">Secure Your Ticket</a>', '<a class="btn-secondary" href="tickets.html" data-ar-link>احجز تذكرتك</a>')
p.rep("<span>Ecommerce Founders</span>", "<span>مؤسسو متاجر إلكترونية</span>")
p.rep("<span>Business Leaders</span>", "<span>قيادات أعمال</span>")
p.rep("<span>Industry Experts</span>", "<span>خبراء في المجال</span>")

# ---------- FEATURED ----------
p.rep("""        <div class="featured-label">
          <span>Main Speakers</span>
        </div>
        <h2 class="featured-title">Learn from operators, not theorists</h2>""", """        <h2 class="featured-title ar-has-sub">المتحدثون الرئيسيون</h2>
        <p class="ar-section-sub">تعلم من أصحاب التجربة، لا من أصحاب النظريات</p>""")

# ---------- FILTERS ----------
p.rep('<label for="spk-search">Search by name or company</label>', '<label for="spk-search">ابحث بالاسم أو الشركة</label>')
p.rep('placeholder="e.g. Mohamed, Meriin"', 'placeholder="مثال: Mohamed أو Meriin"')
p.rep('<span class="filter-meta-count" id="resultCount">1 speaker</span>', '<span class="filter-meta-count" id="resultCount">متحدث واحد</span>')
p.rep("""              Clear Filters
            </button>""", """              مسح الفلاتر
            </button>""")
p.rep('<span class="filter-row-label">Room</span>', '<span class="filter-row-label">القاعة</span>')
p.rep('></span>All Rooms\n', '></span>كل القاعات\n')
p.rep('></span>Stage 1\n', '></span>المسرح 1\n')
p.rep('></span>Stage 2\n', '></span>المسرح 2\n')
p.rep("""            >Acquisition workshops""", """            >ورش مسار جذب العملاء (Acquisition)""")
p.rep("""></span>CRO &amp;
            Retention workshops""", """></span>ورش مسار زيادة المبيعات والاحتفاظ بالعملاء (CRO &amp; Retention)""")
p.rep("""></span>Operations
            &amp; Logistics workshops""", """></span>ورش مسار التشغيل والشحن (Operations &amp; Logistics)""")
p.rep('<span class="filter-row-label">Type</span>', '<span class="filter-row-label">النوع</span>')
p.rep('data-type="Founder">Founder</button>', 'data-type="Founder">مؤسس</button>')
p.rep('data-type="Operator">Operator</button>', 'data-type="Operator">خبير تشغيل</button>')
p.rep('data-type="Executive">Executive</button>', 'data-type="Executive">قيادي تنفيذي</button>')
p.rep("""<button class="chip chip-sm" data-type="Specialist">
            Specialist
          </button>""", """<button class="chip chip-sm" data-type="Specialist">
            متخصص
          </button>""")
p.rep("""          </svg>
          Filters
        </button>""", """          </svg>
          الفلاتر
        </button>""")
p.rep('<div class="filter-row-label" style="margin-bottom: 8px">Room</div>', '<div class="filter-row-label" style="margin-bottom: 8px">القاعة</div>')
p.rep("""            <div class="filter-row-label" style="margin-bottom: 8px">
              Speaker Type
            </div>""", """            <div class="filter-row-label" style="margin-bottom: 8px">
              نوع المتحدث
            </div>""")

# ---------- GRID / LINEUP ----------
p.rep('<div class="lineup-progress-label">Lineup in progress</div>', '<div class="lineup-progress-label">القائمة تكتمل تباعاً</div>')
p.rep("""          More speakers will be announced soon.
        </div>""", """          سيعلن عن مزيد من المتحدثين قريباً.
        </div>""")
p.rep("""          href="tickets.html"
          style="padding: 12px 22px; font-size: 14px"
        >
          Get updates""", """          href="tickets.html"
          data-ar-link
          style="padding: 12px 22px; font-size: 14px"
        >
          تابع الجديد""")

# ---------- CTA ----------
p.rep("""          Build your day around the expertise that can improve your decisions,
          execution, and business results.""", """          اختر الجلسات التي تمس عملك مباشرة، ورتب يومك حولها.""")
p.rep("""            href="agenda.html"
            style="padding: 15px 28px; font-size: 16px"
          >
            View the Agenda""", """            href="agenda.html"
            data-ar-link
            style="padding: 15px 28px; font-size: 16px"
          >
            شاهد الأجندة""")
p.rep("""            href="tickets.html"
            style="
              background: transparent;""", """            href="tickets.html"
            data-ar-link
            style="
              background: transparent;""")
p.rep("""            Book Your Ticket
          </a>""", """            احجز تذكرتك
          </a>""")

# ---------- SCRIPT ----------
p.rep("""Main speakers will be announced soon.</p>';""", """سيعلن عن المتحدثين الرئيسيين قريباً.</p>';""")
p.rep("""'<span class="main-speaker-pill">Main Speaker</span>' +""", """'<span class="main-speaker-pill">متحدث رئيسي</span>' +""")
p.rep("""'<span class="main-speaker-more" aria-hidden="true">About the session →</span>'""", """'<span class="main-speaker-more" aria-hidden="true">عن الجلسة ←</span>'""")
p.rep('''            ? '<a href="agenda.html" class="speaker-session">' +
              esc(s.session) +
              " →</a>"''', '''            ? '<a href="' + EcdI18n.page("agenda.html") + '" class="speaker-session">' +
              esc(s.session) +
              " ←</a>"''')
p.rep('''          ? "The lineup is impressive. More speakers will be announced soon."
          : "More speakers will be announced soon.";''', '''          ? "قائمة المتحدثين قوية، وسنعلن عن المزيد قريباً."
          : "سيعلن عن مزيد من المتحدثين قريباً.";''')
p.rep(''': "Portrait 4:5";''', ''': "";''')
p.rep('''            esc(t.name) +
            "</span>"''', '''            esc(EcdI18n.label(t.name)) +
            "</span>"''')
p.rep('''          ? '<a href="agenda.html" class="speaker-session">' +
            esc(s.session) +
            " →</a>"''', '''          ? '<a href="' + EcdI18n.page("agenda.html") + '" class="speaker-session">' +
            esc(s.session) +
            " ←</a>"''')
p.rep('''        document.getElementById("resultCount").textContent =
          count + (count === 1 ? " speaker" : " speakers");''', '''        document.getElementById("resultCount").textContent = arCount(count);''')
p.rep('''      function renderGrid() {''', '''      // Arabic counting: 1 متحدث واحد, 2 متحدثان, 3-10 متحدثين, 11+ متحدثاً
      function arCount(n) {
        if (n === 0) return "لا يوجد متحدثون";
        if (n === 1) return "متحدث واحد";
        if (n === 2) return "متحدثان";
        if (n <= 10) return n + " متحدثين";
        return n + " متحدثاً";
      }

      function renderGrid() {''')
p.rep(''''" data-room="">All Rooms</button>';''', ''''" data-room="">كل القاعات</button>';''')
p.rep('''            ';"></span>' +
            esc(t.name) +
            "</button>";''', '''            ';"></span>' +
            esc(EcdI18n.label(t.name)) +
            "</button>";''')
p.rep('''              n +
              '">' +
              n +
              "</button>"''', '''              n +
              '">' +
              EcdI18n.label(n) +
              "</button>"''')

p.write()
