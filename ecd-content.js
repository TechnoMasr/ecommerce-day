/**
 * ECommerce Day: hydrate partners / speakers / packages from GET /api/ecd/content.
 * Requires prices.js then ecd-api.js before this file.
 */
(function (global) {
  "use strict";

  // Arabic pages load ecd-i18n.js first. Admin content (names, roles,
  // ticket cards) stays as entered; only these fixed strings change.
  var AR = global.EcdI18n || null;
  var RTL = !!AR;
  var TXT = AR
    ? {
        sponsorsSoon: "نعلن أسماء الرعاة قريباً.",
        mainSpeaker: "متحدث رئيسي",
        aboutSession: "عن الجلسة ←",
        visitSite: "موقع الشريك",
        supportedAsset: "ما يدعمه",
        explore: "التجربة التي يدعمها ←",
        partnerLogo: "شعار الشريك",
        tiers: {
          main: ["الراعي الرئيسي", "الرعاة الرئيسيون"],
          strategic: ["شريك استراتيجي", "شركاء استراتيجيون"],
          growth: ["شريك النمو", "شركاء النمو"],
          fintech: ["شريك التكنولوجيا المالية", "شركاء التكنولوجيا المالية"],
          exhibitor: ["شريك عارض", "العارضون"],
        },
        partnersSoon: "سيعلن عن الشركاء قريباً",
        speakersSoon: "سيعلن عن مزيد من المتحدثين قريباً",
      }
    : {
        sponsorsSoon: "Sponsors will be announced soon.",
        mainSpeaker: "Main Speaker",
        aboutSession: "About the session →",
        visitSite: "Visit Partner Website",
        supportedAsset: "Supported asset",
        explore: "Explore the Supported Experience →",
        partnerLogo: "Partner logo",
        tiers: {
          main: ["Main Sponsor", "Main Sponsors"],
          strategic: ["Strategic Partner", "Strategic Partners"],
          growth: ["Growth Partner", "Growth Partners"],
          fintech: ["Fintech Partner", "Fintech Partners"],
          exhibitor: ["Exhibitor Partner", "Exhibitor Partners"],
        },
        partnersSoon: "Partners announced soon",
        speakersSoon: "More speakers will be announced soon",
      };

  function el(tag, attrs) {
    var node = document.createElement(tag);
    attrs = attrs || {};
    Object.keys(attrs).forEach(function (k) {
      if (k === "text") node.textContent = attrs[k];
      else if (k === "html") node.innerHTML = attrs[k];
      else node.setAttribute(k, attrs[k]);
    });
    return node;
  }

  function checkSvg() {
    return (
      '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#04C44E" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 13l4 4L19 7"/></svg>'
    );
  }

  function xSvg() {
    return (
      '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#9AA3AD" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>'
    );
  }

  // Card without a photo: the person's initials (e.g. "WK"), replaced
  // automatically once the team uploads a photo in the admin (31 Oct 2026).
  function initialsTile(name) {
    var words = String(name || "")
      .replace(/^dr\.?\s*/i, "")
      .split(/\s+/)
      .filter(Boolean);
    var text = words.length
      ? (words[0].charAt(0) + (words.length > 1 ? words[words.length - 1].charAt(0) : "")).toUpperCase()
      : "";
    return el("span", { class: "speaker-initials", "aria-hidden": "true", text: text });
  }

  function silhouetteSvg() {
    return (
      '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#D5DAE0" stroke-width="1.4"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/></svg>'
    );
  }

  // Admin tier "community" (or no tier) = Community Partner; every other tier is a sponsor
  function isSponsor(p) {
    return (p.tier || "community") !== "community";
  }

  function makePartnerTile(p) {
    var inner;
    if (p.logoUrl) {
      inner = el("img", {
        src: p.logoUrl,
        alt: p.name || "Partner",
        class: "partner-logo",
        loading: "lazy",
        decoding: "async",
      });
    } else {
      inner = el("span", { text: p.name || "Partner" });
    }

    if (p.websiteUrl) {
      var a = el("a", {
        href: p.websiteUrl,
        target: "_blank",
        rel: "noopener noreferrer",
        class: "partner-tile",
      });
      a.style.textDecoration = "none";
      a.style.color = "inherit";
      a.style.display = "flex";
      a.style.alignItems = "center";
      a.style.justifyContent = "center";
      a.appendChild(inner);
      return a;
    }

    var tile = el("div", { class: "partner-tile" });
    tile.appendChild(inner);
    return tile;
  }

  // Sponsor lines in display order (admin "Type"), same as the Sponsors page:
  // label color, tile size (main = one large card, large = 3 per row,
  // compact = small logo tiles)
  var SPONSOR_ROWS = [
    { id: "main", color: "#101010", size: "main" },
    { id: "strategic", color: "#04c44e", size: "large" },
    { id: "growth", color: "#006681", size: "large" },
    { id: "fintech", color: "#ffb020", size: "large" },
    { id: "exhibitor", color: "#4a5563", size: "compact" },
  ];

  function logoImg(p) {
    return p.logoUrl
      ? el("img", {
          src: p.logoUrl,
          alt: p.name || "Partner",
          loading: "lazy",
          decoding: "async",
        })
      : el("span", { text: p.name || TXT.partnerLogo });
  }

  // Large / main card: logo, optional blurb, supported asset and links
  function sponsorCard(p) {
    var card = el("div", { class: "featured-card" });
    var slot = el("div", { class: "partner-logo-slot" });
    slot.appendChild(logoImg(p));
    card.appendChild(slot);
    card.appendChild(el("h3", { class: "sr-only", text: p.name || "" }));
    if (p.blurb) card.appendChild(el("div", { class: "featured-line", text: p.blurb }));
    if (p.supportedAsset) {
      var asset = el("div", { class: "supported-asset" });
      asset.appendChild(el("div", { class: "supported-asset-label", text: TXT.supportedAsset }));
      asset.appendChild(el("div", { class: "supported-asset-value", text: p.supportedAsset }));
      card.appendChild(asset);
    }
    if (p.websiteUrl || p.experienceUrl) {
      var actions = el("div", { class: "featured-card-actions" });
      if (p.websiteUrl) {
        actions.appendChild(
          el("a", {
            class: "btn-secondary",
            href: p.websiteUrl,
            target: "_blank",
            rel: "noopener noreferrer",
            text: TXT.visitSite,
          }),
        );
      }
      if (p.experienceUrl) {
        actions.appendChild(
          el("a", { class: "experience-link", href: p.experienceUrl, text: TXT.explore }),
        );
      }
      card.appendChild(actions);
    }
    return card;
  }

  // Compact tile (Exhibitors): logo only, links to the website when set
  function sponsorMini(p) {
    var tile = el(p.websiteUrl ? "a" : "div", { class: "partner-mini", title: p.name || "" });
    if (p.websiteUrl) {
      tile.setAttribute("href", p.websiteUrl);
      tile.setAttribute("target", "_blank");
      tile.setAttribute("rel", "noopener noreferrer");
    }
    tile.appendChild(logoImg(p));
    return tile;
  }

  // Home "Our Sponsors": one line per type, same layout as the Sponsors page;
  // gray tiles hold 6 slots until the first sponsor is added
  function renderSponsors(sponsors) {
    var grid = document.getElementById("sponsorsGrid");
    var rowsHost = document.getElementById("sponsorTiers");
    if (!grid || !rowsHost) return;
    var list = sponsors.slice().sort(function (a, b) {
      return (
        (b.featured ? 1 : 0) - (a.featured ? 1 : 0) ||
        (a.featuredSortOrder || 0) - (b.featuredSortOrder || 0) ||
        (a.sortOrder || 0) - (b.sortOrder || 0) ||
        String(a.name || "").localeCompare(String(b.name || ""))
      );
    });
    // A type the page does not know yet joins the Exhibitor line
    var known = SPONSOR_ROWS.map(function (r) {
      return r.id;
    });
    rowsHost.innerHTML = "";
    SPONSOR_ROWS.forEach(function (r) {
      var items = list.filter(function (p) {
        return p.tier === r.id || (r.id === "exhibitor" && known.indexOf(p.tier) === -1);
      });
      if (!items.length) return;
      var row = el("section", {
        class: "tier-row" + (r.size === "main" ? " tier-row-main" : ""),
      });
      var head = el("div", { class: "tier-head" });
      var dot = el("span", { class: "tier-dot" });
      dot.style.background = r.color;
      head.appendChild(dot);
      head.appendChild(
        el("h3", { class: "tier-name", text: TXT.tiers[r.id][items.length > 1 ? 1 : 0] }),
      );
      row.appendChild(head);
      var cells = el("div", { class: "tier-grid size-" + r.size });
      items.forEach(function (p) {
        cells.appendChild(r.size === "compact" ? sponsorMini(p) : sponsorCard(p));
      });
      row.appendChild(cells);
      rowsHost.appendChild(row);
    });
    rowsHost.hidden = !list.length;
    grid.hidden = !!list.length;
    var status = document.getElementById("sponsorsStatus");
    if (status) {
      status.textContent = list.length ? "" : TXT.sponsorsSoon;
    }
  }

  // Home "Our Community Partners" marquee
  function renderCommunity(partners) {
    var wrap = document.getElementById("communityMarquee");
    if (!wrap) return;
    wrap.innerHTML = "";
    if (!partners.length) {
      wrap.appendChild(
        el("div", {
          class: "partner-tile",
          html: "<span>" + TXT.partnersSoon + "</span>",
        }),
      );
      return;
    }
    var frag = document.createDocumentFragment();
    // Duplicate strip for CSS marquee loop
    partners.concat(partners).forEach(function (p) {
      frag.appendChild(makePartnerTile(p));
    });
    wrap.appendChild(frag);
  }

  function renderPartners(partners) {
    var list = (partners || []).filter(function (p) {
      return p.showOnHome !== false;
    });
    renderSponsors(list.filter(isSponsor));
    renderCommunity(
      list.filter(function (p) {
        return !isSponsor(p);
      }),
    );
  }

  function wireSpeakerCarousel(track) {
    var prev = document.getElementById("prevSpeaker");
    var next = document.getElementById("nextSpeaker");
    if (!prev || !next || track.dataset.carouselBound) return;
    track.dataset.carouselBound = "1";
    // Right-to-left pages scroll the other way: scrollLeft runs from 0 down
    // to negative values, and "next" moves left.
    var side = RTL ? -1 : 1;
    function scrollByCard(dir) {
      var card = track.firstElementChild;
      var amount =
        (card ? card.getBoundingClientRect().width + 20 : 280) * dir * side;
      track.scrollBy({ left: amount, behavior: "smooth" });
    }
    function updateButtons() {
      var pos = track.scrollLeft * side;
      var atStart = pos <= 4;
      var atEnd = pos >= track.scrollWidth - track.clientWidth - 4;
      prev.disabled = atStart;
      next.disabled = atEnd;
    }
    prev.addEventListener("click", function () {
      scrollByCard(-1);
    });
    next.addEventListener("click", function () {
      scrollByCard(1);
    });
    track.addEventListener("scroll", updateButtons, { passive: true });
    track.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") {
        e.preventDefault();
        scrollByCard(side);
      }
      if (e.key === "ArrowLeft") {
        e.preventDefault();
        scrollByCard(-side);
      }
    });
    setTimeout(updateButtons, 0);
  }

  // Main Speakers (admin "Main Speaker" switch, stored as featured): big
  // cards above the carousel, same card as the Speakers page. They move
  // out of the carousel, they are not repeated in it.
  function renderMainSpeakers(main) {
    var host = document.getElementById("mainSpeakers");
    if (!host) return;
    host.innerHTML = "";
    main.forEach(function (s) {
      var card = el("article", { class: "main-speaker" });
      var photo = el("div", { class: "main-speaker-photo" });
      if (s.photoUrl) {
        photo.appendChild(
          el("img", {
            src: s.photoUrl,
            alt: s.name || "Speaker",
            width: 800,
            height: 1000,
            loading: "lazy",
            decoding: "async",
          }),
        );
      } else {
        photo.appendChild(initialsTile(s.name));
      }
      var body = el("div", { class: "main-speaker-body" });
      body.appendChild(el("span", { class: "main-speaker-pill", text: TXT.mainSpeaker }));
      // A speaker with a landing page: the name is the link, and its click
      // area covers the whole card (CSS .main-speaker-link::after)
      var href = global.EcdSite && global.EcdSite.speakerPage ? global.EcdSite.speakerPage(s.id) : null;
      var name = el("h3", { class: "main-speaker-name" });
      if (href) {
        name.appendChild(el("a", { class: "main-speaker-link", href: href, text: s.name || "" }));
      } else {
        name.textContent = s.name || "";
      }
      body.appendChild(name);
      if (s.role) body.appendChild(el("p", { class: "main-speaker-role", text: s.role }));
      if (s.company) body.appendChild(el("p", { class: "main-speaker-company", text: s.company }));
      if (href) {
        body.appendChild(el("span", { class: "main-speaker-more", "aria-hidden": "true", text: TXT.aboutSession }));
      }
      card.appendChild(photo);
      card.appendChild(body);
      host.appendChild(card);
    });
    host.hidden = !main.length;
  }

  function renderSpeakers(all) {
    var track = document.getElementById("speakersTrack");
    if (!track) return;
    var main = (all || [])
      .filter(function (s) {
        return s.featured;
      })
      .sort(function (a, b) {
        return (a.featuredSortOrder || 0) - (b.featuredSortOrder || 0);
      });
    renderMainSpeakers(main);
    var speakers = (all || []).filter(function (s) {
      return !s.featured;
    });
    track.innerHTML = "";
    if (!speakers || !speakers.length) {
      var empty = el("article", { class: "speaker-card" });
      empty.appendChild(
        el("div", { class: "speaker-photo", html: silhouetteSvg() }),
      );
      var info = el("div", { class: "speaker-info" });
      info.appendChild(
        el("div", { class: "speaker-name", text: TXT.speakersSoon }),
      );
      info.appendChild(el("div", { class: "speaker-role", text: "" }));
      empty.appendChild(info);
      track.appendChild(empty);
      wireSpeakerCarousel(track);
      return;
    }
    speakers.forEach(function (s) {
      var card = el("article", { class: "speaker-card" });
      var photo = el("div", { class: "speaker-photo" });
      if (s.photoUrl) {
        var img = el("img", {
          src: s.photoUrl,
          alt: s.name || "Speaker",
          width: 800,
          height: 1000,
          loading: "lazy",
          decoding: "async",
        });
        img.style.width = "100%";
        img.style.height = "100%";
        img.style.objectFit = "cover";
        photo.appendChild(img);
      } else {
        photo.appendChild(initialsTile(s.name));
      }
      var info = el("div", { class: "speaker-info" });
      info.appendChild(el("div", { class: "speaker-name", text: s.name || "" }));
      var roleLine = [s.role, s.company].filter(Boolean).join(", ");
      info.appendChild(el("div", { class: "speaker-role", text: roleLine }));
      card.appendChild(photo);
      card.appendChild(info);
      track.appendChild(card);
    });
    wireSpeakerCarousel(track);
  }

  // Old stage names saved in the admin show as Stage 1 / Stage 2 (ecd-site.js)
  function stages(text) {
    return global.EcdSite && global.EcdSite.stages ? global.EcdSite.stages(text) : text;
  }

  function fillFeatureList(listEl, features, kind) {
    if (!listEl) return;
    listEl.innerHTML = "";
    (features || [])
      .filter(function (f) {
        return f.kind === kind;
      })
      .forEach(function (f) {
        var weight = f.emphasis ? 700 : 400;
        var icon = kind === "excluded" ? xSvg() : checkSvg();
        listEl.appendChild(
          el("li", {
            html:
              icon +
              '<span style="font-weight:' +
              weight +
              '">' +
              stages(f.label) +
              "</span>",
          }),
        );
      });
  }

  function applyPackageCard(ticketType, pkg) {
    if (!pkg) return;
    var card = document.querySelector('[data-ticket-card="' + ticketType + '"]');
    if (!card) return;

    var eyebrow = card.querySelector("[data-pkg-eyebrow]");
    var title = card.querySelector("[data-pkg-title]");
    var desc = card.querySelector("[data-pkg-desc]");
    var badge = card.querySelector("[data-pkg-badge]");
    var cta = card.querySelector("[data-pkg-cta]");

    if (eyebrow) eyebrow.textContent = pkg.eyebrow || pkg.displayName;
    if (title) title.textContent = pkg.title;
    if (desc) desc.textContent = stages(pkg.description);
    // A sold-out card keeps its "Sold Out" button (tickets-section.js)
    if (cta && !card.hasAttribute("data-sold-out")) {
      cta.textContent = pkg.ctaLabel || ("Get " + pkg.displayName);
    }
    if (badge) {
      if (pkg.badge) {
        badge.hidden = false;
        badge.textContent = pkg.badge;
      } else {
        badge.hidden = true;
      }
    }

    if (ticketType === "ct") {
      fillFeatureList(document.getElementById("confIncluded"), pkg.features, "included");
      fillFeatureList(document.getElementById("confExcluded"), pkg.features, "excluded");
    } else {
      fillFeatureList(document.getElementById("allAccess"), pkg.features, "included");
    }
  }

  function hydrate(content, activeTicketId) {
    if (!content) return;
    if (global.EventPrices && global.EventPrices.applyFromPackages) {
      global.EventPrices.applyFromPackages(content.packages, activeTicketId);
    }
    renderPartners(content.partners);
    renderSpeakers(content.speakers);
    if (content.packages) {
      applyPackageCard("ct", content.packages.ct);
      applyPackageCard("fj", content.packages.fj);
      // tickets.html card titles (no data-ticket-card markup)
      if (content.packages.ct && content.packages.ct.displayName) {
        document.querySelectorAll(".ticket-name.standard, .ticket-card.standard .ticket-name").forEach(function (el) {
          el.textContent = content.packages.ct.displayName;
        });
      }
      if (content.packages.fj && content.packages.fj.displayName) {
        document.querySelectorAll(".ticket-name.featured, .ticket-card.featured .ticket-name").forEach(function (el) {
          el.textContent = content.packages.fj.displayName;
        });
        document.querySelectorAll(".avail-title").forEach(function (el) {
          if (/full journey|all access/i.test(el.textContent || "")) {
            el.textContent = content.packages.fj.displayName;
          }
        });
      }
    }
  }

  var readyPromise = null;

  function boot(activeTicketId) {
    if (!global.EcdApi || typeof global.EcdApi.fetchContent !== "function") {
      return Promise.reject(new Error("EcdApi.fetchContent unavailable"));
    }
    if (readyPromise) return readyPromise;
    readyPromise = global.EcdApi.fetchContent()
      .then(function (content) {
        hydrate(content, activeTicketId);
        return content;
      })
      .catch(function (err) {
        console.warn("[ecd-content] fetch failed; using static fallback", err);
        // Unblock checkout with static prices.js fallback
        if (global.EventPrices && global.EventPrices.applyFromPackages) {
          var fallback = {
            ct: {
              priceEgp: global.EventPrices.PRICES.controlTower,
              displayName: global.EventPrices.TICKETS.ct.name,
              tagline: global.EventPrices.TICKETS.ct.tagline,
              description: "",
              features: [],
            },
            fj: {
              priceEgp: global.EventPrices.PRICES.fullJourney,
              displayName: global.EventPrices.TICKETS.fj.name,
              tagline: global.EventPrices.TICKETS.fj.tagline,
              description: "",
              features: [],
            },
          };
          global.EventPrices.applyFromPackages(fallback, activeTicketId);
          return { partners: [], speakers: [], packages: fallback };
        }
        throw err;
      });
    return readyPromise;
  }

  function resolveActiveTicket() {
    try {
      var params = new URLSearchParams(global.location.search);
      return params.get("ticket") === "ct" ? "ct" : "fj";
    } catch (e) {
      return "fj";
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      boot(resolveActiveTicket());
    });
  } else {
    boot(resolveActiveTicket());
  }

  global.EcdContent = {
    hydrate: hydrate,
    boot: boot,
    ready: function () {
      return readyPromise || boot(resolveActiveTicket());
    },
  };
})(window);
