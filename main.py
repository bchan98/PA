import csv, hash
from datetime import datetime, time, timedelta

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
    def importCSV(filename, packageTable):
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
        sTime = self.time.strftime('%I:%M %p')
        return f"The speed of the truck is {self.speed} miles per hour and has travelled {self.miles} miles. The truck is currently at {self.location} at {sTime}. The truck currently contains {len(self.packagesCarried)} packages."

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
        for i in range(len(self.nodes)):
            self.map.insert(self.nodes[i], self.edges[i])
    
    def nearestNeighbourDelivery(self, nuTruck, inputPackageTable):
        # initialize parameters
        curLocation = nuTruck.location
        curLocationID = self.nodes.index(curLocation)

        packageList = nuTruck.packagesCarried
        nearestDistance = 1000.00
        nextPackage = ''

        # loop through to find nearest location
        for i in packageList:
            packageLocationName = inputPackageTable.search(str(i.id)).street
            locationList = self.map.search(packageLocationName)
            edgeWeight = float(locationList[curLocationID])
            if nearestDistance > edgeWeight:
                nearestDistance = edgeWeight
                nextPackage = i.id

        # once nearest distance found, travel there and increment time
        timeCalc = (nearestDistance / 18) * 60
        timeIncrement = timedelta(minutes=timeCalc)

        modifiedTime = nuTruck.time + timeIncrement
        nuTruck.time = modifiedTime

        # additionally, add mileage to the truck
        nuTruck.miles = nuTruck.miles + nearestDistance

        # change current location to destination location
        nuTruck.location = inputPackageTable.search(nextPackage).street

        # print out that a package has been successfully delivered
        print(f"Package no. {nextPackage} has been successfully delivered.")

        # remove package from package list and set package status to have been delivered
        nuTruck.unloadTruck(inputPackageTable.search(nextPackage))

        return

def main():
    # generate hash tables + graphs and fill in information
    packagesTable = hash.hashTable() # this is the packageTable
    Packages.importCSV('CSV/package.csv', packagesTable)
    mapGraph = Graph() # this is the graph for the map
    mapGraph.generateMap('CSV/address.csv', 'CSV/distance.csv') # generates vertexes/edges for graph
    t = datetime(year=2023, month=12, day=5, hour=8, minute=00) # set time to 8:00 AM
    # create trucks
    truck1 = Trucks(18, 0, '4001 South 700 East', t, [])
    truck2 = Trucks(18, 0, '4001 South 700 East', t, [])
    truck3 = Trucks(18, 0, '4001 South 700 East', t, [])

    # generate a list of packages for each truck
    truck1list = [13, 14, 15, 16, 19, 20, 26, 27, 33, 35, 40]
    truck2list = [3, 18, 36, 38, 29, 30, 31, 34, 37, 39]
    truck3list = [1, 2, 4, 5, 7, 10, 11, 12, 17, 21, 22, 23, 24]

    # using the list of packages, get the package object from the hash table and load it into the truck in a for loop
    for i in truck1list:
        truck1.loadTruck(packagesTable.search(str(i)))
    for i in truck2list:
        truck2.loadTruck(packagesTable.search(str(i)))
    for i in truck3list:
        truck3.loadTruck(packagesTable.search(str(i)))
    # once loaded, create a loop - the loop asks either to display status of all packages, or to allow trucks to continue delivery.

    # two flags to check behaviour of looping back to hub
    flag1 = True
    flag2 = True

    while True:
        if len(truck1.packagesCarried) == 0 and len(truck2.packagesCarried) == 0 and len(truck3.packagesCarried) == 0:
            # check to see if all packages have been delivered
            print(f"All packages have been successfully delivered.")
            print(f"Truck 1 has travelled {truck1.miles} miles.")
            print(f"Truck 2 has travelled {truck2.miles} miles.")
            print(f"Truck 3 has travelled {truck3.miles} miles.")
            break
        else:
            # else, begin looping through package delivery
            print("1. Proceed with package delivery.")
            print("2. Display status of all packages.")
            print("3. Exit program.")

            userInput = input("Please enter your choice: ")
            firstCompareTime = time(hour=9, minute=5)
            secondCompareTime = time(hour=10, minute=20)
            # require an if statement to check time of truck 2 to loop back to origin and grab package 6, 25, 28, 32
            if truck2.time.time() >= firstCompareTime and flag1 == True:
                # add mileage of truck to return to hub
                calcLocation = truck2.location
                location2List = mapGraph.map.search(calcLocation)
                edgeAddition = float(location2List[0])
                truck2.miles = truck2.miles + edgeAddition
                # set new truck position to be hub
                truck2.location = mapGraph.nodes[0]
                # set new truck time
                truck2.time = truck2.time + timedelta(minutes=(edgeAddition / 18))
                # load packages onto truck
                truck2.loadTruck(packagesTable.search(str(6)))
                truck2.loadTruck(packagesTable.search(str(25)))
                truck2.loadTruck(packagesTable.search(str(28)))
                truck2.loadTruck(packagesTable.search(str(32)))
                # set flag to false
                flag1 = False
            # require an if statement to check time of truck 3 to loop back to origin and grab package 9, change package 9 information to match update
            if truck3.time.time() >= secondCompareTime and flag2 == True:
                # change package 9 information
                packagesTable.search(str(9)).street = '410 S State St'
                packagesTable.search(str(9)).city = 'Salt Lake City'
                packagesTable.search(str(9)).zip = '84111'
                # move truck
                calcLocation = truck3.location
                location3List = mapGraph.map.search(calcLocation)
                edgeAddition = int(location3List[0])
                truck3.miles = truck3.miles + edgeAddition 
                # set new truck position to be hub
                truck3.location = mapGraph.nodes[0]
                # set new truck time
                truck3.time = truck3.time + timedelta(minutes=(edgeAddition / 18))
                # load packages onto truck
                truck3.loadTruck(packagesTable.search(9))
                # set flag to false
                flag2 = False
            # loop through cycle
            if userInput == '1':
                # run nearest neighbour algorithm for each truck once, checking if the truck is empty
                if len(truck1.packagesCarried) != 0:
                    mapGraph.nearestNeighbourDelivery(truck1, packagesTable)
                if len(truck2.packagesCarried) != 0:
                    mapGraph.nearestNeighbourDelivery(truck2, packagesTable)
                if len(truck3.packagesCarried) != 0:
                    mapGraph.nearestNeighbourDelivery(truck3, packagesTable)
            elif userInput == '2':
                # if status is selected, print out status of all packages, additionally print out mileage for each truck
                for i in range(1, 40):
                    print(packagesTable.search(str(i)))
                print(truck1)
                print(truck2)
                print(truck3)
            elif userInput == '3':
                break
# run main function
if __name__ == "__main__":
    main()
