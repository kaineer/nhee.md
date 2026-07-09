const first = (selector) => document.querySelector(selector);
const html = (el, value) => {
  if (typeof value === "undefined") {
    return el.innerHTML;
  }
  el.innerHTML = value;
  return void 0;
}
const text = (el, value) => {
  if (typeof value === "undefined") {
    return el.textContent;
  }
  el.textContent = value;
  return void 0;
}
const onloaded = (fn) => document.addEventListener('DOMContentLoaded', fn);

onloaded(() => {
  const user = "kaineer";
  const perPage = 5;

  const url = "https://api.github.com/users/" + user + "/repos?sort=pushed&per_page=" + perPage;

  const processRepo = (repo) => {
    const { html_url, name, description } = repo;

    return (`
      <a class="prompt-item" href="${html_url}">
        <div class="prompt-title">${name}</div>
        <div class="prompt-description">${description}</div>
      </a>
    `);
  }

  const fetchRepos = async () => {
    const resp = await fetch(url);
    const data = await resp.json();

    html(
      first(".prompts-list"), 
      data.map(processRepo).join("")
    );
  }

  text(
    first(".page-title"),
    `Last ${perPage} updated public repositories`
  );
  
  fetchRepos();
});
