rule fit_first:
    input: 
        'src/scripts/fit_first.py',
        'src/scripts/_fig_params.py'
    output:
        'src/tex/figures/fit_first.pdf',
        'src/tex/output/lin_bias.txt',
        'src/tex/output/non_bias.txt',
        'src/tex/output/bias_ratio.txt'
    conda:
        'environment.yml'
    shell:
        'cd src/scripts && python fit_first.py'
