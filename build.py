#!/usr/bin/env python3
import os
import markdown
from pathlib import Path
from staticjinja import Site


def md_context(template):
    md = markdown.Markdown(extensions=["meta"])
    markdown_content = Path(template.filename).read_text()
    variables = {"content": md.convert(markdown_content)} | md.Meta

    for key, value in variables.items():
        if isinstance(value, list) and len(value) == 1:
            variables[key] = value[0]

    return variables


def render_md(site, data, **kwargs):
    out = site.outpath / Path(data.name).with_suffix(".html")
    os.makedirs(out.parent, exist_ok=True)
    template = get_template(site, data)
    site.get_template(template).stream(**kwargs).dump(str(out), encoding="utf-8")


def get_template(site, data):
    default_template = "_templates/default.j2"
    template_stem = str(Path(data.name).parent)
    if template_stem == ".":
        template_stem = "__" + str(data.name).split(".")[0]

    template = "_templates/" + template_stem + ".j2"

    if not os.path.exists(os.path.join(site.searchpath, template)):
        print("No template found for " + str(
            data.name) + " Looking at: " + template + ", using default template: " + default_template)
        template = default_template

    return template


def empty_dir(dir_path, remove=False):
    [x if x.is_dir() and empty_dir(x, True) else x.is_file() and x.unlink() for x in Path(dir_path).iterdir()]
    if remove:
        os.rmdir(dir_path)


def main():
    source = "site"
    output = "dist"

    if os.path.exists(output):
        empty_dir(output)

    site = Site.make_site(
        searchpath=source,
        outpath=output,
        contexts=[(r".*\.md", md_context)],
        rules=[(r".*\.md", render_md)],
    )

    site.render()


if __name__ == "__main__":
    main()
