#Python Assinment 1 by Shahid Nawaz Khan Student ID 101072668

#Importing Math Library
import math as libmath
#Setting Earth Radius as Constant
R=6371


#Location of salt lake City
lat1= 40.7607793
lng1= -111.8910474

#location of newyork
lat2= 40.7127837
lng2= -74.0059413

#Changing latlng from degrees to radians

#first set of coordinates changing from degrees to radians
lat1= libmath.radians(lat1)
lng1= libmath.radians(lng1)
#second set of coordinates changing from degrees to radians
lat2= libmath.radians(lat2)
lng2= libmath.radians(lng2)

#Finding differences in latlng and finding their absolute vaues
deltaLat= abs(lat1-lat2)
deltaLng= abs(lng1-lng2)

#This will be the part of equation inside the square root
#just to make things simple we will calcuate individual parts and then combine the equations
rootpart= libmath.sqrt((libmath.pow(libmath.sin((deltaLat)/2),2))+libmath.cos(lat1)*libmath.cos(lat2)*(libmath.pow(libmath.sin((deltaLng)/2),2)))


#Final Distance calculation by substituting the root part inside the main equation
distance = 2*R*libmath.asin(rootpart)

#Printing the distance to desired number of decimal points
print("%.4f" % distance)


