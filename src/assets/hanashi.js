(function () {
  const HIGHLIGHT_TYPES = new Set(["noun", "verb", "phrase"]);

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

  function showNounTooltip(noun) {
    hideNounTooltip();

    const char = noun.dataset.char || noun.textContent || "";
    const reading = noun.dataset.reading || "";
    const meaning = noun.dataset.meaning || "";

    const tooltip = document.createElement("div");
    tooltip.className = "hanashi-tooltip";

    let html = '<div class="hanashi-tooltip-char">' + escapeHtml(char) + "</div>";
    if (reading && reading !== char) {
      html +=
        '<div class="hanashi-tooltip-reading">' + escapeHtml(reading) + "</div>";
    }
    if (meaning) {
      html +=
        '<div class="hanashi-tooltip-meaning">' + escapeHtml(meaning) + "</div>";
    }

    tooltip.innerHTML = html;
    document.body.appendChild(tooltip);

    const charEl = tooltip.querySelector(".hanashi-tooltip-char");
    matchCharAppearance(charEl, noun);
    positionTooltipOverNoun(tooltip, noun);

    activeTooltip = tooltip;
    activeNoun = noun;
  }

  function onPointerOver(event) {
    if (activeTooltip) {
      return;
    }

    const noun = event.target.closest(".vocabulary.noun");
    if (!noun) {
      return;
    }

    showNounTooltip(noun);
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

  document.addEventListener("pointerover", onPointerOver);
  document.addEventListener("pointermove", onPointerMove);

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
