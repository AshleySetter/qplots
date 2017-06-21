import matplotlib as _mpl
import numpy as _np
import matplotlib.pyplot as _plt
import matplotlib.font_manager as _font_manager
from matplotlib.pyplot import show
from matplotlib.widgets import Slider, Button, RadioButtons

#_mpl.rcParams['lines.markeredgewidth'] = 1 # set default markeredgewidth to 1 overriding seaborn's default value of 0
_plt.style.use('seaborn-whitegrid')

def joint_plot(x, y, marginalBins=50, gridsize=50, plotlimits=None, logscale_cmap=False, logscale_marginals=False, alpha_hexbin=0.75, alpha_marginals=0.75, cmap="inferno_r", marginalCol=None, figsize=(8, 8), fontsize=8, *args, **kwargs):
    """
    Plots some x and y data using hexbins along with a colorbar
    and marginal distributions (X and Y histograms).

    Parameters
    ----------
    x : ndarray
        The x data
    y : ndarray
        The y data
    marginalBins : int, optional
        The number of bins to use in calculating the marginal
        histograms of x and y
    gridsize : int, optional
        The grid size to be passed to matplotlib.pyplot.hexbins
        which sets the gridsize in calculating the hexbins
    plotlimits : float, optional
        The limit of the plot in x and y (it produces a square 
        area centred on zero. Defaults to max range of data.
    logscale_cmap : bool, optional
        Sets whether to use a logscale for the colormap.
        Defaults to False.
    logscale_marginals : bool, optional
        Sets whether to use a logscale for the marignals.
        Defaults to False.
    alpha_hexbin : float
        Alpha value to use for hexbins and color map
    alpha_marginals : float
        Alpha value to use for marginal histograms
    cmap : string, optional
        Specifies the colormap to use, see
        https://matplotlib.org/users/colormaps.html
        for options. Defaults to 'inferno_r'
    marginalCol : string, optional
        Specifies color to use for marginals,
        defaults to middle color of colormap 
        for a linear colormap and 70% for a 
        logarithmic colormap.
    figsize : tuple of 2 values, optional
        Sets the figsize, defaults to (8, 8)
    fontsize : int, optional
        Sets the fontsize for all text and axis ticks.
        Defaults to 8.
    *args, **kwargs : optional
        args and kwargs passed to matplotlib.pyplot.hexbins
    
    Returns
    -------
    fig : matplotlib.figure.Figure object
        The figure object created to house the joint_plot
    axHexBin : matplotlib.axes.Axes object
        The axis for the hexbin plot
    axHistx : matplotlib.axes.Axes object
        The axis for the x marginal plot
    axHisty : matplotlib.axes.Axes object
        The axis for the y marginal plot
    cbar : matplotlib.colorbar.Colorbar
        The color bar object
    """
    with _plt.rc_context({'font.size': fontsize,}):
        # definitions for the axes
        hexbin_marginal_seperation = 0.01
        left, width = 0.2, 0.65-0.1 # left = left side of hexbin and hist_x
        bottom, height = 0.1, 0.65-0.1 # bottom = bottom of hexbin and hist_y
        bottom_h = height + bottom + hexbin_marginal_seperation
        left_h = width + left + hexbin_marginal_seperation
        cbar_pos = [0.03, bottom, 0.05, 0.02+width]

        rect_hexbin = [left, bottom, width, height]
        rect_histx = [left, bottom_h, width, 0.2]
        rect_histy = [left_h, bottom, 0.2, height]

        # start with a rectangular Figure
        fig = _plt.figure(figsize=figsize)

        axHexBin = _plt.axes(rect_hexbin)
        axHistx = _plt.axes(rect_histx)
        axHisty = _plt.axes(rect_histy)
        axHisty.set_xticklabels(axHisty.xaxis.get_ticklabels(), y=0, rotation=-90)
        
        # scale specific settings
        if logscale_cmap == True:
            hexbinscale = 'log'
        else:
            hexbinscale = None
        if logscale_marginals == True:
            scale='log'
        else:
            scale='linear'
            

        # set up colors 
        cmapOb = _mpl.cm.get_cmap(cmap)
        cmapOb.set_under(color='white')
        if marginalCol == None:
            if logscale_cmap == True:
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

        # the hexbin plot:
        hb = axHexBin.hexbin(x, y, gridsize=gridsize, bins=hexbinscale, cmap=cmap, alpha=alpha_hexbin, extent=(-plotlimits, plotlimits, -plotlimits, plotlimits), *args, **kwargs)
        axHexBin.axis([-plotlimits, plotlimits, -plotlimits, plotlimits])

        cbaraxes = fig.add_axes(cbar_pos)  # This is the position for the colorbar
        #cbar = _plt.colorbar(axp, cax = cbaraxes)
        cbar = fig.colorbar(hb, cax = cbaraxes, drawedges=False) #, orientation="horizontal"
        cbar.solids.set_edgecolor("face")
        cbar.solids.set_rasterized(True)
        cbar.solids.set_alpha(alpha_hexbin)
        cbar.ax.set_yticklabels(cbar.ax.yaxis.get_ticklabels(), y=0, rotation=45)
        cbar.set_label(cbarlabel, labelpad=-25, y=1.05, rotation=0)
    
        axHexBin.set_xlim((-plotlimits, plotlimits))
        axHexBin.set_ylim((-plotlimits, plotlimits))
        
        # now determine bin size
        binwidth = (2*plotlimits)/marginalBins
        xymax = _np.max([_np.max(_np.fabs(x)), _np.max(_np.fabs(y))])
        lim = plotlimits #(int(xymax/binwidth) + 1) * binwidth

        bins = _np.arange(-lim, lim + binwidth, binwidth)
        axHistx.hist(x, bins=bins, color=marginalCol, alpha=alpha_marginals, linewidth=0)
        axHistx.set_yscale(value=scale)
        axHisty.hist(y, bins=bins, orientation='horizontal', color=marginalCol, alpha=alpha_marginals, linewidth=0)
        axHisty.set_xscale(value=scale)

        _plt.setp(axHistx.get_xticklabels(), visible=False) # sets x ticks to be invisible while keeping gridlines
        _plt.setp(axHisty.get_yticklabels(), visible=False) # sets x ticks to be invisible while keeping gridlines

        axHistx.set_xlim(axHexBin.get_xlim())
        axHisty.set_ylim(axHexBin.get_ylim())
        
    return fig, axHexBin, axHistx, axHisty, cbar

def take_closest(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.
    If two numbers are equally close, return the smallest number.

    Parameters
    ----------
    myList : array
        The list in which to find the closest value to myNumber
    myNumber : float
        The number to find the closest to in MyList

    Returns
    -------
    closestValue : float
        The number closest to myNumber in myList
    """
    pos = _bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
        return after
    else:
        return before

def get_closest_index(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.
    If two numbers are equally close, return the smallest number.

    Parameters
    ----------
    myList : array
        The list in which to find the closest value to myNumber
    myNumber : float
        The number to find the closest to in MyList

    Returns
    -------
    closest_values_index : int
        The index in the array of the number closest to myNumber in myList
    """
    closest_values_index = _np.where(self.time == take_closest(myList, myNumber))[0][0]
    return closest_values_index

r1 = None

def dynamic_zoom_plot(x, y, N, RegionStartSize=1000):
    """
    plots 2 time traces, the top is the downsampled time trace
    the bottom is the full time trace.

    
    """
    x_lowres = x[::N]
    y_lowres = y[::N]
    
    ax1 = _plt.subplot2grid((2, 1), (0, 0), colspan=1)
    ax2 = _plt.subplot2grid((2, 1), (1, 0))
    
    fig = ax1.get_figure()
    _plt.subplots_adjust(bottom=0.25) # makes space at bottom for sliders
    
    CenterTime0 = len(x)/2
    TimeWidth0 = len(x)/RegionStartSize
    
    l1, = ax1.plot(x_lowres, y_lowres, lw=2, color='red')
    global r1
    r1 = ax1.fill_between(x_lowres[int((CenterTime0 - TimeWidth0)/N) : int((CenterTime0 + TimeWidth0)/N)], min(y), max(y), facecolor='green', alpha=0.5)
    l2, = ax2.plot(x, y, lw=2, color='red')
    
    
    axcolor = 'lightgoldenrodyellow'
    axCenterTime = _plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
    axTimeWidth = _plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
    
    SliderCentreTime = Slider(axCenterTime, 'Center Time', 0, len(x), valinit=CenterTime0)
    SliderTimeWidth = Slider(axTimeWidth, 'Time Width', 0, len(x), valinit=TimeWidth0)
    
    
    def update(val):
        TimeWidth = SliderTimeWidth.val
        CentreTime = SliderCentreTime.val
        LeftIndex = int(CentreTime-TimeWidth)
        if LeftIndex < 0:
            LeftIndex = 0
        RightIndex = int(CentreTime+TimeWidth)
        if RightIndex > len(x)-1:
            RightIndex = len(x)-1
        global r1
        r1.remove()
        r1 = ax1.fill_between(x[LeftIndex:RightIndex], min(y), max(y), facecolor='green', alpha=0.5)
        l2.set_xdata(x[LeftIndex:RightIndex])
        l2.set_ydata(y[LeftIndex:RightIndex])
        ax2.set_xlim([x[LeftIndex], x[RightIndex]])
        fig.canvas.draw_idle()
    SliderCentreTime.on_changed(update)
    SliderTimeWidth.on_changed(update)
    
    resetax = _plt.axes([0.8, 0.025, 0.1, 0.04])
    button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
    
    
    def reset(event):
        SliderCentreTime.reset()
        SliderTimeWidth.reset()
    button.on_clicked(reset)    
    
    _plt.show()
