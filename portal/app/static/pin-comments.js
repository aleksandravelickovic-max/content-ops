/* ── Pin-based commenting for Compare View ────────────────── */
(function () {
  "use strict";

  var TOKEN = window.PIN_TOKEN || "";
  var FILENAME = window.PIN_FILENAME || "";
  var REVIEWER_NAME = window.PIN_REVIEWER_NAME || "";
  var CONTENT_PATH = "compare:" + FILENAME;
  var pinsData = [];
  var popoverEl = null;
  var pendingPin = null;
  var sidebarVisible = false;

  function loadComments() {
    fetch("/api/review/" + TOKEN + "/compare-comments/" + FILENAME)
      .then(function (res) { return res.ok ? res.json() : []; })
      .then(function (data) {
        pinsData = data;
        renderAllPins();
        renderSidebar();
      })
      .catch(function () {});
  }

  function renderAllPins() {
    document.querySelectorAll(".pin-bubble").forEach(function (el) { el.remove(); });

    for (var i = 0; i < pinsData.length; i++) {
      var c = pinsData[i];
      if (c.pin_x_percent == null || c.pin_y_percent == null) continue;
      renderPin(c, i + 1);
    }
  }

  function renderPin(comment, num) {
    var pane = findPane(comment.pin_pane);
    if (!pane) return;

    var scrollContainer = pane.querySelector(".compare-frame") || pane.querySelector(".draft-content") || pane;

    var bubble = document.createElement("div");
    bubble.className = "pin-bubble" + (comment.resolved ? " resolved" : "");
    bubble.dataset.commentId = comment.id;
    bubble.textContent = String(num);
    bubble.title = comment.author_name + ": " + comment.body.substring(0, 80);

    bubble.style.left = comment.pin_x_percent + "%";
    bubble.style.top = comment.pin_y_percent + "%";

    bubble.addEventListener("click", function (e) {
      e.stopPropagation();
      scrollToSidebarComment(comment.id);
    });

    pane.style.position = "relative";
    pane.appendChild(bubble);
  }

  function findPane(paneId) {
    if (paneId === "original") return document.querySelector(".pane-original");
    if (paneId === "draft") return document.querySelector(".pane-draft");
    if (paneId === "revised") return document.querySelector(".pane-revised");
    return null;
  }

  function identifyPane(el) {
    if (el.closest(".pane-original")) return "original";
    if (el.closest(".pane-draft")) return "draft";
    if (el.closest(".pane-revised")) return "revised";
    return null;
  }

  function onPaneClick(e) {
    if (e.target.closest(".pin-bubble")) return;
    if (e.target.closest(".pin-popover")) return;
    if (e.target.closest(".pane-label")) return;
    if (e.target.closest(".pane-not-processed")) return;
    if (e.target.tagName === "IFRAME") return;

    var paneId = identifyPane(e.target);
    if (!paneId) return;

    var pane = e.target.closest(".compare-pane");
    if (!pane) return;

    var rect = pane.getBoundingClientRect();
    var xPercent = ((e.clientX - rect.left) / rect.width) * 100;
    var yPercent = ((e.clientY - rect.top) / rect.height) * 100;

    xPercent = Math.max(2, Math.min(98, xPercent));
    yPercent = Math.max(2, Math.min(98, yPercent));

    showPinPopover(pane, xPercent, yPercent, paneId);
  }

  function showPinPopover(pane, xPercent, yPercent, paneId) {
    hidePinPopover();

    pendingPin = {
      pin_x_percent: Math.round(xPercent * 100) / 100,
      pin_y_percent: Math.round(yPercent * 100) / 100,
      pin_pane: paneId,
    };

    var nameField = REVIEWER_NAME
      ? '<input type="hidden" name="author_name" value="' + escapeHtml(REVIEWER_NAME) + '">'
      : '<input type="text" name="author_name" placeholder="Your name" required class="pin-popover-input">';

    popoverEl = document.createElement("div");
    popoverEl.className = "pin-popover";
    popoverEl.innerHTML =
      '<div class="pin-popover-header">Leave feedback on <strong>' + paneId + '</strong> pane</div>' +
      '<form class="pin-popover-form">' +
        nameField +
        '<textarea name="body" placeholder="Your feedback..." required class="pin-popover-textarea" rows="3"></textarea>' +
        '<div class="pin-popover-actions">' +
          '<button type="button" class="pin-popover-cancel">Cancel</button>' +
          '<button type="submit" class="pin-popover-submit">Submit</button>' +
        '</div>' +
      '</form>';

    popoverEl.style.left = xPercent + "%";
    popoverEl.style.top = yPercent + "%";

    pane.style.position = "relative";
    pane.appendChild(popoverEl);

    popoverEl.querySelector(".pin-popover-cancel").addEventListener("click", hidePinPopover);
    popoverEl.querySelector(".pin-popover-form").addEventListener("submit", function (e) {
      e.preventDefault();
      submitPinComment(this);
    });
    popoverEl.addEventListener("mousedown", function (e) { e.stopPropagation(); });
    popoverEl.addEventListener("click", function (e) { e.stopPropagation(); });

    setTimeout(function () {
      var input = popoverEl && (popoverEl.querySelector('textarea[name="body"]') || popoverEl.querySelector('input[name="author_name"]'));
      if (input) input.focus();
    }, 50);
  }

  function hidePinPopover() {
    if (popoverEl && popoverEl.parentNode) popoverEl.parentNode.removeChild(popoverEl);
    popoverEl = null;
    pendingPin = null;
  }

  function submitPinComment(form) {
    var data = {
      author_name: form.author_name.value,
      body: form.body.value,
    };
    if (pendingPin) Object.assign(data, pendingPin);

    var submitBtn = form.querySelector(".pin-popover-submit");
    if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = "Saving..."; }

    fetch("/api/review/" + TOKEN + "/comments/" + encodeURIComponent(CONTENT_PATH), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    }).then(function (res) {
      if (res.ok) {
        hidePinPopover();
        loadComments();
      } else {
        if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = "Submit"; }
        res.json().then(function (err) { alert(err.detail || "Failed to submit"); });
      }
    }).catch(function () {
      if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = "Submit"; }
      alert("Network error.");
    });
  }

  function escapeHtml(str) {
    var div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  // ── Sidebar ──────────────────────────────────────────────

  function renderSidebar() {
    var sidebar = document.getElementById("pinSidebar");
    if (!sidebar) return;

    var list = sidebar.querySelector(".pin-sidebar-list");
    if (!list) return;

    list.innerHTML = "";

    if (pinsData.length === 0) {
      list.innerHTML = '<div class="pin-sidebar-empty">Click anywhere on a pane to leave feedback.</div>';
      updateBadge(0);
      return;
    }

    updateBadge(pinsData.length);

    for (var i = 0; i < pinsData.length; i++) {
      var c = pinsData[i];
      var card = document.createElement("div");
      card.className = "pin-sidebar-comment" + (c.resolved ? " resolved" : "");
      card.dataset.commentId = c.id;

      var paneLabel = c.pin_pane ? c.pin_pane.charAt(0).toUpperCase() + c.pin_pane.slice(1) : "Unknown";
      card.innerHTML =
        '<div class="pin-sidebar-comment-header">' +
          '<span class="pin-sidebar-num">' + (i + 1) + '</span>' +
          '<strong>' + escapeHtml(c.author_name) + '</strong>' +
          '<span class="pin-sidebar-pane">' + paneLabel + '</span>' +
        '</div>' +
        '<div class="pin-sidebar-comment-body">' + escapeHtml(c.body) + '</div>' +
        (c.resolved ? '<span class="pin-sidebar-resolved">Resolved</span>' : '');

      card.addEventListener("click", (function (comment) {
        return function () { flashPin(comment.id); };
      })(c));

      list.appendChild(card);
    }
  }

  function updateBadge(count) {
    var badge = document.querySelector(".pin-sidebar-badge");
    if (badge) badge.textContent = String(count);
  }

  function scrollToSidebarComment(id) {
    if (!sidebarVisible) toggleSidebar();
    var card = document.querySelector('.pin-sidebar-comment[data-comment-id="' + id + '"]');
    if (card) {
      card.scrollIntoView({ block: "center", behavior: "smooth" });
      card.style.outline = "2px solid var(--accent)";
      setTimeout(function () { card.style.outline = ""; }, 2000);
    }
  }

  function flashPin(id) {
    var bubble = document.querySelector('.pin-bubble[data-comment-id="' + id + '"]');
    if (bubble) {
      bubble.scrollIntoView({ block: "center", behavior: "smooth" });
      bubble.classList.add("pin-flash");
      setTimeout(function () { bubble.classList.remove("pin-flash"); }, 1500);
    }
  }

  function toggleSidebar() {
    var sidebar = document.getElementById("pinSidebar");
    if (!sidebar) return;
    sidebarVisible = !sidebarVisible;
    sidebar.classList.toggle("open", sidebarVisible);
  }

  // ── Init ────────────────────────────────────────────────

  function init() {
    if (!TOKEN || !FILENAME) return;

    injectSidebar();

    document.querySelectorAll(".compare-pane").forEach(function (pane) {
      pane.addEventListener("click", onPaneClick);
    });

    document.addEventListener("mousedown", function (e) {
      if (popoverEl && !popoverEl.contains(e.target) && !e.target.closest(".pin-bubble")) {
        hidePinPopover();
      }
    });

    loadComments();
  }

  function injectSidebar() {
    var sidebar = document.createElement("div");
    sidebar.id = "pinSidebar";
    sidebar.className = "pin-sidebar";
    sidebar.innerHTML =
      '<div class="pin-sidebar-header">' +
        '<h3>Feedback <span class="pin-sidebar-badge">0</span></h3>' +
        '<button class="pin-sidebar-close" title="Close">&times;</button>' +
      '</div>' +
      '<div class="pin-sidebar-list"></div>';

    document.body.appendChild(sidebar);

    sidebar.querySelector(".pin-sidebar-close").addEventListener("click", toggleSidebar);

    var toggleBtn = document.createElement("button");
    toggleBtn.className = "pin-sidebar-toggle";
    toggleBtn.innerHTML = '&#128172; <span class="pin-sidebar-badge">0</span>';
    toggleBtn.addEventListener("click", toggleSidebar);
    document.body.appendChild(toggleBtn);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    setTimeout(init, 0);
  }
})();
