import logging

import click

from algorun.core.sandbox import (
    ComposeFileStatus,
    ComposeSandbox,
)

logger = logging.getLogger(__name__)


@click.command("stop", short_help="Stop your Algorand mainnet node")
def stop_command() -> None:
    sandbox = ComposeSandbox()
    compose_file_status = sandbox.compose_file_status()
    if compose_file_status is ComposeFileStatus.MISSING:
        logger.debug("Docker compose file does not exist yet; run `algorun start` to start the maiinnet node")
    else:
        sandbox.stop()
