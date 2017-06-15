import numpy as np
import qplots

# the random data
x = np.random.randn(1000)
y = np.random.randn(1000)

fig, axscatter, axhistx, axhisty, cm = qplots.joint_plot(x, y)

fig.savefig("Example.png")
