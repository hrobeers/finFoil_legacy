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
Created on Mon Oct 03 21:49:24 2011

@author: hrobeers

USAGE:
    obj = SvgParser()
    obj.parseSvgFile("path to your svg file")   OR   obj.parseString("M 0.205,178 C 16.3,147 70.6,65.2 134,64.3 ...") 
    print obj.getPath()



SVG character explanation:
    Capital letter -> absolute coordinates
    Lower case letter -> relative coordinates
    
    M or m: moveto (x,y)
    
    C or c: curveto (x1,y1 x2,y2 x,y) using cubic bezier
    
    S or s: smooth curveto (x2,y2 x,y) using cubic bezier
        x1 and y1 are the reflection of the second control point
        on the previous command relative to the current point.
        If there is no previous command or if the previous command
        was not an C, c, S or s, assume the first control point
        is coincident with the current point.
        
    Z or z: closepath
    
http://www.w3.org/TR/SVG/paths.html
"""

#import os
#from pyparsing import Word, alphas
from xml.dom.minidom import parse
from copy import deepcopy

class SvgParser:
    
    def __init__(self):
        """ init method """

        
    def __filterPathObject__(self, pathid):
        """ filter path string from XML file """
        
        
    def __stringToPoint__(self, pointString):
        """ convert string to point """
        splittedPS = pointString.split(",")
        try:
            point = [float(splittedPS[0]), float(splittedPS[1])]
        except:
            #TODO error handling
            print "Invalid SVG path in *.svg file"
        return point
        
        
    def __generatePathElement__(self, pathType):
        """ generate a path element of the form [pathType, [x1, y1], [x2, y2], ...] """
        if pathType in ["M","m","L","l","T","t"]:
            """ Move to """
            p = self.splittedSVG.pop(0)
            point = self.__stringToPoint__(p)
            pathElement = [pathType, point]
            
        elif pathType in ["C","c"]:
            """ Cubic curve to """
            point = []
            for i in range(3):
                p = self.splittedSVG.pop(0)
                point.append(self.__stringToPoint__(p))
                
            pathElement = [pathType, point[0], point[1], point[2]]
            
        elif pathType in ["S","s","Q","q"]:
            """ Cubic curve to """
            point = []
            for i in range(2):
                p = self.splittedSVG.pop(0)
                point.append(self.__stringToPoint__(p))
                
            pathElement = [pathType, point[0], point[1]]
            
        elif pathType in ["Z","z"]:
            """ Close path """
            pathElement = [pathType]
            
        else:
            pathElement = "error"
            
        return pathElement

        
    def parseString(self, svgString):
        """
        parse SVG string to generate the path List:
        a List with path elements of the form [pathType, [x1, y1], [x2, y2], ...]
        """
        
        svgCommands = ["M","m","Z","z","L","l","H","h","V","v","C","c","S","s","Q","q","T","t","A","a"]
        self.path = []
        
        self.splittedSVG = svgString.split(" ")
#        print self.splittedSVG[1]
#        print svgString
        
        while len(self.splittedSVG) != 0:
            i = self.splittedSVG.pop(0)
            
            if i in svgCommands:
                pathElement = self.__generatePathElement__(i)
            else:
                self.splittedSVG.insert(0, i)
                pathType = self.path[-1][0] # Use the type of the previous pathElement
                pathElement = self.__generatePathElement__(pathType)
                
            self.path.append(pathElement)
        
            
        # TODO error if self.splittedSVG!=[]
        
        
    def parseSvgFile(self, filepath, pathname="fin"):
        """
        Parse SVG file to generate the path List:
        a List with path elements of the form [pathType, [x1, y1], [x2, y2], ...]
        """
        try:
            dom = parse(filepath)
        except:
            """ error handling """ #TODO
            print "Error: Failed parsing SVG file"
            print filepath
            print "possible reasons:"
            print "     - Incorrect path to SVG file"
            print "     - Invalid SVG file"
            return
        
        # put all path elements in List
        elements = dom.getElementsByTagName("path")
        pathIds = []
        for element in elements:
            pathIds.append(element.attributes['id'].value)
        
        # try to find the svgString with id=pathname
#        try:
        pathIndex = pathIds.index(pathname)
        svgString = elements[pathIndex].attributes['d'].value
        self.parseString(svgString)
#        except:
#            """ error handling """ #TODO
#            print "Error: Path name doesn't exist"
#            print "Valid path names are:"
#            print pathIds
#            return

    def getPath(self):
        """ returns a List with path elements of the form [pathType, [x1, y1], [x2, y2], ...] """
        return self.path
        
        
        
class SvgTools:
    @staticmethod    
    def toAbsolutePath(path):
        """ generate absolutePath from path """
        absolutePath = []
        
        for i in range(len(path)):
            pathElement = path[i]
            if pathElement[0].islower():
                correction = absolutePath[-1][-1] # The endpoint of the previous element
                element = []
                element.append(pathElement.pop(0).capitalize())
                while len(pathElement)!=0:
                    point = pathElement.pop(0)
                    point[0] = point[0] + correction[0]
                    point[1] = point[1] + correction[1]
                    element.append(point)
                absolutePath.append(element)
            else:
                absolutePath.append(pathElement)
        
        return absolutePath
        
    @staticmethod
    def toNormalisedPath(path):
        """ move the path to the first point = [0,0] """
        if path[0][0] == "M":
            correction = deepcopy(path[0][1])
        else:
            # TODO error normalise
            """ """
            
        for element in path:
            for i in range(1,len(element)):
                element[i][0] = element[i][0] - correction[0]
                element[i][1] = (element[i][1] - correction[1])*-1
                
        return path
        
        
    @staticmethod
    def toFullBezierPath(path):
        """ """
        fullBezierPath = []
        
        # TODO call toAbsPath
        
        if path[0][0] == "M":
            startPoint = deepcopy(path[0][1])
            for i in range(1,len(path)):
                element = path[i]
                if element[0] == "C":
                    fullBezierPath.append([element[0],[startPoint, element[1], element[2], element[3]]])
                    startPoint = deepcopy(element[-1])
        else:
            """ """
            # TODO error handling
                    
        return fullBezierPath
                        
                
if __name__ == "__main__":
    """ code for testing purposes """
    filepath = "C:/Users/Hrobeers/Documents/PrivProj/fins/RustyQuad/R2front.svg"
    obj = SvgParser()
    obj.parseSvgFile(filepath)
    
    path = obj.getPath()
    absPath = SvgTools.toAbsolutePath(path)
    normPath = SvgTools.toNormalisedPath(absPath)
    fullPath = SvgTools.toFullBezierPath(normPath)
    print fullPath