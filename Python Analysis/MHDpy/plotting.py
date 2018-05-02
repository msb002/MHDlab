# -*- coding: utf-8 -*-
"""
Created on Wed May  2 04:34:21 2018

@author: aspit
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation, rc
from IPython.display import HTML


def PL(Laser, Lasertime, peak1, peak2, PLtime):
    fig, ax1 = plt.subplots(figsize = (8,6))
    ln1 = ax1.plot(PLtime, peak1, 'b.', label = '767 peak')
    ln2 = ax1.plot(PLtime, peak2, 'g.', label = '770 peak')
    
    ax2 = ax1.twinx()
    
    ax2.set_ylabel("Laser Intensity (Normalized)")
    ax2.tick_params('y')
    
    plt.legend()
    
    ln3 = ax2.plot(Lasertime, Laser, 'r', label = 'Laser profile')
    
    ax1.set_xlabel("Gate Delay (ns)")
    # Make the y-axis label, ticks and tick labels match the line color.
    ax1.set_ylabel("$\\Delta$ PL Intensity (Normalized)")
    ax1.tick_params('y')
    
    
    
    
    plt.title("Potassium HVOF PL")
    fig.tight_layout()
    
    lns = ln1+ln2+ln3
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc=0)
    
    ax2.set_yscale('log')
    ax1.set_yscale('log')
    
    #ax1.set_ylim((0.00001),2)
    #ax2.set_ylim((0.00001),2)
    ax1.set_xlim(-20,60)
    
    plt.show()


def spectral_anim(RawData_Frames, spectra_wl,spectra_time_off ):
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
                                   frames=30, interval=15, blit=True)
    
    
    #TML(anim.to_html5_video())
    
    # equivalent to rcParams['animation.html'] = 'html5'
    rc('animation', html='html5')
    
    return anim
