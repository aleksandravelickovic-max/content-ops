/* ── Annotation system for Content Review Portal ─────────────── */
(function () {
  "use strict";

  var annotationMode = false;
  var pendingAnchor = null;
  var tooltipEl = null;
  var commentsData = window.COMMENTS_DATA || [];

  // ── Re-anchoring: find quoted text in rendered content ────────

  function findTextInDom(container, exact, prefix, suffix) {
    var text = container.textContent;
    var idx = text.indexOf(exact);
    if (idx === -1) return null;

    var bestIndex = -1;
    var bestScore = -1;
    while (idx !== -1) {
      var score = 0;
      if (prefix) {
        var before = text.substring(Math.max(0, idx - prefix.length), idx);
        if (before === prefix) score += 2;
        else if (before.indexOf(prefix.slice(-10)) !== -1) score += 1;
      }
      if (suffix) {
        var after = text.substring(idx + exact.length, idx + exact.length + suffix.length);
        if (after === suffix) score += 2;
        else if (after.indexOf(suffix.slice(0, 10)) !== -1) score += 1;
      }
      if (score > bestScore) { bestScore = score; bestIndex = idx; }
      idx = text.indexOf(exact, idx + 1);
    }
    if (bestIndex === -1) bestIndex = text.indexOf(exact);
    if (bestIndex === -1) return null;
    return textOffsetToRange(container, bestIndex, bestIndex + exact.length);
  }

  function textOffsetToRange(container, startOff, endOff) {
    var walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT);
    var current = 0, startNode = null, startLocal = 0, endNode = null, endLocal = 0;
    while (walker.nextNode()) {
      var node = walker.currentNode;
      var len = node.textContent.length;
      if (!startNode && current + len > startOff) { startNode = node; startLocal = startOff - current; }
      if (!endNode && current + len >= endOff) { endNode = node; endLocal = endOff - current; break; }
      current += len;
    }
    if (!startNode || !endNode) return null;
    try {
      var range = document.createRange();
      range.setStart(startNode, startLocal);
      range.setEnd(endNode, endLocal);
      return range;
    } catch (e) { return null; }
  }

  // ── Render inline highlights for existing comments ───────────

  function renderHighlights() {
    var container = document.querySelector(".rendered-content");
    if (!container) return;
    clearHighlights(container);

    var idx = 0;
    for (var i = 0; i < commentsData.length; i++) {
      var c = commentsData[i];
      if (!c.highlight_text) continue;
      idx++;

      var range = findTextInDom(container, c.highlight_text, c.anchor_prefix, c.anchor_suffix);
      if (!range) continue;

      try {
        var span = document.createElement("span");
        span.className = "ann-highlight" + (c.resolved ? " resolved" : "");
        span.dataset.commentId = c.id;
        span.title = c.author_name + ": " + c.body.substring(0, 80);

        var badge = document.createElement("span");
        badge.className = "ann-num";
        badge.textContent = String(idx);

        range.surroundContents(span);
        span.appendChild(badge);

        span.addEventListener("click", (function (id) {
          return function (e) {
            e.stopPropagation();
            scrollToComment(id);
          };
        })(c.id));
      } catch (e) {
        // surroundContents fails if range crosses element boundaries
      }
    }
  }

  function clearHighlights(container) {
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

  function scrollToComment(id) {
    var card = document.querySelector('.comment[data-id="' + id + '"]');
    if (card) {
      card.scrollIntoView({ block: "center", behavior: "smooth" });
      card.style.outline = "2px solid #2563eb";
      setTimeout(function () { card.style.outline = ""; }, 2000);
    }
  }

  // ── Anchor extraction from selection ─────────────────────────

  function extractAnchor(range) {
    var exact = range.toString();
    if (!exact.trim()) return null;

    var container = document.querySelector(".rendered-content");
    var fullText = container.textContent;

    var walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT);
    var offset = 0, startOffset = 0;
    while (walker.nextNode()) {
      if (walker.currentNode === range.startContainer) {
        startOffset = offset + range.startOffset;
        break;
      }
      offset += walker.currentNode.textContent.length;
    }
    var endOffset = startOffset + exact.length;

    var prefix = fullText.substring(Math.max(0, startOffset - 40), startOffset);
    var suffix = fullText.substring(endOffset, endOffset + 40);

    var heading = null;
    var paragraphIndex = 0;
    var node = range.startContainer;
    while (node && node !== container) {
      if (node.previousElementSibling) {
        var sib = node.previousElementSibling;
        while (sib) {
          if (/^H[1-6]$/.test(sib.tagName)) { heading = sib.textContent.trim(); break; }
          if (sib.tagName === "P") paragraphIndex++;
          sib = sib.previousElementSibling;
        }
        if (heading) break;
      }
      node = node.parentNode;
    }

    return {
      highlight_text: exact.substring(0, 500),
      anchor_prefix: prefix,
      anchor_suffix: suffix,
      anchor_start_offset: startOffset,
      anchor_end_offset: endOffset,
      anchor_heading: heading,
      anchor_paragraph_index: paragraphIndex,
    };
  }

  // ── Selection tooltip ────────────────────────────────────────

  function showTooltip(rect) {
    hideTooltip();
    tooltipEl = document.createElement("div");
    tooltipEl.className = "ann-sel-tooltip";
    tooltipEl.textContent = "Add Comment";

    var container = document.querySelector(".rendered-content");
    var containerRect = container.getBoundingClientRect();

    tooltipEl.style.left = (rect.left + rect.width / 2 - containerRect.left) + "px";
    tooltipEl.style.top = (rect.top - containerRect.top - 35 + container.scrollTop) + "px";

    container.style.position = "relative";
    container.appendChild(tooltipEl);

    tooltipEl.addEventListener("mousedown", function (e) {
      e.preventDefault();
      e.stopPropagation();
      applySelectionToForm();
    });
  }

  function hideTooltip() {
    if (tooltipEl && tooltipEl.parentNode) tooltipEl.parentNode.removeChild(tooltipEl);
    tooltipEl = null;
  }

  // ── Wire selection into existing comment form ────────────────

  function applySelectionToForm() {
    hideTooltip();
    if (!pendingAnchor) return;

    var quoteEl = document.getElementById("selectionQuote");
    var quoteText = document.getElementById("quoteText");
    if (quoteEl && quoteText) {
      var displayText = pendingAnchor.highlight_text;
      if (displayText.length > 120) displayText = displayText.substring(0, 120) + "...";
      quoteText.textContent = '"' + displayText + '"';
      quoteEl.classList.add("visible");
    }

    window._pendingAnchor = pendingAnchor;

    var textarea = document.querySelector('.comment-form textarea[name="body"]');
    if (textarea) textarea.focus();
  }

  window.clearTextSelection = function () {
    var quoteEl = document.getElementById("selectionQuote");
    if (quoteEl) quoteEl.classList.remove("visible");
    window._pendingAnchor = null;
    pendingAnchor = null;
  };

  // ── Annotation mode toggle ───────────────────────────────────

  window.toggleAnnotationMode = function () {
    annotationMode = !annotationMode;
    var btn = document.getElementById("annToggle");
    var banner = document.getElementById("annBanner");
    if (annotationMode) {
      btn.classList.add("active");
      if (banner) banner.classList.add("visible");
      document.body.classList.add("annotation-mode");
    } else {
      btn.classList.remove("active");
      if (banner) banner.classList.remove("visible");
      document.body.classList.remove("annotation-mode");
      hideTooltip();
      window.clearTextSelection();
    }
  };

  // ── Selection handler ────────────────────────────────────────

  function onContentMouseUp(e) {
    if (!annotationMode) return;
    if (e.target.closest(".ann-sel-tooltip")) return;
    hideTooltip();

    var sel = window.getSelection();
    if (!sel || sel.isCollapsed || !sel.toString().trim()) return;

    var range = sel.getRangeAt(0);
    var container = document.querySelector(".rendered-content");
    if (!container.contains(range.commonAncestorContainer)) return;

    pendingAnchor = extractAnchor(range);
    if (!pendingAnchor) return;

    showTooltip(range.getBoundingClientRect());
  }

  // ── Patch comment form submission to include anchor data ─────

  function patchCommentForm() {
    var form = document.getElementById("commentForm");
    if (!form) return;

    form.addEventListener("submit", function (e) {
      e.preventDefault();

      var data = {
        author_name: form.author_name.value,
        author_email: form.author_email.value || null,
        body: form.body.value,
      };

      if (window._pendingAnchor) {
        Object.assign(data, window._pendingAnchor);
      }

      fetch("/api/review/" + TOKEN + "/comments/" + CONTENT_PATH, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      }).then(function (res) {
        if (res.ok) { location.reload(); }
        else { res.json().then(function (err) { alert(err.detail || "Failed to submit comment"); }); }
      });
    }, { once: true });

    // Remove the original listener by preventing double-bind
    // The template's inline script also binds — we stop its propagation
    form.dataset.annotationPatched = "true";
  }

  // ── "Jump to highlight" links on comment cards ───────────────

  function addJumpLinks() {
    for (var i = 0; i < commentsData.length; i++) {
      var c = commentsData[i];
      if (!c.highlight_text) continue;
      var card = document.querySelector('.comment[data-id="' + c.id + '"]');
      if (!card) continue;
      var highlight = document.querySelector('.ann-highlight[data-comment-id="' + c.id + '"]');
      if (!highlight) continue;

      var btn = document.createElement("button");
      btn.className = "goto-highlight";
      btn.textContent = "Show in text";
      btn.addEventListener("click", (function (hl) {
        return function (e) {
          e.stopPropagation();
          hl.scrollIntoView({ block: "center", behavior: "smooth" });
          hl.classList.add("ann-flash");
          setTimeout(function () { hl.classList.remove("ann-flash"); }, 1500);
        };
      })(highlight));

      var header = card.querySelector(".comment-header");
      if (header) header.appendChild(btn);
    }
  }

  // ── Init ─────────────────────────────────────────────────────

  function init() {
    renderHighlights();
    addJumpLinks();

    var content = document.querySelector(".rendered-content");
    if (content) content.addEventListener("mouseup", onContentMouseUp);

    patchCommentForm();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    setTimeout(init, 0);
  }
})();
