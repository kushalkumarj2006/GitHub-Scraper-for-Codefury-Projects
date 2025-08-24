import requests

GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"  # <-- Insert your token here for higher rate limits
QUERY = "Codefury"
OUTPUT_FILE = "repos.txt"

headers = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "kushalkumarj2006",
}

if GITHUB_TOKEN:
    headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

def fetch_repos(query):
    repos = []
    url = f"https://api.github.com/search/repositories"
    page = 1
    per_page = 100  # Max allowed by API

    while True:
        params = {
            "q": query,
            "type": "Repositories",
            "sort": "best-match",
            "order": "desc",
            "per_page": per_page,
            "page": page
        }
        resp = requests.get(url, headers=headers, params=params)
        data = resp.json()
        items = data.get("items", [])
        if not items:
            break
        for repo in items:
            repos.append(repo["html_url"])
        print(f"Fetched {len(items)} repos from page {page}")
        if len(items) < per_page:  # Last page
            break
        page += 1
    return repos

if __name__ == "__main__":
    repos = fetch_repos(QUERY)
    with open(OUTPUT_FILE, "w") as f:
        for url in repos:
            f.write(url + "\n")
    print(f"Total repositories collected: {len(repos)}")
