/* ============================================================
   ecd-i18n.js: Arabic strings for the shared components.
   Loaded ONLY by the Arabic pages (the site root), after
   ecd-site.js and before navbar.js:
     <script src="ecd-i18n.js?v=..."></script>
   English pages (en/) never load it, so navbar.js, footer.js,
   breadcrumbs.js and ecd-whatsapp.js keep their English strings
   there (they check for window.EcdI18n). Links between pages come
   from ecd-site.js in both languages.
   ============================================================ */
(function () {
  "use strict";

  var WHATSAPP_TEXT = "مرحباً، محتاج مساعدة بخصوص يوم التجارة الإلكترونية 2026";

  var STRINGS = {
    // Navbar
    "nav.home": "الرئيسية",
    "nav.agenda": "الأجندة",
    "nav.speakers": "المتحدثون",
    "nav.sponsors": "الرعاة",
    "nav.tickets": "التذاكر",
    "nav.faq": "الأسئلة الشائعة",
    "nav.platform": "TrafficMENA",
    "nav.platformMobile": "منصة TrafficMENA",
    "nav.platformAria": "منصة TrafficMENA، الموقع الرئيسي لـ TrafficMENA",
    "nav.homeAria": "الصفحة الرئيسية ليوم التجارة الإلكترونية",
    "nav.logoAlt": "يوم التجارة الإلكترونية من TrafficMENA",
    "nav.primaryAria": "التنقل الرئيسي",
    "nav.menuAria": "القائمة",
    "nav.menu": "القائمة",
    "nav.sponsor": "كن راعياً",
    "nav.ticket": "احجز تذكرتك",
    "nav.switch": "English",
    "nav.switchAria": "View this page in English",
    // Footer
    "footer.experience": "التجربة",
    "footer.speakers": "المتحدثون",
    "footer.tickets": "التذاكر",
    "footer.contact": "تواصل معنا",
    "footer.whatsapp": "واتساب",
    "footer.privacy": "سياسة الخصوصية",
    "footer.rights": "جميع الحقوق محفوظة",
    "footer.socialAria": "حسابات TrafficMENA على مواقع التواصل",
    "footer.on": "TrafficMENA على",
    "footer.newTab": "(يفتح في نافذة جديدة)",
    // Breadcrumb
    "bc.aria": "مسار التنقل",
    // WhatsApp
    "wa.aria": "تواصل معنا على واتساب (يفتح في نافذة جديدة)",
  };

  // Fixed labels that come from the admin panel (R12, user-approved list).
  // A value not listed here shows as entered until it is added.
  var LABELS = {
    // Stage 1 / Stage 2 (26 Oct 2026); the old admin names map to them too
    "stage 1": "المسرح\u00a01",
    "stage 2": "المسرح\u00a02",
    "main stage": "المسرح\u00a01",
    "second stage": "المسرح\u00a02",
    // Workshop rooms (29 Oct 2026); the retired track names map to them too
    "room 1": "القاعة\u00a01",
    "room 2": "القاعة\u00a02",
    "room 3": "القاعة\u00a03",
    "acquisition workshops": "القاعة\u00a01",
    "cro & retention workshops": "القاعة\u00a02",
    "operations & logistics workshops": "القاعة\u00a03",
    keynote: "الكلمة الرئيسية",
    "solo talk": "جلسة فردية",
    "solo talks": "جلسة فردية",
    panel: "جلسة نقاشية",
    workshop: "ورشة عمل",
    intermediate: "مستوى متوسط",
    founder: "مؤسس",
    operator: "خبير تشغيل",
    executive: "قيادي تنفيذي",
    specialist: "متخصص",
    confirmed: "مؤكد",
    "speaker will be announced": "سيعلن عن المتحدث قريباً",
  };

  function label(value) {
    var key = String(value == null ? "" : value).trim().toLowerCase();
    return Object.prototype.hasOwnProperty.call(LABELS, key) ? LABELS[key] : value;
  }

  // Link to another site page: the Arabic copy when it exists, otherwise
  // the English page in en/ (pages list in ecd-site.js).
  function page(href) {
    return window.EcdSite ? window.EcdSite.page(href) : href;
  }

  // Links written in the page as href="agenda.html" data-ar-link go to the
  // Arabic copy when it exists, otherwise to the English page.
  function fixPageLinks() {
    var links = document.querySelectorAll("a[data-ar-link]");
    for (var i = 0; i < links.length; i++) {
      links[i].setAttribute("href", page(links[i].getAttribute("href")));
      links[i].removeAttribute("data-ar-link");
    }
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", fixPageLinks);
  } else {
    fixPageLinks();
  }

  window.EcdI18n = {
    lang: "ar",
    dir: "rtl",
    font: '"IBM Plex Sans Arabic", "Manrope", Tahoma, sans-serif',
    t: function (key, fallback) {
      return Object.prototype.hasOwnProperty.call(STRINGS, key) ? STRINGS[key] : fallback;
    },
    label: label,
    page: page,
    asset: function (path) {
      return window.EcdSite ? window.EcdSite.asset(path) : path;
    },
    whatsappUrl: "https://wa.me/201505437979?text=" + encodeURIComponent(WHATSAPP_TEXT),
  };
})();
