import numpy as np
import matplotlib.pyplot as plt
from tueplots import figsizes
import matplotlib.gridspec as gridspec
from scipy.optimize import curve_fit

import paths
import _fig_params as fp

rng = np.random.default_rng(1)

k = 0.15
A0 = 7.5

def first_order(t: np.ndarray, k: float, A0: float) -> np.ndarray:
    """
    The first order integrated rate equation.

    Args:
        t (:py:attr:`array_like`): The time data.
        k (:py:attr:`float`): The rate constant value.

    :return: The concentration at time t.
    """
    return A0 * np.exp(-1 * k  * t)


t = np.arange(2, 22, 2)
scale = 0.3
size = int(2 ** 15)
At = rng.normal(loc=first_order(t[:, np.newaxis], k, A0), scale=scale, size=(t.size, size))
has_zero = np.where(At < 0)[1]
while has_zero.size > 0:
    At[:, has_zero] = rng.normal(loc=first_order(t[:, np.newaxis], k, A0), scale=scale, size=(t.size, has_zero.size))
    has_zero = np.where(At <= 0)[1]

X = np.array([t, np.ones_like(t)]).T
k_lin = np.array([])
# A0_lin = np.exp(wls[1])
k_non = np.array([])
# A0_non = np.array([])
for i, j in enumerate(At.T):
    prop_scale = scale / j
    W = np.linalg.inv(np.eye(t.size) * prop_scale)
    wls = np.linalg.inv(X.T @ W @ X) @ X.T @ W @ np.log(j)
    k_lin = np.append(k_lin, -wls[0])
    popt, pcov = curve_fit(first_order, t, j, sigma=np.ones_like(t) * scale, p0=[k, A0])
    k_non = np.append(k_non, popt[0])
    # A0_non = np.append(A0_non, popt[1])

figsize = figsizes.icml2022_half(nrows=2, ncols=2, height_to_width_ratio=0.8)['figure.figsize']
fig = plt.figure(figsize=figsize)
gs = gridspec.GridSpec(2, 2, figure=fig, wspace=0.4, hspace=0.6)

axes = []
titles = []

axes.append(fig.add_subplot(gs[0, 0]))
titles.append("a")
axes[-1].errorbar(t, At[:, 0], scale, marker='.', color=fp.colors[2])
axes[-1].set_ylabel('$[\mathrm{H_2O_2}]_t$')
axes[-1].set_xlabel('$t$ / s')
# axes[-1].set_xticks([0, 5, 10])
axes[-1].set_xlim(0, None)
axes[-1].set_ylim(0, None)
axes[-1].set_title('Non-linear form')

axes.append(fig.add_subplot(gs[0, 1]))
titles.append("b")
axes[-1].errorbar(t / 100, At[:, 0], scale, marker='.', color=fp.colors[0])
axes[-1].set_ylabel('$[\mathrm{H_2O_2}]_t$')
axes[-1].set_xlabel('$t$ / s')
axes[-1].set_yscale('log')
# axes[-1].set_xticks([0, 5, 10])
axes[-1].set_xlim(0, None)
axes[-1].set_title('Linearised form')

axes.append(fig.add_subplot(gs[1, 0]))
titles.append("c")
y, x = np.histogram(k_non / k, bins=100, density=True)
axes[-1].stairs(y, x, color=fp.colors[2], alpha=0.5, fill=True)
axes[-1].axvline((k_non / k).mean(), color=fp.colors[2])
axes[-1].set_xlabel('$\hat{k}_{\mathrm{non}} k^{-1}$')
axes[-1].set_ylabel('$p(\hat{k}_{\mathrm{non}} k^{-1})$')
axes[-1].set_xticks([0.9, 1, 1.1])
axes[-1].set_yticks([0, 4, 8])

axes.append(fig.add_subplot(gs[1, 1]))
titles.append("d")
y, x = np.histogram(k_lin / k, bins=100, density=True)
axes[-1].stairs(y, x, color=fp.colors[0], alpha=0.5, fill=True)
axes[-1].axvline((k_lin / k).mean(), color=fp.colors[0])
axes[-1].set_xlabel('$\hat{k}_{\mathrm{lin}} k^{-1}$')
axes[-1].set_ylabel('$p(\hat{k}_{\mathrm{lin}} k^{-1})$')
# axes[-1].set_xticks([1, 2, 3, 4])

f = open(paths.output / 'lin_mean.txt', 'w')
f.write(r'\num{' + f'{np.mean(k_lin / k):.2f}' + r'}')
f.close()
f = open(paths.output / 'non_mean.txt', 'w')
f.write(r'\num{' + f'{np.mean(k_non / k):.2f}' + r'}')
f.close()

f = open(paths.output / 'lin_ci.txt', 'w')
ci_lin = np.percentile(k_lin / k, [2.5, 97.5])
f.write(r'\numrange{' + f'{ci_lin[0]:.2f}' + r'}{' + f'{ci_lin[1]:.2f}' + r'}')
f.close()
f = open(paths.output / 'non_ci.txt', 'w')
ci_non = np.percentile(k_non / k, [2.5, 97.5])
f.write(r'\numrange{' + f'{ci_non[0]:.2f}' + r'}{' + f'{ci_non[1]:.2f}' + r'}')
f.close()

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