import mesa
import numpy as np
from model.general_functions import closest_distance, find_closest

class Camper(mesa.Agent):

    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)
        self.location = None
        self.occupied_spaces = None
        self.width = 1      # shorter edge
        self.height = 2     # longer edge
        self.tol = 3
        print("Camper", self.unique_id)

    def step(self):
        # if not already placed
        if not self.location:
            valid_locations = find_closest(self.model.closest_dist_matrix, self.tol)
            
            if not valid_locations: # if there are no valid places, return
                print("Camper", self.unique_id, "couldn't be placed")
                return
            
            self.location = valid_locations[0][0]

            # check spaces below and to the right for more spaces with the correct tolerances
            if self.height > 1:
                down = (self.location[0]+1,self.location[1])
                right = (self.location[0],self.location[1]+1)
                
                if down[0] != self.model.height:
                    self.occupied_spaces = [self.location,down]
                    for loc in self.occupied_spaces:
                        self.model.campground[loc] = self.unique_id
                    self.model.closest_dist_matrix = closest_distance(self.model.campground, dist='manhattan')
                    print("Camper", self.unique_id, "placed at", self.occupied_spaces)

                elif right[1] != self.model.width:
                    self.occupied_spaces = [self.location,right]
                    for loc in self.occupied_spaces:
                        self.model.campground[loc] = self.unique_id
                    self.model.closest_dist_matrix = closest_distance(self.model.campground, dist='manhattan')
                    print("Camper", self.unique_id, "placed at", self.occupied_spaces)
                
                else:
                    print("No space :(")
