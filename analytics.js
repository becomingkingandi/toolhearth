(function () {
  "use strict";

  window.va = window.va || function () {
    (window.vaq = window.vaq || []).push(arguments);
  };

  document.addEventListener("click", function (event) {
    var link = event.target.closest("a[href]");
    var button = event.target.closest("button, input[type='submit']");

    if (button) {
      window.va("event", {
        name: "tool_action",
        data: {
          action: button.id || button.name || (button.textContent || button.value || "button").trim().slice(0, 60),
          page: window.location.pathname
        }
      });
    }

    if (!link) return;

    if (link.dataset.commercialCta) {
      window.va("event", {
        name: "commercial_cta_click",
        data: {
          destination: link.dataset.commercialCta,
          page: window.location.pathname
        }
      });
    }

    var isAffiliate =
      (link.rel || "").split(/\s+/).includes("sponsored") ||
      Boolean(link.closest(".affiliate, .affiliate-box")) ||
      Boolean(link.dataset.affiliate);

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
