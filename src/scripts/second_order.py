import numpy as np
import matplotlib.pyplot as plt
from tueplots import figsizes
import matplotlib.gridspec as gridspec
from scipy.optimize import curve_fit

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
scale = 0.04
t = np.arange(0, 1400, 200)
true_A0 = 1
true_k = 3.2e-3
A = rng.normal(loc=second_order(t[:, np.newaxis], true_A0, true_k), scale=scale, size=(t.size, size))


figsize = figsizes.icml2022_half(nrows=2, ncols=2, height_to_width_ratio=0.8)['figure.figsize']
fig = plt.figure(figsize=figsize)
gs = gridspec.GridSpec(2, 2, figure=fig, wspace=0.4, hspace=0.6)

axes = []
titles = []

axes.append(fig.add_subplot(gs[0, 0]))
titles.append("a")
axes[-1].errorbar(t / 100, A[:, 0], scale, marker='.', color=fp.colors[2])
axes[-1].set_ylabel('$A(t)$')
axes[-1].set_xlabel('$t$ / $10^2$ s')
axes[-1].set_xticks([0, 5, 10])
axes[-1].set_xlim(0, None)
axes[-1].set_ylim(0, None)
axes[-1].set_title('Non-linear plot')

axes.append(fig.add_subplot(gs[0, 1]))
titles.append("b")
errorbars = 1 / np.array([A[:, 0] - scale, A[:, 0] + scale])
axes[-1].errorbar(t / 100, 1 / A[:, 0], np.abs(errorbars - 1 / A[:, 0]), marker='.', color=fp.colors[0])
axes[-1].set_ylabel('$1/A(t)$')
axes[-1].set_xlabel('$t$ / $10^2$ s')
axes[-1].set_xticks([0, 5, 10])
axes[-1].set_xlim(0, None)
axes[-1].set_ylim(0, None)
axes[-1].set_title('Linear plot')

axes.append(fig.add_subplot(gs[1, 0]))
titles.append("c")
y, x = np.histogram(A[3], bins=fp.NBINS, density=True)
axes[-1].stairs(y, x, color=fp.colors[2], alpha=0.5, fill=True)
# axes[-1].axvline((k_lin / true_k).mean(), color=fp.colors[0])
axes[-1].set_xlabel('$A(600$ s$)$')
axes[-1].set_ylabel('$p[A(600$ s$)]$')

axes.append(fig.add_subplot(gs[1, 1]))
titles.append("d")
y, x = np.histogram(1 / A[3], bins=fp.NBINS, density=True)
axes[-1].stairs(y, x, color=fp.colors[0], alpha=0.5, fill=True)
# axes[-1].axvline((k_non / true_k).mean(), color=fp.colors[2])
axes[-1].set_xlabel('$A(600$ s$)$')
axes[-1].set_ylabel('$p[A(600$ s$)]$')

fig.align_ylabels(axes)

x_correction = [15, 15, 15, 15]
for i, ax in enumerate(axes):
    x = ax.get_window_extent().x0 - x_correction[i]
    y = ax.get_window_extent().y1 + 10
    x, y = fig.transFigure.inverted().transform([x, y])
    fig.text(x, y, titles[i], ha='left', fontweight='bold')

# plt.figlegend(loc='upper center', bbox_to_anchor=(0.5, -0.01), ncol=3)
plt.savefig(paths.figures / "second_order.pdf")
plt.close()