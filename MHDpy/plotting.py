# -*- coding: utf-8 -*-
"""
Various plot classes and functions for making plots during data analysis.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation, rc
from IPython.display import HTML


class PLplot():
    
    def __init__(self,Laser, Lasertime, peak1, peak2, PLtime):
        self.fig, self.ax1 = plt.subplots(figsize = (8,6))
        ln1 = self.ax1.plot(PLtime, peak1, 'b.', label = 'Peak 1')
        ln2 = self.ax1.plot(PLtime, peak2, 'g.', label = 'Peak 2')
        
        self.ax2 = self.ax1.twinx()
        
        self.ax2.set_ylabel("Laser Intensity (Normalized)")
        self.ax2.tick_params('y')
        
        plt.legend()
        
        ln3 = self.ax2.plot(Lasertime, Laser, 'r', label = 'Laser profile')
        
        self.ax1.set_xlabel("Gate Delay (ns)")
        # Make the y-axis label, ticks and tick labels match the line color.
        self.ax1.set_ylabel("$Delta$ PL Intensity (Normalized)")
        self.ax1.tick_params('y')
        
        
        
        
        self.fig.suptitle('Potassium HVOF PL', y = 1)
        self.fig.tight_layout()
        
        lns = ln1+ln2+ln3
        labs = [l.get_label() for l in lns]
        self.ax1.legend(lns, labs, loc=0)
        
        self.ax2.set_yscale('log')
        self.ax1.set_yscale('log')
        
        #self.ax1.set_ylim((0.00001),2)
        #self.ax2.set_ylim((0.00001),2)
        #self.ax1.set_xlim(-20,60)
    
    



def spectral_anim(RawData_Frames, spectra_wl,spectra_time_off , interval = 15):
    """
    Matplotlib Animation Example
    
    author: Jake Vanderplas
    email: vanderplas@astro.washington.edu
    website: http://jakevdp.github.com
    license: BSD
    Please feel free to use and modify this, but keep the above information. Thanks!
    """
    


    
    

    
    xs = spectra_wl
    
    # First set up the figure, the axis, and the plot element we want to animate
    fig = plt.figure()
    ax = plt.axes(xlim=(xs[0], xs[-1]), ylim=(0, 1.1))
    
    line, = ax.plot([], [], lw=2)
    
    time_template = 'Gate Delay = %.1fns'
    time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
    
    
    
    # initialization function: plot the background of each frame
    def init():
        line.set_data([], [])
        time_text.set_text('')
        ax.set_ylabel("Normalized Emission Intensity (a.u.)")
        ax.set_xlabel("Wavelength (nm)") 
        return line,
    
    # animation function.  This is called sequentially
    def animate(i):
        y = RawData_Frames.iloc[:,i].as_matrix()
        y = y/RawData_Frames.max().max()
        line.set_data(xs, y)
        time_text.set_text(time_template % spectra_time_off[i])
        return line, time_text
    
    
    
    # call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=len(spectra_time_off), interval = interval, blit=True)
    
    
    #TML(anim.to_html5_video())
    
    # equivalent to rcParams['animation.html'] = 'html5'
    rc('animation', html='html5')
    
    return anim




def PL_waterfall(RawData_Frames, spectra_wl,spectra_time_off):
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib.collections import PolyCollection
    from matplotlib import colors as mcolors
    
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    
    
    def cc(arg):
        return mcolors.to_rgba(arg, alpha=0.6)
    
    xs = spectra_wl
    verts = []
    zs = spectra_time_off
    i=0
    numexposures = len(zs)- 1
    for z in zs:
        ys = RawData_Frames.iloc[:,numexposures-i].as_matrix()
        i=i+1
        ys[0], ys[-1] = 0, 0
        verts.append(list(zip(xs, ys)))
        
        
    poly = PolyCollection(verts, facecolors = (1,1,1,0), edgecolors=(0,0,1,0.5))
    #poly.set_alpha(0.2)
    #face_color = [0, 0, 0] # alternative: matplotlib.colors.rgb2hex([0.5, 0.5, 1])
    #poly.set_edgecolor(face_color)
    ax.add_collection3d(poly, zs=zs, zdir='y')
    
    
    ax.set_xlabel('X')
    ax.set_xlim3d(xs[0], xs[-1])
    ax.set_ylabel('Y')
    ax.set_ylim3d(zs[0], zs[-1])
    ax.set_zlabel('Z')
    ax.set_zlim3d(0, RawData_Frames.max().max())
    
    
    ax.view_init(20, 300)
    plt.show()
