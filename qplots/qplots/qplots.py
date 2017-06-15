import matplotlib as _mpl
import numpy as _np
import matplotlib.pyplot as _plt
import seaborn as _sns

_mpl.rcParams['lines.markeredgewidth'] = 1 # set default markeredgewidth to 1 overriding seaborn's default value of 0
_sns.set_style("whitegrid")

def joint_plot(x, y, marginalBins=50, gridsize=50, plotlimits=None, logscale=False, cmap="inferno_r", marginalCol=None, figsize=(6, 6), ShowFig=True):
    """

    """

    # definitions for the axes
    scatter_marginal_seperation = 0.01
    left, width = 0.2, 0.65-0.1 # left = left side of scatter and hist_x
    bottom, height = 0.1, 0.65-0.1 # bottom = bottom of scatter and hist_y
    bottom_h = height + bottom + scatter_marginal_seperation
    left_h = width + left + scatter_marginal_seperation
    cbar_pos = [0.03, bottom, 0.05, 0.1+width]

    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom_h, width, 0.2]
    rect_histy = [left_h, bottom, 0.2, height]

    # start with a rectangular Figure
    fig = _plt.figure(1, figsize=figsize)

    axScatter = _plt.axes(rect_scatter)
    axHistx = _plt.axes(rect_histx)
    axHisty = _plt.axes(rect_histy)

    # scale specific settings
    if logscale == True:
        scale='log'
        hexbinscale = 'log'
    else:
        scale='linear'
        hexbinscale = None

    # set up colors 
    cmapOb = _mpl.cm.get_cmap(cmap)
    cmapOb.set_under(color='white')
    if marginalCol == None:
        if logscale == True:
            marginalCol = cmapOb(0.7)
            cbarlabel = 'log10(N)'
        else:
            marginalCol = cmapOb(0.5)
            cbarlabel = 'N'

    # set up limits

    if plotlimits == None:
        xmin = x.min()
        xmax = x.max()
        ymin = y.min()
        ymax = y.max()

        if xmax > ymax:
            plotlimits = xmax * 1.1
        else:
            plotlimits = ymax * 1.1

    # the scatter plot:
    hb = axScatter.hexbin(x, y, gridsize=gridsize, bins=hexbinscale, cmap=cmapOb, alpha=0.8)
    axScatter.axis([-plotlimits, plotlimits, -plotlimits, plotlimits])
    cbaxes = fig.add_axes(cbar_pos)  # This is the position for the colorbar
    #cb = _plt.colorbar(axp, cax = cbaxes)
    cb = fig.colorbar(hb, cax = cbaxes)
    cb.set_label(cbarlabel)

    axScatter.set_xlim((-plotlimits, plotlimits))
    axScatter.set_ylim((-plotlimits, plotlimits))

    # now determine bin size
    binwidth = (2*plotlimits)/marginalBins
    xymax = _np.max([_np.max(_np.fabs(x)), _np.max(_np.fabs(y))])
    lim = plotlimits #(int(xymax/binwidth) + 1) * binwidth

    bins = _np.arange(-lim, lim + binwidth, binwidth)
    axHistx.hist(x, bins=bins, color=marginalCol, alpha=0.7)
    axHistx.set_yscale(value=scale)
    axHisty.hist(y, bins=bins, orientation='horizontal', color=marginalCol, alpha=0.7)
    axHisty.set_xscale(value=scale)

    _plt.setp(axHistx.get_xticklabels(), visible=False) # sets x ticks to be invisible while keeping gridlines
    _plt.setp(axHisty.get_yticklabels(), visible=False) # sets x ticks to be invisible while keeping gridlines

    axHistx.set_xlim(axScatter.get_xlim())
    axHisty.set_ylim(axScatter.get_ylim())


    if ShowFig == True:
        _plt.show()
    return fig, axScatter, axHistx, axHisty, cb

