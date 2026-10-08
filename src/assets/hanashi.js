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

  function pointInRect(clientX, clientY, rect) {
    return (
      clientX >= rect.left &&
      clientX <= rect.right &&
      clientY >= rect.top &&
      clientY <= rect.bottom
    );
  }

  function rectDistance2(clientX, clientY, rect) {
    const x = Math.max(rect.left, Math.min(clientX, rect.right));
    const y = Math.max(rect.top, Math.min(clientY, rect.bottom));
    const dx = clientX - x;
    const dy = clientY - y;
    return dx * dx + dy * dy;
  }

  // Фрагмент перенесённого сочетания под указателем; иначе ближайший / первый
  function anchorRectForPoint(noun, clientX, clientY) {
    const rects = noun.getClientRects();
    if (rects.length === 0) {
      return null;
    }

    if (clientX != null && clientY != null) {
      for (let i = 0; i < rects.length; i += 1) {
        if (pointInRect(clientX, clientY, rects[i])) {
          return rects[i];
        }
      }

      let best = rects[0];
      let bestDistance = rectDistance2(clientX, clientY, best);
      for (let i = 1; i < rects.length; i += 1) {
        const distance = rectDistance2(clientX, clientY, rects[i]);
        if (distance < bestDistance) {
          best = rects[i];
          bestDistance = distance;
        }
      }
      return best;
    }

    return rects[0];
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

  function viewportSize() {
    const vp = window.visualViewport;
    return {
      width: vp ? vp.width : window.innerWidth,
      height: vp ? vp.height : window.innerHeight,
      offsetLeft: vp ? vp.offsetLeft : 0,
      offsetTop: vp ? vp.offsetTop : 0,
    };
  }

  function clampTooltipToViewport(tooltip, left, top) {
    const margin = 8;
    const view = viewportSize();
    const tipRect = tooltip.getBoundingClientRect();
    const minLeft = view.offsetLeft + margin;
    const minTop = view.offsetTop + margin;
    const maxLeft = Math.max(
      minLeft,
      view.offsetLeft + view.width - tipRect.width - margin,
    );
    const maxTop = Math.max(
      minTop,
      view.offsetTop + view.height - tipRect.height - margin,
    );

    return {
      left: Math.min(Math.max(left, minLeft), maxLeft),
      top: Math.min(Math.max(top, minTop), maxTop),
    };
  }

  function positionTooltipOverNoun(tooltip, noun, clientX, clientY) {
    const charEl = tooltip.querySelector(".hanashi-tooltip-char");
    const anchorRect = anchorRectForPoint(noun, clientX, clientY);
    if (!anchorRect) {
      return;
    }

    const view = viewportSize();
    const margin = 8;
    tooltip.style.maxWidth = view.width - margin * 2 + "px";

    // Совпадаем с метриками выбранного визуального фрагмента (строки под указателем)
    charEl.style.whiteSpace = "nowrap";
    charEl.style.height = anchorRect.height + "px";
    charEl.style.lineHeight = anchorRect.height + "px";

    tooltip.style.left = "0px";
    tooltip.style.top = "0px";
    tooltip.style.visibility = "hidden";

    // Длинные сочетания на узком экране — перенос вместо вылезания за край
    if (charEl.scrollWidth > charEl.clientWidth + 1) {
      charEl.style.whiteSpace = "normal";
      charEl.style.height = "auto";
      charEl.style.lineHeight = window.getComputedStyle(noun).lineHeight;
    }

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

    // У краёв экрана смещаем, чтобы весь тултип оставался читаемым
    const clamped = clampTooltipToViewport(tooltip, left, top);
    tooltip.style.left = clamped.left + "px";
    tooltip.style.top = clamped.top + "px";
    tooltip.style.visibility = "visible";
  }

  function showNounTooltip(target, clientX, clientY) {
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
    positionTooltipOverNoun(tooltip, target, clientX, clientY);

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

    showNounTooltip(target, event.clientX, event.clientY);
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

  function onMobileClick(event) {
    const target = event.target.closest(TOOLTIP_TYPES);
    if (target) {
      if (activeTooltip && activeNoun === target) {
        hideNounTooltip();
        return;
      }
      showNounTooltip(target, event.clientX, event.clientY);
      return;
    }

    if (activeTooltip && !event.target.closest(".hanashi-tooltip")) {
      hideNounTooltip();
    }
  }

  function onViewportChange() {
    // При скролле/resize слово уезжает из‑под указателя, а pointermove не приходит
    if (activeTooltip) {
      hideNounTooltip();
    }
  }

  const isMobile = window.matchMedia(
    "(hover: none) and (pointer: coarse)",
  ).matches;

  if (isMobile) {
    document.addEventListener("click", onMobileClick);
  } else {
    document.addEventListener("pointerover", onPointerOver);
    document.addEventListener("pointermove", onPointerMove);
  }
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
