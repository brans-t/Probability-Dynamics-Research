"""Reproduce Project 11.3: KL of a truncated standard normal.

Output paths are relative to the project root. No random samples are used:
all curves are exact evaluations of the standard normal survival function.
"""
import csv
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import log_ndtr

from _paths import ROOT, FIGURES, RESULTS

FIG = FIGURES / "project11_truncated_gaussian_kl.pdf"
DATA = RESULTS / "project11_truncated_gaussian_kl.csv"

b = np.linspace(-3.0, 4.0, 701)
log_upper_tail = log_ndtr(-b)  # numerically stable log P(Z > b)
kl = -log_upper_tail
pdf = np.exp(-0.5 * b * b) / math.sqrt(2 * math.pi)
mills = pdf / np.exp(log_upper_tail)
alpha = 1.0
objective = kl + 0.5 * alpha * (1.0 + b * mills)

with DATA.open("w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["threshold_b", "kl_truncated_vs_standard", "objective_alpha_1"])
    writer.writerows(zip(b, kl, objective))

fig, ax = plt.subplots(figsize=(7.1, 4.3))
ax.plot(b, kl, lw=2, label=r"$D_{\mathrm{KL}}(\mu_b\Vert\nu)=-\log\bar\Phi(b)$")
ax.axvspan(0, 4, alpha=0.08, label=r"Constraint $b\geq 0$")
ax.axvline(0, ls="--", lw=1)
ax.axhline(math.log(2), ls=":", lw=1, label=r"$D_{\mathrm{KL}}(\mu_0\Vert\nu)=\log 2$")
ax.set_xlabel(r"Truncation threshold $b$")
ax.set_ylabel("KL divergence (nats)")
ax.set_xlim(-3.0, 4.0)
ax.grid(True, alpha=0.18)
ax.legend(loc="upper left", frameon=False, fontsize=9)
fig.tight_layout()
FIG.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(FIG)
plt.close(fig)

b0 = float(-log_ndtr(0))
assert abs(b0 - math.log(2)) < 1e-12
assert bool(np.all(np.diff(kl) > 0))
assert abs(float(objective[300]) - (math.log(2) + alpha / 2)) < 1e-12
print(f"Wrote {FIG.relative_to(ROOT)} and {DATA.relative_to(ROOT)}")
print(f"D_KL(mu_0||nu) = {b0:.12f}; min J_alpha (alpha=1) = {math.log(2)+0.5:.12f}")
