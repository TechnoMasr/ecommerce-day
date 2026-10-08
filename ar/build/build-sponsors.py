#!/usr/bin/env python3
"""Build ar/sponsors.html from sponsors.html.  Run: python3 ar/build/build-sponsors.py"""
from common import Page

p = Page("sponsors.html")
p.head("TrafficMENA | ECommerce Day 2026 · Sponsors &amp; Partners", "الرعاة والشركاء | يوم التجارة الإلكترونية 2026")
p.breadcrumb_schema([("ECommerce Day", "يوم التجارة الإلكترونية", None), ("Sponsors & Partners", "الرعاة والشركاء", None)])
p.rep(
    """data-trail='[["ECommerce Day", "index.html"], ["Sponsors & Partners"]]'""",
    """data-trail='[["يوم التجارة الإلكترونية", "index.html"], ["الرعاة والشركاء"]]'""",
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
      .section-label span,
      .hero-note,
      .supported-asset-label,
      .experience-kind-label {
        font-family: "IBM Plex Sans Arabic", "Manrope", sans-serif;
        letter-spacing: 0;
        text-transform: none;
      }
      .section-label span {
        font-size: 14px;
        font-weight: 600;
      }
      .hero-note,
      .experience-kind-label {
        font-size: 13px;
      }
      .hero-title,
      .section-title,
      .cta-title {
        line-height: 1.35;
        letter-spacing: 0;
      }
      /* English names, tiers and blurbs from the admin panel */
      .level-pill,
      .featured-line,
      .supported-asset-value {
        unicode-bidi: plaintext;
      }
      .featured-line,
      .supported-asset-value {
        text-align: right;
      }
""")

# ---------- HERO ----------
p.rep("<span>ECommerce Day 2026 Partners</span>", "<span>شركاء يوم التجارة الإلكترونية 2026</span>")
p.rep("""        The Sponsors Strengthening the
        <span style="color: #04c44e">Ecommerce</span> Ecosystem""",
      """        الرعاة الذين يقوون سوق
        <span style="color: #04c44e">التجارة الإلكترونية</span>""")
p.rep("""        Meet the partners building visibility, authority, and valuable
        relationships across the ecommerce ecosystem.""",
      """        تعرف على الشركاء الذين يبنون حضوراً وثقة وعلاقات مفيدة في كل أطراف
        سوق التجارة الإلكترونية.""")
p.rep('<a href="become-a-sponsor.html" class="btn-primary">Become a Sponsor</a>\n        <a href="#featured-partners"',
      '<a href="become-a-sponsor.html" data-ar-link class="btn-primary">كن راعياً</a>\n        <a href="#featured-partners"')
p.rep('class="btn-secondary">View Our Partners</a>', 'class="btn-secondary">شاهد شركاءنا</a>')
p.rep("""        Strategic opportunities are available across stages, workshops,
        content, and event experiences.""",
      """        فرص الرعاية متاحة على المسارح وفي الورش والمحتوى وتجارب اليوم.""")

# ---------- SPONSORS ----------
p.rep("<span>Our Sponsors</span>", "<span>رعاتنا</span>")
p.rep("""          The Sponsors Behind ECommerce Day
        </h2>""", """          الرعاة الداعمون ليوم التجارة الإلكترونية
        </h2>""")
p.rep("""          Strategic brands bringing expertise, innovation, and market influence
          to the Ecommerce Day experience.""",
      """          علامات تجارية تضيف إلى اليوم خبرتها وأفكارها الجديدة وتأثيرها في
          السوق.""")
p.rep('id="sponsorsStatus">Sponsors will be announced soon.</p>', 'id="sponsorsStatus">سيعلن عن الرعاة قريباً.</p>')
p.rep("""        <div class="band-cta">
          <a href="become-a-sponsor.html" class="btn-primary">Become a Sponsor</a>""",
      """        <div class="band-cta">
          <a href="become-a-sponsor.html" data-ar-link class="btn-primary">كن راعياً</a>""")

# ---------- EXPERIENCES ----------
p.rep("<span>Sponsors Integration</span>", "<span>مكان علامتك في اليوم</span>")
p.rep("""        Choose Where Your Brand
        <strong style="color: #04c44e; font-weight: 800">Takes the Lead</strong>""",
      """        اختر المكان الذي
        <strong style="color: #04c44e; font-weight: 800">تتصدر فيه علامتك</strong>""")
p.rep("""        Position your brand within the experiences where attendees learn,
        engage, and build professional relationships.""",
      """        ضع علامتك داخل التجارب التي يتعلم فيها الحضور ويتفاعلون ويبنون
        علاقاتهم المهنية.""")
p.rep("""        <a href="become-a-sponsor.html" class="btn-primary"
          >Exclusive Partnership Opportunity</a
        >""", """        <a href="become-a-sponsor.html" data-ar-link class="btn-primary"
          >فرصة شراكة حصرية</a
        >""")
p.s = p.s.replace('<span class="experience-kind-label">Stage</span>', '<span class="experience-kind-label">مسرح</span>')
p.s = p.s.replace('<span class="experience-kind-label">Workshops</span>', '<span class="experience-kind-label">ورش عمل</span>')
p.s = p.s.replace('<span class="experience-kind-label">Experience</span>', '<span class="experience-kind-label">تجربة</span>')
p.s = p.s.replace('<span class="experience-kind-label">Research</span>', '<span class="experience-kind-label">بحث</span>')
for en, ar in [
    ('<div class="experience-name">Main Stage</div>', '<div class="experience-name">المسرح الرئيسي</div>'),
    ('<div class="experience-name">Second Stage</div>', '<div class="experience-name">المسرح الثاني</div>'),
    ('<div class="experience-name">Acquisition workshops</div>', '<div class="experience-name">ورش مسار جذب العملاء (Acquisition)</div>'),
    ('<div class="experience-name">CRO &amp; Retention workshops</div>', '<div class="experience-name">ورش مسار زيادة المبيعات والاحتفاظ بالعملاء (CRO &amp; Retention)</div>'),
    ("""          <div class="experience-name">
            Operations &amp; Logistics workshops
          </div>""", """          <div class="experience-name">
            ورش مسار التشغيل والشحن (Operations &amp; Logistics)
          </div>"""),
    ('<div class="experience-name">Leaders Lounge</div>', '<div class="experience-name">ركن القيادات</div>'),
    ('<div class="experience-name">Registration Experience</div>', '<div class="experience-name">تجربة التسجيل</div>'),
    ('<div class="experience-name">Content Studio</div>', '<div class="experience-name">استوديو المحتوى</div>'),
    ('<div class="experience-name">ECommerce Research</div>', '<div class="experience-name">أبحاث التجارة الإلكترونية</div>'),
]:
    p.rep(en, ar)
p.rep('<div class="experience-formula">Presented by [Partner]</div>', '<div class="experience-formula">بالشراكة مع [اسم الشريك]</div>', count=9)

# ---------- COMMUNITY ----------
p.rep("<span>Community</span>", "<span>المجتمع</span>")
p.rep('<h2 class="section-title">Our Community Partners</h2>', '<h2 class="section-title">شركاء المجتمع</h2>')
p.rep('<a href="become-a-sponsor.html" class="btn-primary">Become a Partner</a>', '<a href="become-a-sponsor.html" data-ar-link class="btn-primary">كن شريكاً</a>')

# ---------- TRACK RECORD ----------
p.rep("<span>Across TrafficMENA programs</span>", "<span>عبر برامج TrafficMENA</span>")
p.rep("""        What the community has run so far
      </h2>""", """        ما قدمه المجتمع حتى الآن
      </h2>""")
p.rep("""        Organizer record across previous programs, not a forecast for this
        edition.""", """        أرقام المنظم من برامج سابقة، وليست توقعات لهذه الدورة.""")
p.rep('<div class="stat-label">countries reached</div>', '<div class="stat-label">دولة وصلنا إليها</div>')
p.rep('<div class="stat-label">offline workshops + online workshops</div>', '<div class="stat-label">ورش حضورية + ورش أونلاين</div>')
p.rep('<div class="stat-label">sessions delivered</div>', '<div class="stat-label">جلسة قدمناها</div>')
p.rep('<div class="stat-label">speakers hosted</div>', '<div class="stat-label">متحدث استضفناه</div>')
p.rep('<div class="stat-label">hours of content</div>', '<div class="stat-label">ساعة محتوى</div>')
p.rep('<div class="stat-label">attendees, Ramadan Iftar community event</div>', '<div class="stat-label">حاضر في إفطار المجتمع الرمضاني</div>')

# ---------- CTA ----------
p.rep('<h2 class="cta-title">Put your brand inside the e-commerce journey.</h2>', '<h2 class="cta-title">ضع علامتك داخل رحلة التجارة الإلكترونية.</h2>')
p.rep("""          If your company serves merchants, stores or operators, let's build a
          partnership tied to a real experience inside the day.""",
      """          لو شركتك تخدم التجار أو المتاجر أو فرق التشغيل، فلنبن معاً شراكة
          مرتبطة بتجربة حقيقية داخل اليوم.""")
p.rep("""            href="become-a-sponsor.html"
            class="btn-primary"
            style="padding: 15px 28px; font-size: 16px; text-decoration: none"
          >
            Explore Sponsorship Opportunities""", """            href="become-a-sponsor.html"
            data-ar-link
            class="btn-primary"
            style="padding: 15px 28px; font-size: 16px; text-decoration: none"
          >
            اكتشف فرص الرعاية""")
p.rep("""            href="agenda.html"
            class="btn-secondary\"""", """            href="agenda.html"
            data-ar-link
            class="btn-secondary\"""")
p.rep("""            View the Agenda
          </a>""", """            شاهد الأجندة
          </a>""")

# ---------- SCRIPT ----------
p.rep(': "<span>Partner logo</span>";', ': "<span>شعار الشريك</span>";')
p.rep('style="padding:11px 18px;font-size:13px;text-decoration:none">Visit Partner Website</a>\'',
      'style="padding:11px 18px;font-size:13px;text-decoration:none">موقع الشريك</a>\'')
p.rep("""text-decoration:none">Explore the Supported Experience →</a>'""", """text-decoration:none">التجربة التي يدعمها ←</a>'""")
p.rep('<div class="supported-asset-label">Supported asset</div>', '<div class="supported-asset-label">ما يدعمه</div>')
p.rep('''                : "Sponsors will be announced soon.";''', '''                : "سيعلن عن الرعاة قريباً.";''')
p.rep('''grid-column:1/-1">Community partners will be announced soon.</p>';''', '''grid-column:1/-1">سيعلن عن شركاء المجتمع قريباً.</p>';''')

p.write()
