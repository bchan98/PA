import csv, hash
from datetime import datetime, timedelta

class Packages:
    def __init__(self, id, street, city, zip, deadline, weight, status):
        self.id = id
        self.street = street
        self.city = city
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.status = status

    def __str__(self):
        return f"The package no. {self.id} is to be delivered to {self.street}, {self.city} at zipcode {self.zip} before {self.deadline}. The package weights {self.weight} pounds. The status of the package is: {self.status}"
        return self.id, self.street, self.city, self.zip, self.deadline, self.weight, self.status
    
    def importCSV(self, filename):
        with open(filename, 'r') as csvFile:
            packageCSV = csv.DictReader(csvFile)
            for row in packageCSV:
                insertID = row['ID']
                insertStreet = row['STREET']
                insertCity = row['CITY']
                insertZip = row['ZIP']
                insertDeadline = row['DEADLINE']
                insertWeight = row['WEIGHT']
                insertStatus = 'AT HUB'

                insertPackage = Packages(insertID, insertStreet, insertCity, insertZip, insertDeadline, insertWeight, insertStatus)
                packageTable.insert(insertID, insertPackage)

class Trucks:
    def __init__(self, speed, miles, location, depart, packagesCarried=[]):
        self.speed = speed
        self.miles = miles
        self.location = location
        self.depart = depart
        self.time = depart
        self.packagesCarried = packagesCarried

    def __str__(self):
        return f"The speed of the truck is {self.speed} miles per hour and has travelled {self.miles} miles. The truck is currently at {self.location} at {self.time}. The truck currently contains {len(self.packages)} packages."

    def loadTruck(self, nuPackage):
        nuPackage.status = 'IN DELIVERY'
        self.packagesCarried.append(nuPackage)

    def unloadTruck(self, nuPackage):
        nuPackage.status = 'DELIVERED'
        self.packagesCarried.pop(self.packagesCarried.index(nuPackage))

class Edge:
    def __init__(self, start, end, distance):
        self.start = start
        self.end = end
        self.distance = distance

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.map = hashTable()

    def generateMap(self, addressList, distanceList):
        # get list of all locations
        with open(filename, 'r') as addressList:
            counter = 0
            addressCSV = csv.DictReader(addressList)
            # add each vertex as an entry
            for row in packageCSV:
                vertex = row[2]
                self.nodes.append(vertex)
            
        # get a list of all edges
        with open(filename, 'r') as distanceList:
            distanceCSV = csv.DictReader(distanceList)
            edges = []
            for row in distanceCSV:
                edges.append(row)
        
        # fill out the distance matrix
        for i in range(len(edges)):
            for j in range(len(edges[i]))
                if edges[i][j] == '':
                    edges[i][j] = edges[j][i]
                elif edges[j][i] == '':
                    edges[j][i] = edges[i][j]
        
        # hash in the edge with its matrix
        for i in range(len(edges)):
            map.insert(vertex[i], edges[i])
    
    def nearestNeighbourDelivery(self, nuTruck):
        # initialize parameters
        curLocation = nuTruck.location
        curLocationID = nodes.index(curLocation)

        packageList = nuTruck.packagesCarried
        nearestDistance = 1000
        nextPackage = ''

        # loop through to find nearest location
        for i in packageList:
            locationList = self.map.search(packageList[i])
            edgeWeight = int(locationList[curLocationID])
            if nearestDistance > edgeWeight:
                nearestDistance = edgeWeight
                nextPackage = packageList[i].id

        # once nearest distance found, travel there and increment time
        timeCalc = nearestDistance / 18
        timeIncrement = timedelta(minutes=timeCalc)

        modifiedTime = nuTruck.time + timeIncrement
        nuTruck.time = modifiedTime

        # additionally, add mileage to the truck
        nuTruck.miles = nuTruck.miles + nearestDistance

        # change current location to destination location
        nuTruck.location = packageTable.search(nextPackage).street

        # print out that a package has been successfully delivered
        print (f"Package no. " {nextPackage} " has been successfully delivered.")

        # remove package from package list and set package status to have been delivered
        nuTruck.unloadTruck(packageTable.search(nextPackage))

        return

# generate hash tables + graphs
packageTable = hash.hashTable()
mapGraph = graph()

# create trucks
truck1 = trucks(18, 0, 0, 800, [])
truck2 = trucks(18, 0, 0, 800, [])
truck3 = trucks(18, 0, 0, 800, [])

# manually load each truck

# once loaded, create a loop - the loop asks either to display status of all packages, or to allow trucks to continue delivery.

# finally, once trucks are empty, print out mileage of all trucks.

