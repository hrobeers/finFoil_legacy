#! /usr/bin/env python2

############################################################################
#    Copyright (C) 2011 by Hans Robeers                                    #
#                                                                          #
#    This program is free software; you can redistribute it and#or modify  #
#    it under the terms of the GNU General Public License as published by  #
#    the Free Software Foundation; either version 3 of the License, or     #
#    (at your option) any later version.                                   #
#                                                                          #
#    This program is distributed in the hope that it will be useful,       #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#    GNU General Public License for more details.                          #
#                                                                          #
#    You should have received a copy of the GNU General Public License     #
#    along with this program; if not, write to the                         #
#    Free Software Foundation, Inc.,                                       #
#    59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
############################################################################

#from numpy import *
#from numpy import array, linspace, sqrt, arange, zeros, ones, nan, transpose, isnan, where, size
from numpy import array, linspace, arange, zeros, transpose, isnan, where, size
from Fspline import spline_val, bezier_curve_val #, spline_overhauser_val
from Ffinlib import make_surface, interpolate#, naca_val
import matplotlib.pyplot as plt
from svgParser import SvgParser, SvgTools
#import guiqwt.pyplot as plt


class Fin:
    """
    finFoil class to create Fin objects
     *  written by hrobeers
     *  license: GPL
    """
    def __init__(self):
        """ initialise some values """
        
#        self.fortran = True
        self.thick = 1
        self.resolution = array([1000, 1000])
        pointdata = array([[0,0],[5,6],[9.5,10],[13,12],
	                   [16.25,11.35],[12.9,5],[11.2,0]])
        self.set_pointdata(pointdata)
        self.contour = FinContour(self.resolution)
    
    
    """
    %%%%%%%%%%%%%%%%%%%%%%
    % auxilliary methods %
    %%%%%%%%%%%%%%%%%%%%%%
    """
    
    def thickness(self, height):
        """ generate the thickness profile """
        basethickness = self.thick
        
        y = linspace(0,height,self.resolution[1])
        
        #  0 = a1 * h**2 + b
        a1 = -basethickness/(height**2)
        
        thick = a1 * y**2 + basethickness
        
        return thick
        
    def exponentialThickness(self, baseNumber):
        basethickness = self.thick
        y = linspace(0,1,self.resolution[1])
        
        a = 1/(2**float(baseNumber))

        thick = (a**(1-y)-1)/(a-1) * basethickness
        
        return thick
        
    def percentThickness(self, percent):
        leadingedge = self.contour.getLeadingEdge()
        trailingedge = self.contour.getTrailingEdge()
        
        # initialise the surface matrices
        #surf = ones(self.resolution)*nan #*self.thick
        width = self.contour.getWidth()
        height = self.contour.getHeight()
        x_axis = linspace(0,width,self.resolution[0])
        y_axis = linspace(0,height,self.resolution[1])
        
        # interpolate the edges to fit the grid
        leading_edge = interpolate(leadingedge[:,1],leadingedge[:,0],y_axis,len(leadingedge[:,1]),self.resolution[1])
        trailing_edge = interpolate(trailingedge[:,1],trailingedge[:,0],y_axis,len(trailingedge[:,1]),self.resolution[1])
                
        chordlength = trailing_edge - leading_edge
        
        thick = chordlength * float(percent)
        
        self.set_basethickness(thick[0])
        
        return thick
        
    
    """
    %%%%%%%%%%%%%%%%%%%%%%
    % generation methods %
    %%%%%%%%%%%%%%%%%%%%%%
    """
    
    def gen_surface(self, exponConstant):
        """ generate the 3D surface of the fin """
        
        leadingedge = self.contour.getLeadingEdge()
        trailingedge = self.contour.getTrailingEdge()
        
        # initialise the surface matrices
        #surf = ones(self.resolution)*nan #*self.thick
        width = self.contour.getWidth()
        height = self.contour.getHeight()
        x_axis = linspace(0,width,self.resolution[0])
        y_axis = linspace(0,height,self.resolution[1])
        
        # interpolate the edges to fit the grid
        leading_edge = interpolate(leadingedge[:,1],leadingedge[:,0],y_axis,len(leadingedge[:,1]),self.resolution[1])
        trailing_edge = interpolate(trailingedge[:,1],trailingedge[:,0],y_axis,len(trailingedge[:,1]),self.resolution[1])
        
        
        # rescale to grid
        dx = width / self.resolution[0]
        leading_edge_grid = (leading_edge / dx).round()
        trailing_edge_grid = (trailing_edge / dx).round()
        
        # generate the profiles and surface
        if exponConstant == 0:
            thick = self.thickness(height)
        elif exponConstant < 0:
            thick = self.percentThickness(-exponConstant)
        else:
            thick = self.exponentialThickness(exponConstant)
        
        surf = make_surface(self.resolution[0],leading_edge_grid,trailing_edge_grid,thick,self.resolution[1])
        
        #print surf
        self.surf = surf
        self.x_axis = x_axis
        self.y_axis = y_axis
        

    def gen_contour_fspline(self):
        """ Use Fspline to interpolate the input points """
        
        n_dim = 2
        n_val = self.con_resolution
        n_inputpoints = self.pointdata.size/2
        
        t = arange(0,n_inputpoints)       
        
        t_int = linspace(0,n_inputpoints-1,n_val)
        
        ydata = transpose(self.pointdata)
        
        yval = spline_val(t,ydata,t_int,n_dim,len(t),len(t_int))
        
        self.contour.setContour(yval.transpose())
        
    def genContourSVG(self, svgFilePath, pathName=""):
        """ Generate the contour from an SVG file """
        
        pointsPerBezier = self.con_resolution
        
        svg = SvgParser()
        svg.parseSvgFile(svgFilePath)
        
        path = svg.getPath()
        absPath = SvgTools.toAbsolutePath(path)
        normPath = SvgTools.toNormalisedPath(absPath)
        fullPath = SvgTools.toFullBezierPath(normPath)
        
        contour = zeros((2,len(fullPath)*pointsPerBezier))
        controlPoints = zeros((2,len(fullPath)*4))
        con = zeros((4,2))
        tval = linspace(0,1,pointsPerBezier+1)
        bcval = zeros((2,pointsPerBezier))
        j=0
        for conPartPoints in fullPath:
            for i in arange(0,4):
                con[i,:] = array(conPartPoints[1][i])
            
            bcval = bezier_curve_val(tval,transpose(con),3,pointsPerBezier)
            contour[:,j*pointsPerBezier:(j+1)*pointsPerBezier] = bcval
            controlPoints[:,j*4:(j+1)*4] = transpose(con)
            j = j+1
            
        self.set_pointdata(transpose(controlPoints))
        self.contour.setContour(transpose(contour))
    
    
    """
    %%%%%%%%%%%%%%%%
    % plot methods %
    %%%%%%%%%%%%%%%%
    """
    
    def plot_contour(self):
        """ plot the fin contour """
        
        plt.close(1)
        plt.figure(1)
        plt.plot(self.contour.getX(),self.contour.getY(),'-',self.pointdata[:,0],self.pointdata[:,1],'o')
        plt.axis('equal')
        plt.show()
            
    def plot_surface(self, layer_thick):
        """ plot the fin surface """
        
        n_layers = (self.thick/2)//layer_thick + 2
        layers = linspace(0,n_layers*layer_thick,n_layers+1)
        
        plt.close(2)
        plt.figure(2)
        plt.contourf(self.x_axis, self.y_axis, self.surf.transpose(), layers)
        plt.axis('equal')
        plt.show()
        
    def plot_wireframe(self, lib):
        """ plot the fin wireframe """
        #lib = 'mayavi'
        
        #Filter to lower resolution
        xfilter = arange(0,len(self.x_axis),len(self.x_axis)/1)
        yfilter = arange(0,len(self.y_axis),len(self.y_axis)/1)
        
        x = self.x_axis[xfilter]
        y = self.y_axis[yfilter]
        z = self.surf[xfilter,:]
        z = z[:,yfilter]
        
        if lib == 'gnuplot':
            import Gnuplot
            z[isnan(z)] = 5
            g = Gnuplot.Gnuplot()
            g.splot(Gnuplot.GridData(z, x, y, binary=0))
            raw_input('Please press return to continue...\n')
            
        elif lib == 'matplotlib':
            import mpl_toolkits.mplot3d.axes3d as p3
            fig=plt.figure(3)
            ax = p3.Axes3D(fig)
            
            x2 = zeros((100,100))
            x2[:,:]=x[:]
            
            y2 = zeros((100,100))
            y2[:,:]=y[:]
                        
            ax.plot_wireframe(x2, y2.transpose(), z.transpose())
            
        elif lib == 'mayavi':
            from enthought.mayavi.mlab import surf
            z[isnan(z)] = 0
            surf(x, y, z)
        
    def show_plot(self):
        plt.show()

        
        
    """
    %%%%%%%%%%%%%%%%%%%%%
    % getters & setters %
    %%%%%%%%%%%%%%%%%%%%%
    """
    
    def get_pointdata(self,pointdata):
        """ set the input point data """
        return self.pointdata
        
    def set_pointdata(self,pointdata):
        """ set the input point data """
        self.pointdata = pointdata
        
    def set_resolution(self,resolution):
        """ set resolution """
        self.resolution = resolution
        
    def set_con_resolution(self,con_resolution):
        self.con_resolution = con_resolution
        
    def set_basethickness(self,thick):
        """ set the basethickness """
        self.thick = thick

    #def test_get(self):
        #""" test function """
      
    def set_dataPoint(self,row,col,value):
        self.pointdata[row][col] = value

    
    
        
        
class FinContour:
    """
    finFoil class to create FinContour objects used in the Fin class
     *  written by hrobeers
     *  license: GPL v3
    """
    def __init__(self, resolution):
        """ initialise the contour """
        
    def __setResolution__(self,resolution):
        """ set the resolution """
        self.resolution = resolution
        
    def __splitContour__(self):
        """ split the contour in leading and trailing edge """
        # local variables
        extrema = self.contour.max(axis=0)
        self.width = extrema[0]
        self.height = extrema[1]
        
        # split the outline
        top = int(max(where(self.contour[:,1] == self.height)))
        self.leadingedge = self.contour[:top+1,:]
        self.trailingedge = self.contour[top:,:]
        self.leadingedge[0,1] = 0	# first element of y should be zero for interpolation
        self.trailingedge = self.trailingedge[::-1,:]	# reverse the array for interpolation
        self.trailingedge[0,1] = 0	# first element of y should be zero for interpolation
    
    """
    %%%%%%%%%%%%%%%%%%%%%
    % getters & setters %
    %%%%%%%%%%%%%%%%%%%%%
    """
    def getResolution(self):
        """ return resolution """
        return self.resolution
    
    def getContour(self):
        """ return contour """
        return self.contour
        
    def setContour(self, contour):
        """ set contour """
        resolution = size(contour,0)
        self.__setResolution__(resolution)
        self.contour = contour
        self.__splitContour__()
    
    def getLeadingEdge(self):
        """ return leading edge """
        return self.leadingedge
        
    def getTrailingEdge(self):
        """ return trailing edge """
        return self.trailingedge
        
    def getX(self):
        """ return X """
        return self.contour[:,0]
        
    def setX(self, X):
        """ set X """
        self.contour[:,0] = X
        
    def getY(self):
        """ return Y """
        return self.contour[:,1]
        
    def setY(self, Y):
        """ set Y """
        self.contour[:,1] = Y
        
    def getWidth(self):
        """ return width """
        return self.width
        
    def getHeight(self):
        """ return height """
        return self.height
        
        
        
if __name__ == "__main__":
    fortran = True
    x = Fin()
    
    basethickness = 1
    resolution = array([1000, 1000])
    pointdata = array([[0,0],[5,6],[9.5,10],[13,12],
                        [16.25,11.35],[12.9,5],[11.2,0]])
    
    x.set_basethickness(basethickness)
    x.set_resolution(resolution)
#    x.set_pointdata(pointdata)
    
    x.set_con_resolution(2000)
    #tic = time.time()
    #x.gen_contour_cubic()
#    x.gen_contour_fspline()
    
    x.genContourSVG("/home/frieda/tmp/test.svg")
    
    x.gen_surface(-0.15)
    #toc = time.time()
    
    x.plot_contour()
    
    x.plot_surface(0.8)
    
#    x.plot_wireframe('mayavi')
    raw_input('Please press return to continue...\n')
#    x.show_plot()
    #x.test_get()
    
    #print 'time: ', toc-tic