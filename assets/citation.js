(() => {
  const first = (selector) => document.querySelector(selector);

  const success = {
    message: "✓ Copied to clipboard",
    color: "#a3be8c",
    ms: 1800,
  };
  const error = {
    message: "",
    color: "",
    ms: 2000,
  };

  const feedbackEl = first("#copyFeedback");
  const display = ({ message, color, ms }) => {
    feedbackEl.classList.add("show");
    feedbackEl.innerText = message;
    feedbackEl.style.color = color;
    setTimeout(() => feedbackEl.classList.remove("show"), ms);
  };

  const textEl = first("#textPlaceholder");
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
})();
