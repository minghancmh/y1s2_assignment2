# y1s2_assignment2
Keyword, Location, Price based search of NTU Canteens <br/>
This programme takes a user input based on keywords, locations, or preferred price, and returns the user suggested canteens within NTU.


## Dependencies
"canteens.xlsx" provides the canteen data in NTU, such as the foods that each canteen sells, the price, as well as the location <br/>
"NTU Campus.jpg" is a map of NTU, used for the location based search <br/>
"pin.png" is used as the drop pin image for the location based search

## Introduction
The initial part of this programme is for data cleaning and manipulation. The "canteens.xlsx" file is handled using the pandas library, and dictionaries of the canteens keywords, locations and prices are generated. These dictionaries are then used later to provide relavent search results for the user based on the desired input. pygame is also used for the location based search so that a visual, and more intuitive element within this programme is generated, making this program easier to use.

## Keyword Search
The keyword search takes in a strong, with "and", "or", spaces, or any combination of these between keywords. It then breaks the string up into the various keywords, with "and" taking precedence. <br/>
Spaces are also considered as an "and" requirement. <br/>
For example, if the user keys in "Chicken Indian", then the programme understands this as the user wanting the shop to sell BOTH chicken and indian (ie the keywords in "canteens.xlsx" contain both chicken and indian under its keywords. This is similar to "Chicken and Indian" <br/>
If the user keys in "Chicken or Indian", the user is returned a list of stalls which EITHER sell chicken OR indian. <br/>
If the user keys in "Chicken and Indian or Chinese", he is returned a lsit of stalls which EITHER sells (chicken AND indian) OR (chinese).

## Price-based Search
This search function is similar to the keyword search function, in that it allows the user to key in foods/cuisines that he/she likes to consume, and asks for an additional price parameter, which is the users budget. Following the keyword search function, if the user enters 5, then the user will only be shown results for food places which are under $5.

## Location Based Search
The pygame module is used here, and running this script will show a new window with the NTU Campus map. The user then selects the location of user A and user B (presumably 2 friends), and returns a list of k results back to the user, where k is the number of canteens that the user inputs. The search optimization is done using the lowest TOTAL euclidean (or straight line distnace) of the 2 users. This would make sense because it takes into account the straight line distance of each individual user to the dining location. I chose this over considering the midpoint of the 2 users as it directly calculated euclidean distances between individual and dining location rather than to reach the mid point first before moving off to the dining location.<br/>
The scipy.spatial.distance module was used here, to calculate euclidean distance. Alternatively, pythagoras theorem could be applied using the sqrt function. The euclidean distance function here works similarly. <br/>
Further work could also be done such that the optimization could allow for the return of the shortest distance from A or shortest distane from B, of shortest mean distance. This would only require very minor changes in the programme. 
