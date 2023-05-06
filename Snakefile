rule ols:
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


rule wls:
    input: 
        'src/scripts/wls.py',
        'src/scripts/_fig_params.py'
    output:
        'src/tex/figures/wls.pdf',
        'src/tex/output/lin_err_true.txt',
        'src/tex/output/lin_err.txt',
        'src/tex/output/non_err_true.txt',
        'src/tex/output/non_err.txt'
    conda:
        'environment.yml'
    shell:
        'cd src/scripts && python wls.py'
