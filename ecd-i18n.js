/* ============================================================
   ecd-i18n.js: Arabic mode for the shared components.
   Loaded ONLY by the Arabic pages in ar/, before navbar.js:
     <script src="../ecd-i18n.js?v=..."></script>
   English pages never load it, so navbar.js, footer.js,
   breadcrumbs.js and ecd-whatsapp.js keep their English output
   unchanged there (they check for window.EcdI18n).

   Arabic pages live in ar/ with the same file names as the
   English ones. Shared assets and the English-only pages
   (checkout, booking confirmation) are one level up.
   ============================================================ */
(function () {
  "use strict";

  // Arabic pages that exist so far. Links to any other page go to its
  // English version until the Arabic copy is added here.
  var AR_PAGES = ["index.html", "tickets.html"];

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

  function fileOf(href) {
    return String(href || "").split("#")[0].split("?")[0];
  }

  // Link to another site page: the Arabic copy when it exists,
  // otherwise the English page.
  function page(href) {
    var file = fileOf(href) || "index.html";
    return AR_PAGES.indexOf(file) > -1 ? href : "../" + href;
  }

  // The same page in English, keeping the query (UTM tags) and the
  // section the visitor is on.
  function englishUrl() {
    var file = location.pathname.split("/").pop() || "index.html";
    var target = file === "index.html" ? "../" : "../" + file;
    return target + location.search + location.hash;
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
    page: page,
    asset: function (path) {
      return "../" + path;
    },
    englishUrl: englishUrl,
    whatsappUrl: "https://wa.me/201505437979?text=" + encodeURIComponent(WHATSAPP_TEXT),
  };
})();
