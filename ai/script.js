(() => {
  const textEl = document.getElementById("textPlaceholder");
  const feedbackEl = document.getElementById("copyFeedback");

  async function copyToClipboard() {
    const textToCopy = textEl.innerText;
    try {
      await navigator.clipboard.writeText(textToCopy);
      feedbackEl.classList.add("show");
      setTimeout(() => {
        feedbackEl.classList.remove("show");
      }, 1800);
    } catch (err) {
      feedbackEl.style.color = "#bf616a";
      feedbackEl.innerText = "⚠️ Failed to copy";
      feedbackEl.classList.add("show");
      setTimeout(() => {
        feedbackEl.classList.remove("show");
        feedbackEl.innerText = "✓ Copied to clipboard";
        feedbackEl.style.color = "#a3be8c";
      }, 2000);
    }
  }

  textEl.addEventListener("click", copyToClipboard);
})();
