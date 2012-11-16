#! /usr/bin/env python2

############################################################################
#    Copyright (C) 2011 by Hans Robeers                                    #
#                                                                          #
#    This program is free software; you can redistribute it and#or modify  #
#    it under the terms of the GNU General Public License as published by  #
#    the Free Software Foundation; either version 2 of the License, or     #
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

from fin import Fin
from numpy import array
#import time

fortran = True
x = Fin()

basethickness = 1.0
resolution = array([500, 500])
pointdata = array([[0,0],[5,6],[9.5,10],[13,12],
                    [16.25,11.35],[12.9,5],[11.2,0]])

x.set_basethickness(basethickness)
x.set_resolution(resolution)
x.set_pointdata(pointdata)

x.set_con_resolution(2000)
#tic = time.time()
#x.gen_contour_cubic()
x.gen_contour_fspline()

x.gen_surface()
#toc = time.time()

x.plot_contour()

x.plot_surface(0.1)


#x.plot_wireframe('mayavi')
#raw_input('Please press return to continue...\n')
#x.show_plot()
#x.test_get()

#print 'time: ', toc-tic