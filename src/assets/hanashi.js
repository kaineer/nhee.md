(function () {
  const HIGHLIGHT_TYPES = new Set([
    "noun",
    "verb",
    "verbplus",
    "phrase",
    "grammar",
  ]);
  const TOOLTIP_TYPES =
    ".vocabulary.noun, .vocabulary.verb, .vocabulary.verbplus, .vocabulary.phrase, .vocabulary.grammar";
  const GRAMMAR_GAP = "〜";

  let activeTooltip = null;
  let activeNoun = null;

  function escapeHtml(text) {
    return String(text)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function entryMatchLength(entry) {
    if (entry.type === "grammar") {
      return entry.char.split(GRAMMAR_GAP).join("").length;
    }
    return entry.char.length;
  }

  function rangeFree(taken, start, end) {
    for (let i = start; i < end; i += 1) {
      if (taken[i]) {
        return false;
      }
    }
    return true;
  }

  function markRange(taken, start, end) {
    for (let i = start; i < end; i += 1) {
      taken[i] = true;
    }
  }

  function matchMeta(entry) {
    return {
      type: entry.type,
      char: entry.char,
      reading: entry.reading || "",
      meaning: entry.meaning || "",
      base: entry.base || "",
      breakdown: entry.breakdown || "",
    };
  }

  // Шаблон вида 「〜ば〜ほど」 → литералы ["ば", "ほど"] с пропусками на месте 〜
  function collectGrammarMatches(text, entry, taken) {
    const parts = entry.char.split(GRAMMAR_GAP);
    const literals = parts.filter((part) => part.length > 0);
    if (literals.length === 0) {
      return [];
    }

    const meta = matchMeta(entry);
    const matches = [];
    const first = literals[0];
    let from = 0;

    while (from <= text.length - first.length) {
      const start = text.indexOf(first, from);
      if (start === -1) {
        break;
      }

      const spans = [];
      let cursor = start;
      let ok = true;

      for (let i = 0; i < literals.length; i += 1) {
        const literal = literals[i];
        const index = i === 0 ? start : text.indexOf(literal, cursor);
        if (index === -1 || !rangeFree(taken, index, index + literal.length)) {
          ok = false;
          break;
        }
        // Между литералами должен быть пропуск (〜), хотя бы пустой;
        // следующий литерал не может начинаться раньше конца предыдущего
        if (i > 0 && index < cursor) {
          ok = false;
          break;
        }
        spans.push({ start: index, end: index + literal.length });
        cursor = index + literal.length;
      }

      if (ok) {
        spans.forEach((span) => {
          markRange(taken, span.start, span.end);
          matches.push({
            start: span.start,
            end: span.end,
            ...meta,
          });
        });
        from = start + first.length;
      } else {
        from = start + 1;
      }
    }

    return matches;
  }

  function collectExactMatches(text, entry, taken) {
    const needle = entry.char;
    const meta = matchMeta(entry);
    const matches = [];
    let from = 0;

    while (from <= text.length - needle.length) {
      const index = text.indexOf(needle, from);
      if (index === -1) {
        break;
      }

      if (rangeFree(taken, index, index + needle.length)) {
        markRange(taken, index, index + needle.length);
        matches.push({
          start: index,
          end: index + needle.length,
          ...meta,
        });
      }

      from = index + 1;
    }

    return matches;
  }

  function collectMatches(text, entries) {
    const taken = new Array(text.length).fill(false);
    const matches = [];

    for (const entry of entries) {
      if (entry.type === "grammar") {
        matches.push(...collectGrammarMatches(text, entry, taken));
      } else {
        matches.push(...collectExactMatches(text, entry, taken));
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

  // В шаблоне grammar помечаем совпавший литерал — по нему выравниваем тултип
  function grammarCharHtml(pattern, fragment) {
    if (!fragment) {
      return escapeHtml(pattern);
    }
    const index = pattern.indexOf(fragment);
    if (index === -1) {
      return escapeHtml(pattern);
    }
    return (
      escapeHtml(pattern.slice(0, index)) +
      '<span class="hanashi-tooltip-char-anchor">' +
      escapeHtml(fragment) +
      "</span>" +
      escapeHtml(pattern.slice(index + fragment.length))
    );
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
    const alignEl =
      tooltip.querySelector(".hanashi-tooltip-char-anchor") || charEl;
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
    let alignRect = alignEl.getBoundingClientRect();
    let left = anchorRect.left - (alignRect.left - tipRect.left);
    let top = anchorRect.top - (alignRect.top - tipRect.top);

    tooltip.style.left = left + "px";
    tooltip.style.top = top + "px";

    // Второй проход убирает остаточный сдвиг после layout
    alignRect = alignEl.getBoundingClientRect();
    left += anchorRect.left - alignRect.left;
    top += anchorRect.top - alignRect.top;

    // У краёв экрана смещаем, чтобы весь тултип оставался читаемым
    const clamped = clampTooltipToViewport(tooltip, left, top);
    tooltip.style.left = clamped.left + "px";
    tooltip.style.top = clamped.top + "px";
    tooltip.style.visibility = "visible";
  }

  function showNounTooltip(target, clientX, clientY) {
    hideNounTooltip();

    const char = target.dataset.char || target.textContent || "";
    const fragment = target.textContent || "";
    const reading = target.dataset.reading || "";
    const meaning = target.dataset.meaning || "";
    const base = target.dataset.base || "";
    const breakdown = target.dataset.breakdown || "";
    const isVerb = target.classList.contains("verb");
    const isVerbplus = target.classList.contains("verbplus");
    const isGrammar = target.classList.contains("grammar");

    const tooltip = document.createElement("div");
    tooltip.className = "hanashi-tooltip";

    let html =
      '<div class="hanashi-tooltip-char">' +
      (isGrammar ? grammarCharHtml(char, fragment) : escapeHtml(char)) +
      "</div>";
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

  function vocabularyAtPoint(clientX, clientY) {
    const el = document.elementFromPoint(clientX, clientY);
    return el ? el.closest(TOOLTIP_TYPES) : null;
  }

  function onPointerOver(event) {
    const target = event.target.closest(TOOLTIP_TYPES);
    if (!target) {
      return;
    }
    // Уже открыт для этого слова — не пересоздаём
    if (activeTooltip && activeNoun === target) {
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
    if (isPointInsideTooltip(x, y) || isPointOverNoun(activeNoun, x, y)) {
      return;
    }

    // Ушли со старого тултипа/слова: pointerover по соседнему span
    // мог уже пройти, пока activeTooltip ещё существовал
    const next = vocabularyAtPoint(x, y);
    if (next) {
      showNounTooltip(next, x, y);
      return;
    }

    hideNounTooltip();
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
      .sort((a, b) => entryMatchLength(b) - entryMatchLength(a));

    document.querySelectorAll(".hanashi-paragraph").forEach((paragraph) => {
      paragraph.innerHTML = wrapVocabulary(paragraph.textContent, entries);
    });
  }

  window.highlightHanashiVocabulary = highlightHanashiVocabulary;
})();
