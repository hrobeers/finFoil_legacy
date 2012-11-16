#!/usr/bin/python2

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



import sys
from PyQt4 import QtCore, QtGui
from gui import Ui_MainWindow
from fin import Fin
from numpy import zeros, arange
from fileManager import FileManager
from finFoilDataFile import FFD

class Gui(QtGui.QMainWindow, Ui_MainWindow):
  
  
    n_rows = 0
    contourResolution=2000

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        #Setup
        self.setupUi(self)        
        
        #Attributes
        self.fin = Fin() #Fin is an attribute: loaded fin
        self.fm = FileManager() #File I/O
        
    
        # Initialize the table
        self.__updateTable()
        
        
        #print self.tab_inpoints.item(1,1).text()
       #print self.tab_inpoints.rowCount()
        
        self.__connectWidgets()
     
    def __connectWidgets(self):   
        self.connect(self.but_genSpline, QtCore.SIGNAL("clicked()"), self.genSpline)
        self.connect(self.but_genSurf, QtCore.SIGNAL("clicked()"), self.genSurf)
        self.connect(self.spin_rows, QtCore.SIGNAL("editingFinished()"), self.updateRows)
        self.connect(self.actionSaveAs,QtCore.SIGNAL("triggered()"), self.saveFFD)
        self.connect(self.actionOpenFile,QtCore.SIGNAL("triggered()"), self.openFFD)
        self.connect(self.contour_resolution,QtCore.SIGNAL("valueChanged( int )"), self.setContourResolution)
        self.connect(self.butBrowseSVG, QtCore.SIGNAL("clicked()"), self.selectSvgFile)
     

    #Remains here to be compatble with original code but is redirected to new code
    def updateRows(self):
        self.setRows(self.spin_rows.value())
        
    
    #Set the amount of datapoints (or rows)
    def setRows(self,amount):
        self.n_rows=amount
        self.tab_inpoints.setRowCount(amount)
        self.spin_rows.setValue(int(amount))
    

        
    def __updateTable(self):
        data = self.fin.pointdata
        self.n_rows = len(data) #amount of data points
        self.tab_inpoints.setRowCount(self.n_rows)
        self.spin_rows.setValue(self.n_rows)
        for col in arange(0,2):
            for row in arange(0,len(data)):
                item=QtGui.QTableWidgetItem()
                item.setText(str(data[row,col]))
                self.tab_inpoints.setItem(row, col, item) 
                
    #Set the currently loaded fin
    def setFin(self,fin):
        self.fin=fin
        self.__updateTable()
    
    
    def setContourResolution(self,resolution):
        self.contourResolution = resolution
        self.contour_resolution.setValue(int(resolution))
    
    def genSpline(self):
        self.fin.set_con_resolution(self.contour_resolution.value())        
        
        if self.radioManualInput.isChecked():
            # Read table:
            n_rows = self.tab_inpoints.rowCount()
            data = zeros((n_rows,2))
            for i in arange(0,n_rows):
                data[i,0] = float(self.tab_inpoints.item(i,0).text())
                data[i,1] = float(self.tab_inpoints.item(i,1).text())
            
            self.fin.set_pointdata(data)
            
            self.fin.gen_contour_fspline()
            
        elif self.radioImportSVG.isChecked():
#            pathName = self.linePathName.text()
            self.fin.genContourSVG(str(self.lineSelectedSVG.text()))
        
        
        self.fin.plot_contour()
        #self.fin.show_plot()
        
    def genSurf(self):
        # Read gui input
        xres = self.Xresolution.value()
        yres = self.Yresolution.value()
        thickness = self.spin_thickness.value()
        layer_thick = self.spin_layer.value()
        
        # Generate
        self.fin.set_resolution([xres, yres])
        self.fin.set_basethickness(thickness*2)
        
        if self.exponentialThicknessRadio.isChecked():
            self.fin.gen_surface(self.spin_exponConstant.value())
        elif self.percentualThicknessRadio.isChecked():
            self.fin.gen_surface(-float(self.spin_percentualConstant.value())/100)
        else:
            self.fin.gen_surface(0)
            
        self.fin.plot_surface(layer_thick)
        #self.fin.show_plot()

    def saveFFD(self):
        print "saveFFD"
        
        #Generate an ffd file of current configuration
        ffd = self.generateFFD()
        #load it into the filemanager
        self.fm.loadObject(ffd)
        

        saveFile = QtGui.QFileDialog.getSaveFileName(self, "Save file", "", ".ffd")
        
        #saveFile = saveFile.replace(" ","\ ")
        #saveFile = saveFile.replace("(","\(")
        #saveFile = saveFile.replace(")","\)")
        
        name=saveFile
        print saveFile
        
        #write to file
        self.fm.saveLoadedObject(name)
        
    def openFFD(self):
        print "openFFD"
        
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file','',"*.ffd")

        self.fm.loadObjectFromFile(filename)
        ffd = self.fm.getLoadedObject()
        
        
        #SET FIN
        self.setFin(ffd.getFin())
        
        #SET CONTOUR SETTINGS
        rows = ffd.getContourSetting("nrows")
        contour_resolution = ffd.getContourSetting("contour_resolution")
        
        #
        self.setContourResolution(contour_resolution)
        self.setRows(rows)
        
        
        #SET SURFACE SETTINGS
        self.spin_thickness.setValue(ffd.getSurfaceSetting("fin_base_thickness"))
        self.spin_layer.setValue(ffd.getSurfaceSetting("layer_thickness"))
        self.Xresolution.setValue(ffd.getSurfaceSetting("XResolution"))
        self.Yresolution.setValue(ffd.getSurfaceSetting("YResulution"))
          
      
        
        
        

    def generateFFD(self):
        ffd = FFD()
        
        #add fin
        ffd.setFin(self.fin)
        
        #add contour settings
        ffd.addContourSetting("nrows",self.n_rows)
        ffd.addContourSetting("contour_resolution",self.contour_resolution.value())
        
        
        ffd.addSurfaceSetting("fin_base_thickness",self.spin_thickness.value())
        ffd.addSurfaceSetting("layer_thickness",self.spin_layer.value())
        ffd.addSurfaceSetting("XResolution",self.Xresolution.value())
        ffd.addSurfaceSetting("YResulution",self.Yresolution.value())
        
        
        return ffd
        
    def selectSvgFile(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Import SVG file','',"*.svg")
        self.lineSelectedSVG.setText(filename)
        

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = Gui()
    form.show()
    sys.exit(app.exec_())