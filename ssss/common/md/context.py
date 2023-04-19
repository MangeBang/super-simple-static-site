from pathlib import Path

import markdown


def variables(match_value, search_path):
    source = Path(search_path)
    returned_variables = []

    for file in source.iterdir():
        if file.match(match_value):
            print("Baking " + str(file) + "...")
            returned_variables.append(parse(file))

    return returned_variables


def parse(context_file):
    file_path = Path(context_file)
    md = markdown.Markdown(extensions=["meta"])
    markdown_content = file_path.read_text()
    returned_variables = {"content": md.convert(markdown_content), "file_path": file_path} | md.Meta
    for key, value in returned_variables.items():
        if isinstance(value, list) and len(value) == 1:
            returned_variables[key] = value[0]

    returned_variables["content"] = handle_meta_variables(returned_variables, returned_variables["content"], md=md)

    return returned_variables


def handle_meta_variables(meta_vars, content, md=markdown.Markdown(extensions=["meta"])):
    from jinja2 import Environment

    env = Environment()
    template = env.from_string(content)
    return md.convert(template.render(**meta_vars))
