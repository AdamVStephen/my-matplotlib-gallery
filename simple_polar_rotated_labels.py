# -*- coding: utf-8 -*-

# Ref https://stackoverflow.com/questions/46719340/how-to-rotate-tick-labels-in-polar-matplotlib-plot
# Kudos to ImportanceOfBeingErnest
# Comments added for gallery/pedagogical purpose
# Minor variations on the original theme added.
#
# Adam Vercingetorix Stephen 2023-10-22

import numpy as np
import matplotlib.pyplot as plt
import pdb

r_max = 2
r_ticks = 5

r = np.arange(0, r_max, 0.01)
theta = 2 * np.pi * r

ax = plt.subplot(111, projection='polar')
ax.plot(theta, r)

# Set the radial axis maximum to just fit the data
ax.set_rmax(r_max)
ax.set_rticks(np.arange(0,r_max, r_max/r_ticks))

# For reference : can interrogate default settings
#default_rlabel_position = ax.get_rlabel_position()
#print(default_rlabel_position)

# Or override them
ax.set_rlabel_position(np.radians(0))

# Extract the "x" ticklabels
xticklabels = ax.get_xticklabels()
print(xticklabels)
# We find an array of Text(theta, r, label_string) objects
# which confusingly have r defined as zero.
# Something is going on under the hood to move these out
# to the edge of the plot.
# We can interrogate this via label.get_transform().get_matrix()
#
# This returns 
#label.get_transform().get_matrix()
#Out  [10]: 
#array([[ 54.36,   0.  , 221.4 ],
#       [  0.  ,  54.36, 158.72],
#       [  0.  ,   0.  ,   1.  ]])
#


plt.gcf().canvas.draw()

# Redrawing all of the theta labels, with translated text.
angles = np.linspace(0,2*np.pi,len(ax.get_xticklabels())+1)
angles[np.cos(angles) < 0] = angles[np.cos(angles) < 0] + np.pi
angles = np.rad2deg(angles)
labels = []
for label, angle in zip(ax.get_xticklabels(), angles):
    x,y = label.get_position()
    pdb.set_trace()
    lab = ax.text(x,y, label.get_text(), transform=label.get_transform(),
                ha=label.get_ha(), va=label.get_va())
    lab.set_rotation(angle)
    labels.append(lab)
#ax.set_xticklabels([])

plt.show()