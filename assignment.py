import pygame
from PIL import Image
import time
import pandas as pd
import numpy as np
from scipy.spatial import distance
import validation as vd


# load dataset for keyword dictionary - provided
def load_stall_keywords(data_location="/Users/minghanchan/Desktop/RE1016 - Engineering Computation/Assignment 2/assignment/canteens.xlsx"):
    # get list of canteens and stalls
    canteen_data = pd.read_excel(data_location)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    stalls = canteen_data['Stall'].unique()
    stalls = sorted(stalls, key=str.lower)

    keywords = {}
    for canteen in canteens:
        keywords[canteen] = {}

    copy = canteen_data.copy()
    copy.drop_duplicates(subset="Stall", inplace=True)
    stall_keywords_intermediate = copy.set_index('Stall')['Keywords'].to_dict()
    stall_canteen_intermediate = copy.set_index('Stall')['Canteen'].to_dict()

    for stall in stalls:
        stall_keywords = stall_keywords_intermediate[stall]
        stall_canteen = stall_canteen_intermediate[stall]
        keywords[stall_canteen][stall] = stall_keywords

    return keywords


# load dataset for price dictionary - provided
def load_stall_prices(data_location="canteens.xlsx"):
    # get list of canteens and stalls
    canteen_data = pd.read_excel(data_location)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    stalls = canteen_data['Stall'].unique()
    stalls = sorted(stalls, key=str.lower)

    prices = {}
    for canteen in canteens:
        prices[canteen] = {}

    copy = canteen_data.copy()
    copy.drop_duplicates(subset="Stall", inplace=True)
    stall_prices_intermediate = copy.set_index('Stall')['Price'].to_dict()
    stall_canteen_intermediate = copy.set_index('Stall')['Canteen'].to_dict()

    for stall in stalls:
        stall_price = stall_prices_intermediate[stall]
        stall_canteen = stall_canteen_intermediate[stall]
        prices[stall_canteen][stall] = stall_price

    return prices


# load dataset for location dictionary - provided
def load_canteen_location(data_location="canteens.xlsx"):
    # get list of canteens
    canteen_data = pd.read_excel(data_location)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    # get dictionary of {canteen:[x,y],}
    canteen_locations = {}
    for canteen in canteens:
        copy = canteen_data.copy()
        copy.drop_duplicates(subset="Canteen", inplace=True)
        canteen_locations_intermediate = copy.set_index('Canteen')['Location'].to_dict()
    for canteen in canteens:
        canteen_locations[canteen] = [int(canteen_locations_intermediate[canteen].split(',')[0]),
                                      int(canteen_locations_intermediate[canteen].split(',')[1])]

    return canteen_locations


# get user's location with the use of PyGame - provided
def get_user_location_interface():
    # get image dimensions
    image_location = 'NTUcampus.jpg'
    pin_location = 'pin.png'
    screen_title = "NTU Map"
    image = Image.open(image_location)
    image_width_original, image_height_original = image.size
    scaled_width = int(image_width_original)
    scaled_height = int(image_height_original)
    pinIm = pygame.image.load(pin_location)
    pinIm_scaled = pygame.transform.scale(pinIm, (60, 60))
    # initialize pygame
    pygame.init()
    # set screen height and width to that of the image
    screen = pygame.display.set_mode([scaled_width, scaled_height])
    # set title of screen
    pygame.display.set_caption(screen_title)
    # read image file and rescale it to the window size
    screenIm = pygame.image.load(image_location)

    # add the image over the screen object
    screen.blit(screenIm, (0, 0))
    # will update the contents of the entire display window
    pygame.display.flip()

    # loop for the whole interface remain active
    while True:
        # checking if input detected
        pygame.event.pump()
        event = pygame.event.wait()
        # closing the window
        if event.type == pygame.QUIT:
            pygame.display.quit()
            mouseX_scaled = None
            mouseY_scaled = None
            break
        # resizing the window
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(
                event.dict['size'], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
            screen.blit(pygame.transform.scale(screenIm, event.dict['size']), (0, 0))
            scaled_height = event.dict['h']
            scaled_width = event.dict['w']
            pygame.display.flip()
        # getting coordinate
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # get outputs of Mouseclick event handler
            (mouseX, mouseY) = pygame.mouse.get_pos()
            # paste pin on correct position
            screen.blit(pinIm_scaled, (mouseX - 25, mouseY - 45))
            pygame.display.flip()
            # return coordinates to original scale
            mouseX_scaled = int(mouseX * 1281 / scaled_width)
            mouseY_scaled = int(mouseY * 1550 / scaled_height)
            # delay to prevent message box from dropping down
            time.sleep(0.2)
            break

    pygame.quit()
    pygame.init()
    return mouseX_scaled, mouseY_scaled


# Keyword-based Search Function - to be implemented
#use only "and", "or", or a space between keywords, or any combination of these
def keyword_search_clean_data(keywords):
    keywords = keywords.upper()
    list_of_keywords_by_OR = keywords.split(" OR ")
    clean_list = []
    for keyword in list_of_keywords_by_OR:
        keyword = keyword.strip()
        clean_list.append(keyword)
    # print(clean_list)

    list_of_keywords_and = []
    for item in clean_list:
        if "AND" in item:
            inner_list = item.split("AND")
            inner_list_clean = []
            for item in inner_list:
                item = item.strip()
                inner_list_clean.append(item)
            list_of_keywords_and.append(inner_list_clean)
        else:
            inner_list = item.split(" ")
            list_of_keywords_and.append(inner_list)
            # list_of_keywords_and.append(item)
    return list_of_keywords_and

# def search_by_keyword(keywords)
def search_by_keyword_print():
    keywords = input("Please key in your food preferences, use only AND, OR, or spaces:")
    try:
        if keywords == "":
            raise TypeError("No input detected, please input your preferences.")

        else:
            final_keyword_list = keyword_search_clean_data(keywords)
            reco_stalls_keywords = []
            # for choice in clean_list:
            for key,value in canteen_stall_keywords.items():
                for stall,keywords in value.items():
                    keywords = keywords.upper() 
            
                    for item in final_keyword_list:
                        check_true = np.zeros(len(item))
                        for and_item in item:
                            if and_item in keywords:
                                check_true[item.index(and_item)] = 1
                        if 0 not in check_true:
                            reco_stalls_keywords.append(key+" - "+stall)
                                    
            reco_keywords_count = []                       
            if len(reco_stalls_keywords) == 0:
                print("No matches, try broadening your search parameters or check your spelling")
            else:
                
                for item in reco_stalls_keywords:
                    if reco_stalls_keywords.count(item)==1:
                        reco_keywords_count.append([item,1])
                    else:
                        reco_keywords_count.append([item,reco_stalls_keywords.count(item)])
                final_list = []
                for foodstall in reco_keywords_count:
                    if foodstall not in final_list:
                        final_list.append(foodstall)
                final_list.sort(key = lambda x: x[1])
                print("")
                print("Food Stall(s) found: " + str(len(final_list)))

        
                counter = []
                for item in final_list:
                    counter.append(item[1])
                # print(counter)

                for i in range(max(counter),0,-1):
                    print("")
                    print(f"Food Stalls that match {i} keyword(s):")
                    print("")
                    for item in final_list:
                        if item[1] == i:
                            print(item[0])
                

    except TypeError as err:
        print(err)
    except ValueError as err:
        print(err)



def search_by_keyword_return():
    keywords = input("Please key in your food preferences, use only AND, OR, or spaces")
    try:
        if keywords == "":
            raise TypeError("No input detected, please input your preferences.")
        elif type(keywords) != str:
            raise ValueError("You have not keyed in a string, use double quotation marks.")

        else:
            final_keyword_list = keyword_search_clean_data(keywords)
            reco_stalls_keywords = []
            # for choice in clean_list:
            for key,value in canteen_stall_keywords.items():
                    for stall,keywords in value.items():
                        keywords = keywords.upper()
                        # print(keywords)
                        for item in final_keyword_list:
                            if type(item) != list:
                                if item in keywords:
                                    reco_stalls_keywords.append(stall)
                            else:
                                check_true = np.zeros(len(item))
                                for and_item in item:
                                    if and_item in keywords:
                                        check_true[item.index(and_item)] = 1
                                if 0 not in check_true:
                                    reco_stalls_keywords.append(stall)
                                
            if len(reco_stalls_keywords) == 0:
                print("No matches, try broadening your search parameters or check your spelling")
            else:
                return reco_stalls_keywords                 
    except TypeError as err:
        print(err)
    except ValueError as err:
        print(err)



    # print(canteen_stall_keywords)


                



# Price-based Search Function - to be implemented
# def search_by_price(keywords, max_price):

def search_by_price():
    possibleStalls = search_by_keyword_return()
    # max_price = input("Enter Maximum Meal Price (S$)")
    while True:
        max_price = input("Enter Maximum Meal Price (S$)")
        try:
            max_price = float(max_price)

            if max_price<0:
                raise TypeError("Please key in positive integer or float.")
            break
        except TypeError as err:
            print(err)
            continue
        except ValueError:
            print("Please input an integer or float, not a string!")
            continue

    
        

    final_stall_by_price = []
    final_stall_no_matches = []
    for key,value in canteen_stall_prices.items():
            for stall,price in value.items():
                for a_stall in possibleStalls:
                    if stall == a_stall and price<=max_price:
                        final_stall_by_price.append([key,stall,price])
                    elif stall == a_stall:
                        final_stall_no_matches.append([key,stall,price])
                            
    if len(final_stall_by_price) == 0:
        print("No food stall found with specified price range. Recommended Food Stall with the closest price range.")
        final_stall_no_matches.sort(key = lambda x:x[2])
        print(final_stall_no_matches[0][0] + " - " + final_stall_no_matches[0][1] + " - " +"$" + str("{:.2f}".format(final_stall_no_matches[0][2])))
    else:
        print("Food Stall(s) found: "+ str(len(final_stall_by_price)))
        final_stall_by_price.sort(key = lambda x:x[2])
        # print(final_stall_by_price)
        for item in final_stall_by_price:
            print(item[0] + " - " + item[1] + " - " + "$" + str("{:.2f}".format(item[2])))



    




# Location-based Search Function - to be implemented
# To minimise the TOTAL EUCLIDEAN DISTANCE walked by person A and B 
def search_nearest_canteens(user_locations, k):
    canteen_distance_from_A = {}
    canteen_distance_from_B = {}
    total_dist = {}
    for canteen,coordinates in canteen_locations.items():
        canteen_distance_from_A[canteen] = round(distance.euclidean(user_locations[0],coordinates),2)
        canteen_distance_from_B[canteen] = round(distance.euclidean(user_locations[1],coordinates),2)
        total_dist[canteen] = round(canteen_distance_from_A[canteen] + canteen_distance_from_B[canteen],2)
    # print(type(total_dist["Ananda Kitchen"]))
    total_dist = dict(sorted(total_dist.items(), key=lambda item:item[1]))
    list_of_nearest_canteens = []
    for nearest_canteen,dist in total_dist.items():
        list_of_nearest_canteens.append([nearest_canteen,str(int(dist))])
    # print(total_dist)
    # print(list_of_nearest_canteens)
    print(f'{k} nearest canteen(s) found.')
    list_of_nearest_canteens_short = list_of_nearest_canteens[0:k]
    for loc in list_of_nearest_canteens_short:
        print(loc[0] + " - " + loc[1] + "m")
        
    

    





# Any additional function to assist search criteria

# Main Python Program Template
# dictionary data structures
canteen_stall_keywords = load_stall_keywords("/Users/minghanchan/Desktop/RE1016 - Engineering Computation/Assignment 2/assignment/canteens.xlsx")
canteen_stall_prices = load_stall_prices("/Users/minghanchan/Desktop/RE1016 - Engineering Computation/Assignment 2/assignment/canteens.xlsx")
canteen_locations = load_canteen_location("/Users/minghanchan/Desktop/RE1016 - Engineering Computation/Assignment 2/assignment/canteens.xlsx")
# print(canteen_stall_keywords)
# print(canteen_stall_prices)
# print(len(canteen_locations))
# main program template - provided
def main():
    loop = True


    while loop:

        print("=======================")
        print("F&B Recommendation Menu")
        print("1 -- Display Data")
        print("2 -- Keyword-based Search")
        print("3 -- Price-based Search")
        print("4 -- Location-based Search")
        print("5 -- Exit Program")
        print("=======================")
        option_unclean = input("Enter option [1-5]: ")
        option = vd.inp_valid(option_unclean)

        
        if option == 1:
            # print provided dictionary data structures
            print("1 -- Display Data")
            print("Keyword Dictionary: ", canteen_stall_keywords)
            print("Price Dictionary: ", canteen_stall_prices)
            print("Location Dictionary: ", canteen_locations)
        elif option == 2:
            # keyword-based search
            print("Keyword-based Search")
            # call keyword-based search function
            search_by_keyword_print()
            # search_by_keyword(keywords)
        elif option == 3:
            # price-based search
            print("Price-based Search")

            # call price-based search function
            search_by_price()
            # search_by_price(keywords, max_price)
        elif option == 4:
            # location-based search
            print("Location-based Search")

            # call PyGame function to get two users' locations
            userA_location = get_user_location_interface()
            print("User A's location (x, y): ", userA_location)
            userB_location = get_user_location_interface()
            print("User B's location (x, y): ", userB_location)

            # call location-based search function
            user_locations = [userA_location, userB_location]
            try:
                k = int(input("How many canteens suggestions would you like?"))
                if k<0 or k>15:
                    raise TypeError("Invalid value of k entered, default value k=1 set. k values should be an integer from 1-15.")
            except TypeError as err:
                print("")
                print(err)
                k=1
            except ValueError:
                print("")
                print("Invalid value entered, default value k=1 is set.")
                k=1
            search_nearest_canteens(user_locations, k)
        elif option == 5:
            # exit the program
            print("Exiting F&B Recommendation")
            loop = False


main()

