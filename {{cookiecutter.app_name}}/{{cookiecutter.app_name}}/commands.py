# -*- coding: utf-8 -*-
"""Click commands."""
import os
from subprocess import call

import click

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, "tests")


@click.command()
def test():
    """Run the tests with code coverage report."""
    import pytest

    rv = pytest.main(
        [
            TEST_PATH,
            "--verbose",
            "--cov",
            "{{ cookiecutter.app_name }}",
            "--cov-report",
            "html",
            "--cov-report",
            "term",
        ]
    )
    exit(rv)


@click.command()
@click.option(
    "-f",
    "--fix-imports",
    default=True,
    is_flag=True,
    help="Fix imports using isort, before linting",
)
@click.option(
    "-c",
    "--check",
    default=False,
    is_flag=True,
    help="Don't make any changes to files, just confirm they are formatted correctly",
)
def lint(fix_imports, check):
    """Lint and check code style with black, flake8, and isort."""
    directories = ["{{ cookiecutter.app_name }}", "tests"]

    def execute_tool(description, *args):
        """Execute a checking tool with its arguments."""
        command_line = list(args) + directories
        click.echo(f"{description}: {' '.join(command_line)}")
        rv = call(command_line)
        if rv != 0:
            exit(rv)

    isort_args = []
    black_args = []
    if check:
        isort_args.append("--check")
        black_args.append("--check")
    if fix_imports:
        execute_tool("Fixing import order", "isort", *isort_args)
    execute_tool("Formatting style", "black", *black_args)
    execute_tool("Checking code style", "flake8")
