import click

VERSION = '0.1'


@click.group()
@click.version_option(version=VERSION)
def terminal_client():
    """ Elasmobranch Reference Genome Consortium: Python Toolkit """
    pass
