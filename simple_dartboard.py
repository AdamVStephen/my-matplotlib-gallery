# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 18:06:42 2023

@author: astephen
"""

import sys

if not sys.version_info > (2,7):
    print("Python2 went end of life at Jan 1 2020.  Time to upgrade yourself.")
    sys.exit(42)
elif not sys.version_info >= (3,7):
    print("Using dataclasses which requires >= 3.7")
    sys.exit(37)
    
from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pdb
fig, axi = plt.subplots(subplot_kw={'projection': 'polar'})
fig.set_size_inches((10,10))
 
# the 5,20,1 etc. field grids
axi.set_thetagrids(list(range(9,369,18)),
        [20, 5, 12, 9, 14, 11, 8, 16, 7, 19
         , 3, 17, 2, 15, 10, 6, 13, 4, 18, 1]
        , verticalalignment='center'
        , horizontalalignment = 'center')
# the proportions radius of inners and outer circle
rad = np.linspace(0, 10.5, 21)


# BUG in the original - has the plots shifted by 9 degrees
# because the axes are being rotated so that the top sector
# has bilateral symmetry
# azm = np.linspace(0, 2 * np.pi, 21)

azm = np.linspace(np.radians(9), np.radians(369), 21)


axi.set_rgrids([0.1, 1.8])
        
# radius, r fields outer and inner bullseye
axi.set_rticks([0.3, 0.8, 5.5, 6, 10.0])
axi.set_theta_zero_location("N",offset=0.0)
axi.set_yticklabels([])

radius, theta = np.meshgrid(rad, azm)
#z_values = z_fields

z_values = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ,[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ,[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ,[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ,[1, 0, 0, 0, 0, 0, 0, 10, 20, 20, 30, 40, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ,[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ,[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ,[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ,[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ,[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ,[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ,[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ,[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ,[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ,[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ,[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ,[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ,[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ,[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ,[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ]

#pdb.set_trace()

z_values_np = np.zeros((20,20),int)


z_values_np[14,5:15] = 20
z_values_np[13,5:15] = 30
z_values_np[10,5:15] = 20
z_values_np[4,11:12] = 25
z_values_np[3,5:10] = 10


pdb.set_trace()
plt.pcolormesh(theta, radius, z_values_np, cmap ='twilight')
plt.colorbar(label="throws"
           , orientation="vertical"
           , fraction=0.046
           , pad=0.2)
axi.grid(True)
axi.set_title("Dartboard", va='bottom')