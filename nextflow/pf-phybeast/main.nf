#!/usr/bin/env nextflow

/*
 *
 *  Pipeline            PhyBeast
 *  Version             0.1
 *  Description         Genomic epidemiology and phylodynamics workflows
                        for bacterial pathogens
 *   Authors            Eike Steinig, Michael Meehan, Sebastian Duchene
                        Steven Tong, Emma Mcbryde
 *
 */

log.info """

|========================|
|                        |
|========================|
|            ||          |
|            ||          |
|            ||          |
|===================================================|
|                     PHYBEAST                      |
|                       v0.1                        |
|===================================================|
|||     |||     |||         |||         |||       |||
|||     |||     |||         |||         |||       |||
|||     |||     |||         |||         |||       |||

    PE reads:             $params.fastq
    Outdir:               $params.outdir
    Metadata:             $params.metadata
    Reference:            $params.reference
    Recombination:        $params.recombination
    Phylogeny:            $params.phylogeny
    Molecular clock:      $params.clock

|||     |||     |||         |||         |||       |||
|||     |||     |||         |||         |||       |||
|||     |||     |||         |||         |||       |||
|===================================================|
|===================================================|


"""

help = """
================================================================================
                                 PHYBEAST
                                   v0.1
================================================================================

Phylodynamic workflows for bacterial pathogens.

Required Parameters:

-f|--fastq     Glob for parsing read files (.fastq) in format: {id}_{1,2}.fastq.gz
-r|--reference FASTA reference genome file for alignment and variant calling: {ref}.fasta
-m|--metadata  CSV metadata file with columns: name, date, where name corresponds to {id}


Optional Parameters:

-a|--alignment Precomputed FASTA alignment for prep-flows

-v|--variants  Aligner and variant calling prep-flow [1]
-r|--recomb    Recombination removal prep-flow [1]
-p|--phylogeny Phylogeny construction prep-flow [3]
-c|--clock     Molecular clock assessment prep-flow [1]

Preparation
===========

Variant Calling:

    - 1: Snippy - BWA-MEM -> Freebayes -> snippy-core
    - 2: Spandx - BWA-MEM [minimap2] -> GATK

Recombination:

    - 1: Gubbins - Gubbins recombination, SNP-sites

Phylogeny:

    - 1: RAxML-NG   -   GTR+G + [ASC, BS]
    - 2: FastTree2  -   GTR+G + [BS]
    - 3: PhyML      -   Branch swapping + NNJ + [ASC, BS]


================================================================================

Substitution rate, time-scaled phylogeny
----------------------------------------

    - Root-to-tip regression
    - Date randomisation test
    - Time-scaled phylogenetic tree, MRCA
    - Estimated or fixed substitution rates
    - Estimated dates for missing data

    TimeTree, LSD, Rscripts, Pyscripts

    https://github.com/pf-core/pf-phybeast/docs/substitution.md

Basic reproductive number (R0):
-------------------------------

    BEAST2 computation of changes in basic reproductive number (R0)
    over over decades, going back from the last sampled pathogen in
    the alignment. May be calibrated via phylogenetic trees from the
    phylogeny construction workflow. See manual at:

    BEAST2

    https://github.com/pf-core/pf-phybeast/docs/r0.md

Effective population size (Ne):
-------------------------------

    BEAST2 computation of effective population size changes over time.


================================================================================


Each subworkflow is configured to produce plots summarizing
the analysis and anlysis of analysis.


================================================================================
================================================================================
"""

reference = file(params.reference)  // Declare as file (necessary)
metadata = file(params.metadata)  // Declare as file (necessary)

fastq = Channel
		.fromFilePairs("${params.fastq}", flat: true)
		.ifEmpty { exit 1, "Input read files could not be found." }


process Trimmomatic {

    label "data"
    tag { id }

    input:
    set id, file(forward), file(reverse) from fastq

    output:
    set id, file("${id}_1_paired.fq.gz"), file("${id}_2_paired.fq.gz") into alignment

    """
    trimmomatic PE -threads $task.cpus $forward $reverse \
    ${id}_1_paired.fq.gz ${id}_1_unpaired.fq.gz ${id}_2_paired.fq.gz ${id}_2_unpaired.fq.gz \
    ILLUMINACLIP:${baseDir}/resources/all_adapters.fa:2:30:10: \
    LEADING:10 TRAILING:10 SLIDINGWINDOW:4:15 MINLEN:36
    """

}

process Snippy {

  label "alignment"

  input:
  set id, file(forward), file(reverse) from alignment

  output:
  file("$id") into core_alignment

  """
  snippy --cpus $task.cpus --ram $task.memory --outdir $id --prefix $id \
  --reference $reference --R1 $forward --R2 $reverse
  """

}


// Produces core SNP alignment substituted into reference genome sequence

process SnippyCore {

  label "data"

  publishDir "${params.outdir}", mode: "copy"

  input:
  file(snippy_outputs) from core_alignment.collect()

  output:
  file("core.alignment.fasta") into recombination
  file("core.aln")

  """
  snippy-core --ref $reference --prefix core $snippy_outputs
  snippy-clean_full_aln core.aln > clean.alignment.fasta
  pathfinder phybeast utils remove-reference -a clean.alignment.fasta -o core.alignment.fasta
  """

}

// Remove recombination from the substituted reference genome alignment
// Output only sites containing exclusively ACGT (-c) in Gubbins

process Gubbins {

  label "recombination"
  tag { "$core_alignment" }

  publishDir "${params.outdir}", mode: "copy"

  input:
  file(core_alignment) from recombination

  output:
  file("core.alignment.recombination.fasta") into (phylogeny, clock_align, tree_align, reg_align, rep_align)

  """
  run_gubbins.py -p gubbins --threads $task.cpus $core_alignment
  snp-sites -c gubbins.filtered_polymorphic_sites.fasta > core.alignment.recombination.fasta
  """

}

// TreeBuilders

// Default ascertainment bias (Lewis) correction using core SNPs

process Phylogeny {

  label "phylogeny"
  tag { "$alignment" }

  input:
  file(alignment) from phylogeny

  output:
  file("tree.newick") into ( phylo, phylo_randomisation, phylo_regression )


  script:

  if (params.phylogeny == 'raxml')

    """
    raxml-ng --msa $alignment --model $params.model \
    --threads $task.cpus --prefix phylo --force

    mv phylo.raxml.bestTree tree.newick
    """

  else if (params.phylogeny == 'phyml')

    """
    goalign reformat -i $alignment phylip > aln.phy
    phyml -i phy
    """

  else if (params.phylogeny == 'fasttree')

    """
    FastTree -gtr -nt $alignment > tree.newick
    """


}

// Molecular clock estimates, extracts susbstitution rate estimate

process MolecularClock {

  label "data"
  tag { "$tree" }

  publishDir "${params.outdir}", mode: "copy"

  input:
  file(tree) from phylo
  file(alignment) from clock_align

  output:
  file("clock.txt")
  file("rate.txt") into plot_date_randomisation_rate

  script:

  if (params.clock == 'treetime')

    """
    pathfinder phybeast utils prepare-metadata -m $metadata -p treetime -o treetime.meta
    treetime clock --tree $tree --aln $alignment --dates treetime.meta --allow-negative-rate \
    --outdir clock > clock.txt
    pathfinder phybeast utils extract-rate -f output.txt -p treetime -o rate.txt
    """

  else if (params.clock == 'lsd')

    """
    pathfinder phybeast utils prepare-metadata -m $metadata -p lsd2 -o lsd2.meta
    lsd2 -i $tree -d lsd2.meta -r a -c -o clock.txt
    pathfinder phybeast utils extract-rate -f clock.txt -p lsd2 -o rate.txt
    """

}

// Date regression estimate with TimeTree, separate from clock estimate above

process DateRegression {

  label "data"
  tag { "$tree" }

  publishDir "${params.outdir}", mode: "copy"

  input:
  file(tree) from phylo_regression
  file(alignment) from reg_align

  output:
  file("rtt.csv") into plot_regression

  script:

  """
  pathfinder phybeast utils prepare-metadata -m $metadata -p treetime -o treetime.meta
  treetime clock --tree $tree --aln $alignment --dates treetime.meta --allow-negative-rate --outdir clock > clock.txt
  mv clock/rtt.csv rtt.csv
  """


}


// Date randomisation, test for temporal structure, Duchene et al.

if (params.date_test){

  replicates = 1..params.replicates

  process DateRandomisation {

    label "data"

    input:
    file(alignment) from clock_align
    each rep from replicates

    output:
    set rep, file("random.${rep}.tab") into estimate_rate

    """
    pathfinder phybeast utils randomise-dates --date_file $metadata --output random.${rep}.tab
    """

  }

  process ClockReplicate {

    label "data"

    input:
    set rep, file(random_dates) from estimate_rate
    file(tree) from phylo_randomisation
    file(alignment) from rep_align

    output:
    file("rate.${rep}.txt") into plot_date_randomisation

    script:

    if (params.clock == 'lsd')

      """
      pathfinder phybeast utils prepare-metadata -m $random_dates -p lsd2 -o lsd2.meta
      lsd2 -i $tree -d lsd2.meta -r a -c -o clock.${rep}.txt
      pathfinder phybeast utils extract-rate -f clock.${rep}.txt -p lsd2 -o rate.${rep}.txt
      """

    else if (params.clock == 'treetime')

      """
      pathfinder phybeast utils prepare-metadata -m $random_dates -p treetime -o treetime.meta
      treetime clock --tree $tree --aln $alignment --dates treetime.meta --allow-negative-rate \
      --outdir clock > clock.${rep}.txt
      pathfinder phybeast utils extract-rate -f clock.${rep}.txt -p treetime -o rate.${rep}.txt
      """

  }

  process DateRandomisationPlot {

    label "data"

    publishDir "${params.outdir}", mode: "copy"

    input:
    file(rates) from plot_date_randomisation.collect()
    file(rate) from plot_date_randomisation_rate
    file(regression) from plot_regression

    output:
    file("clock/rtt.csv")
    file("rates.tab")

    script:

    """
    cat $rates > rates.tab
    pathfinder phybeast utils plot-date-randomisation -f rates.tab -r $rate \
    -o date_randomisation.png --regression $regression
    """

  }

// pathfinder phybeast plot-date-random -f rates.tab -r $rate -o date_randomisation.png

}
