from math import *
import requests

class SupplierCalculator:
    def __init__(self):
        self.distance_cost = []

    def setDistanceCost(self, distance_cost):
        self.distance_cost = distance_cost
    
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

##คำนวนค่าขนส่งด้วย

    #เอาค่าขนส่งกลับ
    def getDistanceCost(self, distance):
        cost = 0
        for interval in self.distance_cost:
            start,end = interval[0].split('-')
            cost = interval[1]
            if(distance >= int(start) and distance <= int(end)):
                return cost
        return cost
                
 
    def getCost(self, distance,cost):
        distance = float(distance.split()[0])
        return (distance * self.getDistanceCost(distance))* float(cost)

    def calculate(self,lat_customer,lon_customer, supplier_detail):
        cost_list = []
        for supplier in supplier_detail:
            supplier_lat, supplier_lon = supplier[1].split(',')
            distance = self.getDistance(lat_customer,lon_customer , supplier_lat, supplier_lon)
            cost_list.append((supplier[0],distance,supplier[3]))

        Min = self.getCost(cost_list[0][1],cost_list[0][2])
        best_supplier = cost_list[0]
        
        for supplier in cost_list:
            print(supplier)
            cost = self.getCost(supplier[1],supplier[2])
            if(cost <= Min):
                Min = cost
                best_supplier = supplier

        print(best_supplier)
        print(Min)  
        return best_supplier,str(Min)

    def __str__(self):
        return str(self.distance_cost)

    
    
