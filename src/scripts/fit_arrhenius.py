import numpy as np
import matplotlib.pyplot as plt
from tueplots import figsizes
import matplotlib.gridspec as gridspec
from scipy.optimize import curve_fit
from scipy.constants import R

import paths
import _fig_params as fp

rng = np.random.default_rng(1)

R *= 1e-3

Ea = 50
A = 4e-3


def arrhenius(abscissa: np.ndarray, activation_energy: float=Ea, prefactor: float=A) -> np.ndarray:
    """
    Determine the diffusion coefficient for a given activation energy, and prefactor according to the Arrhenius
    equation.

    Args:
        abscissa (:py:attr:`array_like`): The abscissa data.
        activation_energy (:py:attr:`float`): The activation_energy value.
        prefactor (:py:attr:`float`): The prefactor value.

    :return: The diffusion coefficient data.
    """
    return prefactor * np.exp(-1 * activation_energy / (R * abscissa))


T = np.arange(500, 1001, 100)
scale = 8e-8
size = int(2 ** 15)
k = rng.normal(loc=arrhenius(T[:, np.newaxis]), scale=scale, size=(T.size, size))
has_zero = np.where(k < 0)[1]
while has_zero.size > 0:
    k[:, has_zero] = rng.normal(loc=arrhenius(T[:, np.newaxis]), scale=scale, size=(T.size, has_zero.size))
    has_zero = np.where(k <= 0)[1]

X = np.array([1 / T, np.ones_like(T)]).T
W = np.linalg.inv(np.eye(T.size) * scale)
wls = np.linalg.inv(X.T @ W @ X) @ X.T @ W @ np.log(k)
Ea_lin = -wls[0] * R
A_lin = np.exp(wls[1])
Ea_non = np.array([])
A_non = np.array([])
for i, j in enumerate(k.T):
    popt, pcov = curve_fit(arrhenius, T, j, sigma=np.ones_like(T) * scale, p0=[50, 4e-3])
    Ea_non = np.append(Ea_non, popt[0])
    A_non = np.append(A_non, popt[1])

figsize = figsizes.icml2022_half(nrows=1, ncols=2, height_to_width_ratio=0.8)['figure.figsize']
fig = plt.figure(figsize=figsize)
gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.4, hspace=0.6)

axes = []
titles = []

axes.append(fig.add_subplot(gs[0, 0]))
titles.append("a")
y, x = np.histogram(Ea_non / Ea, bins=100, density=True)
axes[-1].stairs(y, x, color=fp.colors[2], alpha=0.5, fill=True)
axes[-1].axvline((Ea_non / Ea).mean(), color=fp.colors[2])
axes[-1].set_xlabel('$k_{\mathrm{non}} k^{-1}$')
axes[-1].set_ylabel('$p(k_{\mathrm{non}} k^{-1})$')
axes[-1].set_title('Non-linear fit')
# axes[-1].set_xticks([0.8, 1, 1.2])

axes.append(fig.add_subplot(gs[0, 1]))
titles.append("b")
y, x = np.histogram(Ea_lin / Ea, bins=100, density=True)
axes[-1].stairs(y, x, color=fp.colors[0], alpha=0.5, fill=True)
axes[-1].axvline((Ea_lin / Ea).mean(), color=fp.colors[0])
axes[-1].set_xlabel('$k_{\mathrm{lin}} k^{-1}$')
axes[-1].set_ylabel('$p(k_{\mathrm{lin}} k^{-1})$')
axes[-1].set_title('Linear fit')
# axes[-1].set_xticks([1, 2, 3, 4])


fig.align_ylabels(axes)

x_correction = [15, 15, 15, 15]
for i, ax in enumerate(axes):
    x = ax.get_window_extent().x0 - x_correction[i]
    y = ax.get_window_extent().y1 + 10
    x, y = fig.transFigure.inverted().transform([x, y])
    fig.text(x, y, titles[i], ha='left', fontweight='bold')

# plt.figlegend(loc='upper center', bbox_to_anchor=(0.5, -0.01), ncol=3)
plt.savefig(paths.figures / "fit_arrhenius.pdf")
plt.close()