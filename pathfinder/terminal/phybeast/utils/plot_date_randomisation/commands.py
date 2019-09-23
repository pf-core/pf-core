import click

from pathlib import Path
from pathfinder.plots import phybeast_plot_date_randomisation


@click.command()
@click.option(
    "--file", "-f", default="lsd.out", type=Path,
    help="Replicate rate file output from process ClockReplicate",
)
@click.option(
    "--output", "-o", default="date_randomisation.png",
    help="Output plot file; set extension for format.", type=Path,
)
@click.option(
    "--rate", "-r", default="rate.txt", type=Path,
    help="True rate of data set from process MolecularClock; one line.",
)
def plot_date_randomisation(file, output, rate):

    """ Plot date randomisation test by Duchene et al. """

    phybeast_plot_date_randomisation(file=file, output=output, rate=rate)


