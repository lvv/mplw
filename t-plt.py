#!/usr/bin/python
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['figure.title'] = "rc Title"
fig = plt.figure()


rect = 0.5, 0.1, 0.4, 0.8
ax = fig.add_subplot(111, position=rect)
#fig.add_axes(rect)

ax.plot(10*np.random.randn(100), 10*np.random.randn(100), 'o')
ax.set_title('Using hypen instead of unicode minus')
plt.show()

