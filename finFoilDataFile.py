############################################################################
#    Copyright (C) 2011 by Thomas Goossens                                 #
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

'''
Created on 8-aug-2011

@author: Thomas Goossens
@summary: FinFoilData file: contains all datapoints and settings
@contact: thomasgoossens.be
'''
from fin import Fin
class FFD():
    
   
    def __init__(self,loaded=None):
        '''
        Constructor
        '''
        if(loaded == None):
            print("Do nothing")
        else:
            print("Do something")
   
        self.surfaceSettings={}
        self.contourSettings={}
        self.fin=None
    
    ''' SETTERS: FOR OBJECT EDITING ''' 
    #Make a list of settings with name as ID
    def addSurfaceSetting(self,name,value):
        self.surfaceSettings[''+str(name)+'']=value

    def addContourSetting(self,name,value):
        self.contourSettings[''+str(name)+'']=value
        
    def setFin(self,fin):
        self.fin=fin
    
    ''' GETTERS: FOR READING '''
    def getSurfaceSetting(self,name):
        return self.surfaceSettings[''+str(name)+'']

    def getContourSetting(self,name):
        return self.contourSettings[''+str(name)+'']
    
    def getFin(self):
        return self.fin



    #used when written to file: for copying INTERNAL STATE of the object
    def __getstate__(self): 
        dict = self.__dict__.copy()
        return dict
    #restore internal state
    def __setstate__(self, d): 
        self.__dict__ = d
        