(() => {
  const first = (selector, fn) => {
    const el = document.querySelector(selector);

    if (el && typeof fn === "function") {
      return fn(el);
    }
  };

  const success = {
    message: "✓ Copied to clipboard",
    color: "#a3be8c",
    ms: 1800,
  };
  const error = {
    message: "× Failed to copy",
    color: "#bf616a",
    ms: 2000,
  };

  const display = first("#copyFeedback", (el) => {
    return ({ message, color, ms }) => {
      el.classList.add("show");
      el.innerText = message;
      el.style.color = color;
      setTimeout(() => el.classList.remove("show"), ms);
    };
  });

  first("#textPlaceholder", (textEl) => {
    const noTrim = textEl.dataset["no-trim"] === "true";
    const text = noTrim
      ? textEl.innerText
      : textEl.innerText.replace(/\s+/gm, " ");
    const copyToClipboard = async () => {
      try {
        await navigator.clipboard.writeText(text);
        display(success);
      } catch (err) {
        display(error);
      }
    };
    textEl.addEventListener("click", copyToClipboard);
  });
})();
