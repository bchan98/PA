# Brendan Chan - 010555373 - WGU C950 - Python 3.11.4

import csv, hash
from datetime import datetime, time, timedelta

class Packages:
    def __init__(self, id, street, city, zip, deadline, weight, status, statusTime):
        self.id = id
        self.street = street
        self.city = city
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.statusTime = statusTime

    def __str__(self):
        if self.statusTime == None:
            return f"The package no. {self.id} is to be delivered to {self.street}, {self.city} at zipcode {self.zip} before {self.deadline}. The package weights {self.weight} pounds. The status of the package is: {self.status}"
        else:
            return f"The package no. {self.id} is to be delivered to {self.street}, {self.city} at zipcode {self.zip} before {self.deadline}. The package weights {self.weight} pounds. The status of the package is: {self.status}, and was delivered at {self.statusTime}."
    
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
                insertStatusTime = None

                insertPackage = Packages(insertID, insertStreet, insertCity, insertZip, insertDeadline, insertWeight, insertStatus, insertStatusTime)
                packageTable.insert(insertID, insertPackage)
    
    def resetPackage(self):
        self.status = 'AT HUB'
        self.statusTime = None

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
        sTime = self.time.strftime('%I:%M %p')
        nuPackage.statusTime = sTime
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
    
    def nearestNeighbourDelivery(self, nuTruck, inputPackageTable, inputTime):
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

        # once nearest distance found, check the travel time.
        timeCalc = (nearestDistance / nuTruck.speed) * 60
        timeIncrement = timedelta(minutes=timeCalc)

        modifiedTime = nuTruck.time + timeIncrement

        # check if travel time would exceed input time
        if modifiedTime.time() >= inputTime.time():
            # signal delivery would have passed input time
            return 2
        else:
            # if would not, travel to new location and add time to truck
            nuTruck.time = modifiedTime

            # additionally, add mileage to the truck
            nuTruck.miles = nuTruck.miles + nearestDistance

            # change truck's previous location to new location
            nuTruck.location = inputPackageTable.search(nextPackage).street

            # remove package from package list and set package status to have been delivered
            nuTruck.unloadTruck(inputPackageTable.search(nextPackage))

            # signal delivery was successful
            return 1

def main():
    # give introduction + instructions
    print("Welcome to the WGUPS package delivery system.")
    print("This program is designed to deliver packages until the user inputted time has been met. Afterwards, it will pause delivery and give output on the status of all the packages and the trucks.")
    print("If you instead wish to immediately exit the program, please enter 'exit'.")
    print("You can input in a time to check the status of all the packages in delivery. Please provide the time in a 24 hour format as follows: HH:MM")
    
    while True:
        # generate hash tables + graphs and fill in information
        packagesTable = hash.hashTable() # this is the packageTable
        Packages.importCSV('CSV/package.csv', packagesTable)
        mapGraph = Graph() # this is the graph for the map
        mapGraph.generateMap('CSV/address.csv', 'CSV/distance.csv') # generates vertexes/edges for graph
        t = datetime(year=2023, month=12, day=5, hour=8, minute=00) # set time to 8:00 AM

        # create flags to check behaviour of trucks
        flag1 = True
        flag2 = True
        marker = 0

        # two time comparisons to meet requirements of looping back to hub
        firstCompareTime = time(hour=9, minute=5)
        secondCompareTime = time(hour=10, minute=20)

        # inquire for user input
        while True:
            print("You may enter in another time to check in on the status of all packages. If you wish to exit the program, please enter 'exit'.")
            userTime = input("Please input a time: ")
            try:
                timeCheck = datetime.strptime(userTime, '%H:%M')
                break
            except ValueError:
                if userTime == 'exit':
                    exit()
                else:
                    print("Invalid input. Please enter the time in the format HH:MM.")

        # create trucks
        truck1 = Trucks(18.0, 0, '4001 South 700 East', t, [])
        truck2 = Trucks(18.0, 0, '4001 South 700 East', t, [])
        truck3 = Trucks(18.0, 0, '4001 South 700 East', t, [])

        # check if time has passed 8:00 - if not, do not deliver
        if timeCheck.time() < t.time():
            print("The time has been reached. The status of all packages is as follows:")
            for i in range(1, 41):
                print(packagesTable.search(str(i)))
            print("The status of the trucks are as follows:")
            print("The first truck:")
            print(truck1)
            print("The second truck:")
            print(truck2)
            print("The third truck:")
            print(truck3)
            print(f"The total mileage travelled by all trucks is {truck1.miles + truck2.miles + truck3.miles} miles.")
            continue

        # generate a list of packages for each truck
        truck1list = [13, 14, 15, 16, 19, 20, 26, 40]
        truck2list = [3, 8, 18, 36, 38, 29, 30, 31, 34, 37, 39]
        truck3list = [1, 2, 4, 5, 7, 10, 11, 12, 17, 21, 22, 23, 24, 35, 33, 27]
        
        # set the time to start of the day
        checkStartFlag = True
        # reset package status
        for i in range(1, 41):
            packagesTable.search(str(i)).resetPackage()
        # reset delivery flag
        deliveryFlag = True

        # begin delivery loop
        while deliveryFlag == True:
            marker = 0
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
                edgeAddition = float(location3List[0])
                truck3.miles = truck3.miles + edgeAddition 
                # set new truck position to be hub
                truck3.location = mapGraph.nodes[0]
                # set new truck time
                truck3.time = truck3.time + timedelta(minutes=(edgeAddition / 18))
                # load packages onto truck
                truck3.loadTruck(packagesTable.search(str(9)))
                # set flag to false
                flag2 = False

            # check if this is the start of the day
            if checkStartFlag == True:
                # if start of day, using the list of packages, get the package object from the hash table and load packages into the truck via for loop 
                for i in truck1list:
                    truck1.loadTruck(packagesTable.search(str(i)))
                for i in truck2list:
                    truck2.loadTruck(packagesTable.search(str(i)))
                for i in truck3list:
                    truck3.loadTruck(packagesTable.search(str(i)))
                checkStartFlag = False

            # run nearest neighbour algorithm for one cycle, if there are packages on the truck
            if len(truck1.packagesCarried) != 0:
                result1 = mapGraph.nearestNeighbourDelivery(truck1, packagesTable, timeCheck)
            if len(truck2.packagesCarried) != 0:
                result2 = mapGraph.nearestNeighbourDelivery(truck2, packagesTable, timeCheck)
            if len(truck3.packagesCarried) != 0:
                result3 = mapGraph.nearestNeighbourDelivery(truck3, packagesTable, timeCheck)

            # check if any of the deliveries would have passed the input time.
            if result1 and result2 and result3 != 1:
                # if all 3 conditions are true, deliveryFlag is set to false and loop ends
                deliveryFlag = False

            # check if all packages have been delivered
            for i in range(1, 41):
                if packagesTable.search(str(i)).status != 'DELIVERED':
                    marker = 1

            # if all packages have been delivered, deliveryFlag is set to false and loop ends
            if marker == 0:
                deliveryFlag = False
                break

        # after time has been reached, ask to print out status of all packages and trucks
        print("The time has been reached. The status of all packages is as follows:")
        for i in range(1, 41):
            print(packagesTable.search(str(i)))
        print("The status of the trucks are as follows:")
        print("The first truck:")
        print(truck1)
        print("The second truck:")
        print(truck2)
        print("The third truck:")
        print(truck3)
        print(f"The total mileage travelled by all trucks is {truck1.miles + truck2.miles + truck3.miles} miles.")

# run main function
if __name__ == "__main__":
    main()
