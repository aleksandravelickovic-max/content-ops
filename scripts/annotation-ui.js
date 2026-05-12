// ═══════════════════════════════════════════════════════════════════
// Content Navigator — Annotation System
// ═══════════════════════════════════════════════════════════════════
(function () {
  "use strict";

  var API_BASE = window.location.origin;
  var AUTHOR_KEY = "contentops_annotation_author";
  var apiAvailable = false;
  var annotationMode = false;
  var annotationsByDoc = {};
  var currentDocKey = null;
  var popoverEl = null;
  var tooltipEl = null;
  var pendingAnchor = null;

  // ── API Layer ────────────────────────────────────────────────────

  function checkApi() {
    return fetch(API_BASE + "/api/health")
      .then(function (r) {
        return r.ok;
      })
      .catch(function () {
        return false;
      });
  }

  function apiFetch(path, opts) {
    opts = opts || {};
    opts.headers = Object.assign({ "Content-Type": "application/json" }, opts.headers || {});
    return fetch(API_BASE + path, opts).then(function (r) {
      if (r.status === 204) return null;
      if (!r.ok) return r.json().then(function (e) { throw new Error(e.detail || r.statusText); });
      return r.json();
    });
  }

  function loadAnnotations(docKey) {
    return apiFetch("/api/annotations?document_key=" + encodeURIComponent(docKey))
      .then(function (data) {
        annotationsByDoc[docKey] = data || [];
        return annotationsByDoc[docKey];
      })
      .catch(function () {
        annotationsByDoc[docKey] = annotationsByDoc[docKey] || [];
        return annotationsByDoc[docKey];
      });
  }

  // ── Anchor Extraction ────────────────────────────────────────────

  function extractAnchor(range) {
    var exact = range.toString();
    if (!exact.trim()) return null;

    var previewBody = document.getElementById("previewBody");
    var fullText = previewBody.textContent;

    var walker = document.createTreeWalker(previewBody, NodeFilter.SHOW_TEXT);
    var offset = 0;
    var startOffset = 0;
    while (walker.nextNode()) {
      if (walker.currentNode === range.startContainer) {
        startOffset = offset + range.startOffset;
        break;
      }
      offset += walker.currentNode.textContent.length;
    }
    var endOffset = startOffset + exact.length;

    var prefixStart = Math.max(0, startOffset - 40);
    var prefix = fullText.substring(prefixStart, startOffset);
    var suffix = fullText.substring(endOffset, endOffset + 40);

    var heading = null;
    var paragraphIndex = 0;
    var node = range.startContainer;
    while (node && node !== previewBody) {
      if (node.previousElementSibling) {
        var sib = node.previousElementSibling;
        while (sib) {
          if (/^H[1-6]$/.test(sib.tagName)) {
            heading = sib.textContent.trim();
            break;
          }
          if (sib.tagName === "P") paragraphIndex++;
          sib = sib.previousElementSibling;
        }
        if (heading) break;
      }
      node = node.parentNode;
    }

    return {
      anchor_exact: exact.substring(0, 500),
      anchor_prefix: prefix,
      anchor_suffix: suffix,
      anchor_start_offset: startOffset,
      anchor_end_offset: endOffset,
      anchor_heading: heading,
      anchor_paragraph_index: paragraphIndex,
    };
  }

  // ── Re-anchoring ─────────────────────────────────────────────────

  function findTextInDom(container, exact, prefix, suffix) {
    var text = container.textContent;
    var searchFrom = 0;
    var bestIndex = -1;
    var idx = text.indexOf(exact, searchFrom);

    if (idx === -1) return null;

    if (!prefix && !suffix) {
      bestIndex = idx;
    } else {
      var bestScore = -1;
      while (idx !== -1) {
        var score = 0;
        if (prefix) {
          var before = text.substring(Math.max(0, idx - prefix.length), idx);
          if (before === prefix) score += 2;
          else if (before.indexOf(prefix.substring(prefix.length - 10)) !== -1) score += 1;
        }
        if (suffix) {
          var after = text.substring(idx + exact.length, idx + exact.length + suffix.length);
          if (after === suffix) score += 2;
          else if (after.indexOf(suffix.substring(0, 10)) !== -1) score += 1;
        }
        if (score > bestScore) {
          bestScore = score;
          bestIndex = idx;
        }
        idx = text.indexOf(exact, idx + 1);
      }
    }

    if (bestIndex === -1) return null;
    return textOffsetToRange(container, bestIndex, bestIndex + exact.length);
  }

  function textOffsetToRange(container, startOff, endOff) {
    var walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT);
    var current = 0;
    var startNode = null, startLocal = 0;
    var endNode = null, endLocal = 0;

    while (walker.nextNode()) {
      var node = walker.currentNode;
      var len = node.textContent.length;
      if (!startNode && current + len > startOff) {
        startNode = node;
        startLocal = startOff - current;
      }
      if (!endNode && current + len >= endOff) {
        endNode = node;
        endLocal = endOff - current;
        break;
      }
      current += len;
    }
    if (!startNode || !endNode) return null;
    try {
      var range = document.createRange();
      range.setStart(startNode, startLocal);
      range.setEnd(endNode, endLocal);
      return range;
    } catch (e) {
      return null;
    }
  }

  // ── Inline Highlights ────────────────────────────────────────────

  function renderHighlights() {
    clearHighlights();
    var anns = annotationsByDoc[currentDocKey] || [];
    if (!anns.length) return;

    var container = document.getElementById("previewBody");
    var rendered = [];

    for (var i = 0; i < anns.length; i++) {
      var ann = anns[i];
      if (!ann.anchor_exact) continue;
      var range = findTextInDom(container, ann.anchor_exact, ann.anchor_prefix, ann.anchor_suffix);
      if (!range) continue;

      try {
        var span = document.createElement("span");
        span.className = "ann-highlight" + (ann.status === "resolved" ? " resolved" : "");
        span.dataset.annId = ann.id;
        span.title = ann.author + ": " + ann.comment.substring(0, 80);

        var badge = document.createElement("span");
        badge.className = "ann-num";
        badge.textContent = String(i + 1);

        range.surroundContents(span);
        span.appendChild(badge);
        rendered.push(ann.id);

        span.addEventListener("click", (function (id) {
          return function (e) {
            e.stopPropagation();
            scrollToSidebarCard(id);
          };
        })(ann.id));
      } catch (e) {
        // surroundContents fails if range crosses element boundaries
      }
    }
    return rendered;
  }

  function clearHighlights() {
    var container = document.getElementById("previewBody");
    var spans = container.querySelectorAll(".ann-highlight");
    for (var i = 0; i < spans.length; i++) {
      var span = spans[i];
      var badge = span.querySelector(".ann-num");
      if (badge) badge.remove();
      var parent = span.parentNode;
      while (span.firstChild) parent.insertBefore(span.firstChild, span);
      parent.removeChild(span);
      parent.normalize();
    }
  }

  // ── Selection Tooltip ────────────────────────────────────────────

  function showTooltip(rect) {
    hideTooltip();
    tooltipEl = document.createElement("div");
    tooltipEl.className = "ann-sel-tooltip";
    tooltipEl.textContent = "Add Comment";

    var pane = document.getElementById("previewPane");
    var paneRect = pane.getBoundingClientRect();
    var body = document.getElementById("previewBody");
    var bodyRect = body.getBoundingClientRect();

    tooltipEl.style.left = (rect.left + rect.width / 2 - paneRect.left) + "px";
    tooltipEl.style.top = (rect.top - paneRect.top - 35 + pane.querySelector('.preview-body').scrollTop - body.scrollTop) + "px";

    pane.style.position = "relative";
    pane.appendChild(tooltipEl);

    tooltipEl.addEventListener("mousedown", function (e) {
      e.preventDefault();
      e.stopPropagation();
      showPopover(rect);
    });
  }

  function hideTooltip() {
    if (tooltipEl && tooltipEl.parentNode) {
      tooltipEl.parentNode.removeChild(tooltipEl);
    }
    tooltipEl = null;
  }

  // ── Comment Popover ──────────────────────────────────────────────

  function showPopover(rect) {
    hideTooltip();
    hidePopover();

    if (!pendingAnchor) return;

    popoverEl = document.createElement("div");
    popoverEl.className = "ann-popover";

    var savedAuthor = localStorage.getItem(AUTHOR_KEY) || "";
    var quotedText = pendingAnchor.anchor_exact;
    if (quotedText.length > 120) quotedText = quotedText.substring(0, 120) + "...";

    popoverEl.innerHTML =
      '<div class="ann-popover-quote">"' + escapeHtml(quotedText) + '"</div>' +
      '<label>Your Name</label>' +
      '<input type="text" id="annAuthor" value="' + escapeHtml(savedAuthor) + '" placeholder="e.g. Sarah (Zia Tile)">' +
      '<label>Comment</label>' +
      '<textarea id="annComment" placeholder="What should change here?"></textarea>' +
      '<div class="ann-char-count"><span id="annCharCount">0</span> / 500</div>' +
      '<div class="ann-popover-actions">' +
      '  <button onclick="window._annCancel()">Cancel</button>' +
      '  <button class="ann-save" onclick="window._annSave()">Save</button>' +
      '</div>';

    var pane = document.getElementById("previewPane");
    var paneRect = pane.getBoundingClientRect();
    popoverEl.style.left = Math.max(10, Math.min(rect.left - paneRect.left - 100, paneRect.width - 340)) + "px";
    popoverEl.style.top = (rect.bottom - paneRect.top + 10 + pane.querySelector('.preview-body').scrollTop - document.getElementById("previewBody").scrollTop) + "px";

    pane.appendChild(popoverEl);

    var ta = document.getElementById("annComment");
    ta.focus();
    ta.addEventListener("input", function () {
      document.getElementById("annCharCount").textContent = ta.value.length;
    });

    var authorInput = document.getElementById("annAuthor");
    authorInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        ta.focus();
      }
    });
    ta.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        window._annSave();
      }
    });
  }

  function hidePopover() {
    if (popoverEl && popoverEl.parentNode) {
      popoverEl.parentNode.removeChild(popoverEl);
    }
    popoverEl = null;
    pendingAnchor = null;
  }

  window._annCancel = function () { hidePopover(); };

  window._annSave = function () {
    var author = (document.getElementById("annAuthor").value || "").trim();
    var comment = (document.getElementById("annComment").value || "").trim();
    if (!author || !comment) return;
    if (comment.length > 500) { comment = comment.substring(0, 500); }

    localStorage.setItem(AUTHOR_KEY, author);

    var clientMatch = currentDocKey.match(/^clients\/([^/]+)\//);
    var client = clientMatch ? clientMatch[1] : "unknown";

    var payload = Object.assign({
      document_key: currentDocKey,
      client: client,
      author: author,
      comment: comment,
    }, pendingAnchor);

    hidePopover();

    apiFetch("/api/annotations", {
      method: "POST",
      body: JSON.stringify(payload),
    }).then(function (created) {
      if (!annotationsByDoc[currentDocKey]) annotationsByDoc[currentDocKey] = [];
      annotationsByDoc[currentDocKey].push(created);
      renderHighlights();
      renderSidebar();
    }).catch(function (err) {
      alert("Failed to save annotation: " + err.message);
    });
  };

  // ── Sidebar ──────────────────────────────────────────────────────

  function renderSidebar() {
    var sidebar = document.getElementById("annotationSidebar");
    var toggle = document.getElementById("annSidebarToggle");
    if (!sidebar || !toggle) return;

    var anns = annotationsByDoc[currentDocKey] || [];
    var openCount = anns.filter(function (a) { return a.status === "open"; }).length;
    var total = anns.length;

    toggle.querySelector(".ann-count").textContent = openCount + " open" + (total > openCount ? ", " + (total - openCount) + " resolved" : "");
    toggle.style.display = total > 0 || annotationMode ? "" : "none";

    if (!total) {
      sidebar.innerHTML = '<div class="ann-empty">No annotations yet. ' +
        (annotationMode ? 'Highlight text to add one.' : 'Enable annotation mode to start.') + '</div>';
      return;
    }

    var html = "";
    for (var i = 0; i < anns.length; i++) {
      var a = anns[i];
      var time = formatTime(a.created_at);
      var statusCls = a.status === "resolved" ? "resolved" : "";
      var quote = a.anchor_exact ? a.anchor_exact.substring(0, 60) : "";
      if (a.anchor_exact && a.anchor_exact.length > 60) quote += "...";

      html += '<div class="ann-card ' + statusCls + '" data-ann-id="' + a.id + '" onclick="window._annScrollTo(\'' + a.id + '\')">';
      html += '<div class="ann-card-header">';
      html += '<span class="ann-card-num">' + (i + 1) + '</span>';
      html += '<span class="ann-card-author">' + escapeHtml(a.author) + '</span>';
      html += '<span class="ann-status ann-status-' + a.status + '">' + a.status + '</span>';
      html += '<span class="ann-card-time">' + time + '</span>';
      html += '</div>';
      if (quote) html += '<div class="ann-card-quote">"' + escapeHtml(quote) + '"</div>';
      html += '<div class="ann-card-comment">' + escapeHtml(a.comment) + '</div>';

      // Replies
      if (a.replies && a.replies.length) {
        html += '<div class="ann-replies">';
        for (var r = 0; r < a.replies.length; r++) {
          var rep = a.replies[r];
          html += '<div class="ann-reply"><span class="ann-reply-author">' + escapeHtml(rep.author) + '</span> ';
          html += escapeHtml(rep.comment);
          html += ' <span class="ann-reply-time">' + formatTime(rep.created_at) + '</span></div>';
        }
        html += '</div>';
      }

      html += '<div class="ann-card-actions">';
      if (a.status === "open") {
        html += '<button onclick="event.stopPropagation(); window._annResolve(\'' + a.id + '\')">Resolve</button>';
      } else {
        html += '<button onclick="event.stopPropagation(); window._annReopen(\'' + a.id + '\')">Reopen</button>';
      }
      html += '<button onclick="event.stopPropagation(); window._annReply(\'' + a.id + '\', this)">Reply</button>';
      html += '<button class="danger" onclick="event.stopPropagation(); window._annDelete(\'' + a.id + '\')">Delete</button>';
      html += '</div>';
      html += '</div>';
    }
    sidebar.innerHTML = html;
  }

  function scrollToSidebarCard(id) {
    var sidebar = document.getElementById("annotationSidebar");
    if (!sidebar.classList.contains("open")) {
      sidebar.classList.add("open");
      document.getElementById("annSidebarToggle").classList.add("open");
    }
    var card = sidebar.querySelector('[data-ann-id="' + id + '"]');
    if (card) {
      sidebar.querySelectorAll(".ann-card").forEach(function (c) { c.classList.remove("active"); });
      card.classList.add("active");
      card.scrollIntoView({ block: "nearest", behavior: "smooth" });
    }
  }

  window._annScrollTo = function (id) {
    var highlight = document.querySelector('.ann-highlight[data-ann-id="' + id + '"]');
    if (highlight) {
      highlight.scrollIntoView({ block: "center", behavior: "smooth" });
      highlight.style.outline = "2px solid var(--accent)";
      setTimeout(function () { highlight.style.outline = ""; }, 1500);
    }
  };

  window._annResolve = function (id) {
    apiFetch("/api/annotations/" + id, {
      method: "PATCH",
      body: JSON.stringify({ status: "resolved", resolved_by: localStorage.getItem(AUTHOR_KEY) || "team" }),
    }).then(function () {
      return loadAnnotations(currentDocKey);
    }).then(function () {
      renderHighlights();
      renderSidebar();
    });
  };

  window._annReopen = function (id) {
    apiFetch("/api/annotations/" + id, {
      method: "PATCH",
      body: JSON.stringify({ status: "open" }),
    }).then(function () {
      return loadAnnotations(currentDocKey);
    }).then(function () {
      renderHighlights();
      renderSidebar();
    });
  };

  window._annDelete = function (id) {
    if (!confirm("Delete this annotation?")) return;
    apiFetch("/api/annotations/" + id, { method: "DELETE" }).then(function () {
      annotationsByDoc[currentDocKey] = (annotationsByDoc[currentDocKey] || []).filter(function (a) { return a.id !== id; });
      renderHighlights();
      renderSidebar();
    });
  };

  window._annReply = function (id, btn) {
    var card = btn.closest(".ann-card");
    if (card.querySelector(".ann-reply-form")) return;
    var form = document.createElement("div");
    form.className = "ann-reply-form";
    form.innerHTML = '<input type="text" placeholder="Reply..." id="replyInput_' + id + '">' +
      '<button onclick="window._annSendReply(\'' + id + '\')">Send</button>';
    card.appendChild(form);
    form.querySelector("input").focus();
    form.querySelector("input").addEventListener("keydown", function (e) {
      if (e.key === "Enter") window._annSendReply(id);
    });
  };

  window._annSendReply = function (id) {
    var input = document.getElementById("replyInput_" + id);
    if (!input) return;
    var text = input.value.trim();
    if (!text) return;
    var author = localStorage.getItem(AUTHOR_KEY) || "Anonymous";
    apiFetch("/api/annotations/" + id + "/replies", {
      method: "POST",
      body: JSON.stringify({ author: author, comment: text }),
    }).then(function () {
      return loadAnnotations(currentDocKey);
    }).then(function () {
      renderSidebar();
    });
  };

  // ── Helpers ──────────────────────────────────────────────────────

  function escapeHtml(t) {
    var d = document.createElement("div");
    d.textContent = t;
    return d.innerHTML;
  }

  function formatTime(iso) {
    if (!iso) return "";
    var d = new Date(iso);
    var now = new Date();
    var diff = (now - d) / 1000;
    if (diff < 60) return "just now";
    if (diff < 3600) return Math.floor(diff / 60) + "m ago";
    if (diff < 86400) return Math.floor(diff / 3600) + "h ago";
    if (diff < 604800) return Math.floor(diff / 86400) + "d ago";
    return d.toLocaleDateString();
  }

  // ── Mode Toggle ──────────────────────────────────────────────────

  function toggleMode() {
    annotationMode = !annotationMode;
    var btn = document.getElementById("annToggle");
    var banner = document.getElementById("annBanner");
    if (annotationMode) {
      btn.classList.add("active");
      banner.classList.add("visible");
      document.body.classList.add("annotation-mode");
    } else {
      btn.classList.remove("active");
      banner.classList.remove("visible");
      document.body.classList.remove("annotation-mode");
      hideTooltip();
      hidePopover();
    }
    renderSidebar();
  }
  window._annToggleMode = toggleMode;

  // ── Selection Handler ────────────────────────────────────────────

  function onPreviewMouseUp(e) {
    if (!annotationMode) return;
    if (e.target.closest(".ann-popover") || e.target.closest(".ann-sel-tooltip")) return;

    hideTooltip();

    var sel = window.getSelection();
    if (!sel || sel.isCollapsed || !sel.toString().trim()) return;

    var range = sel.getRangeAt(0);
    var previewBody = document.getElementById("previewBody");
    if (!previewBody.contains(range.commonAncestorContainer)) return;

    pendingAnchor = extractAnchor(range);
    if (!pendingAnchor) return;

    var rect = range.getBoundingClientRect();
    showTooltip(rect);
  }

  // ── Hook Into Navigator ──────────────────────────────────────────

  function hookNavigator() {
    var origOpen = window.openPreview;
    window.openPreview = function (key) {
      origOpen(key);
      currentDocKey = key;
      if (apiAvailable) {
        loadAnnotations(key).then(function () {
          renderHighlights();
          renderSidebar();
        });
      }
    };

    var origClose = window.closePreview;
    window.closePreview = function () {
      clearHighlights();
      currentDocKey = null;
      origClose();
    };
  }

  // ── Toggle Sidebar ───────────────────────────────────────────────

  window._annToggleSidebar = function () {
    var sidebar = document.getElementById("annotationSidebar");
    var toggle = document.getElementById("annSidebarToggle");
    sidebar.classList.toggle("open");
    toggle.classList.toggle("open");
  };

  // ── Init ─────────────────────────────────────────────────────────

  function init() {
    checkApi().then(function (ok) {
      apiAvailable = ok;

      var offlineEl = document.getElementById("annOffline");
      if (offlineEl) {
        if (!ok) offlineEl.classList.add("visible");
        else offlineEl.classList.remove("visible");
      }

      var toggleBtn = document.getElementById("annToggle");
      if (toggleBtn) {
        if (!ok) {
          toggleBtn.style.opacity = "0.4";
          toggleBtn.title = "Start the annotation server to enable commenting";
        } else {
          toggleBtn.style.opacity = "1";
          toggleBtn.title = "Toggle annotation mode";
        }
      }
    });

    var previewBody = document.getElementById("previewBody");
    if (previewBody) {
      previewBody.addEventListener("mouseup", onPreviewMouseUp);
    }

    hookNavigator();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    setTimeout(init, 0);
  }
})();
