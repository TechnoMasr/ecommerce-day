#!/usr/bin/env python3
"""Build tickets.html (Arabic, site root) from en/tickets.html.  Run: python3 build/build-tickets.py"""
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
    '<h1>تذكرتان، والفرق <span class="accent">في الورش</span>.</h1>',
)
p.rep("""          Select the pass that fits your goals: Standard Pass for both stages,
          or All Access Pass for stages, workshops, and premium resources.""",
      """          التذكرة الأساسية (Standard Pass) تدخلك المسرحين طوال اليوم. والتذكرة
          الشاملة (All Access Pass) تضيف إليهما ورش العمل، والملفات التي تصلك
          بعدها.""")
p.rep(""">Choose Your Ticket ↓</a""", """>اختر تذكرتك ↓</a""")
p.rep("""          <a href="agenda.html" class="btn btn-outline btn-lg"
            >View the Agenda</a
          >""", """          <a href="agenda.html" data-ar-link class="btn btn-outline btn-lg"
            >شاهد الأجندة</a
          >""")
p.rep("<span>2 Stages</span>", "<span>مسرحان</span>")
p.rep("<span>15+ Workshops</span>", "<span>أكثر من 15 ورشة</span>")
p.rep("<span>Expertise</span>", "<span>حالات حقيقية</span>")
p.rep("<span>Professional Networking</span>", "<span>تعارف</span>")

# ---------- WHY ----------
p.rep("""        <div class="eyebrow">
          <span>Why All Access Costs More</span>
        </div>
        <h2 class="section-heading" style="margin-bottom: 48px">
          You're paying for the work, not the seat
        </h2>""", """        <h2 class="section-heading">لماذا تكلف التذكرة الشاملة أكثر؟</h2>
        <p class="section-sub">لأنك تدفع لتعمل، لا لتجلس فقط</p>""")
p.rep('<div class="why-title">Workshop Access &amp; Reservation</div>', '<div class="why-title">مقعد في الورش</div>')
p.rep("""              Up to 5 workshops across the three workshop tracks, in
              capacity-limited rooms.""", """              حتى 5 ورش من المسارات الثلاثة، في قاعات مقاعدها محدودة.""")
p.rep('<div class="why-title">Presentation Slides</div>', '<div class="why-title">شرائح العروض</div>')
p.rep("""              The presentation slides from the sessions, sent by email after
              the event.""", """              شرائح الجلسات تصلك بالبريد الإلكتروني بعد الفعالية.""")
p.rep('<div class="why-title">Workshop Templates &amp; Files</div>', '<div class="why-title">ملفات ونماذج الورش</div>')
p.rep("""              The templates and files from the workshops, so you can apply the
              work in your own business.""", """              الملفات والنماذج المستخدمة في الورش، لتطبق ما تعلمته على متجرك أنت.""")

# ---------- COMPARISON ----------
p.rep("<span>Full Comparison</span>", "<span>مقارنة كاملة</span>")
p.rep("            Every feature, side by side\n", "            التذكرتان جنباً إلى جنب\n")
p.rep("""              <span>Feature</span>
              <span>Standard Pass</span>
              <span>All Access Pass</span>""", """              <span>الميزة</span>
              <span>التذكرة الأساسية</span>
              <span>التذكرة الشاملة</span>""")
for en, ar in [
    ("Access to Stage 1", "حضور المسرح 1"),
    ("Access to Stage 2", "حضور المسرح 2"),
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
p.rep("""                The Standard Pass covers full-day access to Stage 1 and
                Stage 2: keynotes, panels, case studies, sponsor
                activations and networking. The All Access Pass adds up to 5
                workshops across the three workshop tracks, the presentation
                slides and the Workshop Templates &amp; Files.""",
      """                الأساسية تدخلك المسرح 1 والمسرح 2 طوال اليوم: الكلمات
                الرئيسية، والجلسات النقاشية، ودراسات الحالة، وأنشطة الرعاة،
                والتعارف. والشاملة تضيف حتى 5 ورش عمل من المسارات الثلاثة، وشرائح
                العروض، وملفات ونماذج الورش (Workshop Templates &amp; Files).""")
p.rep("<span>How do workshops work with the All Access Pass?</span>", "<span>كيف تعمل الورش مع التذكرة الشاملة؟</span>")
p.rep("""                Workshops are offline and capacity-limited. Workshop booking
                opens 7-10 days before the event, and we will announce how to
                book. You can select up to 5 workshops; workshops at the same
                time cannot be selected together.""",
      """                الورش حضورية ومقاعدها محدودة. يفتح الحجز قبل الفعالية بـ 7 إلى 10
                أيام وسنعلن طريقته. تختار حتى 5 ورش، على ألا يتداخل موعد ورشتين
                منها.""")
p.rep("<span>Do I get the Workshop Templates &amp; Files?</span>", "<span>هل أحصل على ملفات ونماذج الورش؟</span>")
p.rep("""                Workshop Templates &amp; Files are included with the All Access
                Pass only.""", """                مع التذكرة الشاملة فقط.""")
p.rep(""">Can I upgrade from Standard to All Access later?</span""", """>هل يمكنني الترقية من التذكرة الأساسية إلى الشاملة لاحقاً؟</span""")
p.rep("""                Yes. Our team upgrades passes on request before the event,
                subject to All Access availability. Workshop seats after
                upgrading are subject to availability. Contact us through email
                at info@trafficmena.com or """,
      """                نعم، قبل الفعالية وحسب توفر التذكرة الشاملة. يرقي فريقنا تذكرتك
                عند الطلب، وتختار ورشك من الأماكن المتبقية. اطلبها على
                info@trafficmena.com أو عبر """)
p.rep("<span>Can I transfer my ticket to someone else?</span>", "<span>هل يمكنني نقل تذكرتي لشخص آخر؟</span>")
p.rep("""                No. Tickets are non-transferable and cannot be reassigned to
                another attendee. For help, contact info@trafficmena.com or
""", """                لا، التذاكر شخصية ولا يمكن نقلها لحاضر آخر. لأي مساعدة:
                info@trafficmena.com أو
""")
p.rep("<span>What is the refund policy?</span>", "<span>ما سياسة الاسترداد؟</span>")
p.rep("""                A full refund is available until the end of 30 October 2026, five
                days before the event. To request one, email
                info@trafficmena.com from the email associated with your
                booking. Requests after this date cannot be accepted.""",
      """                الاسترداد الكامل متاح حتى نهاية يوم 30 أكتوبر 2026، أي قبل الفعالية
                بخمسة أيام. أرسل طلبك إلى info@trafficmena.com من البريد الإلكتروني
                الذي حجزت به. بعد هذا التاريخ لا نقبل طلبات الاسترداد.""")
p.rep("<span>Can I get an invoice for my company?</span>", "<span>هل يمكنني الحصول على فاتورة لشركتي؟</span>")
p.rep("""                Yes. An invoice can be requested during checkout or afterwards
                via info@trafficmena.com or """, """                نعم. اطلبها أثناء الحجز أو بعده على info@trafficmena.com أو
                عبر """)
p.rep("<span>Where is the venue?</span>", "<span>أين يقام اليوم؟</span>")
p.rep("""                ECommerce Day takes place at
                <a""", """                في
                <a""")
p.rep(""">Creativa Innovation Hub, Giza</a
                >, on 5 November 2026.""", """>مركز إبداع مصر الرقمية (كريتيفا)</a
                > بالجيزة، يوم الخميس 5 نوفمبر 2026.""")
p.rep("<span>Is there a certificate?</span>", "<span>هل هناك شهادة؟</span>")
p.rep("""                No, there is no certificate. All Access Pass holders receive the
                presentation slides and the Workshop Templates &amp; Files by
                email after the event.""",
      """                لا نصدر شهادات حضور. ويستلم حاملو التذكرة الشاملة بعد الفعالية
                شرائح العروض وملفات ونماذج الورش بالبريد الإلكتروني.""")

# ---------- FINAL CTA ----------
p.rep("<h2>Pick your pass. Build your ECommerce Day.</h2>", "<h2>المسرحان فقط، أم اليوم كاملاً؟</h2>")
p.rep("""          Start with Stage 1, or take the full journey with workshops,
          hands-on practice and Workshop Templates &amp; Files.""",
      """          ابدأ بالمسرحين، أو خذ اليوم كله مع الورش والتطبيق العملي والملفات.""")
p.rep("            Book Standard Pass\n", "            احجز التذكرة الأساسية\n")
p.rep("            All Access Pass · Sold Out\n", "            التذكرة الشاملة · نفدت التذاكر\n")

p.write()
