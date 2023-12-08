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
    
    @staticmethod
    def importCSV(self, filename, packageTable):
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
        return f"The speed of the truck is {self.speed} miles per hour and has travelled {self.miles} miles. The truck is currently at {self.location} at {self.time}. The truck currently contains {len(self.packagesCarried)} packages."

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
        self.map = hash.hashTable()

    def generateMap(self, addressFile, distanceFile):
        # get list of all locations
        with open(addressFile, 'r') as addressList:
            counter = 0
            addressCSV = csv.reader(addressList)
            # add each vertex as an entry
            for row in addressCSV:
                vertex = row[2]
                self.nodes.append(vertex)
            
        # get a list of all edges
        with open(distanceFile, 'r') as distanceList:
            distanceCSV = csv.reader(distanceList)
            for row in distanceCSV:
                self.edges.append(row)
        
        # fill out the distance matrix
        for i in range(len(self.edges)):
            for j in range(len(self.edges[i])):
                if self.edges[i][j] == '':
                    self.edges[i][j] = self.edges[j][i]
                elif self.edges[j][i] == '':
                    self.edges[j][i] = self.edges[i][j]
        
        # hash in the edge with its matrix
        for i in range(len(self.edges)):
            self.map.insert(vertex[i], self.edges[i])
    
    def nearestNeighbourDelivery(self, nuTruck, packageTable):
        # initialize parameters
        curLocation = nuTruck.location
        curLocationID = self.nodes.index(curLocation)

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
        print(f"Package no. {nextPackage} has been successfully delivered.")

        # remove package from package list and set package status to have been delivered
        nuTruck.unloadTruck(packageTable.search(nextPackage))

        return

def main():
    # generate hash tables + graphs and fill in information
    packagesList = hash.hashTable() # this is the packageTable
    Packages.importCSV('CSV/package.csv', packagesList)
    mapGraph = Graph() # this is the graph for the map
    mapGraph.generateMap('CSV/address.csv', 'CSV/distance.csv') # generates vertexes/edges for graph

    # create trucks
    truck1 = Trucks(18, 0, 0, 800, [])
    truck2 = Trucks(18, 0, 0, 800, [])
    truck3 = Trucks(18, 0, 0, 800, [])

    # generate a list of packages for each truck
    truck1list = [13, 14, 15, 16, 19, 20, 26, 27, 33, 35, 40]
    truck2list = [3, 18, 36, 38, 29, 30, 31, 34, 37, 39]
    truck3list = [1, 2, 4, 5, 7, 10, 11, 12, 17, 21, 22, 23, 24]

    # using the list of packages, get the package object from the hash table and load it into the truck in a for loop
    for i in truck1list:
        truck1.loadTruck(packagesList.search(truck1list[i]))
        truck2.loadTruck(packagesList.search(truck2list[i]))
        truck3.loadTruck(packagesList.search(truck3list[i]))
    # once loaded, create a loop - the loop asks either to display status of all packages, or to allow trucks to continue delivery.
    while True:
        print("1. Proceed with package delivery.")
        print("2. Display status of all packages.")
        print("3. Exit program.")

        userInput = input("Please enter your choice: ")
        # require an if statement to check time of truck 2 to loop back to origin and grab package 6, 25, 28, 32
        if truck2.time >= 9005:
            # add mileage of truck to return to hub
            calcLocation = truck2.location
            location2List = mapGraph.search(calcLocation)
            edgeAddition = int(location2List[0])
            truck2.miles = truck2.miles + edgeAddition
            # set new truck position to be hub
            truck2.location = mapGraph.nodes[0]
            # set new truck time
            truck2.time = truck2.time + timedelta(minutes=(edgeAddition / 18))
            # load packages onto truck
            truck2.loadTruck(packagesList.search(6))
            truck2.loadTruck(packagesList.search(25))
            truck2.loadTruck(packagesList.search(28))
            truck2.loadTruck(packagesList.search(32))
        # require an if statement to check time of truck 3 to loop back to origin and grab package 9, change package 9 information to match update
        if truck3.time >= 1020:
            # change package 9 information
            packagesList.search(9).street = '410 S State St'
            packagesList.search(9).city = 'Salt Lake City'
            packagesList.search(9).zip = '84111'
            # move truck
            calcLocation = truck3.location
            location3List = mapGraph.search(calcLocation)
            edgeAddition = int(location3List[0])
            truck3.miles = truck3.miles + edgeAddition 
            # set new truck position to be hub
            truck3.location = mapGraph.nodes[0]
            # set new truck time
            truck3.time = truck3.time + timedelta(minutes=(edgeAddition / 18))
            # load packages onto truck
            truck3.loadTruck(packagesList.search(9))
        # loop through cycle
        if userInput == '1':
            # run nearest neighbour algorithm for each truck once, checking if the truck is empty
            if len(truck1.packagesCarried) != 0:
                mapGraph.nearestNeighbourDelivery(truck1, packagesList)
            if len(truck2.packagesCarried) != 0:
                mapGraph.nearestNeighbourDelivery(truck2, packagesList)
            if len(truck3.packagesCarried) != 0:
                mapGraph.nearestNeighbourDelivery(truck3, packagesList)
        elif userInput == '2':
            # if status is selected, print out status of all packages, additionally print out mileage for each truck
            for i in range(1, 40):
                print(packagesList.search(i))
            print(truck1)
            print(truck2)
            print(truck3)
        elif userInput == '3':
            break
        elif len(truck1.packagesCarried) == 0 and len(truck2.packagesCarried) == 0 and len(truck3.packagesCarried) == 0:
            # finally, once trucks are empty, print out mileage of all trucks.
            print(f"Truck 1 has travelled {truck1.miles} miles.")
            print(f"Truck 2 has travelled {truck2.miles} miles.")
            print(f"Truck 3 has travelled {truck3.miles} miles.")
            break

# run main function
if __name__ == "__main__":
    main()
