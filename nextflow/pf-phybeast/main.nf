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

|===================================================|
|                     PHYBEAST                      |
|                       v0.1                        |
|===================================================|
|||                                               |||
|||                                               |||
|||                                               |||

    PE reads:             $params.fastq
    Metadata:             $params.metadata
    Reference:            $params.reference
    Recombination:        $params.recombination
    Phylogeny:            $params.phylogeny
    Molecular clock:      $params.clock

|||                                               |||
|||                                               |||
|||                                               |||
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

-f|--fastq     Glob for FASTQ read files
-r|--reference FASTA reference genome file

-m|--metadata  CSV metadata file with date column
v_

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
  tag { id }

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
  tag { "Core SNP Alignment" }

  publishDir "${params.outdir}", mode: "copy"

  input:
  file(snippy_outputs) from core_alignment.collect()

  output:
  file("alignment.fasta") into recombination
  file("core.aln")

  """
  snippy-core --ref $reference --prefix core $snippy_outputs
  snippy-clean_full_aln core.full.aln > clean.alignment.fasta
  python $baseDir/scripts/remove_reference.py -a clean.alignment.fasta -o alignment.fasta
  """

}

// Remove recombination from the substituted reference genome alignment
// Output only sites containing exclusively ACGT (-c) in Gubbins

process Gubbins {

  label "recombination"
  tag { "$clean_alignment" }

  publishDir "${params.outdir}", mode: "copy"

  input:
  file(clean_alignment) from recombination

  output:
  file("core.alignment.fasta") into phylogeny // Base phylogeny
  file("core.alignment.fasta") into clock_align
  file("core.alignment.fasta") into tree_align

  when:
  params.recombination

  """
  run_gubbins.py -p gubbins --threads $task.cpus $clean_alignment
  snp-sites -c gubbins.filtered_polymorphic_sites.fasta > core.alignment.fasta
  """

}

// TreeBuilders

// ASC_LEWIS for ascertainment bias correction (using core SNPs)

process Phylogeny {

  label "phylogeny"
  tag { "$alignment" }

  input:
  file(alignment) from phylogeny

  output:
  file("tree.newick") into phylo


  script:

  if params.phylogeny == 'raxml':

    """
    raxml-ng --msa $alignment --model $model --tree rand{10} \
    --threads $task.cpus --prefix phylo --force
    mv phylo.raxml.bestTree tree.newick
    """

  else if params.phylogeny == 'phyml':

    """
    goalign reformat -i $alignment phylip > aln.phy
    phyml -i phy 
    """

  else if params.phylogeny == 'fasttree':

    """
    FastTree -gtr -nt $alignment > tree.newick
    """


}

// Molecular clock estimates

process MolecularClockEstimate {

  label "phylogeny"
  tag { "$tree" }

  publishDir "${params.outdir}", mode: "copy"

  input:
  file(alignment) from clock_align
  file(tree) from phylo

  output:
  file("clock/")

  script:

  if params.clock == 'treetime':

    """
    treetime clock --tree $tree --dates $metadata --allow-negative-rate \
    --aln $alignment --outdir clock > output.txt
    """
  else if params.clock == 'lsd':
    """
    lsd -i $tree -d $dates -r a -c -o clock
    """



}


// Date randomisation, test for temporal structure, Duchene et al.

if (params.date_test){

  process RandomizeDates {

    label "date_random"
    tag { "$alignment" }

    publishDir "${params.outdir}", mode: "copy"

    input:
    file(alignment) from clock_align
    each rep from params.replicates

    output:
    file("random.${rep}.tab") into estimate_rate

    """
    $baseDir/scripts/randomize_dates.py --date_file $metadata --output_file random.${rep}.tab
    """

  }

  process EstimateSubstitutionRate {

    label "date_random"
    tag { "$alignment" }

    publishDir "${params.outdir}", mode: "copy"

    input:
    file(random_dates) from estimate_rate

    output:
    file("") into plot_distribution

    script:

    if params.clock == 'lsd':

      """
      lsd -i $tree -d $random_dates -r a -c -o replicate_date
      """

    else if params.clock == 'treetime':

      """
      treetime clock --tree $tree --dates $metadata --allow-negative-rate \
      --aln $alignment --outdir clock_align > output.txt
      """


  }

  process PlotDateRandomisations {



  }
}
