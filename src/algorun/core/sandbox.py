import enum
import json
import logging
from pathlib import Path
from typing import Any, cast

from algorun.core.conf import get_app_config_dir
from algorun.core.proc import RunResult, run, run_interactive

logger = logging.getLogger(__name__)


DOCKER_COMPOSE_MINIMUM_VERSION = "2.5.0"


class ComposeFileStatus(enum.Enum):
    MISSING = enum.auto()
    UP_TO_DATE = enum.auto()
    OUT_OF_DATE = enum.auto()


class ComposeSandbox:
    def __init__(self) -> None:
        self.directory = get_app_config_dir()
        if not self.directory.exists():
            logger.debug("Node directory does not exist yet; creating it")
            self.directory.mkdir()
        self._latest_yaml = get_docker_compose_yml()
        self._latest_config_json = get_config_json()

    @property
    def compose_file_path(self) -> Path:
        return self.directory / "docker-compose.yml"

    @property
    def algod_config_file_path(self) -> Path:
        return self.directory / "config.json"

    def compose_file_status(self) -> ComposeFileStatus:
        try:
            compose_content = self.compose_file_path.read_text()
            config_content = self.algod_config_file_path.read_text()
        except FileNotFoundError:
            # treat as out of date if compose file exists but algod config doesn't
            # so that existing setups aren't suddenly reset
            if self.compose_file_path.exists():
                return ComposeFileStatus.OUT_OF_DATE
            return ComposeFileStatus.MISSING
        else:
            if compose_content == self._latest_yaml and config_content == self._latest_config_json:
                return ComposeFileStatus.UP_TO_DATE
            else:
                return ComposeFileStatus.OUT_OF_DATE

    def write_compose_file(self) -> None:
        self.compose_file_path.write_text(self._latest_yaml)
        self.algod_config_file_path.write_text(self._latest_config_json)

    def _run_compose_command(
        self,
        compose_args: str,
        stdout_log_level: int = logging.INFO,
        bad_return_code_error_message: str | None = None,
    ) -> RunResult:
        return run(
            ["docker", *compose_args.split()],
            cwd=self.directory,
            stdout_log_level=stdout_log_level,
            bad_return_code_error_message=bad_return_code_error_message,
        )

    def up(self) -> None:
        logger.info("Starting Algorand mainnet node now...")
        self._run_compose_command(
            "compose up -d",
            bad_return_code_error_message="Failed to start node",
        )
        logger.info("Started; the node is now catching up to the latest ledger state")

    def stop(self) -> None:
        logger.info("Stopping Algorand mainnet node now...")
        self._run_compose_command("compose stop", bad_return_code_error_message="Failed to stop node")
        logger.info("Node Stopped; execute `algorun start` to start it again.")

    def down(self) -> None:
        logger.info("Deleting current node...")
        self._run_compose_command("down", stdout_log_level=logging.DEBUG)

    def pull(self) -> None:
        logger.info("Looking for latest algod images from DockerHub...")
        self._run_compose_command("pull --ignore-pull-failures --quiet")

    def logs(self, *, follow: bool = False, no_color: bool = False, tail: str | None = None) -> None:
        compose_args = ["logs"]
        if follow:
            compose_args += ["--follow"]
        if no_color:
            compose_args += ["--no-color"]
        if tail is not None:
            compose_args += ["--tail", tail]
        run_interactive(
            ["docker", "compose", *compose_args],
            cwd=self.directory,
            bad_return_code_error_message="Failed to get logs, are the containers running?",
        )

    def ps(self, service_name: str | None = None) -> list[dict[str, Any]]:
        run_results = self._run_compose_command(
            f"ps {service_name or ''} --format json", stdout_log_level=logging.DEBUG
        )
        if run_results.exit_code != 0:
            return []
        data = json.loads(run_results.output)
        assert isinstance(data, list)
        return cast(list[dict[str, Any]], data)


def get_config_json() -> str:
    return '{"Version":27, "MaxCatchpointDownloadDuration": 604800000000000}'


def get_docker_compose_yml() -> str:
    return """version: '3'

services:
  algod:
    container_name: mainnet-container
    image: algorand/algod:latest
    ports:
      - 4190:8080
    environment:
      - NETWORK=mainnet
      - FAST_CATCHUP=1
      - PROFILE=participation
    volumes:
      - ${PWD}/data:/algod/data/:rw
      - ${PWD}/config.json:/etc/algorand/config.json:rw

networks:
  host:
    external: true
"""


DOCKER_COMPOSE_VERSION_COMMAND = ["docker", "compose", "version", "--format", "json"]
