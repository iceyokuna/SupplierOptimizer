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
        return (distance * self.getDistanceCost(distance))+ float(cost)
    
    def sortSupplier(self,cost_list):
        for i in range(0, len(cost_list)):
            for j in range(i, len(cost_list)):
                if(self.getCost(cost_list[i][1],cost_list[i][2]) > self.getCost(cost_list[j][1],cost_list[j][2])):
                    temp = cost_list[j]
                    cost_list[j] = cost_list[i]
                    cost_list[i] = temp
        return cost_list


    def calculate(self,lat_customer,lon_customer, supplier_detail):
        cost_list = []
        for supplier in supplier_detail:
            supplier_lat, supplier_lon = supplier[1].split(',')
            distance = self.getDistance(lat_customer,lon_customer , supplier_lat, supplier_lon)
            cost_list.append((supplier[0],distance,supplier[3]))

        #เรียงแล้ว ดีสุด อยู่ที่ 0
        cost_list = self.sortSupplier(cost_list)

        #เอา 3 อันดับ ใส่ list
        best_supplier_list = []
        best_supplier_list.append((cost_list[0], self.getCost(cost_list[0][1],cost_list[0][2])))
        best_supplier_list.append((cost_list[1], self.getCost(cost_list[1][1],cost_list[1][2])))
        best_supplier_list.append((cost_list[2], self.getCost(cost_list[2][1],cost_list[2][2])))

        print("-------------------------")
        print(best_supplier_list[0])
        print("-------------------------")

        return best_supplier_list

    def __str__(self):
        return str(self.distance_cost)

    
    
