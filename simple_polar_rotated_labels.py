# -*- coding: utf-8 -*-

# Ref https://stackoverflow.com/questions/46719340/how-to-rotate-tick-labels-in-polar-matplotlib-plot
# Kudos to ImportanceOfBeingErnest
# Comments added for gallery/pedagogical purpose
# Minor variations on the original theme added.
#
# Adam Vercingetorix Stephen 2023-10-22

# TODO: for fun, animations with the red and black labels rotating on the spot
# spinning around the outside (two counter rotating sets)
# running out and back...
# then animating within the plane while the plane itself flips and rotates


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
import pdb

@dataclass
class PolarPlotter():
    """
    Encapsulate variations on a theme of the original.
    
    Initializer created automatically via @dataclass decorator
    
    Usage
    
    pp = PolarPlotter()
             r_max = 2, 
             r_ticks = 5,
             rotate_xticks = True,
             translate_xticks_degrees = 0,
             animate = False)
    """
    r_max: int = 2
    r_ticks: int = 5
    rotate_xticks: bool = True
    translate_xticks_degrees: float = 0.0
    animate: bool = False
    verbose: bool = False
    trace: bool = False
    
    def print(self, msg):
        """
        Yet another self invented debug/print mechanism.
        """
        if self.verbose: print(msg)
        
    def set_trace(self):
        """
        Leave the option to drop into pdb scattered around but harmless.
        """
        if self.trace: pdb.set_trace()
        
    def plot(self):
        
        r_max= self.r_max 
        r_ticks = self.r_ticks
        
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
        self.print(xticklabels)
        #self.set_trace()
        
        # We find an array of Text(theta, r, label_string) objects
        # which confusingly have r defined as zero.
        # Something is going on under the hood to move these out
        # to the edge of the plot.
        # We can interrogate this via label.get_transform().get_matrix()
        #
        # This returns 
        # label.get_transform().get_matrix()
        # Out  [10]: 
        # array([[ 54.36,   0.  , 221.4 ],
        #       [  0.  ,  54.36, 158.72],
        #       [  0.  ,   0.  ,   1.  ]])
        #
        # This is scaling in the X,Y directions by 54.36
        # and translating proportional to the Z component of any vector.
        #
        # Transformations are used to determine the final position of
        # elements drawn on the canvas.
        #
        # Transforms have affine and non-affine parts.
        #
        # Affine = translate/scale/rotate/skew - preserve parallel lines
        #  but not necessarily euclidean distances and angles.
        
        
        plt.gcf().canvas.draw()
        
        # Redrawing all of the theta labels, with translated text.
        angles = np.linspace(0,2*np.pi,len(ax.get_xticklabels())+1)
        angles[np.cos(angles) < 0] = angles[np.cos(angles) < 0] + np.pi
        angles = np.rad2deg(angles)
        labels = []
        for label, angle in zip(ax.get_xticklabels(), angles):
            x,y = label.get_position()
            # By virtue of the projection, 
            # x is angle in radians
            # y is incomprehensibly zero
            # We will print three versionsof the label
            # In blue, the original position, rotated
            lab = ax.text(x,y, label.get_text(), transform=label.get_transform(),
                        ha=label.get_ha(), va=label.get_va(), color="blue")
            lab.set_rotation(angle)
            x_dtheta = x + np.radians(self.translate_xticks_degrees)
            lab_dtheta = ax.text(x_dtheta,y, label.get_text(), transform=label.get_transform(),
                        ha=label.get_ha(), va=label.get_va(), color="red")
            y_dr = -0.2 * r_max
            lab_dr= ax.text(x, y_dr, label.get_text(), transform=label.get_transform(),
                        ha=label.get_ha(), va=label.get_va(), color="black")
            
            lab_dtheta.set_rotation(angle)
            
            labels.extend([lab, lab_dtheta, lab_dr])
        #self.set_trace()
        ax.set_xticklabels([])
        
        plt.show()
        
if __name__ == '__main__':
    pp = PolarPlotter(trace = True, translate_xticks_degrees=22.5)
    pp.plot()