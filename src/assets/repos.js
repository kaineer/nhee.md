document.addEventListener('DOMContentLoaded', () => {
  const user = "kaineer";
  const perPage = 4;

  const url = "https://api.github.com/users/" + user + "/repos?sort=pushed&per_page=" + perPage;

  const fetchRepos = async () => {
    const resp = await fetch(url);
    const data = await resp.json();

    console.log(data);
  }
  
  fetchRepos();
});
