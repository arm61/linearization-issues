rule fit_first:
    input: 
        'src/scripts/fit_first.py',
        'src/scripts/_fig_params.py'
    output:
        'src/tex/figures/fit_first.pdf',
        'src/tex/output/lin_mean.txt',
        'src/tex/output/non_mean.txt',
        'src/tex/output/lin_ci.txt',
        'src/tex/output/non_ci.txt'
    conda:
        'environment.yml'
    shell:
        'cd src/scripts && python fit_first.py'
