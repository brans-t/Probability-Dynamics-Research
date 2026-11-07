"""Reproduce the supplied 61-frame nonlinear-flow animation.

Run from any directory; outputs default to output/flow_deformation/.
The original PNG files embedded in the manuscript are left unchanged.
"""

import argparse
import os
import math
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

# Vector field: dx/dt = 0.2 x, dy/dt = 0.1 y + 0.3 x^2
# Exact flow: Phi_{0,t}(x0,y0) =
# (exp(0.2t)x0, exp(0.1t)y0 + (exp(0.4t)-exp(0.1t))x0^2)

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--output-dir", type=Path,
    default=Path(__file__).resolve().parents[1] / "output/flow_deformation",
    help="Directory for regenerated frames and the optional GIF.",
)
parser.add_argument("--skip-gif", action="store_true", help="Generate only the PNG frames.")
args = parser.parse_args()
out_dir = args.output_dir.resolve()
frames_dir = os.path.join(out_dir, "frames")
os.makedirs(frames_dir, exist_ok=True)
times = np.linspace(0, 1.5, 61)
x0_grid = np.linspace(-1, 1, 401)
x_grid_lines = np.linspace(-1, 1, 7)
y_grid_lines = np.linspace(-0.7, 0.7, 7)
frame_paths = []

for i, t in enumerate(times):
    fig = plt.figure(figsize=(12.2, 4.8), dpi=110, constrained_layout=True)
    gs = fig.add_gridspec(1, 3, width_ratios=[1.0, 0.55, 1.25])
    ax0, axm, ax1 = fig.add_subplot(gs[0,0]), fig.add_subplot(gs[0,1]), fig.add_subplot(gs[0,2])

    ax0.fill_between([-1,1], [-0.7,-0.7], [0.7,0.7], alpha=0.08)
    for xx in x_grid_lines: ax0.plot([xx,xx], [-0.7,0.7], linewidth=0.9, alpha=0.75)
    for yy in y_grid_lines: ax0.plot([-1,1], [yy,yy], linewidth=0.9, alpha=0.75)
    ax0.plot([-1,1,1,-1,-1], [-0.7,-0.7,0.7,0.7,-0.7], linewidth=2)
    p0 = (0.35,0.15)
    ax0.scatter([p0[0]],[p0[1]],s=55,zorder=5)
    ax0.set(xlim=(-1.25,1.25), ylim=(-0.95,0.95), xlabel=r"$x_0$", ylabel=r"$y_0$")
    ax0.set_aspect("equal"); ax0.set_title("Initial region (s = 0)")

    axm.axis("off")
    axm.annotate("", xy=(0.96,0.50), xytext=(0.04,0.50),
                 xycoords="axes fraction", textcoords="axes fraction",
                 arrowprops=dict(arrowstyle="->", linewidth=2.2))
    axm.text(0.5,0.66,r"$\Phi_{0,t}$",ha="center",transform=axm.transAxes,fontsize=18)
    axm.text(0.5,0.34,"nonlinear flow",ha="center",transform=axm.transAxes,fontsize=9)

    ex, ey = math.exp(0.2*t), math.exp(0.1*t)
    q = math.exp(0.4*t)-math.exp(0.1*t)
    x_img = ex*x0_grid
    y_top, y_bottom = ey*0.7+q*x0_grid**2, -ey*0.7+q*x0_grid**2
    ax1.fill_between(x_img,y_bottom,y_top,alpha=0.10)
    for yy0 in y_grid_lines: ax1.plot(x_img,ey*yy0+q*x0_grid**2,linewidth=0.9,alpha=0.8)
    y0_values = np.linspace(-0.7,0.7,180)
    for xx0 in x_grid_lines:
        ax1.plot(np.full_like(y0_values,ex*xx0),ey*y0_values+q*xx0**2,linewidth=0.9,alpha=0.8)
    ax1.plot(x_img,y_top,linewidth=2.2); ax1.plot(x_img,y_bottom,linewidth=2.2)
    for xx0 in (-1.0,1.0):
        ax1.plot(np.full_like(y0_values,ex*xx0),ey*y0_values+q*xx0**2,linewidth=2.2)
    xp, yp = ex*p0[0], ey*p0[1]+q*p0[0]**2
    ax1.scatter([xp],[yp],s=55,zorder=6)
    J, area = math.exp(0.3*t), 2.8*math.exp(0.3*t)
    ax1.text(0.035,0.965,rf"$J(t)=e^{{0.3t}}={J:.3f}$"+"\n"+rf"$|\Phi_{{0,t}}(R)|={area:.3f}$",
             transform=ax1.transAxes,ha="left",va="top",fontsize=10,
             bbox=dict(boxstyle="round,pad=0.35",facecolor="white",alpha=0.82,edgecolor="0.75"))
    ax1.set(xlim=(-1.65,1.65),ylim=(-1.10,1.75),xlabel=r"$x$",ylabel=r"$y$")
    ax1.set_aspect("equal"); ax1.set_title(f"Deformed region (t = {t:.2f})")
    fig.suptitle("Exact nonlinear flow and Liouville--Jacobi formula",fontsize=14)
    path=os.path.join(frames_dir,f"flow_frame_{i}.png")
    fig.savefig(path,dpi=110,bbox_inches="tight"); plt.close(fig); frame_paths.append(path)

if not args.skip_gif:
    frames = []
    for path in frame_paths:
        with Image.open(path) as frame:
            frames.append(frame.convert("P", palette=Image.Palette.ADAPTIVE))
    frames[0].save(os.path.join(out_dir, "flow_deformation.gif"), save_all=True,
                   append_images=frames[1:], duration=50, loop=0, optimize=False, disposal=2)
    for frame in frames:
        frame.close()
print(f"Generated {len(frame_paths)} frames in {frames_dir}")
