/**
 * ECommerce Day 2026: backend bridge for static HTML pages.
 * Talks to trafficmena `/api/ecd/*` with a temporary checkout token (not Better Auth).
 *
 * Configure API_BASE for your environment. Package prices/names come from
 * GET /content (ecd-content.js → EventPrices.applyFromPackages); server re-validates on session/pay.
 */
(function (global) {
  "use strict";

  // API_BASE follows the host serving the page, so the same files work on
  // www (production), staging and localhost without editing. Never hardcode
  // one environment here: the backend rejects cross-environment origins
  // (ECD_ORIGIN_DENIED), which leaves prices empty and blocks checkout.
  function resolveApiBase() {
    var host = (global.location && global.location.hostname) || "";
    if (host === "localhost" || host === "127.0.0.1") return "http://localhost:8080/api/ecd";
    if (host === "staging.trafficmena.com") return "https://staging.trafficmena.com/api/ecd";
    return "https://www.trafficmena.com/api/ecd";
  }

  var CONFIG = {
    API_BASE: resolveApiBase(),
    STORAGE_TOKEN: "ecd2026_checkout_token",
    STORAGE_PUBLIC: "ecd2026_public_token",
    STORAGE_BOOKING: "ecd2026_booking",
    EVENT: {
      title: "ECommerce Day 2026",
      // First talk 10:30 AM, day ends 7:30 PM Cairo (UTC+2 in November). Registration opens 9:30.
      startIso: "2026-11-05T10:30:00+02:00",
      endIso: "2026-11-05T19:30:00+02:00",
      location: "Creativa Innovation Hub, Giza",
    },
  };

  function getToken() {
    try {
      return sessionStorage.getItem(CONFIG.STORAGE_TOKEN) || "";
    } catch (e) {
      return "";
    }
  }

  function setSession(payload) {
    try {
      if (payload.checkoutToken) {
        sessionStorage.setItem(CONFIG.STORAGE_TOKEN, payload.checkoutToken);
      }
      if (payload.publicToken) {
        sessionStorage.setItem(CONFIG.STORAGE_PUBLIC, payload.publicToken);
      }
      sessionStorage.setItem(
        CONFIG.STORAGE_BOOKING,
        JSON.stringify({
          orderCode: payload.orderCode,
          bookingId: payload.bookingId,
          publicToken: payload.publicToken,
          checkoutToken: payload.checkoutToken,
          ticketType: payload.ticketType,
          qty: payload.qty,
          totalCents: payload.totalCents,
        }),
      );
    } catch (e) {}
  }

  function getStoredBooking() {
    try {
      var raw = sessionStorage.getItem(CONFIG.STORAGE_BOOKING);
      return raw ? JSON.parse(raw) : null;
    } catch (e) {
      return null;
    }
  }

  function getPublicToken() {
    try {
      return sessionStorage.getItem(CONFIG.STORAGE_PUBLIC) || "";
    } catch (e) {
      return "";
    }
  }

  // Every request gets a time limit, so a stalled mobile connection shows
  // an error instead of loading forever (10 Oct 2026). Requests that are safe
  // to repeat (reads, checkout session, promo check, payment checks) are tried
  // once more after a network error, a time-out or a 502/503/504. Pay, sponsor
  // enquiries, workshop picks and uploads are never repeated automatically:
  // a second Pay could start a second payment.
  var TIMEOUT_MS = 20000;
  var RETRY_DELAY_MS = 1500;

  function requestOnce(url, init, timeoutMs) {
    var controller =
      typeof AbortController === "function" ? new AbortController() : null;
    var timer = null;
    if (controller && timeoutMs) {
      timer = setTimeout(function () {
        controller.abort();
      }, timeoutMs);
      init.signal = controller.signal;
    }
    function done() {
      if (timer) clearTimeout(timer);
    }
    function networkError(timedOut) {
      var err = new Error(
        timedOut
          ? "The connection timed out. Check your internet and try again."
          : "We couldn't reach the server. Check your internet and try again.",
      );
      err.code = timedOut ? "TIMEOUT" : "NETWORK";
      err.network = true;
      return err;
    }
    return fetch(url, init).then(
      async function (res) {
        try {
          var json = null;
          try {
            json = await res.json();
          } catch (e) {
            // The answer started but stopped before the end: a time-out,
            // not an empty answer.
            if (e && e.name === "AbortError") throw networkError(true);
            json = null;
          }
          if (!res.ok) {
            var err = new Error(
              (json && json.error && json.error.message) ||
                "Request failed (" + res.status + ")",
            );
            err.status = res.status;
            err.code = json && json.error && json.error.code;
            err.payload = json;
            throw err;
          }
          return json && json.data !== undefined ? json.data : json;
        } finally {
          done();
        }
      },
      function (e) {
        done();
        throw networkError(e && e.name === "AbortError");
      },
    );
  }

  function isRetryable(err) {
    return !!(
      err &&
      (err.network || err.status === 502 || err.status === 503 || err.status === 504)
    );
  }

  function api(path, options) {
    options = options || {};
    var headers = Object.assign(
      { "Content-Type": "application/json" },
      options.headers || {},
    );
    var token = options.token !== undefined ? options.token : getToken();
    if (token) headers.Authorization = "Bearer " + token;
    var method = options.method || "GET";
    var retry = options.retry !== undefined ? options.retry : method === "GET";

    function attempt() {
      return requestOnce(
        CONFIG.API_BASE + path,
        {
          method: method,
          headers: headers,
          body: options.body ? JSON.stringify(options.body) : undefined,
          credentials: "omit",
        },
        options.timeoutMs || TIMEOUT_MS,
      );
    }

    return attempt().catch(function (err) {
      if (!retry || !isRetryable(err)) throw err;
      return new Promise(function (resolve) {
        setTimeout(resolve, RETRY_DELAY_MS);
      }).then(attempt);
    });
  }

  function createSession(payload) {
    return api("/session", {
      method: "POST",
      body: payload,
      token: "",
      retry: true,
    }).then(
      function (data) {
        setSession(data);
        return data;
      },
    );
  }

  function validatePromo(payload) {
    return api("/promo/validate", {
      method: "POST",
      body: payload,
      token: "",
      retry: true,
    });
  }

  function fetchPaymentMethods() {
    return api("/payment-methods");
  }

  // Never retried, and a longer limit: the server may wait on the gateway.
  function pay(payload) {
    return api("/pay", { method: "POST", body: payload, retry: false, timeoutMs: 45000 });
  }

  function verify(bookingId) {
    return api("/verify", {
      method: "POST",
      body: bookingId ? { bookingId: bookingId } : {},
      retry: true,
    });
  }

  /** Verify via order + access token (after Fawaterk redirect; no Bearer needed). */
  function verifyByAccess(orderCode, accessToken) {
    var access =
      accessToken ||
      (typeof window !== "undefined"
        ? new URLSearchParams(window.location.search).get("access")
        : "") ||
      "";
    try {
      if (!access) access = sessionStorage.getItem("ecd2026_access") || "";
    } catch (e) {}
    return api("/booking/" + encodeURIComponent(orderCode) + "/verify-payment", {
      method: "POST",
      body: { access: access },
      token: "",
      retry: true,
    }).then(function (data) {
      try {
        if (data && data.access) {
          sessionStorage.setItem("ecd2026_access", data.access);
        }
      } catch (e) {}
      return data;
    });
  }

  function fetchBooking(orderCode, publicToken, accessToken) {
    var token = getToken();
    var q = publicToken || getPublicToken();
    var access =
      accessToken ||
      (typeof window !== "undefined"
        ? new URLSearchParams(window.location.search).get("access")
        : "") ||
      "";
    try {
      if (!access) access = sessionStorage.getItem("ecd2026_access") || "";
    } catch (e) {}
    // When URL/session has a booking access token, prefer it as the auth path.
    // Skip stale checkout Bearer so a leftover session cannot block the GET.
    var useBearer = access ? "" : token || "";
    var path = "/booking/" + encodeURIComponent(orderCode);
    var qs = [];
    if (q) qs.push("publicToken=" + encodeURIComponent(q));
    if (access) qs.push("access=" + encodeURIComponent(access));
    if (qs.length) path += "?" + qs.join("&");
    return api(path, { token: useBearer }).then(function (data) {
      try {
        if (access) sessionStorage.setItem("ecd2026_access", access);
      } catch (e) {}
      return data;
    });
  }

  function fetchMyBooking() {
    return api("/me/booking");
  }

  /** Public CMS payload: partners, speakers, packages (ct/fj). */
  function fetchContent() {
    return api("/content", { token: "" });
  }

  /**
   * Persist FJ workshop picks for a paid booking.
   * Auth: Bearer checkout token and/or publicToken / access query.
   */
  function reserveWorkshops(orderCode, sessionSlugs) {
    var q = getPublicToken();
    var access = "";
    try {
      access = sessionStorage.getItem("ecd2026_access") || "";
    } catch (e) {}
    if (!access && typeof window !== "undefined") {
      access = new URLSearchParams(window.location.search).get("access") || "";
    }
    var path = "/booking/" + encodeURIComponent(orderCode) + "/workshops";
    var qs = [];
    if (q) qs.push("publicToken=" + encodeURIComponent(q));
    if (access) qs.push("access=" + encodeURIComponent(access));
    if (qs.length) path += "?" + qs.join("&");
    return api(path, {
      method: "POST",
      body: { sessionSlugs: sessionSlugs || [] },
    });
  }

  /** Upload composited attending-frame image as multipart (avoids 1MB JSON limit). */
  function uploadAttendeeFrame(orderCode, imageDataUrl, accessToken) {
    var q = getPublicToken();
    var access =
      accessToken ||
      (typeof window !== "undefined"
        ? new URLSearchParams(window.location.search).get("access")
        : "") ||
      "";
    try {
      if (!access) access = sessionStorage.getItem("ecd2026_access") || "";
    } catch (e) {}
    var path = "/booking/" + encodeURIComponent(orderCode) + "/attendee-frame";
    var qs = [];
    if (q) qs.push("publicToken=" + encodeURIComponent(q));
    if (access) qs.push("access=" + encodeURIComponent(access));
    if (qs.length) path += "?" + qs.join("&");

    var form = new FormData();
    var blob = dataUrlToBlob(imageDataUrl);
    var ext = (blob.type || "image/jpeg").indexOf("png") >= 0 ? "png" : "jpg";
    form.append("file", blob, "attending." + ext);

    var headers = {};
    var token = getToken();
    if (token) headers.Authorization = "Bearer " + token;

    return requestOnce(
      CONFIG.API_BASE + path,
      {
        method: "POST",
        headers: headers,
        body: form,
        credentials: "omit",
      },
      90000,
    );
  }

  function dataUrlToBlob(dataUrl) {
    var parts = String(dataUrl || "").split(",");
    var mimeMatch = parts[0] && parts[0].match(/:(.*?);/);
    var mime = (mimeMatch && mimeMatch[1]) || "image/jpeg";
    var binary = atob(parts[1] || "");
    var len = binary.length;
    var bytes = new Uint8Array(len);
    for (var i = 0; i < len; i++) bytes[i] = binary.charCodeAt(i);
    return new Blob([bytes], { type: mime });
  }

  /** Partnership inquiry from become-a-sponsor.html */
  function submitSponsorInquiry(payload) {
    return api("/sponsor-inquiries", {
      method: "POST",
      body: payload,
      token: "",
    });
  }

  function buildIcs(event) {
    event = event || CONFIG.EVENT;
    function fmt(iso) {
      var d = new Date(iso);
      return (
        d.getUTCFullYear() +
        pad(d.getUTCMonth() + 1) +
        pad(d.getUTCDate()) +
        "T" +
        pad(d.getUTCHours()) +
        pad(d.getUTCMinutes()) +
        pad(d.getUTCSeconds()) +
        "Z"
      );
    }
    function pad(n) {
      return String(n).padStart(2, "0");
    }
    var uid = "ecd26-" + Date.now() + "@trafficmena.com";
    return [
      "BEGIN:VCALENDAR",
      "VERSION:2.0",
      "PRODID:-//TrafficMENA//ECommerce Day 2026//EN",
      "CALSCALE:GREGORIAN",
      "METHOD:PUBLISH",
      "BEGIN:VEVENT",
      "UID:" + uid,
      "DTSTAMP:" + fmt(new Date().toISOString()),
      "DTSTART:" + fmt(event.startIso),
      "DTEND:" + fmt(event.endIso),
      "SUMMARY:" + (event.title || CONFIG.EVENT.title),
      "LOCATION:" + (event.location || CONFIG.EVENT.location),
      "DESCRIPTION:ECommerce Day 2026 by TrafficMENA",
      "END:VEVENT",
      "END:VCALENDAR",
    ].join("\r\n");
  }

  function downloadIcs(event) {
    var ics = buildIcs(event);
    var blob = new Blob([ics], { type: "text/calendar;charset=utf-8" });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url;
    a.download = "ecommerce-day-2026.ics";
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }

  function centsFromPricesJs(ticketId, qty, promoCode) {
    if (!global.EventPrices) return null;
    var totals = global.EventPrices.calcTotals(ticketId, qty, promoCode);
    if (!totals || totals.total == null) return null;
    return Math.round(Number(totals.total) * 100);
  }

  function clearSession() {
    try {
      sessionStorage.removeItem(CONFIG.STORAGE_TOKEN);
      sessionStorage.removeItem(CONFIG.STORAGE_PUBLIC);
      sessionStorage.removeItem(CONFIG.STORAGE_BOOKING);
    } catch (e) {}
  }

  global.EcdApi = {
    CONFIG: CONFIG,
    createSession: createSession,
    validatePromo: validatePromo,
    fetchPaymentMethods: fetchPaymentMethods,
    pay: pay,
    verify: verify,
    verifyByAccess: verifyByAccess,
    fetchBooking: fetchBooking,
    fetchMyBooking: fetchMyBooking,
    getToken: getToken,
    getPublicToken: getPublicToken,
    getStoredBooking: getStoredBooking,
    setSession: setSession,
    clearSession: clearSession,
    buildIcs: buildIcs,
    downloadIcs: downloadIcs,
    centsFromPricesJs: centsFromPricesJs,
    fetchContent: fetchContent,
    reserveWorkshops: reserveWorkshops,
    uploadAttendeeFrame: uploadAttendeeFrame,
    submitSponsorInquiry: submitSponsorInquiry,
  };
})(window);
