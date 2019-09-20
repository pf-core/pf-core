import subprocess
import shlex
import sys
import dendropy
import pandas
import pysam
from pathlib import Path


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


# Alignment support functions

def remove_sample(alignment: Path, outfile: Path, remove: str or list) -> None:

    """ Remove any sequence from the alignment file by sequence name or list of sequence names

    :param alignment: alignment file (.fasta)
    :param outfile: output file (.fasta)
    :param remove: sequence identifiers to remove

    :return:  None, outputs alignment file with sequences removed

    """

    if isinstance(remove, str):
        remove = [remove]

    with pysam.FastxFile(alignment) as fin, outfile.open(mode='w') as fout:
        for entry in fin:
            if entry.name not in remove:
                fout.write(str(entry))


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


def randomise_date_file(date_file: Path, output_file: Path = None, **kwargs) -> pandas.DataFrame:

    """ Randomise order of dates in file

    DataFrame input options can be passed as **kwargs

    :param date_file: Path to date file with columns: name and date
    :param output_file: Path to tab-delimited output file for randomised dates
    :param kwargs: Additional arguments passed to `pandas.read_csv`

    :returns DataFrame with shuffled

    """

    df = pandas.read_csv(date_file, **kwargs)
    df['date'] = df.drop('name', axis=1).sample(frac=1).reset_index()

    if output_file is not None:
        df.to_csv(output_file, sep='\t', header=None, index=False)

    return df


def plot_date_randomisation():

    pass
