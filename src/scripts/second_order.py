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
scale = 0.02
t = np.arange(0, 1400, 100)
true_A0 = 1
true_k = 3.2e-3
A = rng.normal(loc=second_order(t[:, np.newaxis], true_A0, true_k), scale=scale, size=(t.size, size))

X = np.array([t, np.ones_like(t)]).T
ols_ = np.matmul(np.matmul(np.linalg.inv(np.matmul(X.T, X)), X.T), 1/A)
k_ols = ols_[0]
A0_non = 1 / ols_[1]
k_non = np.array([])
A0_non = np.array([])
for i, j in enumerate(A.T):
    popt, pcov = curve_fit(second_order, t, j, p0=[1, 3e-3])
    A0_non = np.append(A0_non, popt[0])
    k_non = np.append(k_non, popt[1])

figsize = figsizes.icml2022_half(nrows=2, ncols=2, height_to_width_ratio=0.8)['figure.figsize']
fig = plt.figure(figsize=figsize)
gs = gridspec.GridSpec(2, 2, figure=fig, wspace=0.4, hspace=0.6)

axes = []
titles = []

axes.append(fig.add_subplot(gs[0, 0]))
titles.append("Linear plot")
axes[-1].errorbar(t / 100, 1 / A[:, 1], scale / A[:, 1] ** 2, marker='.', color=fp.colors[0], zorder=10)
axes[-1].set_ylabel('$1/A(t)$')
axes[-1].set_xlabel('$t$ / $10^2$ s')
axes[-1].set_xticks([0, 5, 10])

axes.append(fig.add_subplot(gs[0, 1]))
titles.append("Non-linear plot")
axes[-1].errorbar(t / 100, A[:, 1], scale, marker='.', color=fp.colors[2], zorder=10)
axes[-1].set_ylabel('$A(t)$')
axes[-1].set_xlabel('$t$ / $10^2$ s')
axes[-1].set_xticks([0, 5, 10])

axes.append(fig.add_subplot(gs[1, 0]))
axes[-1].hist(k_ols / true_k, color=fp.colors[0], bins=100, alpha=0.5)
axes[-1].axvline((k_ols / true_k).mean(), color=fp.colors[0], zorder=10)
axes[-1].set_xlabel('$k_{\mathrm{lin}}$ / M$^{-1}$s$^{-1}$')
axes[-1].set_ylabel('$p(k_{\mathrm{lin}})$ / Ms')

axes.append(fig.add_subplot(gs[1, 1]))
axes[-1].hist(k_non / true_k, color=fp.colors[2], bins=100, alpha=0.5)
axes[-1].axvline((k_non / true_k).mean(), color=fp.colors[2], zorder=10)
axes[-1].set_xlabel('$k_{\mathrm{non}}$ / M$^{-1}$s$^{-1}$')
axes[-1].set_ylabel('$p(k_{\mathrm{non}})$ / Ms')

fig.align_ylabels(axes)

x_correction = [15, 15] * 2
for i, ax in enumerate(axes[:2]):
    x = ax.get_window_extent().x0 - x_correction[i]
    y = ax.get_window_extent().y1 + 10
    x, y = fig.transFigure.inverted().transform([x, y])
    fig.text(x, y, titles[i], ha='left')

# plt.figlegend(loc='upper center', bbox_to_anchor=(0.5, -0.01), ncol=3)
plt.savefig(paths.figures / "second_order.pdf")
plt.close()