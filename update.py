import sys
from github import Github
import re

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

g = Github(sys.argv[1], per_page=100)

prs = g.search_issues("is:pr author:chomosuke is:public")

contrib = "\n"
for pr in prs:
    if "chomosuke" not in pr.html_url:
        contrib += pr.html_url + "\n"

readme = re.sub(
    "<!--CONTRIB BEGIN-->.*<!--CONTRIB END-->",
    "<!--CONTRIB BEGIN-->" + contrib + "<!--CONTRIB END-->",
    readme,
    flags=re.DOTALL,
)

with open("README.md", "w") as readme_file:
    readme_file.write(readme)
