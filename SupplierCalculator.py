from math import *
import requests

class SupplierCalculator:
    def __init__(self):
        self.distance_cost = []
    
    def getDistance(self, lat1, lon1, lat2, lon2):
        #call google API
        lat1 = str(float(lat1))
        lon1 = str(float(lon1))
        lat2 = str(float(lat2))
        lon2 = str(float(lon2))
        origin = lat1 + ',' + lon1
        destination = str(lat2) + ',' + lon2
        resp = requests.get('https://maps.googleapis.com/maps/api/directions/json?origin='+ origin +'&destination='+ destination +'&key=AIzaSyBmt-IXSmfgH8AsEYAalEUgXuF23GCuNVQ')
        return resp.json()["routes"][0]["legs"][0]["distance"]["text"]

    def getCost(self, distance,cost):
        return distance * cost

    def calculate(self,lat_customer,lon_customer, supplier_detail):
        cost_list = []
        for supplier in supplier_detail:
            supplier_lat, supplier_lon = supplier[1].split(',')
            distance = self.getDistance(lat_customer,lon_customer , supplier_lat, supplier_lon)
            cost_list.append((supplier[0],distance,supplier[3]))

        Min = self.getCost(cost_list[0][1],cost_list[0][2])
        best_supplier_name = cost_list[0][0]
        
        for supplier in cost_list:
            cost = self.getCost(supplier[1],supplier[2])
            if(cost <= Min):
                Min = cost
                best_supplier_name = supplier[0]
                
        return best_supplier_name

    def __str__(self):
        return str(self.distance_cost)

    
    
