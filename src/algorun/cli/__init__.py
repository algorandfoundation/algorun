import click

from algorun.cli.bootstrap import bootstrap_group
from algorun.cli.goal import goal_command
from algorun.cli.start import start_command
from algorun.cli.stop import stop_command
from algorun.core.conf import PACKAGE_NAME
from algorun.core.log_handlers import color_option, verbose_option
from algorun.core.version_prompt import do_version_prompt, skip_version_check_option


@click.group(
    context_settings={
        "help_option_names": ["-h", "--help"],
        "max_content_width": 120,
    },
)
@click.version_option(package_name=PACKAGE_NAME)
@verbose_option
@color_option
@skip_version_check_option
def algorun(*, skip_version_check: bool) -> None:
    """
    ░█████╗░██╗░░░░░░██████╗░░█████╗░██████╗░░█████╗░███╗░░██╗██████╗░
    ██╔══██╗██║░░░░░██╔════╝░██╔══██╗██╔══██╗██╔══██╗████╗░██║██╔══██╗
    ███████║██║░░░░░██║░░██╗░██║░░██║██████╔╝███████║██╔██╗██║██║░░██║
    ██╔══██║██║░░░░░██║░░╚██╗██║░░██║██╔══██╗██╔══██║██║╚████║██║░░██║
    ██║░░██║███████╗╚██████╔╝╚█████╔╝██║░░██║██║░░██║██║░╚███║██████╔╝
    ╚═╝░░╚═╝╚══════╝░╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░"""
    if not skip_version_check:
        do_version_prompt()


algorun.add_command(start_command)
algorun.add_command(stop_command)
algorun.add_command(goal_command)
algorun.add_command(bootstrap_group)
