import click

from .extract_rate import extract_rate
from .remove_reference import remove_reference
from .randomise_dates import randomise_dates
from .prepare_metadata import prepare_metadata
from .plot_date_randomisation import plot_date_randomisation

VERSION = '0.1'


@click.group()
@click.version_option(version=VERSION)
def phybeast():

    """ Phybeast: phylodynamic analysis pipelines for bacterial pathogens """

    pass


phybeast.add_command(extract_rate)
phybeast.add_command(remove_reference)
phybeast.add_command(randomise_dates)
phybeast.add_command(prepare_metadata)
phybeast.add_command(plot_date_randomisation)