from jinja2 import FileSystemLoader, Environment

from ssss.common.application.variables import application_default_output_extension, application_default_template_file


def execute(rules_ext, baked_variables, config):
    templates = config["templates"]
    output = config["outpath"]
    env = Environment(loader=FileSystemLoader(templates), autoescape=False)
    for context in baked_variables:
        template = env.get_template(find_template(env, context, rules_ext))
        template.stream(**context).dump(
            output + "/" + context["file_path"].stem + application_default_output_extension())


def find_template(env, data, rules_ext):
    template = data["file_path"].stem + rules_ext.split("*")[1]
    if template in env.list_templates():
        return template
    else:
        return application_default_template_file()
