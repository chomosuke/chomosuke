import sys
from github import Github
import re
import time

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

g = Github(sys.argv[1], per_page=100)

prs = g.search_issues("is:pr author:chomosuke is:public")

repos = {}
for pr in prs:
    if "chomosuke" not in pr.html_url:
        k = re.fullmatch(r"^https://github.com/(.*)/pull/\d+$", pr.html_url)
        assert k is not None
        k = k.group(1)
        repos.setdefault(k, []).append(pr)

repo_prss = []
for k in repos:
    repo = repos[k][0].repository
    prs = []
    for pr in repos[k]:
        if sys.argv[2] == 'release':
            # throttle when running in github action
            time.sleep(1)
        pr = pr.as_pull_request()
        if pr.merged or pr.closed_at is None:
            # only include merge and opened pr
            prs.append(pr)
    prs.sort(key=lambda pr: pr.comments * 5 + pr.additions + pr.deletions, reverse=True)
    if len(prs) > 0:
        repo_prss.append((repo, prs))

repo_prss.sort(key=lambda repo_prs: repo_prs[0].stargazers_count, reverse=True)

contrib = "\n"
for repo_prs in repo_prss:
    k = repo_prs[0]
    contrib += (
        "#### ["
        + k.name
        + "]("
        + k.html_url
        + ") ![](./assets/star.svg)"
        + str(k.stargazers_count)
        + "\n"
    )
    for pr in repo_prs[1]:
        contrib += (
            "- ["
            + pr.title
            + "]("
            + pr.html_url
            + ") "
            + ("![](./assets/merged.svg)" if pr.merged else "![](./assets/open.svg)")
            + "\n"
        )

readme = re.sub(
    r"<!--CONTRIB BEGIN-->.*<!--CONTRIB END-->",
    "<!--CONTRIB BEGIN-->" + contrib + "<!--CONTRIB END-->",
    readme,
    flags=re.DOTALL,
)

with open("README.md", "w") as readme_file:
    readme_file.write(readme)
