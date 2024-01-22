Authored by Brendan Chan - contact at bchan7@wgu.edu
This was written for the Data Structures and Algorithms II Course at Western Governer's University.
This program was written in Python version 3.11.4 in Visual Studio Code, with no external libraries.

This program is designed to simulate a set of trucks delivering an assortment of packages with various requirements. Trucks are implemented as simple objects containing an array of packages, as well as a set of attributes indicating location, distance travelled, and truck's current time. Deliveries are carried out in a multi-step proccess. First, the program takes a .csv file containing a matrix of distances between various nodes. This .csv is turned into a graph structure using a hash table for quick lookup. Once the graph has been established, a greedy algorithm is used to determine the delivery route. 

To use this program, input a point in time into the program. The program will then simulate deliveries up until the input time, after which it will output information pertaining to the status of various packages and trucks. Once all packages have been delivered, the program will output a final report on package delivery times and total mileage of the trucks.
