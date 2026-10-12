/* ============================================================
   ecd-site.js: where every page lives, for links between pages.
   Loaded on every page right after ecd-analytics.js and before
   the shared components (navbar, footer, breadcrumb, prices...).

   Arabic is the main site (user decision, 12 Oct 2026):
     /ecommerce-day/              Arabic: index, agenda, speakers,
                                  sponsors, tickets
     /ecommerce-day/en/           English: every marketing page
     /ecommerce-day/checkout.html and booking-confirmation.html
                                  stay at the root, English only.
   Pages without an Arabic copy (Become a Sponsor, FAQ, Policies)
   open in English from the Arabic pages.

   Checkout and Booking Confirmation link back in the language the
   buyer came from: Arabic CTAs open checkout with ?lang=ar, and
   ecd-analytics.js keeps that choice in this tab for the payment
   trip back to Booking Confirmation.
   ============================================================ */
(function () {
  "use strict";

  // Pages with an Arabic copy at the root.
  var AR_PAGES = ["index.html", "agenda.html", "speakers.html", "sponsors.html", "tickets.html"];
  // English-only pages that stay at the root.
  var ROOT_ONLY = ["checkout.html", "booking-confirmation.html"];
  var LANG_KEY = "ecd_checkout_lang";

  var path = location.pathname;
  var inEn = /\/en\/[^/]*$/.test(path);
  var current = path.split("/").pop() || "index.html";
  var rootOnly = !inEn && ROOT_ONLY.indexOf(current) > -1;

  function buyerLang() {
    try {
      if (current === "checkout.html") {
        return new URLSearchParams(location.search).get("lang") === "ar" ? "ar" : "en";
      }
      return sessionStorage.getItem(LANG_KEY) === "ar" ? "ar" : "en";
    } catch (e) {
      return "en";
    }
  }

  var lang = /^ar/i.test(document.documentElement.getAttribute("lang") || "")
    ? "ar"
    : inEn
      ? "en"
      : rootOnly
        ? buyerLang()
        : "ar";

  function fileOf(href) {
    return String(href || "").split("#")[0].split("?")[0];
  }

  // A path from the site root ("en/agenda.html") written relative to
  // this page.
  function fromHere(target) {
    if (!inEn) return target;
    return target.indexOf("en/") === 0 ? target.slice(3) : "../" + target;
  }

  // Link to another site page, written as its file name
  // ("agenda.html", "policy.html#refund", "checkout.html?ticket=2"):
  // the page in this visitor's language when it exists, otherwise English.
  // Links that are already complete (other sites, #sections, en/...,
  // ../...) are returned unchanged.
  function page(href) {
    href = String(href == null ? "" : href);
    if (/^(?:[a-z][a-z0-9+.-]*:|#|\/|\.\.\/|en\/)/i.test(href)) return href;
    var file = fileOf(href) || "index.html";
    var target;
    if (ROOT_ONLY.indexOf(file) > -1) target = href;
    else if (lang === "ar" && AR_PAGES.indexOf(file) > -1) target = href;
    else target = "en/" + href;
    return fromHere(target);
  }

  // Shared files (scripts, assets/) live at the root.
  function asset(p) {
    return fromHere(String(p));
  }

  // The same page in the other language, keeping the query (UTM tags)
  // and the section the visitor is on. Null where there is no switcher
  // (Checkout, Booking Confirmation).
  function otherLangUrl() {
    if (rootOnly) return null;
    var keep = location.search + location.hash;
    if (inEn) {
      // English-only pages (Become a Sponsor, FAQ, Policies) have no
      // Arabic copy yet: their switcher opens the Arabic home page.
      if (AR_PAGES.indexOf(current) === -1) return "../";
      return (current === "index.html" ? "../" : "../" + current) + keep;
    }
    return (current === "index.html" ? "en/" : "en/" + current) + keep;
  }

  // Links written in a page as <a href="tickets.html" data-site-link>
  // (Checkout, Booking Confirmation) follow the same rule.
  function fixLinks() {
    var links = document.querySelectorAll("a[data-site-link]");
    for (var i = 0; i < links.length; i++) {
      links[i].setAttribute("href", page(links[i].getAttribute("data-site-link") || links[i].getAttribute("href")));
    }
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", fixLinks);
  } else {
    fixLinks();
  }

  window.EcdSite = {
    lang: lang,
    inEn: inEn,
    rootOnly: rootOnly,
    page: page,
    asset: asset,
    otherLangUrl: otherLangUrl,
  };
})();
