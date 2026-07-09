document.addEventListener('DOMContentLoaded', () => {
  const user = "kaineer";
  const perPage = 5;

  const url = "https://api.github.com/users/" + user + "/repos?sort=pushed&per_page=" + perPage;

  const processRepo = (repo) => {
    const { html_url, name, description } = repo;

    const itemHtml = `
      <a class="prompt-item" href="${html_url}">
        <div class="prompt-title">${name}</div>
        <div class="prompt-description">${description}</div>
      </a>
    `;

    return itemHtml;
  }

  const fetchRepos = async () => {
    const resp = await fetch(url);
    const data = await resp.json();

    const html = data.map(processRepo).join("");

    document.querySelector(".prompts-list").innerHTML = (
      `<ul>${html}</ul>`
    );
  }

  const title = document.querySelector(".page-title");
  title.textContent = `Last ${perPage} updated public repositories`;
  
  fetchRepos();
});
