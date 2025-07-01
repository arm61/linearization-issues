# Is there still a place for linearization in the chemistry curriculum?

<p align="justify">
The use of mathematical transformations to reduce non-linear functions to linear problems, which can be tackled with analytical linear regression, is commonplace in the chemistry curriculum. 
The linearization procedure, however, assumes an incorrect statistical model for real experimental data; leading to biased estimates of regression parameters and should therefore not be used in formal data analysis. 
This fact is overlooked in many chemistry degrees, students do not yet have the mathematical knowledge to appreciate why linearization leads to bias when it is introduced.
I hope that this commentary will start a discussion around the place of linearization in the chemistry curriculum, and more broadly around how mathematical and statistical training is currently provided to chemistry students. 
</p>

---

<p align="center">
<a href="https://github.com/arm61/linearization-issues/actions/workflows/build.yml">
<img src="https://github.com/arm61/linearization-issues/actions/workflows/build.yml/badge.svg" alt="Article status"/>
</a>
<a href="https://github.com/arm61/linearization-issues/raw/main-pdf/arxiv.tar.gz">
<img src="https://img.shields.io/badge/article-tarball-blue.svg?style=flat" alt="Article tarball"/>
</a>
<a href="https://github.com/arm61/linearization-issues/raw/main-pdf/ms.pdf">
<img src="https://img.shields.io/badge/article-pdf-blue.svg?style=flat" alt="Read the article"/>
</a>
<a href="https://doi.org/10.5281/zenodo.7949905">
<img src="https://zenodo.org/badge/DOI/10.5281/zenodo.7949905.svg"/>
</a>
<a href="https://doi.org/10.1021/acs.jchemed.3c00466">
<img src=https://img.shields.io/badge/publication%20DOI-10.1021/acs.jchemed.3c00466-yellow.svg?style=flat"/>
</a>
<a href="https://orcid.org/0000-0003-3381-5911">Andrew R. McCluskey</a>&ast;<br>
&ast;<a href="mailto:andrew.mccluskey@bristol.ac.uk">andrew.mccluskey@bristol.ac.uk</a>
</p>

---

This is the electronic supplementary information (ESI) associated with the publication "Is there still a place for linearization in the chemistry curriculum?". 
This ESI uses [`showyourwork`](https://show-your.work) to provide a completely reproducible and automated analysis, plotting, and paper generation workflow. 
To run the workflow and generate the paper locally using the cached data run the following: 
```
git clone git@github.com:arm61/linearization-issues.git
cd linearization-issues
pip install showyourwork
showyourwork build 
```
Full details of the workflow can be determined from the [`Snakefile`](https://github.com/arm61/linearization-issues/blob/main/Snakefile) and the [`showyourwork.yml`](https://github.com/arm61/linearization-issues/blob/main/showyourwork.yml).

## Contents

Shown below is a documented directory structure for this repository. 
For those interested in the Jupyter Notebook that shows the general approach to non-linear optimisation, this can be found at [`src/scripts/weighted-non-linear.ipynb`](https://github.com/arm61/linearization-issues/blob/main/src/scripts/weighted-non-linear.ipynb).

```
├── .github/workflows                  # Workflows for builidng the manuscript on Github
├── src
│   ├── scripts
│   │   ├── .gitignore
│   │   ├── LICENCE
│   │   ├── _fig_params.py             # Custom figure formatting
│   │   ├── distributions.py           # Script to produce Figure 3
│   │   ├── matplotlibrc
│   │   ├── ols.py                     # Script to produce Figure 1
│   │   ├── paths.py                   # Helper file to control paths
│   │   └── weighted-non-linear.ipynb  # Jupyter Notebook showing weighted non-linear optimization
│   │   ├── wls.py                     # Script to produce Figure 2
│   └── tex
│   │   ├── figures                    # Figure pdfs are placed here when compiled
│   │   ├── outputs                    # TeX snippets are placed here when compiled
│   │   ├── .gitignore
│   │   ├── LICENCE
│   │   ├── bib.bib                    # Bibliography
│   │   ├── ms.tex                     # TeX of the manuscript
│   │   └── showyourwork.sty           # LaTeX styles for showyourwork
├── .gitignore
├── LICENCE
├── README.md                          # You are here
├── Snakefile                          # Additional snakemake rules
├── environment.yml                    # conda/mamba environment file
└── showyourwork.yml                   # Defines showyourwork structure and options
```
