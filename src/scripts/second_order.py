import numpy as np
import matplotlib.pyplot as plt
from tueplots import figsizes
import matplotlib.gridspec as gridspec

import paths
import _fig_params as fp


def second_order(t: np.ndarray, A0: float, k: float) -> np.ndarray:
    """
    Second order integrated rate law.

    :param t: Time.
    :param A0: Initial concentration.
    :param k: Rate constant. 
    
    :returns: Concentration at each t. 
    """
    return 1 / ((1 / A0) + k * t)


rng = np.random.default_rng(1)

size = int(2 ** 14)
scale = 0.02
t = np.arange(0, 1400, 100)
true_A0 = 1
true_k = 3.2e-3
A = rng.normal(loc=second_order(t[:, np.newaxis], true_A0, true_k), scale=scale, size=(t.size, size))


figsize = figsizes.icml2022_half(nrows=2, ncols=2, height_to_width_ratio=0.8)['figure.figsize']
fig = plt.figure(figsize=figsize)
gs = gridspec.GridSpec(2, 2, figure=fig, wspace=0.4, hspace=0.6)

axes = []
titles = []

axes.append(fig.add_subplot(gs[0, 0]))
titles.append("Linear plot")
axes[-1].errorbar(t, 1 / A[:, 1], scale / A[:, 1] ** 2, marker='.', color=fp.colors[0], label='$A$', zorder=10)
axes[-1].set_ylabel('$1/A(t)$')
axes[-1].set_xlabel('$t$/s')

axes.append(fig.add_subplot(gs[0, 1]))
# titles.append("Linear plot")
axes[-1].errorbar(t, A[:, 1], A[:, 1], marker='.', color=fp.colors[1], label='$A$', zorder=10)
axes[-1].set_ylabel('$A(t)$')
axes[-1].set_xlabel('$t$/s')

fig.align_ylabels(axes)

x_correction = [36, 26] * 2
for i, ax in enumerate(axes):
    x = ax.get_window_extent().x0 - x_correction[i]
    y = ax.get_window_extent().y1 + 10
    x, y = fig.transFigure.inverted().transform([x, y])
    fig.text(x, y, titles[i], ha='left')

# plt.figlegend(loc='upper center', bbox_to_anchor=(0.5, -0.01), ncol=3)
plt.savefig(paths.figures / "second_order.pdf")
plt.close()