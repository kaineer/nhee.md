(() => {
  const sourceEl = document.querySelector("#markdownSource");
  const button = document.querySelector("#copyMarkdown");

  if (!sourceEl || !button) {
    return;
  }

  const flash = (cls) => {
    button.classList.remove("is-copied", "is-failed");
    void button.offsetWidth;
    button.classList.add(cls);
  };

  button.addEventListener("animationend", (event) => {
    if (event.target.classList.contains("markdown-copy-ghost")) {
      button.classList.remove("is-copied");
    }
  });

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(sourceEl.value);
      flash("is-copied");
    } catch (err) {
      flash("is-failed");
      setTimeout(() => button.classList.remove("is-failed"), 700);
    }
  };

  button.addEventListener("click", copyToClipboard);
})();
