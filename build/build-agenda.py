#!/usr/bin/env python3
"""Build agenda.html (Arabic, site root) from en/agenda.html.  Run: python3 build/build-agenda.py"""
from common import Page, VENUE

p = Page("agenda.html")
p.head("TrafficMENA | ECommerce Day 2026 · Agenda", "الأجندة | يوم التجارة الإلكترونية 2026")
p.breadcrumb_schema([("ECommerce Day", "يوم التجارة الإلكترونية", None), ("Agenda", "الأجندة", None)])
p.rep(
    """data-trail='[["ECommerce Day", "index.html"], ["Agenda"]]'""",
    """data-trail='[["يوم التجارة الإلكترونية", "index.html"], ["الأجندة"]]'""",
)
p.whatsapp_links()

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
      /* Labels set in mono capitals become plain Arabic: letter-spacing and
         capitals break Arabic letters (times keep their digits). */
      .font-mono,
      .hero-meta {
        font-family: "IBM Plex Sans Arabic", "Manrope", sans-serif !important;
        letter-spacing: 0 !important;
        text-transform: none !important;
      }
      .section-label .font-mono {
        font-size: 14px;
        font-weight: 600;
      }
      .hero-title,
      .section-title {
        line-height: 1.35;
        letter-spacing: 0;
      }
      /* Buttons and chips were set in Manrope inline */
      button,
      .session-card {
        font-family: "IBM Plex Sans Arabic", "Manrope", sans-serif !important;
      }
      /* The divider between the two view tabs sits on the inner side */
      #btnRoom {
        border-left: none !important;
        border-right: 1px solid #d5dae0 !important;
      }
      /* English session titles from the admin panel keep their own order */
      .session-card > div:nth-child(2) {
        unicode-bidi: plaintext;
        text-align: right;
      }
      .wa-btn {
        font-family: "IBM Plex Sans Arabic", "Manrope", sans-serif;
      }
      /* Plan your day + FAQ: big heading with a line under it, no small label */
      .section-title.ar-has-sub {
        margin-bottom: 12px;
      }
      .ar-section-sub {
        font-size: 18px;
        line-height: 1.7;
        color: #4a5563;
        max-width: 60ch;
        margin: 0 0 32px;
      }
      @media (max-width: 768px) {
        .ar-section-sub {
          font-size: 16px;
        }
      }
""")

# FAQ buttons and session cards were left-aligned inline
p.s = p.s.replace("              text-align: left;\n            \"", "              text-align: right;\n            \"")
p.rep("text-align:left;background:#ffffff;border:1px solid #d5dae0;border-radius:12px;padding:",
      "text-align:right;background:#ffffff;border:1px solid #d5dae0;border-radius:12px;padding:")
p.rep(";font-family:Manrope,sans-serif;display:block;width:100%;", ";display:block;width:100%;")
# the "shareable" note was pushed to the far end with margin-left:auto
p.rep("""              color: #6b747e;
              margin-left: auto;""", """              color: #6b747e;
              margin-right: auto;""")

# ---------- HERO ----------
p.text("ECommerce Day 2026 Agenda", "أجندة يوم التجارة الإلكترونية 2026")
p.rep("""        From First <span style="color: #04c44e">Click</span> to Profitable
        Growth""", """        من أول <span style="color: #04c44e">نقرة</span> إلى نمو مربح""")
p.text("Meet market leaders, gain wider business insight, strengthen your decisions, and build a high-value ecommerce network.",
       "30 جلسة على مسرحين وثلاث قاعات ورش. اختر منها ما يخدم عملك، وقابل في الاستراحات من قد تعمل معهم لاحقاً.")
p.text("5 November 2026", "5 نوفمبر 2026")
p.text("Offline in Cairo", "حضورياً في كريتيفا، الجيزة")
p.text("Two stages and three workshop rooms", "مسرحان وثلاث قاعات ورش")
p.rep('<a href="tickets.html" class="btn-primary">Book Your Ticket</a>', '<a href="tickets.html" data-ar-link class="btn-primary">احجز تذكرتك</a>')
p.rep('<a href="tickets.html" class="btn-secondary">Compare Tickets</a>', '<a href="tickets.html" data-ar-link class="btn-secondary">قارن بين التذاكر</a>')

# ---------- NOTICE ----------
p.text("ECommerce Day offers 15+ workshops covering 3 core ecommerce functions. All Access Pass holders can select and attend up to 5 workshops, subject to availability. Workshop booking opens 7-10 days before the event, and we will announce how to book. Workshops scheduled at the same time cannot be selected together.",
       "أكثر من 15 ورشة عمل في 3 مسارات. مع التذكرة الشاملة (All Access Pass) تختار منها حتى 5 ورش حسب الأماكن المتاحة. يفتح الحجز قبل الفعالية بـ 7 إلى 10 أيام وسنعلن طريقته، ولا يمكنك اختيار ورشتين في التوقيت نفسه.")

# ---------- VIEW SWITCHER + FILTERS ----------
p.rep('aria-label="Agenda view"', 'aria-label="طريقة عرض الأجندة"')
p.text("Timeline View", "عرض الجدول الزمني")
p.text("Room View", "عرض حسب القاعة")
p.text("30 sessions", "30 جلسة")
p.text("Clear filters", "مسح الفلاتر")
p.rep(""">Workshops</span
          >""", """>القاعة</span
          >""")
p.text("All Sessions", "كل الجلسات")
p.text("Stage 1", "المسرح 1", count=3)
p.text("Stage 2", "المسرح 2", count=3)
p.text("Acquisition workshops", "ورش مسار جذب العملاء", count=2)
p.text("CRO & Retention workshops", "ورش مسار زيادة المبيعات والاحتفاظ بالعملاء", count=2)
p.text("Operations & Logistics workshops", "ورش مسار التشغيل والشحن", count=2)
p.text("Acquisition", "مسار جذب العملاء")
p.text("CRO & Retention", "مسار زيادة المبيعات والاحتفاظ بالعملاء")
p.text("Operations & Logistics", "مسار التشغيل والشحن")
p.text("Formats", "نوع الجلسة")
p.text("Keynotes", "الكلمات الرئيسية")
p.text("Panels", "الجلسات النقاشية")
p.text("Solo Talks", "الجلسات الفردية")
p.text("Workshops", "ورش العمل")
p.text("* Selection updates the URL, filtered views are shareable", "* الفلاتر تحفظ في رابط الصفحة، فيمكنك مشاركته كما هو")

# ---------- ROOM INTRO CARDS ----------
p.text("STAGE 1", "المسرح 1")
p.text("The full picture of the business", "الصورة الكبيرة")
p.text("Founders, leaders, decision makers", "مؤسسون وقيادات يتكلمون عن قرارات اتخذوها")
p.text("STAGE 2", "المسرح 2")
p.text("Local brands on what actually happened", "علامات محلية تحكي ما حدث فعلاً")
p.text("Anyone who wants the detail behind a result", "لمن يسأل: وكيف وصلتم لهذا الرقم؟")
p.text("ACQUISITION", "مسار جذب العملاء (Acquisition)")
p.text("Build the system that brings demand", "ابن نظاماً يجلب الطلبات باستمرار")
p.text("Marketing, performance, SEO, content", "التسويق، والإعلانات المدفوعة، وSEO، والمحتوى")
p.text("CRO & RETENTION", "مسار زيادة المبيعات والاحتفاظ بالعملاء (CRO & Retention)")
p.text("Turn visits into orders, and orders into repeat customers", "حول الزيارات إلى طلبات، والطلبات إلى عملاء يعودون")
p.text("Product, design, CRO, growth", "المنتج، والتصميم، وCRO، والنمو")
p.text("OPERATIONS & LOGISTICS", "مسار التشغيل والشحن (Operations & Logistics)")
p.text("Deliver on time and protect the margin", "سلم في الموعد واحم هامش الربح")
p.text("Operations, CX, fulfillment", "التشغيل، وتجربة العميل، وتجهيز الطلبات")

# ---------- TIMELINE / ROOM VIEW ----------
p.text("Session topics and times are still being finalized, so a few may shift slightly over the coming days.",
       "نؤكد الآن موضوعات الجلسات ومواعيدها مع المتحدثين، فقد يتغير بعضها قليلاً في الأيام القادمة.")
p.text("Loading agenda…", "جار تحميل الأجندة...")
p.text("Times shown are working times and may change before the final run of show.",
       "المواعيد المعروضة مبدئية، وقد تتغير قبل الجدول النهائي.")

# ---------- PLAN YOUR DAY ----------
p.rep("""      <div class="section-label">
        <span class="font-mono">Plan Your Day</span>
      </div>
      <h2 class="section-title">Logistics, in one place</h2>""", """      <h2 class="section-title ar-has-sub">خطط ليومك</h2>
      <p class="ar-section-sub">ما تحتاجه قبل أن تخرج من البيت</p>""")
p.text("Event Timing", "مواعيد اليوم")
p.text("Registration", "التسجيل")
p.text("Opening", "الافتتاح")
p.text("Sessions", "الجلسات")
p.text("Closing", "الختام")
p.text("Networking", "التعارف")
p.text("10:00 AM", "10:00 صباحاً")
p.text("11:00 AM", "11:00 صباحاً")
p.text("11:00 AM - 7:00 PM", "من 11:00 صباحاً إلى 7:00 مساءً")
p.text("TIME COMING SOON", "يعلن الموعد قريباً", count=2)
p.text("Venue", "المكان")
p.rep('alt="Aerial view of Creativa Innovation Hub courtyard with the TrafficMENA logo"',
      'alt="صورة من أعلى لساحة كريتيفا وعليها شعار TrafficMENA"')
p.rep('aria-label="Creativa Innovation Hub, Giza (open in Google Maps, new tab)"',
      f'aria-label="{VENUE} (يفتح في خرائط Google في نافذة جديدة)"')
p.text("Creativa Innovation Hub, Giza", VENUE)
p.text("Entrance, parking and accessibility info will follow.", "نرسل لك قبل الفعالية تفاصيل الدخول ومواقف السيارات وتسهيلات الحركة.")
p.text("Room Guide", "دليل القاعات")
p.text("Registration · Sponsors Area · Prayer Room · Help Desk", "التسجيل · منطقة الرعاة · مصلى · مكتب المساعدة")
p.text("Before You Arrive", "قبل أن تصل")
p.text("Have your QR ticket ready on your phone", "جهز تذكرتك (رمز QR) على هاتفك")
p.text("Book your workshops when booking opens, 7-10 days before the event", "احجز ورشك فور فتح الحجز، قبل الفعالية بـ 7 إلى 10 أيام")
p.text("Bring a laptop if your workshop needs one", "أحضر حاسوبك المحمول إن كانت ورشتك تحتاجه")
p.text("Arrive early. Registration takes time", "تعال مبكراً، التسجيل يأخذ وقتاً")

# ---------- FAQ ----------
p.rep("""      <div class="section-label">
        <span class="font-mono">Agenda FAQ</span>
      </div>
      <h2 class="section-title">Plan Your Day With Confidence</h2>""", """      <h2 class="section-title ar-has-sub">أسئلة عن الأجندة</h2>
      <p class="ar-section-sub">حتى لا تفاجأ يوم الفعالية</p>""")
for en, ar in [
    ("Which sessions can I access with each pass?", "ما الجلسات المتاحة مع كل تذكرة؟"),
    ("How do I select my workshops?", "كيف أختار ورشي؟"),
    ("Can I change my workshop selection after booking?", "هل يمكنني تغيير اختيار الورش بعد الحجز؟"),
    ("Can I upgrade from Standard to All Access?", "هل يمكنني الترقية من التذكرة الأساسية إلى الشاملة؟"),
    ("When will the final agenda be announced?", "متى تعلن الأجندة النهائية؟"),
    ("Are workshop templates and files included with both passes?", "هل ملفات ونماذج الورش متاحة مع التذكرتين؟"),
    ("What post-event content is included with each pass?", "ما المحتوى الذي يصلني بعد الفعالية مع كل تذكرة؟"),
    ("Can I request a refund or transfer my ticket?", "هل يمكنني استرداد ثمن التذكرة أو نقلها لشخص آخر؟"),
]:
    p.text(en, ar)

# Answers follow the document's paragraphs (12 Oct 2026): two English
# paragraphs become one Arabic paragraph where the document has one.
P1 = '<p style="margin: 0 0 12px">'
P0 = '<p style="margin: 0">'
def one(en1, en2, ar):
    p.rep(f"{P1}{en1}</p>\n            {P0}{en2}</p>", f"{P0}{ar}</p>")
one("The Standard Pass includes access to Stage 1 and Stage 2.",
    "The All Access Pass includes both stages, plus the opportunity to select up to five workshops from more than 15 options across three core ecommerce functions.",
    "التذكرة الأساسية (Standard Pass) تدخلك المسرح 1 والمسرح 2. والتذكرة الشاملة (All Access Pass) تدخلك المسرحين، ومعهما حتى خمس ورش تختارها من أكثر من 15 ورشة في ثلاثة مسارات.")
one("Workshop booking opens 7-10 days before the event, and we will announce how to book. All Access holders can select up to five workshops, subject to availability.",
    "Your selected workshops must not overlap, allowing you to attend each one in full.",
    "يفتح الحجز قبل الفعالية بـ 7 إلى 10 أيام، وسنعلن طريقته. لحاملي التذكرة الشاملة حتى خمس ورش حسب الأماكن المتاحة، بشرط ألا تتداخل مواعيدها حتى تحضر كل ورشة من أولها لآخرها.")
one("Workshop selections are final once your booking is confirmed.",
    "Each selection reserves a limited seat that immediately becomes unavailable to other attendees, so changes cannot be accommodated after confirmation. We recommend reviewing the workshop timings carefully before completing your booking.",
    "لا. يصبح اختيارك نهائياً بمجرد تأكيد الحجز، لأن كل مقعد تحجزه يخرج فوراً من المتاح لغيرك. راجع المواعيد جيداً قبل أن تؤكد.")
# Upgrade: one paragraph, no contact line (user, 12 Oct 2026)
up_start = f"{P1}Yes. Our team upgrades passes on request before the event, subject to All Access availability.</p>"
i = p.s.index(up_start)
k = p.s.index("Contact us through email at", i)
j = p.s.index("</p>", k) + len("</p>")
p.s = p.s[:i] + f"{P0}نعم، قبل الفعالية وحسب توفر التذكرة الشاملة. يرقي فريقنا تذكرتك عند الطلب، وتختار ورشك من الأماكن المتبقية وقت تأكيد الترقية.</p>" + p.s[j:]
one("The agenda will continue to be updated as speakers and sessions are confirmed.",
    "The complete schedule will be shared before the event, and registered attendees will receive all key updates directly.",
    "نحدثها كلما تأكد متحدث أو جلسة، وننشر الجدول الكامل قبل الفعالية. وأي تغيير مهم يصل للحضور المسجلين مباشرة.")
one("Workshop templates and supporting files are exclusive to the All Access Pass.",
    "All Access holders will receive these resources by email after the event.",
    "لا، هي لحاملي التذكرة الشاملة فقط، وتصلهم بالبريد الإلكتروني بعد الفعالية.")
one("The Standard Pass covers the live day on both stages.",
    "The All Access Pass adds the presentation slides and the Workshop Templates &amp; Files, sent by email after the event.",
    "التذكرة الأساسية تغطي يوم الحضور على المسرحين فقط. والشاملة تضيف شرائح العروض وملفات ونماذج الورش، نرسلها بالبريد الإلكتروني بعد الفعالية.")
p.rep(f"""{P1}A full refund is available until the end of 30 October 2026, five days before the event.</p>
            {P1}To request a refund, email info@trafficmena.com before the deadline using the email associated with your booking.</p>
            {P1}Requests received after this date cannot be accepted. Tickets are non-transferable and cannot be reassigned to another attendee.</p>
            {P1}Approved refunds will be returned through the original payment method.</p>""",
      f"""{P1}الاسترداد الكامل متاح حتى نهاية يوم 30 أكتوبر 2026، أي قبل الفعالية بخمسة أيام. أرسل طلبك إلى info@trafficmena.com من البريد الإلكتروني الذي حجزت به، ويعود المبلغ بوسيلة الدفع نفسها. بعد هذا التاريخ لا نقبل طلبات الاسترداد.</p>
            {P1}التذاكر شخصية ولا يمكن نقلها لحاضر آخر.</p>""")
p.text("For assistance, contact", "تواصل معنا:")
p.text("or", "أو")

# ---------- FINAL CTA ----------
p.text("Pick the sessions you'll attend. Build your ECommerce Day.", "اختر جلساتك، ورتب يومك بنفسك.")
p.rep("""            href="tickets.html"
            class="btn-primary"
            style="padding: 15px 28px; font-size: 16px"
          >
            Book Your Ticket""", """            href="tickets.html"
            data-ar-link
            class="btn-primary"
            style="padding: 15px 28px; font-size: 16px"
          >
            احجز تذكرتك""")
p.rep("""            href="tickets.html"
            class="btn-secondary"
            style="
              background: transparent;""", """            href="tickets.html"
            data-ar-link
            class="btn-secondary"
            style="
              background: transparent;""")
p.text("Compare Ticket Types", "قارن بين التذاكر")

# ---------- SCRIPT ----------
p.rep('title: stageText(s.title || "Will be announced"),', 'title: stageText(s.title || "يعلن قريباً"),')
p.rep('output: s.output || "Announced soon",', 'output: s.output || "يعلن قريباً",')
p.rep('level: s.level || "All levels",', 'level: s.level || "كل المستويات",')
p.rep('font-weight:600;background:#f4f6f8;border:1px solid #e6eaee;color:#4a5563;">All Tickets</span>\';',
      'font-weight:600;background:#f4f6f8;border:1px solid #e6eaee;color:#4a5563;">كل التذاكر</span>\';')
p.rep('font-weight:600;background:#101010;border:1px solid #101010;color:#05ef62;">All Access Pass Only</span>\';',
      'font-weight:600;background:#101010;border:1px solid #101010;color:#05ef62;">التذكرة الشاملة فقط</span>\';')
p.rep('''          esc(s.fmt) +
          "</span></div>" +''', '''          esc(EcdI18n.label(s.fmt)) +
          "</span></div>" +''')
p.rep('''          esc(s.speaker) +
          "</div>" +''', '''          esc(EcdI18n.label(s.speaker)) +
          "</div>" +''')
p.rep('''          "STAGE 1",
          "STAGE 2",
          "ACQUISITION",
          "CRO & RETENTION",
          "OPERATIONS & LOGISTICS",''', '''          "المسرح 1",
          "المسرح 2",
          "جذب العملاء",
          "زيادة المبيعات والاحتفاظ بالعملاء",
          "التشغيل والشحن",''')
p.rep('label: "Dhuhr prayer break" }', 'label: "استراحة صلاة الظهر" }')
p.rep('label: "Lunch break" }', 'label: "استراحة الغداء" }')
p.rep('label: "Asr prayer break" }', 'label: "استراحة صلاة العصر" }')
p.rep('label: "Maghrib prayer break" }', 'label: "استراحة صلاة المغرب" }')
p.rep('var CLOSING = { start: "6:40", end: "6:50", label: "Closing" };', 'var CLOSING = { start: "6:40", end: "6:50", label: "الختام" };')
p.rep('''<p style="font-size:12px;color:#6b747e;margin:0;">Coming soon</p>';''', '''<p style="font-size:12px;color:#6b747e;margin:0;">قريباً</p>';''')
p.rep('''<p style="grid-column:1/-1;font-size:13px;color:#6b747e;">Coming soon</p>';''', '''<p style="grid-column:1/-1;font-size:13px;color:#6b747e;">قريباً</p>';''')
p.rep('''          resultCount.textContent =
            sessions.filter(matchSession).length + " sessions";''', '''          resultCount.textContent = arSessions(sessions.filter(matchSession).length);''')
p.rep('''      function refreshAgendaViews() {''', '''      // Arabic counting: 1 جلسة واحدة, 2 جلستان, 3-10 جلسات, 11+ جلسة
      function arSessions(n) {
        if (n === 0) return "لا توجد جلسات";
        if (n === 1) return "جلسة واحدة";
        if (n === 2) return "جلستان";
        if (n <= 10) return n + " جلسات";
        return n + " جلسة";
      }

      function refreshAgendaViews() {''')
p.rep("font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.06em;text-transform:uppercase;color:#4a5563;",
      "font-size:10px;color:#4a5563;")
p.rep('el.textContent = "Agenda unavailable (API not loaded).";', 'el.textContent = "الأجندة غير متاحة الآن.";')
p.rep('''                "Could not load agenda. Refresh to try again.";''', '''                "تعذر تحميل الأجندة. حدث الصفحة وحاول مرة أخرى.";''')

p.write()
