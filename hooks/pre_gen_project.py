import logging
import re
import sys

logging.basicConfig()
_logger = logging.getLogger(__name__)
MODULE_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"


class bcolors:
    WARNING = "\033[93m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


def colorize(escape_code, text):
    code = getattr(bcolors, escape_code)
    return "{code}{text}{end_code}".format(code=code, text=text, end_code=bcolors.ENDC)


def log_module_name_warning(module_name, logger):
    warning = (
        "\n{warning} {fmt_module_name}"
        " is not a valid Python module name!\n"
        "See https://www.python.org/dev/peps/pep-0008/#package-and-module-names"
        " for naming standards.\n"
    ).format(
        warning=colorize("WARNING", "WARNING:"),
        fmt_module_name=colorize("BOLD", module_name),
    )
    logger.warning(warning)


def validate_python_module_name():
    module_name = "{{ cookiecutter.app_name }}"
    if not re.match(MODULE_REGEX, module_name):
        log_module_name_warning(module_name, _logger)
        sys.exit(1)


if __name__ == "__main__":
    validate_python_module_name()
