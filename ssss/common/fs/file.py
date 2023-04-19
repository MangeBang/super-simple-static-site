import os
from pathlib import Path

from ssss.common.application import application_name
from ssss.common.fs.directory import get_user_config_directory, get_current_directory


def find_config() -> str:
    found = search_config_in_dirs()
    if found is not None:
        return found
    else:
        raise FileNotFoundError


def application_config_file_extension() -> list[str]:
    return [".yml", ".yaml"]


def search_config_in_dir(directory) -> str | None:
    for ext in application_config_file_extension():
        if os.path.exists(directory + "/" + application_name() + ext) and os.path.isfile(
                directory + "/" + application_name() + ext):
            return os.path.abspath(directory + "/" + application_name() + ext)
    return None


def search_config_in_dirs() -> str | None:
    directories = [
        get_current_directory(),
        get_user_config_directory(),
    ]

    for directory in directories:
        found = search_config_in_dir(directory)
        if found is not None:
            return found
    return None


def touch_if_not_exists(path) -> bool:
    exists = os.path.exists(path)
    if not exists:
        Path(path).touch()

    return exists
