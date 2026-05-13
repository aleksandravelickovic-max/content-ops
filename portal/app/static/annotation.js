/* ── Inline annotation system for Content Review Portal ────── */
(function () {
  "use strict";

  var commentsData = window.COMMENTS_DATA || [];
  var popoverEl = null;
  var pendingAnchor = null;

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
      } catch (e) {}
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

  // ── Inline comment popover ──────────────────────────────────

  function showPopover(rect, anchor) {
    hidePopover();
    pendingAnchor = anchor;

    popoverEl = document.createElement("div");
    popoverEl.className = "ann-popover";

    var displayText = anchor.highlight_text;
    if (displayText.length > 100) displayText = displayText.substring(0, 100) + “…”;

    var reviewerName = window.REVIEWER_NAME || “”;
    var nameField = reviewerName
      ? '<input type=”hidden” name=”author_name” value=”' + escapeHtml(reviewerName) + '”>'
      : '<input type=”text” name=”author_name” placeholder=”Your name” required class=”ann-popover-input”>';

    popoverEl.innerHTML =
      '<div class=”ann-popover-quote”>”' + escapeHtml(displayText) + '”</div>' +
      '<form class=”ann-popover-form”>' +
        nameField +
        '<textarea name=”body” placeholder=”Your feedback…” required class=”ann-popover-textarea” rows=”3”></textarea>' +
        '<div class=”ann-popover-actions”>' +
          '<button type=”button” class=”ann-popover-cancel”>Cancel</button>' +
          '<button type=”submit” class=”ann-popover-submit”>Submit</button>' +
        '</div>' +
      '</form>';

    var container = document.querySelector(".rendered-content");
    var containerRect = container.getBoundingClientRect();

    var left = rect.left + rect.width / 2 - containerRect.left;
    var top = rect.bottom - containerRect.top + container.scrollTop + 8;

    var popoverWidth = 320;
    var maxLeft = container.offsetWidth - popoverWidth / 2 - 8;
    var minLeft = popoverWidth / 2 + 8;
    if (left > maxLeft) left = maxLeft;
    if (left < minLeft) left = minLeft;

    popoverEl.style.left = left + "px";
    popoverEl.style.top = top + "px";

    container.style.position = "relative";
    container.appendChild(popoverEl);

    popoverEl.querySelector(".ann-popover-cancel").addEventListener("click", hidePopover);

    popoverEl.querySelector(".ann-popover-form").addEventListener("submit", function (e) {
      e.preventDefault();
      submitInlineComment(this);
    });

    // Prevent clicks inside popover from dismissing it
    popoverEl.addEventListener("mousedown", function (e) { e.stopPropagation(); });

    setTimeout(function () {
      var input = popoverEl && popoverEl.querySelector('input[name="author_name"]');
      if (input) input.focus();
    }, 50);
  }

  function hidePopover() {
    if (popoverEl && popoverEl.parentNode) popoverEl.parentNode.removeChild(popoverEl);
    popoverEl = null;
    pendingAnchor = null;
  }

  function escapeHtml(str) {
    var div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  function submitInlineComment(form) {
    var data = {
      author_name: form.author_name.value,
      body: form.body.value,
    };
    if (pendingAnchor) Object.assign(data, pendingAnchor);

    var submitBtn = form.querySelector(".ann-popover-submit");
    if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = "Saving…"; }

    fetch("/api/review/" + TOKEN + "/comments/" + CONTENT_PATH, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    }).then(function (res) {
      if (res.ok) { location.reload(); }
      else {
        if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = "Submit"; }
        res.json().then(function (err) { alert(err.detail || "Failed to submit"); });
      }
    }).catch(function () {
      if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = "Submit"; }
      alert("Network error — check your connection.");
    });
  }

  // ── Selection handler (always active, document-level) ────────

  function onDocumentMouseUp(e) {
    if (e.target.closest(".ann-popover")) return;

    var container = document.querySelector(".rendered-content");
    if (!container) return;

    var sel = window.getSelection();
    if (!sel || sel.isCollapsed || !sel.toString().trim()) {
      if (popoverEl && !e.target.closest(".ann-popover")) hidePopover();
      return;
    }

    var range = sel.getRangeAt(0);
    if (!container.contains(range.commonAncestorContainer)) return;

    var anchor = extractAnchor(range);
    if (!anchor) return;

    hidePopover();
    showPopover(range.getBoundingClientRect(), anchor);
  }

  // Dismiss popover on click outside
  function onDocumentMouseDown(e) {
    if (popoverEl && !popoverEl.contains(e.target)) {
      hidePopover();
    }
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

    document.addEventListener("mouseup", function (e) {
      setTimeout(function () { onDocumentMouseUp(e); }, 10);
    });
    document.addEventListener("mousedown", onDocumentMouseDown);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    setTimeout(init, 0);
  }
})();
