import click

from .download import download

VERSION = '0.1'


@click.group()
@click.version_option(version=VERSION)
def terminal_client():
    """ PathFinder: population genomic analysis pipelines for bacterial pathogens """
    pass

terminal_client.add_command(download)

