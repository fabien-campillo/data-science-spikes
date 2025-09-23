# utils/plot_all_sweeps.py

import numpy as np
import matplotlib.pyplot as plt

def plot_abf_traces_with_scalebar(abf, color_adc="C0", color_dac="C3", lw=0.8, figsize=(8,5)):
    """
    Plot ADC and DAC sweeps stacked with scale bars.

    Parameters
    ----------
    abf : pyabf.ABF
        The ABF object to plot.
    color_adc : str
        Color for ADC traces.
    color_dac : str
        Color for DAC traces.
    lw : float
        Line width for traces.
    figsize : tuple
        Size of the figure.

    Returns
    -------
    fig, ax1, ax2 : matplotlib objects
    """

    fig, ax1 = plt.subplots(figsize=figsize)

    # --- ADC scaling ---
    all_adc = []
    for s in abf.sweepList:
        abf.setSweep(s)
        all_adc.append(abf.sweepY)
    adc_range = np.max(all_adc) - np.min(all_adc)
    adc_spacing = adc_range * 1.2  

    for i, s in enumerate(abf.sweepList):
        abf.setSweep(s)
        offset = i * adc_spacing
        ax1.plot(abf.sweepX, abf.sweepY + offset, color=color_adc, lw=lw)

    ax1.set_xlabel(abf.sweepLabelX)
    ax1.tick_params(axis='y', which='both', length=0)
    ax1.set_yticklabels([])
    ax1.set_ylabel(abf.sweepLabelY, color=color_adc)

    # --- DAC scaling ---
    all_dac = []
    for s in abf.sweepList:
        abf.setSweep(s)
        all_dac.append(abf.sweepC)
    dac_range = np.max(all_dac) - np.min(all_dac)
    dac_spacing = dac_range * 1.2

    ax2 = ax1.twinx()
    for i, s in enumerate(abf.sweepList):
        abf.setSweep(s)
        offset = i * dac_spacing
        ax2.plot(abf.sweepX, abf.sweepC + offset, color=color_dac, lw=lw)

    ax2.tick_params(axis='y', which='both', length=0)
    ax2.set_yticklabels([])
    ax2.set_ylabel(abf.sweepLabelC, color=color_dac)

    # --- helpers ---
    def nice_scale(value):
        exp = int(np.floor(np.log10(abs(value)))) if value != 0 else 0
        base = value / (10**exp) if value != 0 else 0
        if base <= 1:
            nice = 1
        elif base <= 2:
            nice = 2
        elif base <= 5:
            nice = 5
        else:
            nice = 10
        return nice * 10**exp

    def format_scale_label_latex(value, unit):
        if value == 0:
            return rf"$0\,\mathrm{{{unit}}}$"
        exp = int(np.floor(np.log10(abs(value))))
        mant = value / (10**exp)
        return rf"${mant:.1f} \times 10^{{{exp}}}\,\mathrm{{{unit}}}$"

    # --- Compute scale bars ---
    adc_bar = nice_scale(adc_range * 1)
    dac_bar = nice_scale(dac_range * 1)

    # --- Anchors below first sweep ---
    y_anchor_adc = -0.5 * adc_spacing
    y_anchor_dac = -0.5 * dac_spacing

    x0 = abf.sweepX[0] - (abf.sweepX[-1] - abf.sweepX[0]) * 0.05
    x1 = abf.sweepX[-1] + (abf.sweepX[-1] - abf.sweepX[0]) * 0.05

    # --- Left (ADC) scale bar ---
    ax1.plot([x0, x0], [y_anchor_adc, y_anchor_adc + adc_bar], color=color_adc, lw=1.5)
    ax1.text(x0 - 0.01, y_anchor_adc + adc_bar/2,
             format_scale_label_latex(adc_bar, abf.sweepUnitsY),
             va="center", ha="right", color=color_adc)
    ax1.margins(x=0)

    # --- Right (DAC) scale bar ---
    ax2.plot([x1, x1], [y_anchor_dac, y_anchor_dac + dac_bar], color=color_dac, lw=1.5)
    ax2.text(x1 + 0.01, y_anchor_dac + dac_bar/2,
             format_scale_label_latex(dac_bar, abf.sweepUnitsC),
             va="center", ha="left", color=color_dac)

    # remove box spines, keep only bottom (time axis)
    for spine in ["top", "left", "right"]:
        ax1.spines[spine].set_visible(False)
        ax2.spines[spine].set_visible(False)
    ax2.margins(x=0)

    ax1.spines["bottom"].set_visible(True)

    return fig, ax1, ax2


def plot_abf_sweeps_colored(abf, cmap="tab10", lw=0.8, alpha=1.0, figsize=(8,6)):
    """
    Plot all ADC and DAC sweeps in two vertically stacked subplots,
    each sweep with a unique but corresponding color.

    Parameters
    ----------
    abf : pyabf.ABF
        The ABF object to plot.
    cmap : str or Colormap
        Matplotlib colormap to cycle through for sweeps.
    lw : float
        Line width for traces.
    alpha : float
        Transparency of traces (0 = fully transparent, 1 = opaque).
    figsize : tuple
        Size of the figure.

    Returns
    -------
    fig, (ax1, ax2) : matplotlib objects
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, sharex=True)

    # Pick a colormap and generate colors
    cmap = plt.get_cmap(cmap)
    colors = [cmap(i % cmap.N) for i in range(len(abf.sweepList))]

    # --- Plot ADC sweeps ---
    for i, s in enumerate(abf.sweepList):
        abf.setSweep(s)
        ax1.plot(
            abf.sweepX, abf.sweepY,
            color=colors[i], lw=lw, alpha=alpha,
            label=f"Sweep {s}"
        )
    ax1.set_ylabel(abf.sweepLabelY)
    ax1.set_title("ADC sweeps")

    # --- Plot DAC sweeps ---
    for i, s in enumerate(abf.sweepList):
        abf.setSweep(s)
        ax2.plot(
            abf.sweepX, abf.sweepC,
            color=colors[i], lw=lw, alpha=alpha
        )
    ax2.set_xlabel(abf.sweepLabelX)
    ax2.set_ylabel(abf.sweepLabelC)
    ax2.set_title("DAC sweeps")

    # Optional: add legends (only if not too many sweeps)
    if len(abf.sweepList) <= 10:
        ax1.legend(loc="upper right", fontsize="small", ncol=2)

    fig.tight_layout()
    return fig, (ax1, ax2)



def plot_abf_sweeps_with_legend(
    abf, cmap="tab10", lw=0.8, alpha=1.0, figsize=(10,6),
    legend_loc='upper right', legend_bbox=(1.02, 0.95), legend_pad=0.5, legend_fontsize='small'
):
    """
    Plot all ADC and DAC sweeps with a customizable legend.
    
    legend_loc : str
        Reference location of the legend (Matplotlib loc string).
    legend_bbox : tuple
        Coordinates to shift legend relative to loc (x, y).
    legend_pad : float
        Padding between axes and legend.
    legend_fontsize : str or int
        Font size of legend labels.
    """
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, sharex=True, constrained_layout=True)

    cmap = plt.get_cmap(cmap)
    colors = [cmap(i % cmap.N) for i in range(len(abf.sweepList))]

    for i, s in enumerate(abf.sweepList):
        abf.setSweep(s)
        ax1.plot(abf.sweepX, abf.sweepY, color=colors[i], lw=lw, alpha=alpha)
        ax2.plot(abf.sweepX, abf.sweepC, color=colors[i], lw=lw, alpha=alpha)

    ax1.set_ylabel(abf.sweepLabelY)
    ax1.set_title("ADC sweeps")
    ax2.set_xlabel(abf.sweepLabelX)
    ax2.set_ylabel(abf.sweepLabelC)
    ax2.set_title("DAC sweeps")

    handles = [plt.Line2D([0], [0], color=colors[i], lw=3, alpha=alpha) for i in range(len(abf.sweepList))]
    labels = [f"{s}" for s in abf.sweepList]

    fig.legend(
        handles, labels,
        loc=legend_loc,
        bbox_to_anchor=legend_bbox,
        borderaxespad=legend_pad,
        title="Sweeps",
        fontsize=legend_fontsize
    )

    return fig, (ax1, ax2)


def plot_abf_sweeps_with_legend3(
    abf, file_path=None, cmap="tab10", lw=0.8, alpha=1.0, figsize=(10,6),
    legend_loc='upper right', legend_bbox=(1.02, 0.95), legend_pad=0.5, legend_fontsize='small'
):
    """
    Plot all ADC and DAC sweeps with a customizable legend.
    
    Parameters
    ----------
    abf : pyabf.ABF
        Loaded ABF object.
    file_path : str, optional
        Path of the ABF file, used to set the figure title.
    legend_loc : str
        Reference location of the legend (Matplotlib loc string).
    legend_bbox : tuple
        Coordinates to shift legend relative to loc (x, y).
    legend_pad : float
        Padding between axes and legend.
    legend_fontsize : str or int
        Font size of legend labels.
    """
    import matplotlib.pyplot as plt
    import os

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, sharex=True, constrained_layout=True)

    cmap = plt.get_cmap(cmap)
    colors = [cmap(i % cmap.N) for i in range(len(abf.sweepList))]

    for i, s in enumerate(abf.sweepList):
        abf.setSweep(s)
        ax1.plot(abf.sweepX, abf.sweepY, color=colors[i], lw=lw, alpha=alpha)
        ax2.plot(abf.sweepX, abf.sweepC, color=colors[i], lw=lw, alpha=alpha)

    ax1.set_ylabel(abf.sweepLabelY)
    ax1.set_title("ADC sweeps")
    ax2.set_xlabel(abf.sweepLabelX)
    ax2.set_ylabel(abf.sweepLabelC)
    ax2.set_title("DAC sweeps")

    # Legend with sweep numbers
    handles = [plt.Line2D([0], [0], color=colors[i], lw=3, alpha=alpha) for i in range(len(abf.sweepList))]
    labels = [f"{s}" for s in abf.sweepList]
    fig.legend(
        handles, labels,
        loc=legend_loc,
        bbox_to_anchor=legend_bbox,
        borderaxespad=legend_pad,
        title="Sweeps",
        fontsize=legend_fontsize
    )

    # Title = filename (if provided)
    if file_path is not None:
        fig.suptitle(os.path.abspath(file_path), fontsize=8, y=1.02)

    return fig, (ax1, ax2)



def plot_abf_sweep(abf, sweep=0, color_adc="C0", color_dac="C3", lw=0.8):
    """
    Plot a single sweep from an ABF file with ADC on the left y-axis
    and DAC on the right y-axis.
    
    Parameters:
    -----------
    abf : pyabf.ABF
        The ABF object.
    sweep : int
        Sweep number to plot (default 0).
    color_adc : str
        Color for the ADC waveform (default "C0").
    color_dac : str
        Color for the DAC waveform (default "C3").
    lw : float
        Line width (default 0.8).
    """
    # Set the sweep
    abf.setSweep(sweep)
    
    # Create the figure
    fig, ax1 = plt.subplots(figsize=(8, 5))
    
    # Plot the recorded curve (ADC) on the left axis
    ax1.plot(abf.sweepX, abf.sweepY, color=color_adc, lw=lw, label="ADC waveform")
    ax1.set_xlabel(abf.sweepLabelX)
    ax1.set_ylabel(abf.sweepLabelY, color=color_adc)
    ax1.tick_params(axis='y', labelcolor=color_adc)
    
    # Create a second y-axis for the control curve (DAC)
    ax2 = ax1.twinx()
    ax2.plot(abf.sweepX, abf.sweepC, color=color_dac, lw=lw, label="DAC waveform")
    ax2.set_ylabel(abf.sweepLabelC, color=color_dac)
    ax2.tick_params(axis='y', labelcolor=color_dac)
    
    # Improve layout
    fig.tight_layout()
    plt.show()

