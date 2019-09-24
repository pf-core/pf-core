import click

from .utils import client


VERSION = '0.1'


@click.group()
@click.version_option(version=VERSION)
def phybeast():

    """ Phybeast: phylodynamic analysis pipelines for bacterial pathogens """

    pass


phybeast.add_command(client.utils)
