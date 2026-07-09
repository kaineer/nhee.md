const first = (selector) => document.querySelector(selector);
const attrfn = (name) => (el, value) => {
  if (typeof value === "undefined") {
    return el[name];
  }
  el[name] = value;
  return void 0;
}

const html = attrfn("innerHTML");
const text = attrfn("textContent");

const onloaded = (fn) => document.addEventListener('DOMContentLoaded', fn);

const getRepoUrl = (user, count) => {
  // "https://api.github.com/users/" + user + "/repos?sort=pushed&per_page=" + perPage;
  return ([
    "https://api.github.com/users/",
    user,
    "/repos?sort=pushed&per_page=",
    String(count)
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

  (async () => {
    const resp = await fetch(getRepoUrl(user, perPage));
    const data = await resp.json();

    html(
      first(".prompts-list"), 
      data.map(processRepo).join("")
    );
  })();

  text(
    first(".page-title"),
    `Last ${perPage} updated public repositories`
  );
});
