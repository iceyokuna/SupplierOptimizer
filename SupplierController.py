from SupplierCalculator import *

class SupplierController:
    def __init__(self):
        self.supplier_detail_list = []
        self.supplier_set = []
        self.item_set = []
        self.calculator = SupplierCalculator()

    def addSupplier(self, supplier):
        self.supplier_detail_list.append(supplier)
        
        self.supplier_set.append(supplier[0])
        self.item_set.append(supplier[2])
        self.supplier_set = list(set(self.supplier_set))
        self.item_set = list(set(self.item_set))

    def reSupplier(self):
        self.supplier_detail_list.clear()
        self.supplier_set.clear()
        self.item_set.clear()
        
    def getAllSupplier(self):
        return self.supplier_set

    def getAllItems(self):
        return self.item_set

    def getSupplierByItem(self, item):
        supplier_list = []
        for supplier in self.supplier_detail_list:
            if(item == supplier[2]):
                supplier_list.append(supplier)
                
        return supplier_list

    def getLocation(self, supplier):
        for supply in self.supplier_detail_list:
            if (supplier == supply[0]):
                return supply[1]
        return None

    def getBestSupplier(self, item, customer_lat, customer_lon):
        supplier_list_detail = self.getSupplierByItem(item)
        best_supplier = self.calculator.calculate(customer_lat,customer_lon,supplier_list_detail)
        return best_supplier
        

    def __str__(self):
        return str(self.supplier_detail_list)
