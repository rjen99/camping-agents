import mesa
import numpy as np
from model.general_functions import closest_distance, find_closest

class Camper(mesa.Agent):

    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)
        self.location = None
        self.happiness = 5
        self.occupied_spaces = []
        self.checked_spaces = []
        self.width = 2      # shorter edge
        self.height = 3     # longer edge
        self.tol = 3
        self.given_up = False
        print("Camper", self.unique_id)

    def step(self):
        
        # if the camper couldn't find a space with the lowest tolerance, they give up/go home
        if self.given_up:
            print("Camper", self.unique_id, "has given up")
            return
        
        # if not already placed
        if not self.location:
            print("Camper", self.unique_id, ":", self.tol, ":", self.location)
            valid_locations = find_closest(self.model.closest_dist_matrix, self.tol)
            
            if not valid_locations: # if there are no valid places, return
                
                if self.tol > 1:
                    self.happiness -= 2
                    self.tol -= 1

                print("Camper", self.unique_id, "couldn't be placed")
                return
            
            if len(self.checked_spaces) < len(valid_locations):
                self.location = valid_locations[len(self.checked_spaces)][0]
            else:
                if self.tol > 2:
                    self.checked_spaces = []
                    self.happiness -= 2
                    max_tol = np.amax(self.model.closest_dist_matrix)
                    if max_tol < self.tol:
                        self.tol = max_tol
                    else:
                        self.tol -= 1
                else:
                    self.given_up = True
                    self.happiness -= 10

                print("Camper", self.unique_id, "couldn't be placed")
                return

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
                        print("Camper", self.unique_id, "placing failed")
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
                            print("Camper", self.unique_id, "placing failed")
                            return
            for loc in self.occupied_spaces:
                self.model.campground[loc] = self.unique_id
            self.model.closest_dist_matrix = closest_distance(self.model.campground, dist='manhattan')
            self.happiness += 5
            print("Camper", self.unique_id, "placed at", self.occupied_spaces)

