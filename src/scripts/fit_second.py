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

size = int(2 ** 15)
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

figsize = figsizes.icml2022_half(nrows=1, ncols=2, height_to_width_ratio=0.8)['figure.figsize']
fig = plt.figure(figsize=figsize)
gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.4, hspace=0.6)

axes = []
titles = []

axes.append(fig.add_subplot(gs[0, 0]))
titles.append("a")
y, x = np.histogram(k_non / true_k, bins=100, density=True)
axes[-1].stairs(y, x, color=fp.colors[2], alpha=0.5, fill=True)
axes[-1].axvline((k_non / true_k).mean(), color=fp.colors[2])
axes[-1].set_xlabel('$k_{\mathrm{non}} k^{-1}$')
axes[-1].set_ylabel('$p(k_{\mathrm{non}} k^{-1})$')
axes[-1].set_title('Non-linear fit')

axes.append(fig.add_subplot(gs[0, 1]))
titles.append("b")
y, x = np.histogram(k_lin / true_k, bins=100, density=True)
axes[-1].stairs(y, x, color=fp.colors[0], alpha=0.5, fill=True)
axes[-1].axvline((k_lin / true_k).mean(), color=fp.colors[0])
axes[-1].set_xlabel('$k_{\mathrm{lin}} k^{-1}$')
axes[-1].set_ylabel('$p(k_{\mathrm{lin}} k^{-1})$')
axes[-1].set_title('Linear fit')

print(k_lin.mean() - true_k)
for f in open(paths.output / 'non_bias.txt', 'w'):
    f.write(f'{k_non.mean() - true_k}:.3e')
print((k_lin.mean() - true_k) / (k_non.mean() - true_k))

fig.align_ylabels(axes)

x_correction = [15, 15, 15, 15]
for i, ax in enumerate(axes):
    x = ax.get_window_extent().x0 - x_correction[i]
    y = ax.get_window_extent().y1 + 10
    x, y = fig.transFigure.inverted().transform([x, y])
    fig.text(x, y, titles[i], ha='left', fontweight='bold')

# plt.figlegend(loc='upper center', bbox_to_anchor=(0.5, -0.01), ncol=3)
plt.savefig(paths.figures / "fit_second.pdf")
plt.close()