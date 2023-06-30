import click
from algorun.core.version_prompt import version_prompt_configuration_command


@click.group("config", short_help="Configure algorun settings.")
def config_group() -> None:
    """Configure settings used by algorun"""


config_group.add_command(version_prompt_configuration_command)
