# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 10:41:24 2023

@author: astephen
"""

# -*- coding: utf-8 -*-


# Ref https://medium.com/@symon.kopec/smart-way-to-create-dartboard-heat-map-plot-in-python-using-matplotlib-c6c1fb2b3cb1#:~:text=A%20Smart%20Way%20to%20Create%20Dartboard%20Heatmap%20Plots%20in%20Python%20Using%20Matplotlib,-SymKo&text=One%20of%20the%20easiest,illustrative%20statistics%20from%20dart%20throws.
# Kudos to Symon Kopec
#
# Derivative work using a similar technique, but with some improvements
# and some significant differences.
#
# Adam Vercingetorix Stephen 2023-10-22


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
    
        
# Python type hinting was a WIP for a while, which is a pain.
# TODO: Refactor when I nure what list of strings is supported in which python  
# @dataclass
class DartboardHeatmap():
    """
    Encapsulate variations on a theme of the original.
        
    Draws a dartboard of azimuthal sectors labelled by labels
    array of strings.   
    
    Initializer created automatically via @dataclass decorator
    
    Arguments are logically flexible such that 
        if azm_labels is provided, n_azm is calculated
    
    Usage : 
        dh = DartboardHeatmap(args as per decorations below)
        dh.setup()
        dh.plot()
   """

    # Python type hinting was a WIP for a while, which is a pain
    # labels: list[str] = [ 20, 5, 12, 9, 14, 11, 8, 16, 7, 19, 3, 17, 2, 15, 10, 6, 13, 4, 18, 1]
    def __init__(self, labels=[], title = ""):
        if len(labels) == 0:
            self.labels = [ 20, 5, 12, 9, 14, 11, 8, 16, 7, 19, 3, 17, 2, 15, 10, 6, 13, 4, 18, 1]
            self.title = "Dartboard"
        else:
            self.labels = labels
            self.title = title
  
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
        
    def setup(self):
        """
        Geometrical calculations
    
        Returns
        -------
        None.

        """
        self.n_r = 21
        self.n_theta = len(self.labels)
        self.azm_delta = int(360/self.n_theta)
        self.azm_offset_degrees = int(self.azm_delta/2)
        self.draw()
        return None
        
    def draw(self):
        self.fig, self.axi = plt.subplots(subplot_kw={'projection': 'polar'})
        self.fig.set_size_inches((10,10))
        # the 5,20,1 etc. field grids
        self.axi.set_thetagrids(list(range(
                    self.azm_offset_degrees, 
                    360 + self.azm_offset_degrees,
                    self.azm_delta))
                           , self.labels
                           , verticalalignment='center'
                           , horizontalalignment = 'center')
        
        # the proportions radius of inners and outer circle
        rad = np.linspace(0, 10.5, self.n_r)
        azm = np.linspace(0, 2 * np.pi, self.n_theta)
        
        #self.axi.set_rgrids([0.1, 1.8])
            
        # radius, r fields outer and inner bullseye
        self.axi.set_rticks([1.8, 5.5, 6, 10.0,10.5])
        self.axi.set_theta_zero_location("N",offset=0.0)
        self.axi.set_yticklabels([])
        
        # Redrawing all of the theta labels, with translated text.
        angles = np.linspace(0,2*np.pi,len(self.axi.get_xticklabels())+1)
        angles[np.cos(angles) < 0] = angles[np.cos(angles) < 0] + np.pi
        angles = np.rad2deg(angles)
        labels = []
        for label, angle in zip(self.axi.get_xticklabels(), angles):
            x,y = label.get_position()
            # By virtue of the projection, 
            # x is angle in radians
            # y is incomprehensibly zero
            # We will print three versionsof the label
            # In blue, the original position, rotated
            x_dtheta = x + np.radians(-1*self.azm_offset_degrees)
            lab_dtheta = self.axi.text(x_dtheta,y, label.get_text(), transform=label.get_transform(),
                                 ha=label.get_ha(), va=label.get_va(), color="red", fontsize='x-large')
            
            #lab_dtheta.set_rotation(angle)
            
            labels.append(lab_dtheta)
            #pdb.set_trace()
        #self.axi.set_xticklabels([])
        
            
    def annotate(self, x, y, text, color = "black",org = None):
        self.axi.set_xticklabels([])
        org_colours = {
            "com" : "blue",
            "edu" : "orange",
            "lab": "green", 
            "proj" : "purple",
            "acu" : "red"
            }
        if org in org_colours : 
            color = org_colours[org]
        elif org == None:
            color= "purple"
        else:
            color = "black"
            
        self.axi.text(x,y,text, 
                      color=color, 
                      fontsize='xx-large', 
                      multialignment="center")
        
    def light_up_the_trebles(self):
        pass
        
    def plot(self):    
        plt.show()
        
            
if __name__ == '__main__':
    #pp = PolarPlotter(trace = True, translate_xticks_degrees=22.5)
    #pp.plot()
    dh = DartboardHeatmap()
    dh.setup()
    dh.plot()
    # Dartboard that runs from 1 to 10
    ten_dh = DartboardHeatmap(labels=[1,2,3,4,5,6,7,8,9,10])
    ten_dh.setup()
    ten_dh.plot()
    # Dartboard Diagram for Computing Division
    cd_dh = DartboardHeatmap(labels=["STEP", "RACE", "SPO", "Innovation", "BD", "OAS"])
    cd_dh.setup()
    for th in range(0, 10,2):
        for rr in range(0,10,2):
            #cd_dh.annotate(np.pi*2*th/10, rr, "(%.1f,%.1f)" % (th, rr))
            pass
    cd_dh.annotate(1.7, 1.0, "Adv\nControl", org = "acu")
    
    cd_dh.annotate(0.3, 8.5, "CyberSecurity\nNetworks", org="proj")
    cd_dh.annotate(0.3, 6.5, "PCS Architecture\nDiagnostics")
    cd_dh.annotate(0.3, 3.5, "CosyLab", org="com")
    
    cd_dh.annotate(0.85, 8.5, "RTstudio")
    
    cd_dh.annotate(1.2, 8.5, "JET\nRTCC2\nPCS")
    cd_dh.annotate(1.1,4.5, "digiLab", org="com")
   
    cd_dh.annotate(1.8, 9.5, "MAST-U\nPCS")
    cd_dh.annotate(2.1, 9, "ITER\nPFPO1")
    cd_dh.annotate(2.0, 4.5, "IPP", org="lab")
    
    cd_dh.annotate(3.1, 9, "NIMBUS")
    cd_dh.annotate(2.8, 4.0, "UPM", org="edu")
    cd_dh.annotate(2.8, 5.0, "Tok.Energy", org="com")
    
    cd_dh.annotate(4., 7, "CFS + GF\nConsultancy", org="com")
    
    cd_dh.annotate(5.5, 6.5, "Fusionics\nSkills")
    cd_dh.annotate(5.5, 3.0, "Sygensys", org="com")
    
    cd_dh.plot()
    