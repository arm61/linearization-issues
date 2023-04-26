import numpy as np
import matplotlib.pyplot as plt
from tueplots import figsizes
import matplotlib.gridspec as gridspec
from scipy.optimize import curve_fit

import paths
import _fig_params as fp

rng = np.random.default_rng(1)

k = 0.1

def first_order(t: np.ndarray, k: float, A0: float) -> np.ndarray:
    """
    The first order integrated rate equation.

    Args:
        t (:py:attr:`array_like`): The time data.
        k (:py:attr:`float`): The rate constant value.
        A0 (:py:attr:`float`): The initial reactant concentration value.

    :return: The concentration at time t.
    """
    return A0 * np.exp(-1 * k  * t)


T = np.arange(2, 22, 2)
scale = 0.5
size = int(2 ** 15)
k = rng.normal(loc=first_order(T[:, np.newaxis]), scale=scale, size=(T.size, size))
# has_zero = np.where(k < 0)[1]
# while has_zero.size > 0:
#     k[:, has_zero] = rng.normal(loc=first_order(T[:, np.newaxis]), scale=scale, size=(T.size, has_zero.size))
#     has_zero = np.where(k <= 0)[1]

X = np.array([1 / T, np.ones_like(T)]).T
W = np.linalg.inv(np.eye(T.size) * scale)
wls = np.linalg.inv(X.T @ W @ X) @ X.T @ W @ np.log(k)
k_lin = -wls[0]
A0_lin = np.exp(wls[1])
k_non = np.array([])
A0_non = np.array([])
for i, j in enumerate(k.T):
    popt, pcov = curve_fit(first_order, T, j, sigma=np.ones_like(T) * scale, p0=[k, 7])
    k_non = np.append(k_non, popt[0])
    A0_non = np.append(A0_non, popt[1])

figsize = figsizes.icml2022_half(nrows=1, ncols=2, height_to_width_ratio=0.8)['figure.figsize']
fig = plt.figure(figsize=figsize)
gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.4, hspace=0.6)

axes = []
titles = []

axes.append(fig.add_subplot(gs[0, 0]))
titles.append("a")
y, x = np.histogram(k_non / k, bins=100, density=True)
axes[-1].stairs(y, x, color=fp.colors[2], alpha=0.5, fill=True)
axes[-1].axvline((k_non / k).mean(), color=fp.colors[2])
axes[-1].set_xlabel('$\hat{E}_{\mathrm{a,non}} E_{\mathrm{a}}^{-1}$')
axes[-1].set_ylabel('$p(\hat{E}_{\mathrm{a,non}} E_{\mathrm{a}}^{-1})$')
axes[-1].set_title('Non-linear fit')
# axes[-1].set_xticks([0.8, 1, 1.2])

axes.append(fig.add_subplot(gs[0, 1]))
titles.append("b")
y, x = np.histogram(k_lin / k, bins=100, density=True)
axes[-1].stairs(y, x, color=fp.colors[0], alpha=0.5, fill=True)
axes[-1].axvline((k_lin / k).mean(), color=fp.colors[0])
axes[-1].set_xlabel('$\hat{E}_{\mathrm{a,lin}} E_{\mathrm{a}}^{-1}$')
axes[-1].set_ylabel('$p(\hat{E}_{\mathrm{a,lin}} E_{\mathrm{a}}^{-1})$')
axes[-1].set_title('Linear fit')
# axes[-1].set_xticks([1, 2, 3, 4])

# f = open(paths.output / 'lin_bias_ea.txt', 'w')
# f.write(r'\num{' + f'{(Ea_lin.mean() - Ea) / Ea:.1e}' + r'}')
# f.close()
# f = open(paths.output / 'non_bias_ea.txt', 'w')
# f.write(r'\num{' + f'{(Ea_non.mean() - Ea) / Ea:.1e}' + r'}')
# f.close()
# f = open(paths.output / 'bias_ratio_ea.txt', 'w')
# f.write(r'\num{' + f'{((Ea_lin.mean() - Ea) / Ea) / ((Ea_non.mean() - Ea) / Ea):.1f}' + r'}')
# f.close()

fig.align_ylabels(axes)

x_correction = [15, 15, 15, 15]
for i, ax in enumerate(axes):
    x = ax.get_window_extent().x0 - x_correction[i]
    y = ax.get_window_extent().y1 + 10
    x, y = fig.transFigure.inverted().transform([x, y])
    fig.text(x, y, titles[i], ha='left', fontweight='bold')

# plt.figlegend(loc='upper center', bbox_to_anchor=(0.5, -0.01), ncol=3)
plt.savefig(paths.figures / "fit_first.pdf")
plt.close()