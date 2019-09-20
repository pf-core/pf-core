#!/usr/env/bin python

import click

from pathfinder.utils import remove_sample


@click.command()
@click.option(
    "--alignment", "-a", default="input_alignment.fasta", help="Input alignment."
)
@click.option(
    "--output", "-o", default="output_alignment.fasta", help="Output alignment."
)
@click.option(
    "--remove", "-r", default="Reference", help="Remove sequencence with this name."
)
def remove_reference(alignment, outfile):

    """ Remove 'Reference' from Snippy alignment output file """

    remove_sample(alignment=alignment, outfile=outfile, remove='Reference')

