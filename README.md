# Stated Problem  

The Western Governors University Parcel Service (WGUPS) needs to determine an efficient route and delivery distribution for their daily local deliveries (DLD) because packages are not currently being consistently delivered by their promised deadline. The Salt Lake City DLD route has three trucks, two drivers, and an average of 40 packages to deliver each day. Each package has specific criteria and delivery requirements.  


The purpose of this project is to determine an algorithm, write code, and present a solution where all 40 packages (listed in the attached “WGUPS Package File”) will be delivered on time while meeting each package’s requirements and keeping the combined total distance traveled under 140 miles for both trucks. The specific delivery locations are shown on the attached “Salt Lake City Downtown Map,” and distances to each location are given in the attached “WGUPS Distance Table.” The intent is to use the program for this specific location and also for many other cities in each state where WGU has a presence.

# Assumptions  

• Each truck can carry a maximum of 16 packages, and the ID number of each package is unique.

• The trucks travel at an average speed of 18 miles per hour and have an infinite amount of gas with no need to stop.

• There are no collisions.

• Three trucks and two drivers are available for deliveries. Each driver stays with the same truck as long as that truck is in service.

• Drivers leave the hub no earlier than 8:00 a.m., with the truck loaded, and can return to the hub for packages if needed.

• The delivery and loading times are instantaneous, i.e., no time passes while at a delivery or when moving packages to a truck at the hub (that time is factored into the calculation of the average speed of the trucks).

• There is up to one special note associated with a package.

• The delivery address for package #9, Third District Juvenile Court, is wrong and will be corrected at 10:20 a.m. WGUPS is aware that the address is incorrect and will be updated at 10:20 a.m. However, WGUPS does not know the correct address (410 S State St., Salt Lake City, UT 84111) until 10:20 a.m.

• The distances provided in the WGUPS Distance Table are equal regardless of the direction traveled.

• The day ends when all 40 packages have been delivered.  

#Write Up  
## Algorithm Identification  

The Nearest Neighbor Algorithm (a type of Greedy Algorithm) is a self-adjusting algorithm that decides what to do in each step only based on the current situation. It does not look at the whole problem at one time. This can be used to determine the most efficient delivery route.  

##Data Structure Identification  

A hash table is a self-adjusting algorithm that can be used to store and manage package data. This structure will allow us to use constant-time lookups, insertions, and updates. Each package will have a unique ID that will be used as the key, and the package’s attributes will be stored as values.  

##Explanation of Data Structure  

Each entry in the hash table will represent a package, and the key will be the unique package ID. The value will be a dictionary containing the associated delivery information. This design will allow the program to access and update the package status. The design will also allow the program to track the delivery time and constraints. The hash table will facilitate fast data retrieval for tracking and progress updates during the delivery.  

##Algorithm's Logic  

```python
Start all trucks at hub
WHILE there are undelivered packages (packagelist > 0):
	IF truck is at hub:
		Load packages
	WHILE truck has packages:
		Use Nearest Neighbor to find the closest delivery location
		Drive to location
		Deliver package
		Record delivery time and update package status
		Remove package from packagelist
	IF packages remain at hub:
		Return to hub and repeat
```

##Development Environment  

The programming environment I will be using is a PC running Windows 11 OS for the operating system. It is connected via DisplayPort to 3 monitors. A keyboard is connected via USB, and a mouse is connected via Bluetooth. The software environment I will be using is Python 3.11 in PyCharm on the Windows 11 OS. Testing and version control will be managed using Git.  

##Space and Time Complexity Using Big-O Notation  

For the hash table operations, the Big-O notation is O(1) for lookup, insert, and update. For the Nearest Neighbor Route, it has a complexity of O(n^2) where n is the number of delivery locations. The total program complexity is O(n^2) for route optimization, and O(n) for data storage. Finally, the space complexity is O(n) for storing package data and the distance table.  

##Scalability and Adaptability  

The system is scalable to a high package count by increasing the resources of trucks or batching deliveries together. The design supports loading new data files even without changing the algorithm. The code is readable, so if something does need to be changed, it will be easy to do so. The hash table can manage larger datasets as it will maintain a complexity of O(1).  

##Software Efficiency and Maintainability  

The software is structured into functional modules, including: data loading, route calculation, and delivery tracking. Each module will be using standard Python structures and commented code explaining what everything does. Future improvements can be implemented with minimal refactoring.  

##Self-Adjusting Data Structures  

The hash table will dynamically adjust to handle any changes in the data set. For example, a change in delivery status updates or address corrections. Hash tables benefit from having fast access and updates using simple implementation. The are “a fast and efficient way for looking up, creating, and deleting stored data.” (Chresfield K., 2019). Hash table’s weakness it that it has no order, and it does not use extra storage. The programmer would have to re-hash the table to fix it. This is not a problem in our case.  

##Data Key  

The package ID will be used as the key in the hash table. It is a unique identifier that will guarantee accurate access to each package’s information. The package ID will also be good for avoiding duplication. Some key choices that could be duplicated are the delivery address and the delivery zip code.  

##Sources  

Chresfield, K. (2019, January 21). Pros & Cons of Hash Tables. Medium. https://medium.com/@kaelyn.chresfield/pros-cons-of-hash-tables-bc5d3097ffa7 
