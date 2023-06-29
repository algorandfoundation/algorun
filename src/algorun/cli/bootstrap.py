import logging
from pathlib import Path

import click

from algorun.core.bootstrap import (
    bootstrap_any_including_subdirs,
    bootstrap_env,
    bootstrap_poetry,
    project_minimum_algorun_version_check,
)

logger = logging.getLogger(__name__)


@click.option(
    "force", "--force", is_flag=True, default=False, help="Continue even if minimum algorun version is not met"
)
@click.group(
    "bootstrap", short_help="Bootstrap local dependencies in an algorun project; run from project root directory."
)
def bootstrap_group(*, force: bool) -> None:
    """
    Expedited initial setup for any developer by installing and configuring dependencies and other
    key development environment setup activities.
    """
    project_minimum_algorun_version_check(Path.cwd(), ignore_version_check_fail=force)


@bootstrap_group.command(
    "all", short_help="Runs all bootstrap sub-commands in the current directory and immediate sub directories."
)
def bootstrap_all() -> None:
    cwd = Path.cwd()
    bootstrap_any_including_subdirs(cwd)
    logger.info(f"Finished bootstrapping {cwd}")


@bootstrap_group.command(
    "env",
    short_help="Copies .env.template file to .env in the current working directory "
    "and prompts for any unspecified values.",
)
def env() -> None:
    bootstrap_env(Path.cwd())


@bootstrap_group.command(
    "poetry",
    short_help="Installs Python Poetry (if not present) and runs `poetry install` in the "
    "current working directory to install Python dependencies.",
)
def poetry() -> None:
    bootstrap_poetry(Path.cwd())
