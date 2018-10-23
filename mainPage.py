import sys
from openpyxl import load_workbook
from PySide2 import QtCore, QtGui
from PySide2.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from SupplierController import *
from MapController import *

#Blueprint of main page
class MainPage(QObject):
    def __init__(self, parent=None):
        super(MainPage,self).__init__(parent)
        #Read File
        ui_file = QFile('mainPage.ui')
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load('UI\mainPage.ui')
        ui_file.close()    

        #Setup mainpage 
        self.ui.setWindowTitle("Tar the God Project")

        #MainPage Attribute
        self.SupplierController = SupplierController()
        self.MapController = MapController()

        #Add Object
        ##Object List
        self.supplier_list = self.ui.findChild(QListWidget, 'supplierList')
        self.item_list = self.ui.findChild(QListWidget, 'itemList')
        self.supplier_list.clicked.connect(self.clickList)

        ##Object Button
        self.import_excel_button = self.ui.findChild(QPushButton, 'importExcelButton')
        self.import_excel_button.clicked.connect(self.importExcel)

        ##Object Text Edit
        self.customer_location = self.ui.findChild(QLineEdit, 'customer_location_edit')

        ##Object Label
        self.supplier_label = self.ui.findChild(QLabel, 'supplier_label')
        self.supplier_location_label = self.ui.findChild(QLabel, 'supplier_location_label')
        self.supply_label = self.ui.findChild(QLabel, 'supply_label')
        self.transport_cost_label = self.ui.findChild(QLabel, 'transport_cost_label')
        self.supply_cost_label = self.ui.findChild(QLabel, 'supply_cost_label')

        ##initialize web engine
        self.web_widget = self.ui.findChild(QWidget, 'map_widget')
        self.webEngineView = QWebEngineView()
        mapHTML = self.MapController.getHTML()
        self.webEngineView.setHtml(mapHTML)
        self.webEngineView.resize(721, 531);
        self.webEngineView.setParent(self.web_widget)
        

    def importExcel(self):
        dialog = QFileDialog()
        filename = QFileDialog.getOpenFileName(dialog, "Import Supplier (.xlsx)",None, "Excel files (*.xlsx)")
        excel_location = filename[0]
        
        excel = load_workbook(excel_location)
        sheet = excel.get_sheet_by_name("Sheet1")

        row = 2
        while(True):
            #If data is None then break the loop
            if(sheet.cell(row, 1).value is None):
                break
            self.SupplierController.addSupplier((sheet.cell(row, 1).value,
                                             sheet.cell(row, 2).value,
                                             sheet.cell(row, 3).value,
                                             sheet.cell(row, 4).value))
            row += 1
            
        self.updateData()

    def updateData(self): 
        for supplier in self.SupplierController.getAllSupplier():
            self.supplier_list.addItem(supplier)
            
        for items in self.SupplierController.getAllItems():
            self.item_list.addItem(items)

    def clickList(self):
        clicked_supplier = self.supplier_list.selectedItems()[0].text()
        location = self.SupplierController.getLocation(clicked_supplier)
        lat , lon = location.split(',')
        self.MapController.setNewCenter(lat,lon)
        self.webEngineView.setHtml(self.MapController.getHTML())
        
    def showUI(self):
        self.ui.show()
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MainPage()
    form.showUI()
    sys.exit(app.exec_())

##AIzaSyBmt-IXSmfgH8AsEYAalEUgXuF23GCuNVQ
##KMITL location 13.729835, 100.778261
