import importlib.metadata
import os


def application_name() -> str:
    return "ssss"


def application_description() -> str:
    long_description = importlib.metadata.metadata(application_name())["description"]
    short_description = long_description.split(".")[1]
    return application_name() + " - " + "".join([c for c in short_description if c.isalnum() or c.isspace()])


def application_version() -> str:
    return application_name() + " " + importlib.metadata.version(application_name())


def application_default_template_path() -> str:
    return "_templates"


def application_default_template_name() -> str:
    return "default"


def application_default_template_extension() -> str:
    return ".j2"


def application_default_output_extension() -> str:
    return ".html"


def application_default_encoding() -> str:
    return "utf8"


def application_default_data() -> str:
    return "*.md"


def application_default_rule() -> str:
    return "*" + application_default_template_extension()


def application_default_output() -> str:
    return "site" + os.sep + "build"


def application_default_source() -> str:
    return "site" + os.sep + "source"


def application_default_followlinks() -> bool:
    return True


def application_default_filters() -> dict:
    return {}


def application_default_site() -> dict:
    return {
        "title": "Site Name",
        "description": "Site Description",
        "author": "Site Author",
        "url": "https://example.com",
        "email": "asssa@example.com",
    }


def application_default_template_file() -> str:
    return application_default_template_name() \
        + application_default_template_extension()


def application_default_base_html() -> str:
    return "base.html"


def application_default_config_data() -> dict:
    return {
        "site": application_default_site(),
    }
