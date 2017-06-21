import qplots
import numpy as np

a0 = 5
f0 = 5
x = np.arange(0.0, 1.0, 0.00001)
y = a0*np.sin(2*np.pi*f0*x)

qplots.dynamic_zoom_plot(x, y, 2000)
