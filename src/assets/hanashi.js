(function () {
  const HIGHLIGHT_TYPES = new Set(["noun", "verb", "verbplus", "phrase"]);
  const TOOLTIP_TYPES =
    ".vocabulary.noun, .vocabulary.verb, .vocabulary.verbplus, .vocabulary.phrase";

  let activeTooltip = null;
  let activeNoun = null;

  function escapeHtml(text) {
    return String(text)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function collectMatches(text, entries) {
    const taken = new Array(text.length).fill(false);
    const matches = [];

    for (const entry of entries) {
      const needle = entry.char;
      let from = 0;

      while (from <= text.length - needle.length) {
        const index = text.indexOf(needle, from);
        if (index === -1) {
          break;
        }

        let free = true;
        for (let i = index; i < index + needle.length; i += 1) {
          if (taken[i]) {
            free = false;
            break;
          }
        }

        if (free) {
          for (let i = index; i < index + needle.length; i += 1) {
            taken[i] = true;
          }
          matches.push({
            start: index,
            end: index + needle.length,
            type: entry.type,
            char: entry.char,
            reading: entry.reading || "",
            meaning: entry.meaning || "",
            base: entry.base || "",
            breakdown: entry.breakdown || "",
          });
        }

        from = index + 1;
      }
    }

    matches.sort((a, b) => a.start - b.start);
    return matches;
  }

  function wrapVocabulary(text, entries) {
    const matches = collectMatches(text, entries);
    let html = "";
    let cursor = 0;

    for (const match of matches) {
      if (cursor < match.start) {
        html += escapeHtml(text.slice(cursor, match.start));
      }
      html +=
        '<span class="vocabulary ' +
        match.type +
        '" data-char="' +
        escapeHtml(match.char) +
        '" data-reading="' +
        escapeHtml(match.reading) +
        '" data-meaning="' +
        escapeHtml(match.meaning) +
        '" data-base="' +
        escapeHtml(match.base) +
        '" data-breakdown="' +
        escapeHtml(match.breakdown) +
        '">' +
        escapeHtml(text.slice(match.start, match.end)) +
        "</span>";
      cursor = match.end;
    }

    if (cursor < text.length) {
      html += escapeHtml(text.slice(cursor));
    }

    return html;
  }

  function hideNounTooltip() {
    if (activeTooltip) {
      activeTooltip.remove();
    }
    activeTooltip = null;
    activeNoun = null;
  }

  function firstLineRect(noun) {
    const rects = noun.getClientRects();
    return rects.length > 0 ? rects[0] : null;
  }

  function pointInRect(clientX, clientY, rect) {
    return (
      clientX >= rect.left &&
      clientX <= rect.right &&
      clientY >= rect.top &&
      clientY <= rect.bottom
    );
  }

  function isPointInsideTooltip(clientX, clientY) {
    if (!activeTooltip) {
      return false;
    }
    return pointInRect(clientX, clientY, activeTooltip.getBoundingClientRect());
  }

  function isPointOverNoun(noun, clientX, clientY) {
    if (!noun) {
      return false;
    }
    const rects = noun.getClientRects();
    for (let i = 0; i < rects.length; i += 1) {
      if (pointInRect(clientX, clientY, rects[i])) {
        return true;
      }
    }
    return false;
  }

  function matchCharAppearance(charEl, noun) {
    const style = window.getComputedStyle(noun);
    charEl.style.fontFamily = style.fontFamily;
    charEl.style.fontSize = style.fontSize;
    charEl.style.fontWeight = style.fontWeight;
    charEl.style.fontStyle = style.fontStyle;
    charEl.style.letterSpacing = style.letterSpacing;
    charEl.style.color = style.color;
  }

  function positionTooltipOverNoun(tooltip, noun) {
    const charEl = tooltip.querySelector(".hanashi-tooltip-char");
    const anchorRect = firstLineRect(noun);
    if (!anchorRect) {
      return;
    }

    // Совпадаем с метриками первого визуального фрагмента (первой строки)
    charEl.style.height = anchorRect.height + "px";
    charEl.style.lineHeight = anchorRect.height + "px";

    tooltip.style.left = "0px";
    tooltip.style.top = "0px";
    tooltip.style.visibility = "hidden";

    let tipRect = tooltip.getBoundingClientRect();
    let charRect = charEl.getBoundingClientRect();
    let left = anchorRect.left - (charRect.left - tipRect.left);
    let top = anchorRect.top - (charRect.top - tipRect.top);

    tooltip.style.left = left + "px";
    tooltip.style.top = top + "px";

    // Второй проход убирает остаточный сдвиг после layout
    charRect = charEl.getBoundingClientRect();
    left += anchorRect.left - charRect.left;
    top += anchorRect.top - charRect.top;
    tooltip.style.left = left + "px";
    tooltip.style.top = top + "px";
    tooltip.style.visibility = "visible";
  }

  function showNounTooltip(target) {
    hideNounTooltip();

    const char = target.dataset.char || target.textContent || "";
    const reading = target.dataset.reading || "";
    const meaning = target.dataset.meaning || "";
    const base = target.dataset.base || "";
    const breakdown = target.dataset.breakdown || "";
    const isVerb = target.classList.contains("verb");
    const isVerbplus = target.classList.contains("verbplus");

    const tooltip = document.createElement("div");
    tooltip.className = "hanashi-tooltip";

    let html = '<div class="hanashi-tooltip-char">' + escapeHtml(char) + "</div>";
    if (reading && reading !== char) {
      html +=
        '<div class="hanashi-tooltip-reading">' + escapeHtml(reading) + "</div>";
    }
    if (isVerb && base && base !== char) {
      html +=
        '<div class="hanashi-tooltip-base">' + escapeHtml(base) + "</div>";
    }
    if (isVerbplus && breakdown) {
      html +=
        '<div class="hanashi-tooltip-breakdown">' +
        escapeHtml(breakdown) +
        "</div>";
    }
    if (meaning) {
      html +=
        '<div class="hanashi-tooltip-meaning">' + escapeHtml(meaning) + "</div>";
    }

    tooltip.innerHTML = html;
    document.body.appendChild(tooltip);

    const charEl = tooltip.querySelector(".hanashi-tooltip-char");
    matchCharAppearance(charEl, target);
    positionTooltipOverNoun(tooltip, target);

    activeTooltip = tooltip;
    activeNoun = target;
  }

  function onPointerOver(event) {
    if (activeTooltip) {
      return;
    }

    const target = event.target.closest(TOOLTIP_TYPES);
    if (!target) {
      return;
    }

    showNounTooltip(target);
  }

  function onPointerMove(event) {
    if (!activeTooltip) {
      return;
    }

    const x = event.clientX;
    const y = event.clientY;
    if (
      !isPointInsideTooltip(x, y) &&
      !isPointOverNoun(activeNoun, x, y)
    ) {
      hideNounTooltip();
    }
  }

  function onViewportChange() {
    // При скролле/resize слово уезжает из‑под указателя, а pointermove не приходит
    if (activeTooltip) {
      hideNounTooltip();
    }
  }

  document.addEventListener("pointerover", onPointerOver);
  document.addEventListener("pointermove", onPointerMove);
  window.addEventListener("scroll", onViewportChange, true);
  window.addEventListener("resize", onViewportChange);

  function highlightHanashiVocabulary(vocabulary) {
    hideNounTooltip();

    const entries = (vocabulary || [])
      .filter(
        (item) =>
          item &&
          HIGHLIGHT_TYPES.has(item.type) &&
          typeof item.char === "string" &&
          item.char.length > 0,
      )
      .sort((a, b) => b.char.length - a.char.length);

    document.querySelectorAll(".hanashi-paragraph").forEach((paragraph) => {
      paragraph.innerHTML = wrapVocabulary(paragraph.textContent, entries);
    });
  }

  window.highlightHanashiVocabulary = highlightHanashiVocabulary;
})();
