#!/usr/bin/env python3
"""Build ar/tickets.html from tickets.html.  Run: python3 ar/build/build-tickets.py"""
from common import Page, VENUE

p = Page("tickets.html")
p.head("TrafficMENA | Tickets", "التذاكر | يوم التجارة الإلكترونية 2026")
p.breadcrumb_schema([("ECommerce Day", "يوم التجارة الإلكترونية", None), ("Tickets", "التذاكر", None)])
p.rep(
    """data-trail='[["ECommerce Day", "index.html"], ["Tickets"]]'""",
    """data-trail='[["يوم التجارة الإلكترونية", "index.html"], ["التذاكر"]]'""",
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
      /* Letter-spacing and capitals break Arabic letters */
      .eyebrow span,
      .hero-meta,
      .cmp-head {
        font-family: "IBM Plex Sans Arabic", "Manrope", sans-serif;
        letter-spacing: 0;
        text-transform: none;
      }
      .eyebrow span {
        font-size: 14px;
        font-weight: 600;
      }
      .hero-meta {
        font-size: 14px;
        font-weight: 600;
      }
      .cmp-head {
        font-size: 13px;
      }
      .hero h1,
      .section-heading,
      .cta-section h2 {
        line-height: 1.35;
      }
      .wa-btn {
        font-family: "IBM Plex Sans Arabic", "Manrope", sans-serif;
      }
      @media (max-width: 768px) {
        .hero {
          text-align: right;
        }
      }
""")

# ---------- HERO ----------
p.rep("<span>ECommerce Day 2026 Tickets</span>", "<span>تذاكر يوم التجارة الإلكترونية 2026</span>")
p.rep(
    '<h1>Choose how <span class="accent">deep</span> you want to go.</h1>',
    '<h1>اختر <span class="accent">العمق</span> الذي يناسبك.</h1>',
)
p.rep("""          Select the pass that fits your goals: Standard Pass for both stages,
          or All Access Pass for stages, workshops, and premium resources.""",
      """          اختر التذكرة الأقرب لأهدافك: التذكرة الأساسية (Standard Pass)
          لحضور المسرحين، أو التذكرة الشاملة (All Access Pass) للمسرحين وورش
          العمل والملفات الإضافية.""")
p.rep(""">Choose Your Ticket ↓</a""", """>اختر تذكرتك ↓</a""")
p.rep("""          <a href="agenda.html" class="btn btn-outline btn-lg"
            >View the Agenda</a
          >""", """          <a href="agenda.html" data-ar-link class="btn btn-outline btn-lg"
            >شاهد الأجندة</a
          >""")
p.rep("<span>2 Stages</span>", "<span>مسرحان</span>")
p.rep("<span>15+ Workshops</span>", "<span>أكثر من 15 ورشة عمل</span>")
p.rep("<span>Expertise</span>", "<span>خبرات عملية</span>")
p.rep("<span>Professional Networking</span>", "<span>تعارف مهني</span>")

# ---------- WHY ----------
p.rep("<span>Why All Access Costs More</span>", "<span>لماذا سعر التذكرة الشاملة أعلى</span>")
p.rep("          You're paying for the work, not the seat\n", "          أنت تدفع مقابل العمل، لا مقابل المقعد\n")
p.rep('<div class="why-title">Workshop Access &amp; Reservation</div>', '<div class="why-title">حضور الورش وحجزها</div>')
p.rep("""              Up to 5 workshops across the three workshop tracks, in
              capacity-limited rooms.""", """              حتى 5 ورش عمل من المسارات الثلاثة، في قاعات أماكنها محدودة.""")
p.rep('<div class="why-title">Presentation Slides</div>', '<div class="why-title">شرائح العروض</div>')
p.rep("""              The presentation slides from the sessions, sent by email after
              the event.""", """              شرائح العروض من الجلسات، نرسلها بالبريد الإلكتروني بعد الفعالية.""")
p.rep('<div class="why-title">Workshop Templates &amp; Files</div>', '<div class="why-title">ملفات ونماذج الورش</div>')
p.rep("""              The templates and files from the workshops, so you can apply the
              work in your own business.""", """              ملفات الورش ونماذجها، لتطبق ما تعلمته على عملك أنت.""")

# ---------- COMPARISON ----------
p.rep("<span>Full Comparison</span>", "<span>مقارنة كاملة</span>")
p.rep("            Every feature, side by side\n", "            كل الميزات جنباً إلى جنب\n")
p.rep("""              <span>Feature</span>
              <span>Standard Pass</span>
              <span>All Access Pass</span>""", """              <span>الميزة</span>
              <span>التذكرة الأساسية</span>
              <span>التذكرة الشاملة</span>""")
for en, ar in [
    ("Access to the Main Stage", "حضور المسرح الرئيسي"),
    ("Access to the Second Stage", "حضور المسرح الثاني"),
    ("Access to Workshop Tracks", "حضور مسارات الورش"),
    ("Workshop selection (up to 5)", "اختيار الورش (حتى 5)"),
    ("Workshop Templates &amp; Files", "ملفات ونماذج الورش"),
    ("Presentation slides", "شرائح العروض"),
]:
    p.rep(f'<span class="feature">{en}</span>', f'<span class="feature">{ar}</span>')
p.s = p.s.replace('data-label="Standard">Yes</span>', 'data-label="الأساسية">نعم</span>')
p.s = p.s.replace('data-label="Standard">No</span>', 'data-label="الأساسية">لا</span>')
p.s = p.s.replace('data-label="All Access">Yes</span>', 'data-label="الشاملة">نعم</span>')
if 'data-label="Standard"' in p.s or 'data-label="All Access"' in p.s:
    raise SystemExit("comparison labels left in English")

# ---------- FAQ ----------
p.rep("<span>FAQ &amp; Policies</span>", "<span>الأسئلة الشائعة والسياسات</span>")
p.rep("            Before you book\n", "            قبل أن تحجز\n")
p.rep("<span>What is the difference between the two tickets?</span>", "<span>ما الفرق بين التذكرتين؟</span>")
p.rep("""                The Standard Pass covers full-day access to the Main Stage and
                the Second Stage: keynotes, panels, case studies, sponsor
                activations and networking. The All Access Pass adds up to 5
                workshops across the three workshop tracks, the presentation
                slides and the Workshop Templates &amp; Files.""",
      """                تتيح التذكرة الأساسية حضور المسرح الرئيسي والمسرح الثاني طوال
                اليوم: الكلمات الرئيسية، والجلسات النقاشية، ودراسات الحالة،
                وأنشطة الرعاة، والتعارف. وتضيف التذكرة الشاملة حتى 5 ورش عمل من
                المسارات الثلاثة، وشرائح العروض، وملفات ونماذج الورش (Workshop
                Templates &amp; Files).""")
p.rep("<span>How do workshops work with the All Access Pass?</span>", "<span>كيف تعمل الورش مع التذكرة الشاملة؟</span>")
p.rep("""                Workshops are offline and capacity-limited. Workshop booking
                opens 7-10 days before the event, and we will announce how to
                book. You can select up to 5 workshops; workshops at the same
                time cannot be selected together.""",
      """                الورش حضورية وأماكنها محدودة. يفتح حجز الورش قبل الفعالية بـ
                7-10 أيام، وسنعلن طريقة الحجز. يمكنك اختيار حتى 5 ورش، ولا يمكن
                اختيار ورشتين في الوقت نفسه.""")
p.rep("<span>Do I get the Workshop Templates &amp; Files?</span>", "<span>هل أحصل على ملفات ونماذج الورش؟</span>")
p.rep("""                Workshop Templates &amp; Files are included with the All Access
                Pass only.""", """                ملفات ونماذج الورش متاحة لحاملي التذكرة الشاملة فقط.""")
p.rep(""">Can I upgrade from Standard to All Access later?</span""", """>هل يمكنني الترقية من التذكرة الأساسية إلى الشاملة لاحقاً؟</span""")
p.rep("""                Yes. Our team upgrades passes on request before the event,
                subject to All Access availability. Workshop seats after
                upgrading are subject to availability. Contact us through email
                at info@trafficmena.com or """,
      """                نعم. يرقي فريقنا التذاكر عند الطلب قبل الفعالية، حسب توفر
                التذكرة الشاملة. وأماكن الورش بعد الترقية حسب المتاح. تواصل
                معنا بالبريد الإلكتروني على info@trafficmena.com أو """)
p.rep("<span>Can I transfer my ticket to someone else?</span>", "<span>هل يمكنني نقل تذكرتي لشخص آخر؟</span>")
p.rep("""                No. Tickets are non-transferable and cannot be reassigned to
                another attendee. For help, contact info@trafficmena.com or
""", """                لا. التذاكر غير قابلة للتحويل، ولا يمكن نقلها لحاضر آخر.
                للمساعدة، راسلنا على info@trafficmena.com أو
""")
p.rep("<span>What is the refund policy?</span>", "<span>ما سياسة الاسترداد؟</span>")
p.rep("""                A full refund is available until the end of 30 October 2026, five
                days before the event. To request one, email
                info@trafficmena.com from the email associated with your
                booking. Requests after this date cannot be accepted.""",
      """                يمكنك استرداد المبلغ كاملاً حتى نهاية يوم 30 أكتوبر 2026، أي قبل
                الفعالية بخمسة أيام. لطلب الاسترداد، راسلنا على
                info@trafficmena.com من البريد الإلكتروني الذي حجزت به. ولا
                نقبل الطلبات بعد هذا التاريخ.""")
p.rep("<span>Can I get an invoice for my company?</span>", "<span>هل يمكنني الحصول على فاتورة لشركتي؟</span>")
p.rep("""                Yes. An invoice can be requested during checkout or afterwards
                via info@trafficmena.com or """, """                نعم. يمكنك طلب فاتورة أثناء الحجز أو بعده عبر
                info@trafficmena.com أو """)
p.rep("<span>Where is the venue?</span>", "<span>أين يقام اليوم؟</span>")
p.rep("""                ECommerce Day takes place at
                <a""", """                يقام يوم التجارة الإلكترونية في
                <a""")
p.rep(""">Creativa Innovation Hub, Giza</a
                >, on 5 November 2026.""", f""">{VENUE}</a
                >، يوم 5 نوفمبر 2026.""")
p.rep("<span>Is there a certificate?</span>", "<span>هل هناك شهادة؟</span>")
p.rep("""                No, there is no certificate. All Access Pass holders receive the
                presentation slides and the Workshop Templates &amp; Files by
                email after the event.""",
      """                لا، لا توجد شهادة. ويستلم حاملو التذكرة الشاملة شرائح العروض
                وملفات ونماذج الورش بالبريد الإلكتروني بعد الفعالية.""")

# ---------- FINAL CTA ----------
p.rep("<h2>Pick your pass. Build your ECommerce Day.</h2>", "<h2>اختر تذكرتك. وابن يومك كما تريده.</h2>")
p.rep("""          Start with the Main Stage, or take the full journey with workshops,
          hands-on practice and Workshop Templates &amp; Files.""",
      """          ابدأ بالمسرح الرئيسي، أو خذ التجربة كاملة مع ورش العمل والتطبيق
          العملي وملفات ونماذج الورش.""")
p.rep("            Book Standard Pass\n", "            احجز التذكرة الأساسية\n")
p.rep("            Book All Access Pass\n", "            احجز التذكرة الشاملة\n")

p.write()
