import logging

import click
from algorun.core import proc
from algorun.core.sandbox import (
    DOCKER_COMPOSE_MINIMUM_VERSION,
    DOCKER_COMPOSE_VERSION_COMMAND,
    ComposeFileStatus,
    ComposeSandbox,
)
from algorun.core.utils import extract_version_triple, is_minimum_version

logger = logging.getLogger(__name__)


@click.command("start", short_help="Start your Algorand mainnet node")
def start_command() -> None:
    try:
        compose_version_result = proc.run(DOCKER_COMPOSE_VERSION_COMMAND)
    except OSError as ex:
        # an IOError (such as PermissionError or FileNotFoundError) will only occur if "docker"
        # isn't an executable in the user's path, which means docker isn't installed
        raise click.ClickException(
            "Docker not found; please install Docker and add to path.\n"
            "See https://docs.docker.com/get-docker/ for more information."
        ) from ex
    if compose_version_result.exit_code != 0:
        raise click.ClickException(
            "Docker Compose not found; please install Docker Compose and add to path.\n"
            "See https://docs.docker.com/compose/install/ for more information."
        )

    try:
        compose_version_str = extract_version_triple(compose_version_result.output)
        compose_version_ok = is_minimum_version(compose_version_str, DOCKER_COMPOSE_MINIMUM_VERSION)
    except Exception:
        logger.warning(
            "Unable to extract docker compose version from output: \n"
            + compose_version_result.output
            + f"\nPlease ensure a minimum of compose v{DOCKER_COMPOSE_MINIMUM_VERSION} is used",
            exc_info=True,
        )
    else:
        if not compose_version_ok:
            raise click.ClickException(
                f"Minimum docker compose version supported: v{DOCKER_COMPOSE_MINIMUM_VERSION}, "
                f"installed = v{compose_version_str}\n"
                "Please update your Docker install"
            )

    proc.run(["docker", "version"], bad_return_code_error_message="Docker engine isn't running; please start it.")
    sandbox = ComposeSandbox()
    compose_file_status = sandbox.compose_file_status()
    if compose_file_status is ComposeFileStatus.MISSING:
        logger.debug("Docker compose file does not exist yet; writing it out for the first time")
        sandbox.write_compose_file()
    elif compose_file_status is ComposeFileStatus.UP_TO_DATE:
        logger.debug("Docker compose file does not require updating")
    else:
        logger.warning("Docker definition is out of date; please run algorun localnet reset")
    sandbox.up()
