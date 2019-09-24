import subprocess
import shlex
import sys
import dendropy
import pandas
import pysam
from random import shuffle
from pathlib import Path

import matplotlib.pyplot as plt

from pathfinder.plots import plot_date_randomisation, plot_regression


def run_cmd(cmd, callback=None, watch=False, background=False, shell=False):

    """ Runs the given command and gathers the output.

    If a callback is provided, then the output is sent to it, otherwise it
    is just returned.

    Optionally, the output of the command can be "watched" and whenever new
    output is detected, it will be sent to the given `callback`.

    Returns:
        A string containing the output of the command, or None if a `callback`
        was given.
    Raises:
        RuntimeError: When `watch` is True, but no callback is given.

    """

    if watch and not callback:
        raise RuntimeError(
            "You must provide a callback when watching a process."
        )

    output = None
    try:
        if shell:
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        else:
            proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)

        if background:
            # Let task run in background and return pmid for monitoring:
            return proc.pid, proc

        if watch:
            while proc.poll() is None:
                line = proc.stdout.readline()
                if line != "":
                    callback(line)

            # Sometimes the process exits before we have all of the output, so
            # we need to gather the remainder of the output.
            remainder = proc.communicate()[0]
            if remainder:
                callback(remainder)
        else:
            output = proc.communicate()[0]
    except:
        err = str(sys.exc_info()[1]) + "\n"
        output = err

    if callback and output is not None:
        return callback(output)

    return output


# Survey support functions

def get_aspera_key() -> Path:

    """ Return path to aspera key for connections to ENA """

    return Path(__file__).parent / "resources" / "asperaweb_id_dsa.openssh"


def get_genome_sizes() -> pandas.DataFrame:

    """ Return a dataframe from the `genome.size` file in `pathfinder.resources`

    Genome sizes are computed as media genome size for given taxonomic
    identifier from the NCBI Prokaryot DB.

    :return Dataframe with one column size and row index taxid

    """

    genome_sizes = Path(__file__).parent / "resources" / "genome.sizes"
    genome_sizes = pandas.read_csv(genome_sizes, index_col=0)

    return genome_sizes


# Alignment support functions

def remove_sample(alignment: Path, outfile: Path, remove: str or list) -> None:

    """ Remove any sequence from the alignment file by sequence names

    :param alignment: alignment file (.fasta)
    :param outfile: output file (.fasta)
    :param remove: sequence identifiers to remove

    :return:  None, outputs alignment file with sequences removed

    """

    if isinstance(remove, str):
        remove = [remove]

    with pysam.FastxFile(alignment) as fin, outfile.open('w') as fout:
            for entry in fin:
                if entry.name not in remove:
                    fout.write(str(entry) + '\n')


# Phylogenetics support functions

def get_tree_dates(newick_file: Path) -> pandas.DataFrame:

    """ Get the leaf names and dates from the input tree

    :param newick_file: tree file in newick format

    :returns `pandas.DataFrame` with two columns: name, date

    """

    tree = dendropy.Tree.get(path=newick_file, schema="newick")

    return pandas.DataFrame(
        data=[taxon.label.split() for taxon in tree.taxon_namespace],
        columns=['name', 'date']
    )


# Phybeast support functions



def phybeast_randomise_date_file(
    date_file: Path,
    output_file: Path = None
) -> pandas.DataFrame:

    """ Randomise order of dates in file

    DataFrame input options can be passed as **kwargs

    :param date_file: path to date file with columns: name and date
    :param output_file: path to tab-delimited output file for randomised dates

    :returns DataFrame with shuffled dates

    :raises ValueError if date and name not in column headers

    """

    df = pandas.read_csv(date_file, sep='\t')

    if 'date' not in df.columns or 'name' not in df.columns:
        raise ValueError('Could not find date and name in columns')

    # Suppress warning
    with pandas.option_context('mode.chained_assignment', None):
        dates = df.date
        shuffle(dates)
        df.date = dates

    if output_file is not None:
        df.to_csv(output_file, sep='\t', header=True, index=False)

    return df


def phybeast_prepare_metadata_file(
    meta_file: Path,
    prep: str = 'lsd2',
    output_file: Path = Path.cwd() / 'lsd2.meta'
) -> None:

    """ Prepare the tab-delimited input file for pf-phybeast

    :param meta_file: tab-delimited meta data file with columns: name, date
    :param prep: output file type to prepare for: lsd2, treetime
    :param output_file: output file path

    :returns None, writes to file :param out_file

    """

    df = pandas.read_csv(meta_file, sep='\t')

    if 'date' not in df.columns or 'name' not in df.columns:
        raise ValueError('Could not find date and name in columns')

    if prep == 'treetime':
        df.to_csv(output_file, header=True, sep=',', index=False)

    if prep == 'lsd2':
        with output_file.open('w') as outfile:
            outfile.write(
                f'{len(df)}\n'
            )

            # TODO: document no spaces in unique ids
            df[['name', 'date']].to_csv(
                outfile, header=False, sep=' ', index=False
            )


def phybeast_extract_rate(
    result_file: Path,
    prep: str = 'lsd2',
    output_file: Path = Path.cwd() / 'rate.txt'
) -> None:

    """ Prepare the tab-delimited input file for pf-phybeast

    :param result_file: path to summary output file from: lsd2 or treetime
    :param prep: output file type to prepare for: lsd2 or treetime
    :param output_file: Output file path

    :returns None, writes to file :param output_file

    """

    if prep == 'lsd2':

        with result_file.open('r') as infile, output_file.open('w') as outfile:
            for line in infile:
                if line.strip().startswith('rate'):
                    rate = float(
                        line.strip().split()[1].strip(',')
                    )
                    tmrca = float(
                        line.strip().split()[3].strip(',')
                    )
                    print(rate, tmrca)
                    outfile.write(f"{rate}\t{tmrca}\n")


def phybeast_plot_date_randomisation(
    replicate_file: Path,
    rate_file: Path,
    output_file: Path = Path("date_randomisation.png"),
    regression_file: Path = None
) -> None:

    """ Plot distribution of date randomised substitution rates

    :param replicate_file: `rates.tab` with replicates from `DateRandomisationPlot`
    :param rate_file: `rate.txt` containing true rate from `MolecularClock`
    :param output_file: output plot file, format by extension
    :param regression_file: `rtt.csv` file from TimeTree clock regression

    :returns None, writes to file :param output_file

    """

    # one panel:
    if regression_file is None:
        fig, ax1 = plt.subplots(figsize=(27.0, 9))
        ax2 = None
    else:
        fig, axes = plt.subplots(ncols=2, figsize=(27.0, 9))
        ax2, ax1 = axes.flatten()  # observe order

    # Date Randomisation

    replicate_df = pandas.read_csv(
        replicate_file, sep='\t', names=['replicate', 'tmrca']
    )

    replicates = replicate_df.replicate.tolist()

    rate_df = pandas.read_csv(
         rate_file, sep='\t', names=['rate', 'tmrca']
    )

    rate = float(rate_df.iloc[0, 0])

    plot_date_randomisation(
        ax=ax1, replicates=replicates, rate=rate
    )

    # Regression plot
    if regression_file is not None:
        # Regression file from TimeTree
        data = pandas.read_csv(
            regression_file, skiprows=2, header=None,
            names=['name', 'date', 'distance']
        )
        plot_regression(
            ax=ax2, regression_data=data.iloc[:, 1:]
        )

    fig.savefig(output_file)




