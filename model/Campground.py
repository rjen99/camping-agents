import mesa
import numpy as np
from model.Camper import Camper
from model.general_functions import closest_distance

class Campground(mesa.Model):

    def __init__(self, N, width, height):
        self.num_agents = N
        self.width = width
        self.height = height
        self.campground = np.zeros((width, height))
        self.closest_dist_matrix = closest_distance(self.campground, dist='manhattan')
        self.schedule = mesa.time.RandomActivation(self)

        self.campground_record = np.zeros((width, height,1))
        for i in range(1, self.num_agents+1):
            a = Camper(i, self)
            self.schedule.add(a)
    
    def step(self):
        self.schedule.step()
        #print(self.campground)
        self.campground_record = np.dstack([self.campground_record, self.campground])
