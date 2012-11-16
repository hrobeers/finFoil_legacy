# -*- coding: utf-8 -*-
"""
Created on Mon Oct 03 16:04:51 2011

This file contains code from the finFoil project that is not used anymore but
wich can still be usefull in the future

@author: hrobeers
"""

def naca(self, thickness, points):
    """ generate the 4-digit naca airfoil profile """
    
    x = linspace(0,1,points)
    #t = thickness/chordlength
    
    a1 = 0.2969  * sqrt(x)
    b1 = -0.1260 * (x)
    c1 = -0.3516 * (x)**2
    d1 = 0.2843 * (x)**3
    e1 = -0.1015 * (x)**4
    profile = thickness/0.2 * (a1+b1+c1+d1+e1) # * chordlength
    
    return profile

"""
"""

def gen_contour_cubic(self):
    """ Cubic spline interpolate the input points """
    
    n_inputpoints = self.pointdata.size/2
    
    t = arange(0,n_inputpoints)
    x = interp1d(t,self.pointdata[:,0],kind='cubic')
    y = interp1d(t,self.pointdata[:,1],kind='cubic')        
    
    t_int = linspace(0,n_inputpoints-1,self.con_resolution)
    self.contour.setX(x(t_int))
    self.contour.setY(y(t_int))

"""
"""

if self.fortran:
    surf = make_surface(self.resolution[0],leading_edge_grid,trailing_edge_grid,thick,self.resolution[1])
else:
    surf = ones(self.resolution)*nan #*self.thick
    points = trailing_edge_grid - leading_edge_grid
    for i in arange(0,self.resolution[1]-1):
        if False:
            # naca in fortran
            surf[leading_edge_grid[i]:trailing_edge_grid[i],i] = naca_val(thick[i],points[i])
        else:
            # naca in python
            surf[leading_edge_grid[i]:trailing_edge_grid[i],i] = self.naca(thick[i],points[i])
            
"""
"""

if self.fortran:
    # Loop in fortran
    yval = spline_val(t,ydata,t_int,n_dim,len(t),len(t_int))
else:
    # Loop in python, val in fortran
    lt = len(t)
    yval = zeros((2,n_val))
    
    for i in arange(0,n_val):
        yval[:,i] = spline_overhauser_val(t,ydata,t_int[i],n_dim,lt)