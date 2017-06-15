import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

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
    
a0 = 5
f0 = 5
x = np.arange(0.0, 1.0, 0.00001)
y = a0*np.sin(2*np.pi*f0*x)

N=1
x_lowres = x[::N]
y_lowres = y[::N]

ax1 = plt.subplot2grid((2, 1), (0, 0), colspan=1)
ax2 = plt.subplot2grid((2, 1), (1, 0))

fig = ax1.get_figure()
plt.subplots_adjust(bottom=0.25) # makes space at bottom for sliders

CenterTime0 = len(x)/2
TimeWidth0 = len(x)/2

l1, = ax1.plot(x_lowres, y_lowres, lw=2, color='red')
r1 = ax1.fill_between(x[int(CenterTime0 - TimeWidth0) : int(CenterTime0 + TimeWidth0)], min(y), max(y), facecolor='green', alpha=0.5)
l2, = ax2.plot(x, y, lw=2, color='red')


axcolor = 'lightgoldenrodyellow'
axCenterTime = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
axTimeWidth = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)

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

resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')


def reset(event):
    SliderCentreTime.reset()
    SliderTimeWidth.reset()
button.on_clicked(reset)


plt.show()
