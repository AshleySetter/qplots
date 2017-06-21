import numpy as np
import qplots

#import seaborn # this breaks my fontsize argument =/
#seaborn.set_style("whitegrid") 

# the random data
x = np.random.randn(100000)
y = np.random.randn(100000) 

fig, axscatter, axhistx, axhisty, cm = qplots.joint_plot(x, y, fontsize=8)
axscatter.set_xlabel("variable 1")
axscatter.set_ylabel("variable 2")
qplots.show()

fig.savefig("Example.png")
