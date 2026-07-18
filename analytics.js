(function () {
  "use strict";

  window.va = window.va || function () {
    (window.vaq = window.vaq || []).push(arguments);
  };

  document.addEventListener("click", function (event) {
    var link = event.target.closest("a[href]");
    if (!link) return;

    var isAffiliate =
      (link.rel || "").split(/\s+/).includes("sponsored") ||
      Boolean(link.closest(".affiliate, .affiliate-box"));

    if (isAffiliate) {
      var destination;
      try {
        destination = new URL(link.href, window.location.href).hostname;
      } catch (_) {
        destination = "unknown";
      }
      window.va("event", {
        name: "affiliate_click",
        data: { destination: destination, page: window.location.pathname }
      });
    }
  });

  var originalFetch = window.fetch;
  if (originalFetch) {
    window.fetch = async function () {
      var response = await originalFetch.apply(this, arguments);
      var request = arguments[0];
      var url = typeof request === "string" ? request : request && request.url;

      if (response.ok && url) {
        if (url.indexOf("/api/contact") !== -1) {
          window.va("event", { name: "contact_submission" });
        } else if (url.indexOf("/api/subscribe") !== -1) {
          window.va("event", { name: "newsletter_subscription" });
        }
      }

      return response;
    };
  }
})();
