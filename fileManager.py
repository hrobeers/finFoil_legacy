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
@contact: thomasgoossens.be

@summary: Can write objects to a file and load them. Classes can manipulate the loaded object via method call and save it again
@summary: An object has to be loaded before one can be saved
'''

#import cPickle
import pickle

class FileManager():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        #Attributes
        self.loadedObject = None

    #Save the currently loaded object to a file
    def saveLoadedObject(self,filename):
        self.__saveObjectToFile(self.getLoadedObject(),filename)
   
    def loadObjectFromFile(self,filename):
        object = pickle.load(open(''+str(filename)+'', 'rb'))
        self.__setLoadedObject(object)
         
    def getLoadedObject(self):
        return self.loadedObject
    
    def loadObject(self,object):
        self.__setLoadedObject(object)

    ''' Private methods '''
    # Sets the loaded object internaly
    def __setLoadedObject(self,object):
        self.loadedObject=object    
        
    #Saves an object to a file
    def __saveObjectToFile(self,object,filename):
        pickle.dump(object, open(''+str(filename)+'', 'wb'))
