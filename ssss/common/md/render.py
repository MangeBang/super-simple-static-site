from pathlib import Path
import os


def run(site, data, **kwargs):
    out = site.outpath / Path(data.name).with_suffix(".html")
    os.makedirs(out.parent, exist_ok=True)
    template = find_template(site, data)
    site.get_template(template).stream(**kwargs).dump(str(out), encoding="utf-8")


def find_template(site, data):
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
