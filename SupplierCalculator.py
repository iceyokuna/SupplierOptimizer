from math import *

class SupplierCalculator:
    def __init__(self):
        self.distance_cost = []
    
    def getDistance(self, lat1, lon1, lat2, lon2):
        #call google API
        return sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

    def calculate(self,supplier, customer):
        supplier

    def setDistanceCost(self, distance_cost):
        self.distance_cost = distance_cost

    def __str__(self):
        return str(self.distance_cost)

    
    
