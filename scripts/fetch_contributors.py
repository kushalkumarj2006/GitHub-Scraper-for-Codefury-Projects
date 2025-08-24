import requests
import json
from google.colab import files

# Optional GitHub token (recommended for higher limits)
GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"

headers = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "kushalkumarj2006"
}
if GITHUB_TOKEN:
    headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

def get_contributors(repo_url):
    """Fetch contributors for a repo (returns dict with name, profile, avatar)."""
    parts = repo_url.rstrip('/').split('/')
    owner, repo = parts[-2], parts[-1]
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contributors"

    contributors = []
    page = 1
    while True:
        params = {"per_page": 100, "page": page}
        resp = requests.get(api_url, headers=headers, params=params)
        if resp.status_code != 200:
            print(f"❌ Failed contributors for {repo_url}: {resp.status_code}")
            break
        data = resp.json()
        if not data:
            break
        for c in data:
            username = c.get("login")
            contributors.append({
                "name": c.get("login"),  # placeholder for now
                "profile": c.get("html_url"),
                "avatar": c.get("avatar_url")
            })
        if len(data) < 100:
            break
        page += 1
    return contributors

def get_repo_info(repo_url):
    """Fetch repo details including unique ID."""
    parts = repo_url.rstrip('/').split('/')
    owner, repo = parts[-2], parts[-1]
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    resp = requests.get(api_url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        return {
            "id": data["id"],
            "full_name": data["full_name"],
            "html_url": data["html_url"]
        }
    return None

# === Main ===
uploaded = files.upload()
file_path = list(uploaded.keys())[0]

all_results = {}

with open(file_path, "r") as f:
    for line in f:
        repo_url = line.strip()
        if not repo_url:
            continue
        print(f"🔍 Fetching repo: {repo_url}")
        repo_info = get_repo_info(repo_url)
        if not repo_info:
            continue

        repo_id = str(repo_info["id"])
        print(f"✅ Adding {repo_info['full_name']} (ID: {repo_id})")
        contributors = get_contributors(repo_url)

        all_results[repo_id] = {
            "repo": repo_info,
            "contributors": {c["profile"].split("/")[-1]: c for c in contributors}
        }

# Save JSON with a fresh name
output_file = "all_contributors_fresh.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2)

print(f"🎉 Done! Saved {len(all_results)} repos in {output_file}")
files.download(output_file)
