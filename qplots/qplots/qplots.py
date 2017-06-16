import matplotlib as _mpl
import numpy as _np
import matplotlib.pyplot as _plt
import matplotlib.font_manager as _font_manager
from matplotlib.pyplot import show
from matplotlib.widgets import Slider, Button, RadioButtons

#_mpl.rcParams['lines.markeredgewidth'] = 1 # set default markeredgewidth to 1 overriding seaborn's default value of 0
_plt.style.use('seaborn-ticks')

def joint_plot(x, y, marginalBins=50, gridsize=50, plotlimits=None, logscale=False, cmap="inferno_r", marginalCol=None, figsize=(6, 6), fontsize=8, *args, **kwargs):
    """

    """
    with _plt.rc_context({'font.size': fontsize,
    }
    ):
        # definitions for the axes
        scatter_marginal_seperation = 0.01
        left, width = 0.2, 0.65-0.1 # left = left side of scatter and hist_x
        bottom, height = 0.1, 0.65-0.1 # bottom = bottom of scatter and hist_y
        bottom_h = height + bottom + scatter_marginal_seperation
        left_h = width + left + scatter_marginal_seperation
        cbar_pos = [0.03, bottom, 0.05, 0.02+width]

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
        hb = axScatter.hexbin(x, y, gridsize=gridsize, bins=hexbinscale, cmap=cmapOb, alpha=0.8,  *args, **kwargs)
        axScatter.axis([-plotlimits, plotlimits, -plotlimits, plotlimits])

        cbaxes = fig.add_axes(cbar_pos)  # This is the position for the colorbar
        #cb = _plt.colorbar(axp, cax = cbaxes)
        cb = fig.colorbar(hb, cax = cbaxes) #, orientation="horizontal"
        cb.set_label(cbarlabel, labelpad=-25, y=1.05, rotation=0)        
    
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
        
    return fig, axScatter, axHistx, axHisty, cb

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
