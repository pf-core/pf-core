import click

from pathlib import Path
from pathfinder.utils import phybeast_plot_date_randomisation


@click.command()
@click.option(
    "--file", "-f", type=Path,
    help="Replicate rate file from process DateRandomisationPlot",
)
@click.option(
    "--rate", "-r", type=Path,
    help="True rate file from process MolecularClock; one line.",
)
@click.option(
    "--output", "-o", default="date_randomisation.png",
    help="Output plot file; set extension for format.", type=Path,
)
@click.option(
    "--regression", type=Path, default=None,
    help="Regression data file  from process DateRegression.",
)
def plot_date_randomisation(file, output, rate, regression):

    """ Plot date randomisation test by Duchene et al. """

    phybeast_plot_date_randomisation(
        replicate_file=file,
        rate_file=rate,
        output_file=output,
        regression_file=regression
    )


