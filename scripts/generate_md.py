import json

# Use the existing JSON file already in Colab
file_path = "all_contributors_fresh.json"

with open(file_path, "r", encoding="utf-8") as f:
    all_results = json.load(f)

# === Markdown Generation ===
lines = []
lines.append("# 🚀 Contributors\n")

# Sort repos alphabetically by full_name
sorted_repos = sorted(all_results.items(), key=lambda x: x[1]["repo"]["full_name"].lower())

for idx, (repo_id, repo_data) in enumerate(sorted_repos, start=1):
    repo = repo_data["repo"]
    contributors = repo_data["contributors"]

    lines.append(f"### {idx}. [{repo['html_url']}]({repo['html_url']})")
    lines.append(f"**🆔 Repo ID: {repo_id}**")
    lines.append(f"**👥 {len(contributors)} contributors**\n")

    for username, c in contributors.items():
        name = c.get("name", "") or username
        profile = c["profile"]
        avatar = c["avatar"]

        lines.append(
            f"- [<img src=\"{avatar}\" width=\"40\">]({profile}) **{name}** "
            f"[@{username}]({profile})  "
        )

    lines.append("\n---\n")

# Save Markdown
output_file = "all_contributors_sorted.md"
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ Markdown generated: {output_file}")
