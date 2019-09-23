import click

from pathlib import Path
from pathfinder.utils import remove_sample


@click.command()
@click.option(
    "--alignment", "-a", default="input_alignment.fasta", help="Input alignment.", type=Path,
)
@click.option(
    "--output", "-o", default="output_alignment.fasta", help="Output alignment.", type=Path,
)
@click.option(
    "--remove", "-r", default="Reference", help="Remove sequences with this name."
)
def remove_reference(alignment, output, remove):

    """ Remove 'Reference' from Snippy alignment output file """

    remove_sample(alignment=alignment, outfile=output, remove='Reference')


