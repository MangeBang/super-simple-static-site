import os

from staticjinja import Site

import ssss.common.fs as fs
import ssss.common.md as md


def main():
    source = "site"
    output = "dist"

    if os.path.exists(output):
        fs.directory.make_empty(output)

    site = Site.make_site(
        searchpath=source,
        outpath=output,
        contexts=[(r".*\.md", md.info.variables)],
        rules=[(r".*\.md", md.render.run)]
    )

    site.render()
