import mesa
import numpy as np
from model.general_functions import closest_distance, find_closest, create_tol_neighbourhood, within_bounds

UNHAPPINESS_MULTIPLIER = 1

class Camper(mesa.Agent):

    def __init__(self, unique_id, model, shape=(2,3), tol=3) -> None:
        super().__init__(unique_id, model)
        self.location = None
        self.happiness = 5
        self.occupied_spaces = []
        self.checked_spaces = []
        self.width = shape[0]      # shorter edge
        self.height = shape[1]     # longer edge
        self.tol = tol
        self.max_tol = tol
        self.neighbourhood = dict()
        self.moving_hap = 3
        self.leaving_hap = 0
        self.given_up = False
        self.time_placed = np.nan
        print("Camper", self.unique_id)

    def step(self):
        
        # if the camper couldn't find a space with the lowest tolerance, they give up/go home
        if self.given_up:
            #print("Camper", self.unique_id, "has given up")
            return
        
        # if not already placed
        if not self.location:
            #print("Camper", self.unique_id, ":", self.tol, ":", self.location)
            valid_locations = find_closest(self.model.closest_dist_matrix, self.tol)
            if not valid_locations: # if there are no valid places, return
                
                if self.tol > 2:
                    self.lower_tol()
                else:
                    self.given_up = True
                    self.happiness -= 10
                    print("Camper", self.unique_id, "has given up")
    
                #print("Camper", self.unique_id, "couldn't be placed")
                return
            
            if len(self.checked_spaces) < len(valid_locations):
                self.location = valid_locations[len(self.checked_spaces)][0]
            else:
                if self.tol > 2:
                    self.checked_spaces = []
                    self.lower_tol()
                else:
                    self.given_up = True
                    self.happiness -= 10
                    print("Camper", self.unique_id, "has given up")
    
                #print("Camper", self.unique_id, "couldn't be placed")
                return
            self.location_search(valid_locations)

        else:
            #check neighbourhood
            for i in range(2,self.tol):
                curr_tol_neighbourhood = self.neighbourhood[i]
                for j in curr_tol_neighbourhood:
                    if self.model.campground[j[0],j[1]] != 0:
                        self.happiness -= (self.tol-i)*UNHAPPINESS_MULTIPLIER
                        self.tol = i
                        return

            #move if unhappy
            if self.happiness <= self.moving_hap:
                print("Camper", self.unique_id, "looking for better location")
                max_tol = np.amax(self.model.closest_dist_matrix)
                if max_tol > self.tol:
                    valid_locations = find_closest(self.model.closest_dist_matrix, self.tol+1, priority='largest')
                    
                    if not valid_locations: # if there are no valid places, return
                        
                        if self.happiness <= self.leaving_hap:
                            for loc in self.occupied_spaces:
                                self.model.campground[loc] = self.unique_id
                            self.model.closest_dist_matrix = closest_distance(self.model.campground, dist='manhattan')
                            self.given_up = True
                            self.time_placed = np.nan
                            print("Camper", self.unique_id, "became unhappy and left")
                        return

                    if len(self.checked_spaces) < len(valid_locations):
                        self.location = valid_locations[len(self.checked_spaces)][0]
                    else:
                        return

                    self.location_search(valid_locations)
                    if self.happiness <= self.leaving_hap:
                        for loc in self.occupied_spaces:
                            self.model.campground[loc] = self.unique_id
                        self.model.closest_dist_matrix = closest_distance(self.model.campground, dist='manhattan')
                        self.given_up = True
                        self.time_placed = np.nan
                        print("Camper", self.unique_id, "became unhappy and left")

    def create_neighbourhood(self):
        for i in range(2,self.tol):
            self.neighbourhood[i]=[]
        
        non_unique_neighbouhood = []
        np_occ_spaces = np.array(self.occupied_spaces)
        
        top_bound = max(np_occ_spaces[:,0])
        lower_bound = min(np_occ_spaces[:,0])
        left_bound = min(np_occ_spaces[:,1])
        right_bound = max(np_occ_spaces[:,1])

        upper_left = [top_bound,left_bound]
        upper_right = [top_bound,right_bound]
        lower_left = [lower_bound,left_bound]
        lower_right = [lower_bound,right_bound]
        corners = [upper_left, upper_right, lower_left, lower_right]

        for i in range(2,self.tol):
            curr_tol = self.model.tol_dict[i]
            non_unique_neighbouhood = []
            for j in range(4):
                direction = curr_tol[j]
                corner = corners[j]
                for k in direction:
                    neighbourhood_loc = list(np.add(corner, k))
                    if within_bounds(20,20,neighbourhood_loc):
                        non_unique_neighbouhood.append(neighbourhood_loc)
            
            if within_bounds(20,20,[top_bound+i,0]):
                non_unique_neighbouhood.extend([[top_bound+i, j] for j in range(left_bound,right_bound+1)])   # top edge

            if within_bounds(20,20,[lower_bound-i,0]):
                non_unique_neighbouhood.extend([[lower_bound-i, j] for j in range(left_bound,right_bound+1)]) # bottom edge

            if within_bounds(20,20,[0,left_bound-i]):
                non_unique_neighbouhood.extend([[j, left_bound-i] for j in range(lower_bound,top_bound+1)])   # left edge

            if within_bounds(20,20,[0,right_bound+i]):
                non_unique_neighbouhood.extend([[j, right_bound+i] for j in range(lower_bound,top_bound+1)])  # right edge

            self.neighbourhood[i] = np.unique(non_unique_neighbouhood,axis=0)

    def location_search(self, valid_locations):
        valid_locations = [x[0] for x in valid_locations]
        #print(valid_locations)
        if self.height == 1: # one-square camper
            self.occupied_spaces = [self.location]
            self.happiness += 5
            print("Camper", self.unique_id, "placed at", self.occupied_spaces)
            return
        
        check_loc = self.location
        try_other_orientation = False

        for i in range(self.height):
            for j in range(self.width):

                check_loc = (self.location[0]+i,self.location[1]+j)
                #print(check_loc)

                if check_loc in valid_locations:
                    self.occupied_spaces.append(check_loc)
                    #print("yeah")
                elif i < self.width:
                    #print("nah")
                    # if the height that is being checked is less than the width, the space isn't going
                    # to be valid when the tent is transposed
                    self.checked_spaces.append(self.location)
                    self.occupied_spaces = []
                    self.location = None
                    #self.happiness -= 1
                    #print("Camper", self.unique_id, "placing failed")
                    return
                else:
                    #print("eh")
                    try_other_orientation = True
                    self.occupied_spaces = []
                    break
            if try_other_orientation:
                break

        if try_other_orientation:
            for i in range(self.height):
                for j in range(self.width):

                    check_loc = (self.location[0]+j,self.location[1]+i)

                    if check_loc in valid_locations:
                        self.occupied_spaces.append(check_loc)
                    else:
                        # if something isn't valid now, no orientation will work so end the attempt
                        self.checked_spaces.append(self.location)
                        self.occupied_spaces = []
                        self.location = None
                        #self.happiness -= 1
                        #print("Camper", self.unique_id, "placing failed")
                        return
        for loc in self.occupied_spaces:
            self.model.campground[loc] = self.unique_id
        self.model.closest_dist_matrix = closest_distance(self.model.campground, dist='manhattan')
        self.happiness += 5
        self.create_neighbourhood()
        self.time_placed = self.model.timestep

        print("Camper", self.unique_id, "placed at", self.occupied_spaces)
    
    def lower_tol(self):
        self.happiness -= 2
        max_tol = np.amax(self.model.closest_dist_matrix)
        if max_tol < self.tol:
            self.tol = max_tol
        else:
            self.tol -= 1