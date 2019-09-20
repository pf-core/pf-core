import click

from pathlib import Path


@click.command()
@click.option(
    '--data', '-d', help='Input data file'
)
def util(data, outdir, copy, delimiter, uuid):
    """ Template """



