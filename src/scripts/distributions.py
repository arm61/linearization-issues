import numpy as np
import matplotlib.pyplot as plt
from tueplots import figsizes
import matplotlib.gridspec as gridspec
from scipy.stats import norm

import paths
import _fig_params as fp

rng = np.random.default_rng(1)

distribution = rng.normal(loc=50, scale=10, size=int(2 ** 15))

figsize = figsizes.icml2022_half(nrows=1, ncols=3, height_to_width_ratio=0.8)['figure.figsize']
fig = plt.figure(figsize=figsize)
gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.4, hspace=0.6)

axes = []
titles = []

axes.append(fig.add_subplot(gs[0, 0]))
titles.append("a")
y, x = np.histogram(distribution, bins=fp.NBINS, density=True)
axes[-1].stairs(y * 1e2, x, color=fp.colors[2], alpha=0.5, fill=True)
axes[-1].set_xlabel('$y$')
axes[-1].set_ylabel('$P(y)$ / $10^{-2}$')
axes[-1].set_title('Normal')
# axes[-1].set_xticks([0.8, 1, 1.2])

axes.append(fig.add_subplot(gs[0, 1]))
titles.append("b")
y, x = np.histogram(1 / distribution, bins=fp.NBINS, density=True)
axes[-1].stairs(y * 1e-1, x * 1e2, color=fp.colors[0], alpha=0.5, fill=True)
axes[-1].set_xlabel('$y^{-1}$ / $10^{-2}$')
axes[-1].set_ylabel('$P(y^{-1})$ / $10^{1}$')
axes[-1].set_title('Reciprocal')
# axes[-1].set_xticks([1, 2, 3, 4])

axes.append(fig.add_subplot(gs[0, 2]))
titles.append("c")
y, x = np.histogram(np.log(distribution), bins=fp.NBINS, density=True)
axes[-1].stairs(y, x, color=fp.colors[1], alpha=0.5, fill=True)
axes[-1].set_xlabel('$\ln{(y)}$')
axes[-1].set_ylabel('$P[\ln{(y)}]$')
axes[-1].set_title('Logarithm')
# axes[-1].set_xticks([1, 2, 3, 4])

fig.align_ylabels(axes)

x_correction = [15, 15, 15, 15]
for i, ax in enumerate(axes):
    x = ax.get_window_extent().x0 - x_correction[i]
    y = ax.get_window_extent().y1 + 10
    x, y = fig.transFigure.inverted().transform([x, y])
    fig.text(x, y, titles[i], ha='left', fontweight='bold')

# plt.figlegend(loc='upper center', bbox_to_anchor=(0.5, -0.01), ncol=3)
plt.savefig(paths.figures / "distributions.pdf")
plt.close()