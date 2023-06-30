import logging

import click

from algorun.core.sandbox import (
    ComposeFileStatus,
    ComposeSandbox,
)

logger = logging.getLogger(__name__)


@click.command("reset", short_help="Reset your Algorand mainnet node")
@click.option(
    "--update/--no-update",
    default=False,
    help="Enable or disable updating to the latest available Algod version, default: don't update",
)
def reset_command(*, update: bool) -> None:
    sandbox = ComposeSandbox()
    compose_file_status = sandbox.compose_file_status()
    if compose_file_status is ComposeFileStatus.MISSING:
        logger.debug("Existing node not found; creating from scratch...")
        sandbox.write_compose_file()
    else:
        sandbox.down()
        if compose_file_status is not ComposeFileStatus.UP_TO_DATE:
            logger.info("Node definition is out of date; updating it to latest")
            sandbox.write_compose_file()
        if update:
            sandbox.pull()
    sandbox.up()
