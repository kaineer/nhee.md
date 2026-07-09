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

const getRepoUrl = (user, count) => {
  // "https://api.github.com/users/" + user + "/repos?sort=pushed&per_page=" + perPage;
  return ([
    "https://api.github.com/users/",
    user,
    "/repos?sort=pushed&per_page=",
    String(perPage)
  ].join(""));
}

onloaded(() => {
  const user = "kaineer";
  const perPage = 5;

  const processRepo = (repo) => {
    const { html_url: itemUrl, name: title, description } = repo;

    return (`
      <a class="prompt-item" href="${itemUrl}">
        <div class="prompt-title">${title}</div>
        <div class="prompt-description">${description}</div>
      </a>
    `);
  }

  const fetchRepos = async () => {
    const resp = await fetch(getRepoUrl(user, perPage));
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
