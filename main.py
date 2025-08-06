#Student ID 012328034


import csv
import datetime

# Load address and distance data from CSV files into lists
with open("address.csv") as addyCSV:
    AddressCSV = list(csv.reader(addyCSV))
with open("distance.csv") as disCSV:
    DistanceCSV = list(csv.reader(disCSV))


class HashTableWChains:
    #Hash table
    def __init__(self, initialcapacity=40):
        # Initialize the table as a list of empty lists (buckets)
        self.table = [[] for _ in range(initialcapacity)]

    def insert(self, key, item):
        #Insert or update a key value pair
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # If the key already exists, update its value
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True
        # Otherwise append a new [key, value] pair to the bucket
        bucket_list.append([key, item])
        return True

    def search(self, key):
        #Search for the given key and return its value, or none
        bucket = hash(key) % len(self.table)
        for kv in self.table[bucket]:
            if kv[0] == key:
                return kv[1]
        return None

    def remove(self, key):
        #Remove the item with the given key from the hash table
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # Remove matching entry if present
        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove(kv)
                return True
        return False


class Packages:
    #Represents a delivery package with all relevant metadata and status tracking
    def __init__(self, ID, street, city, state, zip, deadline, weight, notes, status,
                 departureTime, deliveryTime):
        self.ID = ID
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.departureTime = None
        self.deliveryTime = None

    def __str__(self):
        return (
            f"ID: {self.ID}, {self.street:20}, {self.city}, {self.state}, {self.zip}, "
            f"Deadline: {self.deadline}, Weight: {self.weight}, Status: {self.status}, "
            f"Departure Time: {self.departureTime}, Delivery Time: {self.deliveryTime}"
        )

    def statusUpdate(self, timeChange):
        """
        Update the package status based on the provided query time.
        If not yet departed or en route, stays 'At the hub';
        after deliveryTime, status becomes 'Delivered'.
        Special logic for package ID 9 address correction after 10:20.
        """
        if self.ID in (6, 25, 28, 32) and timeChange < datetime.timedelta(hours=9, minutes=6):
            self.status = "Delayed"
            return
        if self.deliveryTime is None:
            self.status = "At the hub"
        elif timeChange < self.departureTime:
            self.status = "At the hub"
        elif timeChange < self.deliveryTime:
            self.status = "En route"
        else:
            self.status = "Delivered"

        # Correct address for package 9 after 10:20
        if self.ID == 9:
            if timeChange > datetime.timedelta(hours=10, minutes=20):
                self.street = "410 S State St"
                self.zip = "84111"
            else:
                self.street = "300 State St"
                self.zip = "84103"


def loadPackageData(filename):
    #Read package data from CSV and insert package objects into the global hash table.

    with open(filename) as packages:
        reader = csv.reader(packages)
        next(reader)  # Skip header row
        for row in reader:
            pID = int(row[0])
            pStreet, pCity, pState, pZip = row[1], row[2], row[3], row[4]
            pDeadline, pWeight, pNotes = row[5], row[6], row[7]
            pStatus = "At the hub"

            pkg = Packages(pID, pStreet, pCity, pState, pZip,
                           pDeadline, pWeight, pNotes, pStatus,
                           departureTime=None, deliveryTime=None)
            packageHash.insert(pID, pkg)


# Create the global package hash table
packageHash = HashTableWChains()


class Trucks:
    """
    Represents a delivery truck, tracking its speed, miles driven, current location,
    departure time, and assigned package IDs.
    """
    def __init__(self, speed, miles, currentLocation, departTime, packages):
        self.speed = speed
        self.miles = miles
        self.currentLocation = currentLocation
        self.departTime = departTime
        self.time = departTime
        self.packages = packages

    def __str__(self):
        return (f"Speed: {self.speed}, Miles: {self.miles}, Location: {self.currentLocation}, "
                f"Time: {self.time}, Packages: {self.packages}")


def addresss(address):
    #Look up the numeric address ID for the given street string in AddressCSV.
    for row in AddressCSV:
        if address in row[2]:
            return int(row[0])
    raise ValueError(f"Address '{address}' not found.")


def Betweenst(addy1, addy2):
    #Return the distance between two address IDs using the distance matrix CSV.

    dist = DistanceCSV[addy1][addy2]
    if dist == '':
        dist = DistanceCSV[addy2][addy1]
    return float(dist)



# Load packages from CSV into the hash table
loadPackageData("package.csv")

# Initialize three trucks with speeds, start location, departure times, and package lists
truck1 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=8),
                [1, 13, 14, 15, 16, 19, 20, 27, 29, 30, 31, 34, 37, 40])
truck2 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=11),
                [2, 3, 4, 5, 9, 18, 26, 28, 32, 35, 36, 38])
truck3 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5),
                [6, 7, 8, 10, 11, 12, 17, 21, 22, 23, 24, 25, 33, 39])


def truckDeliverPackages(truck):
    """
    Deliver all packages on the given truck using a nearest neighbor algorithm.
    Updates each packages departure and delivery times, and tracks miles driven.
    """
    # Gather package objects into an 'en route' list
    enroute = [packageHash.search(pid) for pid in truck.packages]
    truck.packages.clear()

    # Continue until all packages have been delivered
    while enroute:
        nextAddy = float('inf')
        nextPackage = None
        #Check for any priority packages that need forced delivery order
        for pkg in enroute:
            if pkg.ID in (25, 6):
                nextPackage = pkg
                nextAddy = Betweenst(addresss(truck.currentLocation), addresss(pkg.street))
                break
            # Otherwise pick the closest next package
            dist = Betweenst(addresss(truck.currentLocation), addresss(pkg.street))
            if dist < nextAddy:
                nextAddy = dist
                nextPackage = pkg

        # Drive to that package
        truck.miles += nextAddy
        truck.currentLocation = nextPackage.street
        drive_time = datetime.timedelta(hours=nextAddy / truck.speed)
        truck.time += drive_time

        # Record delivery and departure times on the package
        nextPackage.departureTime = truck.departTime
        nextPackage.deliveryTime = truck.time

        # Mark package as delivered and remove from en route list
        truck.packages.append(nextPackage.ID)
        enroute.remove(nextPackage)


# Run deliveries: truck1 and truck3 start immediately. truck2 waits until one returns
truckDeliverPackages(truck1)
truckDeliverPackages(truck3)
truck2.departTime = min(truck1.time, truck3.time)
truckDeliverPackages(truck2)

# total miles driven by the fleet
print("Western Governors University Parcel Service")
print("The overall miles are:", truck1.miles + truck2.miles + truck3.miles)

# Interactive status query loop
while True:
    # Ask user for a query time (HH:MM)
    userTime = input("Enter query time (HH:MM): ")
    h, m = map(int, userTime.split(':'))
    query_time = datetime.timedelta(hours=h, minutes=m)

    # Optionally filter by a single package ID
    try:
        pkg_id = int(input("Enter a Package ID to view (or press Enter): "))
        ids = [pkg_id]
    except ValueError:
        ids = range(1, 41)

    # Update and display status and truck number for each requested package
    for pid in ids:
        pkg = packageHash.search(pid)
        pkg.statusUpdate(query_time)

        # Figure out which truck delivered this package
        if pid in truck1.packages:
            truck_num = 1
        elif pid in truck2.packages:
            truck_num = 2
        elif pid in truck3.packages:
            truck_num = 3
        else:
            truck_num = 'N/A'  #not yet delivered

        print(f"{pkg} — Truck: {truck_num}")

