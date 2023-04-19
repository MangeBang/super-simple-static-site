import os
import subprocess
from os import unlink

from ssss.common.fs import make_empty
from ssss.common.fs.file import touch_if_not_exists


def run_ssss(*args):
    result = subprocess.run(["ssss"] + list(args), capture_output=True, text=True)
    return result.stdout, result.returncode


def test_ssss_no_args():
    output, returncode = run_ssss()
    assert returncode == 1
    assert "No configuration file found" in output


def test_ssss_no_args_after_init():
    output, returncode = run_ssss("--init", "-c", "test.yml")
    assert returncode == 0
    assert "Baking /home/magnus/Repos/Python/staticjinja/ssss/site/source/index.md" in output

    output, returncode = run_ssss("-c", "test.yml")
    assert returncode == 0
    assert "Baking /home/magnus/Repos/Python/staticjinja/ssss/site/source/index.md" in output

    unlink('test.yml')
    make_empty('glob_ext', True)


def test_ssss_no_args_after_init_with_empty_config():
    touch_if_not_exists('test.yml')
    output, returncode = run_ssss("-c", "test.yml")

    assert returncode == 1
    assert "Configuration file is empty." in output

    unlink('test.yml')


def test_ssss_short_help():
    output, returncode = run_ssss("-h")
    assert returncode == 0
    assert "-h, --help" in output and "show this help message and exit" in output


def test_ssss_long_help():
    output, returncode = run_ssss("--help")
    assert returncode == 0
    assert "-h, --help" in output and "show this help message and exit" in output


def test_ssss_init():
    output, returncode = run_ssss("--init")
    assert returncode == 0

    with open('ssss.yml', 'r') as f:
        actual_contents = f.read()

    with open('tests/data/ssss.yml', 'r') as f:
        expected_contents = f.read()

    unlink('ssss.yml')

    assert actual_contents == expected_contents


def test_ssss_init_with_config():
    output, returncode = run_ssss("--init", "--config", "custom_config.yaml")
    assert returncode == 0

    with open('custom_config.yaml', 'r') as f:
        actual_contents = f.read()

    with open('tests/data/ssss.yml', 'r') as f:
        expected_contents = f.read()

    unlink('custom_config.yaml')

    assert actual_contents == expected_contents


def test_ssss_init_file_structure():
    output, returncode = run_ssss("--init")
    assert returncode == 0

    site_exists = os.path.exists('site')
    source_exists = os.path.exists('site/source/index.md')
    template_exists = os.path.exists('site/source/_templates/default.j2')
    base_exists = os.path.exists('site/source/_templates/base.html')
    data_exists = os.path.exists('site/build/index.html')

    unlink('ssss.yml')
    make_empty('site', True)
    assert site_exists and source_exists and template_exists and base_exists and data_exists
