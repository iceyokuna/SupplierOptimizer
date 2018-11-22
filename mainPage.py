import sys
from openpyxl import load_workbook
from PySide2 import QtCore, QtGui
from PySide2.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
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
        self.window = self.ui.findChild(QWidget, 'mainWidget')
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("UI/background.jpg")))
        self.ui.setPalette(palette)
        
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
        self.supplier_list.clicked.connect(self.supplierListClicked)
        self.item_list.clicked.connect(self.itemListClicked)

        ##Object Button
        self.import_excel_button = self.ui.findChild(QPushButton, 'importExcelButton')
        self.start_button = self.ui.findChild(QPushButton, 'startButton')
        self.import_excel_button.clicked.connect(self.importExcel)
        self.start_button.clicked.connect(self.startCalculate)

        ##Object Text Edit
        self.customer_location = self.ui.findChild(QLineEdit, 'customer_location_edit')
        self.customer_location.setText("13.7297987,100.77533169999992")

        ##Object Label
        self.supplier_label = self.ui.findChild(QLabel, 'supplier_label')
        self.supplier_location_label = self.ui.findChild(QLabel, 'supplier_location_label')
        self.supply_label = self.ui.findChild(QLabel, 'supply_label')
        self.transport_cost_label = self.ui.findChild(QLabel, 'transport_cost_label')
        self.supply_cost_label = self.ui.findChild(QLabel, 'supply_cost_label')

        #ตัวแปล ข้อมูลตัวอักษรเริ่มค้น
        self.supplier_str = "ชื่อซัพพลายเออร์ :"
        self.supplier_location_str = "ตำแหน่ง   :"
        self.supply_str = "สินค้า    :"
        self.transport_cost_str = "ราคาขนส่ง  :"
        self.supply_cost_str = "ต้นทุนสินค้า   :"

        ##initialize web engine
        self.web_widget = self.ui.findChild(QWidget, 'map_widget')
        self.webEngineView = QWebEngineView()
        
        lat , lon = self.customer_location.text().split(',')
        self.MapController.setCustomerMarker(lat , lon)
        self.MapController.setSupplierMarker(lat , lon)
        mapHTML = self.MapController.getHTML()
        self.webEngineView.setHtml(mapHTML)
        self.webEngineView.resize(761, 721);
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
        self.supplier_list.clear()
        self.item_list.clear()
        for supplier in self.SupplierController.getAllSupplier():   
            self.supplier_list.addItem(supplier)
            
        for items in self.SupplierController.getAllItems():
            self.item_list.addItem(items)

        self.supplier_label.setText(self.supplier_str)
        self.supplier_location_label.setText(self.supplier_location_str)
        self.supply_label.setText(self.supply_str)
        self.transport_cost_label.setText(self.transport_cost_str)
        self.supply_cost_label.setText(self.supply_cost_str)

    def supplierListClicked(self):
        clicked_supplier = self.supplier_list.selectedItems()[0].text()
        self.setPath(clicked_supplier)

    def itemListClicked(self):
        pass

    def startCalculate(self):
        if(self.item_list.selectedItems() != []):
            lat , lon = self.customer_location.text().split(',')
            best_supplier,distance = self.SupplierController.getBestSupplier(self.item_list.selectedItems()[0].text(), lat,lon)
            self.setPath(best_supplier)
            
            self.supplier_label.setText(self.supplier_str + best_supplier)
            self.supplier_location_label.setText(self.supplier_location_str + self.SupplierController.getLocation(best_supplier))
            self.supply_label.setText(self.supply_str + self.SupplierController.getItem(best_supplier))
            self.transport_cost_label.setText(self.transport_cost_str + distance)
            self.supply_cost_label.setText(self.supply_cost_str + str(self.SupplierController.getCost(best_supplier)))
            

    def setPath(self, supplier_name):
        location = self.SupplierController.getLocation(supplier_name)
        lat , lon = self.customer_location.text().split(',')
        self.MapController.setCustomerMarker(lat , lon)
        lat , lon = location.split(',')
        self.MapController.setSupplierMarker(lat,lon)
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
##resp = requests.get('https://maps.googleapis.com/maps/api/directions/json?origin=13.646667,100.681164&destination=13.730054,100.778890&key=AIzaSyBmt-IXSmfgH8AsEYAalEUgXuF23GCuNVQ')
##print(resp.json()["routes"][0]["legs"][0]["distance"]["text"])
