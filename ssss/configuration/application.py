import os
from pathlib import Path

import yaml

from ssss.common.application import application_default_config_data
from ssss.common.application.variables import application_default_template_path, application_default_template_file, \
    application_default_base_html, application_default_source, application_default_output, application_default_data, \
    application_default_encoding, application_default_followlinks, application_default_filters, \
    application_default_site, application_default_rule
from ssss.common.fs import find_config
from ssss.common.fs.directory import get_full_path, create_directory_if_not_exists, have_write_permission
from ssss.common.fs.file import touch_if_not_exists
from ssss.common.md import variables, rule
from ssss.configuration.arguments import Arguments
from ssss.configuration.default import config_file_path


class Application(Arguments):

    def __init__(self):
        self.config = {}
        self.__init_config = None

        super().__init__()

        self.data = application_default_config_data()

        if self.__init_config:
            self.init_config()

        if self.__config is None:
            self.__config = find_config()

        self.load_config()

    def __call__(self):
        return self.config

    def handle_args(self):
        self.parse.add_argument(
            "-c",
            "--config",
            help="Path to configuration file"
        )
        self.parse.add_argument(
            "--init",
            action="store_true",
            help="Initialize configuration file and glob_ext structure",
            default=False
        )
        args = self.parse.parse_args()

        if args.config is not None:
            if os.path.exists(args.config) and os.path.isfile(args.config):
                self.__config = os.path.abspath(args.config)
            else:
                self.__config = os.path.join(os.getcwd(), args.config)

        else:
            self.__config = None

        self.__init_config = args.init

    def load_config(self):
        with open(self.__config, "r") as file:
            yaml_data = yaml.safe_load(file)

        if yaml_data is not None:
            site_data = self.data.get("glob_ext", {}) | yaml_data.get("glob_ext", {})
            site_filters = self.data.get("filters", {}) | yaml_data.get("filters", {})
            self.data = self.data | yaml_data
            self.data["glob_ext"] = site_data
            self.data["filters"] = site_filters

            self.set_config()

            if self.__init_config:
                self.create_structure()

        else:
            raise NotImplementedError

    def set_config(self):
        self.data = {k: v for k, v in self.data.items() if v}
        self.config["searchpath"] = get_full_path(self.data.get("source", application_default_source()))
        self.config["outpath"] = get_full_path(self.data.get("output", application_default_output()))
        self.config["templates"] = get_full_path(
            self.data.get("templates", os.path.join(application_default_source(), application_default_template_path())))
        self.config["contexts"] = [(self.data.get("data", application_default_data()), variables)]
        self.config["rules"] = [(self.data.get("data", application_default_rule()), rule.execute)]
        self.config["encoding"] = str(self.data.get("encoding", application_default_encoding()))
        self.config["followlinks"] = str(self.data.get("followlinks", application_default_followlinks()))
        self.config["filters"] = dict(self.data.get("filters", application_default_filters()))
        self.config["env_globals"] = dict(self.data.get("glob_ext", application_default_site()))

    def init_config(self):

        if self.__config is None:
            config_path = config_file_path()
        else:
            config_path = Path(self.__config)

        self.__config = config_path.absolute()

        if have_write_permission(config_path.parent):
            if not config_path.exists():
                with open(config_path, "w") as file:
                    yaml.dump(application_default_config_data(), file)
        else:
            raise PermissionError

    def __getitem__(self, item):
        return self.config[item]

    def create_structure(self):
        base_html = os.path.join(
            self.config["searchpath"],
            application_default_template_path(),
            application_default_base_html()
        )

        default_template = os.path.join(
            self.config["searchpath"],
            application_default_template_path(),
            application_default_template_file()
        )

        index_md = os.path.join(
            os.path.join(
                self.config["searchpath"],
                "index.md"
            )
        )

        default_template_path = os.path.join(
            self.config["searchpath"],
            application_default_template_path()
        )

        create_directory_if_not_exists(self.config["outpath"])
        create_directory_if_not_exists(self.config["searchpath"])
        create_directory_if_not_exists(default_template_path)
        touch_if_not_exists(default_template)
        touch_if_not_exists(index_md)
        touch_if_not_exists(base_html)
