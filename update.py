import sys
from github import Github
import re

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

g = Github(sys.argv[1], per_page=100)

prs = g.search_issues("is:pr author:chomosuke is:public")

repos = {}
for pr in prs:
    if "chomosuke" not in pr.html_url:
        repo = re.fullmatch(r"^https://github.com/(.*)/pull/\d+$", pr.html_url)
        assert repo != None
        repo = repo.group(1)
        repos.setdefault(repo, []).append(pr)

repo_prss = []
for repo in repos:
    repo_prss.append((repos[repo][0].repository, repos[repo]))

repo_prss.sort(key=lambda repo_prs: repo_prs[0].stargazers_count, reverse=True)

contrib = "\n"
for repo_prs in repo_prss:
    repo = repo_prs[0]
    contrib += "#### [" + repo.name + "](" + repo.html_url + ")\n"
    for pr in repo_prs[1]:
        contrib += "- [" + pr.title + "](" + pr.html_url + ")\n"

readme = re.sub(
    r"<!--CONTRIB BEGIN-->.*<!--CONTRIB END-->",
    "<!--CONTRIB BEGIN-->" + contrib + "<!--CONTRIB END-->",
    readme,
    flags=re.DOTALL,
)

with open("README.md", "w") as readme_file:
    readme_file.write(readme)
