def application_name() -> str:
    return "ssss"


def application_description() -> str:
    return "ssss or super simple static site, a static site generator templated with jinja and markdown."


def application_version() -> str:
    return "0.0.0a0.post0.dev2"


def application_template_path() -> str:
    return "_templates"


def application_default_config_data() -> dict:
    return {
        "source": "site/source",
        "output": "site/build",
        "data": r".*\.md",
        "encoding": "utf8",
        "followlinks": True,
        "filters": {},
        "globals": {},
    }
