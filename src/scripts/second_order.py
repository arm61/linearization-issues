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

X = np.array([t, np.ones_like(t)]).T
W = np.linalg.inv(np.eye(t.size) * scale)
wls = np.linalg.inv(X.T @ W @ X) @ X.T @ W @ (1/A)
k_lin = wls[0]
A0_lin = 1 / wls[1]
k_non = np.array([])
A0_non = np.array([])
for i, j in enumerate(A.T):
    popt, pcov = curve_fit(second_order, t, j, sigma=np.ones_like(t) * scale, p0=[1, 3e-3])
    A0_non = np.append(A0_non, popt[0])
    k_non = np.append(k_non, popt[1])

figsize = figsizes.icml2022_half(nrows=2, ncols=2, height_to_width_ratio=0.8)['figure.figsize']
fig = plt.figure(figsize=figsize)
gs = gridspec.GridSpec(2, 2, figure=fig, wspace=0.4, hspace=0.6)

axes = []
titles = []

axes.append(fig.add_subplot(gs[0, 0]))
titles.append("Linear plot")
errorbars = 1 / np.array([A[:, 0] - 2 * scale, A[:, 0] + 2 * scale])
axes[-1].errorbar(t / 100, 1 / A[:, 0], errorbars, marker='.', color=fp.colors[0])
axes[-1].set_ylabel('$1/A(t)$')
axes[-1].set_xlabel('$t$ / $10^2$ s')
axes[-1].set_xticks([0, 5, 10])

axes.append(fig.add_subplot(gs[0, 1]))
titles.append("Non-linear plot")
axes[-1].errorbar(t / 100, A[:, 0], scale, marker='.', color=fp.colors[2])
axes[-1].set_ylabel('$A(t)$')
axes[-1].set_xlabel('$t$ / $10^2$ s')
axes[-1].set_xticks([0, 5, 10])

axes.append(fig.add_subplot(gs[1, 0]))
y, x = np.histogram(k_lin / true_k, bins=100)
axes[-1].stairs(y / 100, x, color=fp.colors[0], alpha=0.5, fill=True)
axes[-1].axvline((k_lin / true_k).mean(), color=fp.colors[0])
axes[-1].set_xlabel('$k_{\mathrm{lin}} k^{-1}$ / M$^{-1}$s$^{-1}$')
axes[-1].set_ylabel('$p(k_{\mathrm{lin}} k^{-1})$ / $10^{-2}$ Ms')

axes.append(fig.add_subplot(gs[1, 1]))
y, x = np.histogram(k_non / true_k, bins=100)
axes[-1].stairs(y / 100, x, color=fp.colors[2], alpha=0.5, fill=True)
axes[-1].axvline((k_non / true_k).mean(), color=fp.colors[2])
axes[-1].set_xlabel('$k_{\mathrm{non}} k^{-1}$ / M$^{-1}$s$^{-1}$')
axes[-1].set_ylabel('$p(k_{\mathrm{non}} k^{-1})$ / $10^{-2}$ Ms')

print(k_lin.mean() - true_k)
print(k_non.mean() - true_k)
print((k_lin.mean() - true_k) / (k_non.mean() - true_k))

fig.align_ylabels(axes)

# x_correction = [15, 15] * 2
for i, ax in enumerate(axes[:2]):
    x = ax.get_window_extent().x0# - x_correction[i]
    y = ax.get_window_extent().y1 + 10
    x, y = fig.transFigure.inverted().transform([x, y])
    fig.text(x, y, titles[i], ha='center')

# plt.figlegend(loc='upper center', bbox_to_anchor=(0.5, -0.01), ncol=3)
plt.savefig(paths.figures / "second_order.pdf")
plt.close()