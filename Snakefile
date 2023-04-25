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

rule fit_arrhenius:
    input: 
        'src/scripts/fit_arrhenius.py',
        'src/scripts/_fig_params.py'
    output:
        'src/tex/figures/fit_arrhenius.pdf',
        'src/tex/output/lin_bias_ea.txt',
        'src/tex/output/non_bias_ea.txt',
        'src/tex/output/bias_ratio_ea.txt'
    conda:
        'environment.yml'
    shell:
        'cd src/scripts && python fit_arrhenius.py'
