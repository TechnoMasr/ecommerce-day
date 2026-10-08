#!/usr/bin/env python3
"""Build ar/agenda.html from agenda.html.  Run: python3 ar/build/build-agenda.py"""
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
       "قابل قيادات السوق، ووسع نظرتك للعمل كله، واتخذ قرارات أقوى، وابن شبكة علاقات قيمة في التجارة الإلكترونية.")
p.text("5 November 2026", "5 نوفمبر 2026")
p.text("Offline in Cairo", "حضورياً في القاهرة")
p.text("Two stages and three workshop rooms", "مسرحان وثلاث قاعات للورش")
p.rep('<a href="tickets.html" class="btn-primary">Book Your Ticket</a>', '<a href="tickets.html" data-ar-link class="btn-primary">احجز تذكرتك</a>')
p.rep('<a href="tickets.html" class="btn-secondary">Compare Tickets</a>', '<a href="tickets.html" data-ar-link class="btn-secondary">قارن بين التذاكر</a>')

# ---------- NOTICE ----------
p.text("ECommerce Day offers 15+ workshops covering 3 core ecommerce functions. All Access Pass holders can select and attend up to 5 workshops, subject to availability. Workshop booking opens 7-10 days before the event, and we will announce how to book. Workshops scheduled at the same time cannot be selected together.",
       "في يوم التجارة الإلكترونية أكثر من 15 ورشة عمل تغطي 3 مسارات أساسية في التجارة الإلكترونية. ويمكن لحاملي التذكرة الشاملة (All Access Pass) اختيار وحضور حتى 5 ورش حسب الأماكن المتاحة. يفتح حجز الورش قبل الفعالية بـ 7-10 أيام، وسنعلن طريقة الحجز. ولا يمكن اختيار ورشتين في الوقت نفسه.")

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
p.text("Main Stage", "المسرح الرئيسي", count=3)
p.text("Second Stage", "المسرح الثاني", count=3)
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
p.text("* Selection updates the URL, filtered views are shareable", "* اختيارك يظهر في رابط الصفحة، فتقدر تشارك العرض كما هو")

# ---------- ROOM INTRO CARDS ----------
p.text("MAIN STAGE", "المسرح الرئيسي")
p.text("The full picture of the business", "الصورة الكاملة للعمل")
p.text("Founders, leaders, decision makers", "مؤسسون وقيادات وأصحاب قرار")
p.text("SECOND STAGE", "المسرح الثاني")
p.text("Local brands on what actually happened", "علامات محلية تحكي ما حدث فعلاً")
p.text("Anyone who wants the detail behind a result", "لكل من يريد التفاصيل وراء أي نتيجة")
p.text("ACQUISITION", "مسار جذب العملاء")
p.text("Build the system that brings demand", "ابن النظام الذي يجلب الطلب")
p.text("Marketing, performance, SEO, content", "التسويق، والإعلانات المدفوعة، وSEO، والمحتوى")
p.text("CRO & RETENTION", "مسار زيادة المبيعات والاحتفاظ بالعملاء")
p.text("Turn visits into orders, and orders into repeat customers", "حول الزيارات إلى طلبات، والطلبات إلى عملاء يعودون")
p.text("Product, design, CRO, growth", "المنتج، والتصميم، وCRO، والنمو")
p.text("OPERATIONS & LOGISTICS", "مسار التشغيل والشحن")
p.text("Deliver on time and protect the margin", "سلم في الموعد واحم هامش الربح")
p.text("Operations, CX, fulfillment, retention", "التشغيل، وتجربة العميل، وتجهيز الطلبات، والاحتفاظ بالعملاء")

# ---------- TIMELINE / ROOM VIEW ----------
p.text("Session topics and times are still being finalized, so a few may shift slightly over the coming days.",
       "ما زلنا نضع اللمسات الأخيرة على موضوعات الجلسات ومواعيدها، لذلك قد يتغير بعضها قليلاً في الأيام القادمة.")
p.text("Loading agenda…", "جار تحميل الأجندة...")
p.text("Times shown are working times and may change before the final run of show.",
       "المواعيد المعروضة مبدئية، وقد تتغير قبل الجدول النهائي.")

# ---------- PLAN YOUR DAY ----------
p.text("Plan Your Day", "خطط ليومك")
p.text("Logistics, in one place", "كل التفاصيل العملية في مكان واحد")
p.text("Event Timing", "مواعيد اليوم")
p.text("Registration", "التسجيل")
p.text("Opening", "الافتتاح")
p.text("Sessions", "الجلسات")
p.text("Closing", "الختام")
p.text("Networking", "التعارف")
p.text("TIME COMING SOON", "يعلن الموعد قريباً", count=5)
p.text("Venue", "المكان")
p.rep('alt="Aerial view of Creativa Innovation Hub courtyard with the TrafficMENA logo"',
      'alt="صورة من أعلى لساحة كريتيفا وعليها شعار TrafficMENA"')
p.rep('aria-label="Creativa Innovation Hub, Giza (open in Google Maps, new tab)"',
      f'aria-label="{VENUE} (يفتح في خرائط Google في نافذة جديدة)"')
p.text("Creativa Innovation Hub, Giza", VENUE)
p.text("Entrance, parking and accessibility info will follow.", "سنرسل تفاصيل الدخول والانتظار وتسهيلات الحركة لاحقاً.")
p.text("Room Guide", "دليل القاعات")
p.text("Registration · Sponsors Area · Prayer Room · Help Desk", "التسجيل · منطقة الرعاة · مصلى · مكتب المساعدة")
p.text("Before You Arrive", "قبل أن تصل")
p.text("Have your QR ticket ready on your phone", "جهز تذكرتك (رمز QR) على هاتفك")
p.text("Book your workshops when booking opens, 7-10 days before the event", "احجز ورشك عند فتح الحجز، قبل الفعالية بـ 7-10 أيام")
p.text("Bring a laptop if your workshop needs one", "أحضر حاسوبك المحمول إن كانت ورشتك تحتاجه")
p.text("Arrive early. Registration takes time", "تعال مبكراً، فالتسجيل يأخذ وقتاً")

# ---------- FAQ ----------
p.text("Agenda FAQ", "أسئلة عن الأجندة")
p.text("Plan Your Day With Confidence", "خطط ليومك وأنت مطمئن")
FAQ = [
    ("Which sessions can I access with each pass?", "ما الجلسات المتاحة مع كل تذكرة؟"),
    ("The Standard Pass includes access to the Main Stage and Second Stage.",
     "تتيح التذكرة الأساسية (Standard Pass) حضور المسرح الرئيسي والمسرح الثاني."),
    ("The All Access Pass includes both stages, plus the opportunity to select up to five workshops from more than 15 options across three core ecommerce functions.",
     "وتتيح التذكرة الشاملة (All Access Pass) حضور المسرحين، مع اختيار حتى خمس ورش من أكثر من 15 ورشة في ثلاثة مسارات أساسية للتجارة الإلكترونية."),
    ("How do I select my workshops?", "كيف أختار ورشي؟"),
    ("Workshop booking opens 7-10 days before the event, and we will announce how to book. All Access holders can select up to five workshops, subject to availability.",
     "يفتح حجز الورش قبل الفعالية بـ 7-10 أيام، وسنعلن طريقة الحجز. ويمكن لحاملي التذكرة الشاملة اختيار حتى خمس ورش حسب الأماكن المتاحة."),
    ("Your selected workshops must not overlap, allowing you to attend each one in full.",
     "يجب ألا تتداخل مواعيد الورش التي تختارها، حتى تحضر كل واحدة منها كاملة."),
    ("Can I change my workshop selection after booking?", "هل يمكنني تغيير اختيار الورش بعد الحجز؟"),
    ("Workshop selections are final once your booking is confirmed.", "اختيار الورش نهائي بمجرد تأكيد حجزك."),
    ("Each selection reserves a limited seat that immediately becomes unavailable to other attendees, so changes cannot be accommodated after confirmation. We recommend reviewing the workshop timings carefully before completing your booking.",
     "كل اختيار يحجز مقعداً محدوداً يصبح فوراً غير متاح لغيرك، لذلك لا نستطيع تغييره بعد التأكيد. راجع مواعيد الورش جيداً قبل أن تكمل الحجز."),
    ("Can I upgrade from Standard to All Access?", "هل يمكنني الترقية من التذكرة الأساسية إلى الشاملة؟"),
    ("Yes. Our team upgrades passes on request before the event, subject to All Access availability.",
     "نعم. يرقي فريقنا التذاكر عند الطلب قبل الفعالية، حسب توفر التذكرة الشاملة."),
    ("Workshop selection will depend on the remaining capacity at the time your upgrade is confirmed.",
     "ويعتمد اختيار الورش على الأماكن المتبقية وقت تأكيد الترقية."),
    ("Contact us through email at", "تواصل معنا بالبريد الإلكتروني على"),
    ("When will the final agenda be announced?", "متى تعلن الأجندة النهائية؟"),
    ("The agenda will continue to be updated as speakers and sessions are confirmed.",
     "نحدث الأجندة باستمرار مع تأكيد المتحدثين والجلسات."),
    ("The complete schedule will be shared before the event, and registered attendees will receive all key updates directly.",
     "وسننشر الجدول الكامل قبل الفعالية، ويصل كل جديد مهم إلى الحضور المسجلين مباشرة."),
    ("Are workshop templates and files included with both passes?", "هل ملفات ونماذج الورش متاحة مع التذكرتين؟"),
    ("Workshop templates and supporting files are exclusive to the All Access Pass.",
     "ملفات ونماذج الورش حصرية للتذكرة الشاملة."),
    ("All Access holders will receive these resources by email after the event.",
     "ويستلمها حاملو التذكرة الشاملة بالبريد الإلكتروني بعد الفعالية."),
    ("What post-event content is included with each pass?", "ما المحتوى الذي يصلني بعد الفعالية مع كل تذكرة؟"),
    ("The Standard Pass covers the live day on both stages.", "تغطي التذكرة الأساسية يوم الحضور على المسرحين."),
    ("The All Access Pass adds the presentation slides and the Workshop Templates & Files, sent by email after the event.",
     "وتضيف التذكرة الشاملة شرائح العروض وملفات ونماذج الورش، ونرسلها بالبريد الإلكتروني بعد الفعالية."),
    ("Can I request a refund or transfer my ticket?", "هل يمكنني استرداد ثمن التذكرة أو نقلها لشخص آخر؟"),
    ("A full refund is available until the end of 30 October 2026, five days before the event.",
     "يمكنك استرداد المبلغ كاملاً حتى نهاية يوم 30 أكتوبر 2026، أي قبل الفعالية بخمسة أيام."),
    ("To request a refund, email info@trafficmena.com before the deadline using the email associated with your booking.",
     "لطلب الاسترداد، راسلنا على info@trafficmena.com قبل الموعد من البريد الإلكتروني الذي حجزت به."),
    ("Requests received after this date cannot be accepted. Tickets are non-transferable and cannot be reassigned to another attendee.",
     "لا نقبل الطلبات بعد هذا التاريخ. والتذاكر غير قابلة للتحويل، ولا يمكن نقلها لحاضر آخر."),
    ("Approved refunds will be returned through the original payment method.", "يعود المبلغ المسترد بوسيلة الدفع الأصلية نفسها."),
    ("For assistance, contact", "للمساعدة، تواصل معنا على"),
]
for en, ar in FAQ:
    p.text(en, ar)
p.text("or", "أو", count=2)

# ---------- FINAL CTA ----------
p.text("Pick the sessions you'll attend. Build your ECommerce Day.", "اختر الجلسات التي ستحضرها. وابن يومك كما تريده.")
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
p.text("Compare Ticket Types", "قارن بين أنواع التذاكر")

# ---------- SCRIPT ----------
p.rep('title: s.title || "Will be announced",', 'title: s.title || "يعلن قريباً",')
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
p.rep('''          "MAIN STAGE",
          "SECOND STAGE",
          "ACQUISITION",
          "CRO & RETENTION",
          "OPERATIONS & LOGISTICS",''', '''          "المسرح الرئيسي",
          "المسرح الثاني",
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
