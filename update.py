import sys
from github import Github
import re

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

g = Github(sys.argv[1], per_page=100)

prs = g.search_issues("is:pr author:chomosuke is:public")

repo_prs = {}
for pr in prs:
    if "chomosuke" not in pr.html_url:
        repo = re.fullmatch(r"^https://github.com/(.*)/pull/\d+$", pr.html_url)
        assert(repo != None)
        repo = repo.group(1)
        repo_prs.setdefault(repo, []).append(pr)

contrib = "\n"
for repo in repo_prs:
    contrib += "#### " + repo + "\n"
    for pr in repo_prs[repo]:
        contrib += "- [" + pr.title + "](" + pr.html_url + ")\n"

readme = re.sub(
    r"<!--CONTRIB BEGIN-->.*<!--CONTRIB END-->",
    "<!--CONTRIB BEGIN-->" + contrib + "<!--CONTRIB END-->",
    readme,
    flags=re.DOTALL,
)

with open("README.md", "w") as readme_file:
    readme_file.write(readme)
