const first = (selector) => document.querySelector(selector);
const isVoid = (obj) => (typeof obj === "undefined");
const attrfn = (name) => (el, value) => {
  if (isVoid(value)) return el[name];
  return (el[name] = value, void 0);
}

const [html, text] = ["innerHTML", "textContent"].map(attrfn);

const onloaded = (fn) => document.addEventListener('DOMContentLoaded', fn);

const getRepoUrl = (user, count) => (
  `https://api.github.com/users/${user}/repos?sort=pushed&per_page=${count}`
);

onloaded(() => {
  const user = "kaineer";
  const perPage = 4;

  const fetchRepos = async () => {
    const key = "nhee.repos";
    const reposItem = sessionStorage.getItem(key);
    if (reposItem === null) {
      const resp = await fetch(getRepoUrl("kaineer", 4));
      const data = await resp.json(); 
      sessionStorage.setItem(key, JSON.stringify(data));
      return data;
    } else {
      return JSON.parse(reposItem);
    }
  }

  const processRepo = ({ 
    html_url: itemUrl,
    name: title,
    description,
  }) => (`
    <a class="list-item" href="${itemUrl}">
      <div class="list-title">${title}</div>
      <div class="list-description">${description}</div>
    </a>
  `);

  (async () => {
    const data = await fetchRepos();

    html(
      first(".list"), 
      data.map(processRepo).join("")
    );
  })();

  text(
    first(".page-title"),
    `Last ${perPage} updated public repositories`
  );
});
