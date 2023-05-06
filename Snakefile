rule fit_first:
    input: 
        'src/scripts/ols.py',
        'src/scripts/_fig_params.py'
    output:
        'src/tex/figures/ols.pdf',
        'src/tex/output/lin_mean_ols.txt',
        'src/tex/output/non_mean_ols.txt',
        'src/tex/output/lin_ci_ols.txt',
        'src/tex/output/non_ci_ols.txt'
    conda:
        'environment.yml'
    shell:
        'cd src/scripts && python ols.py'
