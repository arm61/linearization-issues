# Is there still a place for linearization in the chemistry curriculum?

<p align="justify">
The use of mathematical transformations to reduce non-linear functions to linear problems that can be tackled with analytical linear regression is commonplace in chemistry textbooks and degree programs. 
However, the linearisation procedure can lead to biased estimates of regression parameters, when real measured data is used. 
Only introducing students to linearization, without discussion of the shortcomings, leads to researchers applying this biased process in formal analysis.
Modern computing technology means that non-linear optimization is more accessible than ever. 
I hope to start a discussion in the community as to the place of linearization, and more broadly the adequacy of the current training in data handling skills we offer to students.
</p>

---

<p align="center">
<a href="https://github.com/arm61/against-linearisation/actions/workflows/build.yml">
<img src="https://github.com/arm61/against-linearisation/actions/workflows/build.yml/badge.svg" alt="Article status"/>
</a>
<a href="https://github.com/arm61/against-linearisation/raw/main-pdf/arxiv.tar.gz">
<img src="https://img.shields.io/badge/article-tarball-blue.svg?style=flat" alt="Article tarball"/>
</a>
<a href="https://github.com/arm61/against-linearisation/raw/main-pdf/ms.pdf">
<img src="https://img.shields.io/badge/article-pdf-blue.svg?style=flat" alt="Read the article"/>
</a>
<a href="https://doi.org/10.5281/zenodo.xxxxxxx">
<img src="https://zenodo.org/badge/DOI/10.5281/zenodo.xxxxxxx.svg"/>
</a>
<a href="https://arxiv.org/abs/xxxx.xxxxx">
<img src="https://img.shields.io/badge/arXiv-xxxx.xxxxx-orange.svg"/>
</a>
<br><br>
<a href="https://orcid.org/0000-0003-3381-5911">Andrew R. McCluskey</a>&ast;<br>
&ast;<a href="mailto:andrew.mccluskey@ess.eu">andrew.mccluskey@ess.eu</a>
</p>

---

This is the electronic supplementary information (ESI) associated with the publication "Is there still a place for linearization in the chemistry curriculum?". 
This ESI uses [`showyourwork`](https://show-your.work) to provide a completely reproducible and automated analysis, plotting, and paper generation workflow. 
To run the workflow and generate the paper locally using the cached data run the following: 
```
git clone git@github.com:arm61/against-linearisation.git
cd against-linearisation
pip install showyourwork
showyourwork build 
```
Full details of the workflow can be determined from the [`Snakefile`](https://github.com/arm61/against-linearisation/blob/main/Snakefile) and the [`showyourwork.yml`](https://github.com/arm61/against-linearisation/blob/main/showyourwork.yml).

## Contents

```
├── src
│   ├── scripts
│   │   ├── .gitignore
│   │   ├── _fig_params.py                  # Custom figure formatting
│   │   ├── distributions.py                # Script to produce Figure 2
│   │   ├── fit_first.py                    # Script to produce Figure 1
│   │   ├── matplotlibrc
│   │   ├── paths.py                        # Helper file to control paths
│   │   └── weighted-non-linear.ipynb       # Jupyter Notebook showing weighted non-linear optimization
│   └── tex
│   │   ├── figures                         # Figure pdfs are placed here when compiled
│   │   ├── outputs                         # TeX snippets are placed here when compiled
│   │   ├── .gitignore
│   │   ├── LICENCE
│   │   ├── bib.bib                         # Bibliography
│   │   ├── ms.tex                          # TeX of the manuscript
│   │   └── showyourwork.sty                # LaTeX styles for showyourwork
├── LICENCE
├── README.md                               # You are here
├── showyourwork.yml                        # Defines showyourwork structure and options
└── Snakefile                               # Additional snakemake rules
```