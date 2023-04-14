from pathlib import Path
import markdown


def variables(template):
    md = markdown.Markdown(extensions=["meta"])
    markdown_content = Path(template.filename).read_text()
    returned_variables = {"content": md.convert(markdown_content)} | md.Meta

    for key, value in returned_variables.items():
        if isinstance(value, list) and len(value) == 1:
            returned_variables[key] = value[0]

    return returned_variables
