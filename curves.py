# -*- coding: utf-8 -*-

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

"""
Created on Wed Oct 05 15:51:18 2011

@author: hrobeers
"""

from numpy import isnan, nan

class Bezier:
    """ This class makes cubic bezier curve objects """
    
    @staticmethod 
    def interpolateBezier(bezier):
        """ interpolate the Bezier object to """
        if bezier.type == "cubic":
            print "this is a cubic bezier"
        else:
            print "This version only supports cubic Bezier splines" #TODO error handling
            
    
    def __init__(self, point1, point2, point3, point4=nan):
        """
        points are numpy arrays of the form [x,y]
        """
        if isnan(point4):
            self.type = "quadratic"
            self.points = [point1, point2, point3]
        else:
            self.type = "cubic"
            self.points = [point1, point2, point3, point4]
    