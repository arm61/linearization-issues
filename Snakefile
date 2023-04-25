rule fit_second:
    input: 
        'src/scripts/fit_second.py',
        'src/scripts/_fig_params.py'
    output:
        'src/tex/figures/fit_second.pdf',
        'src/tex/output/lin_bias.txt',
        'src/tex/output/non_bias.txt',
        'src/tex/output/bias_ratio.txt'
    conda:
        'environment.yml'
    shell:
        'cd src/scripts && python fit_second.py'
