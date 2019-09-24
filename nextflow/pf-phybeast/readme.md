
![](resources/phybeast.png)


# phybeast 

![](https://img.shields.io/badge/version-0.1-blue.svg)
![](https://img.shields.io/badge/docs-none-green.svg)
![](https://img.shields.io/badge/lifecycle-experimental-orange.svg)

Overview
---

Phylodynamic and outbreak analysis pipelines for bacterial pathogens.

Dependencies
---

* Conda / Docker
* Python v3.7
* Nextflow


Install
---

Pathfinder base command line interface from the **pf-core** repository:

```
pip install git@github.com:pf-core/pf-core
```

Configuration
---

View the `Nextflow` configuration file. Parameter settings and resource specifications, as well as configuration of the virtual environments and job submission to clusters can be found here:

```
cat nextflow.config
```

Execution
---

Parameter settings can be set from the command line and are always prepended with a double dash, while native settings for `Nextflow` are set with a single dash, in this case we set a pre-defined execution environment for the `PBSPRO` job submitter on our cluster:

```
nextflow pybeast.nf
```

Datasets
---

These are some example datasets that we can test the pipeline on. These are somewhat convenient to pull from the European Nucleotide Archive with `Pathfinder`. I have stored the metadata in `phybeast/dev/data/` alongside some test outputs and reports. **Note**: Download needs to be fixed to allow `FTP` instead of `Aspera`.

*Mycobacterium tuberculosis* | Daru island outbreak
---

Setup the download from the Daru outbreak paper by Lachlan's group (Bainomugisa et al. 2018). Remove a set of five isolates that do not belong to the outbreak cluster.

```
pf download --project PRJNA385247 --outdir daru
cd daru && rm SRR5520609* SRR5551667* SRR5520557* SRR5520597* SRR5520603*
```

Execute the workflow to generate all output data in the Daru configuration, execute `local` - you can change your cluster executor by substituting `cluster`.

```
nextflow phybeast.nf -c phybeast/dev/data/daru.config -profile local
```

*Staphylococcus aureus* | East Asia clone ST59
---

Ward et al. (2016) describe on the global transmission of the ST59 lineage of community-associated MRSA in the US and in Taiwan. Download all the sequence read files from the submitted files, whose identifications match the metadata from the paper.

```
pf download --project PRJEB12470 --outdir st59/ --submitted
```

Execute the workflow to generate all output data in default parameter configuration, with organism specific parameters specified from the command line:

```
nextflow phybeast.nf -c phybeast/dev/data/st59.config -profile local
```

Authors
---

![](https://img.shields.io/badge/preprint-v0.1-blue.svg)

**Contributors**:

  * Eike Steinig
  * Michael Meehan
  * Sebastian Duchene
  * Jake Lacey
  * Emma McBryde
  * Steve Tong
