import mesa
import numpy as np
from model.Camper import Camper
from model.manual_organisation import ManualCamper
from model.general_functions import closest_distance, create_tol_neighbourhood

class Campground(mesa.Model):

    def __init__(self, N, width, height, manual=False):
        self.num_agents = N
        self.width = width
        self.height = height
        self.campground = np.zeros((width, height))
        self.closest_dist_matrix = closest_distance(self.campground, dist='manhattan')
        self.schedule = mesa.time.RandomActivation(self)
        self.timestep = 0

        self.campground_record = np.zeros((width, height,1))
        self.tol_dict = dict()
    
    def init_campers(self, camper_type_list=np.array([[2,3,3,1]])):
        max_tol = int(np.max(camper_type_list[:,2]))
        self.tol_dict = create_tol_neighbourhood(max_tol-1)

        n_camper_type = len(camper_type_list)
        prop_sum = np.sum(camper_type_list[:,3])
        if prop_sum != 1:
            raise RuntimeError("Camper proportions should sum to 1")
        camper_quantity_list = []
        for camper_type in range(n_camper_type):
            camper_quantity_list.append(int(camper_type_list[camper_type,3]*self.num_agents))
        
        unique_id = 1
        for camper_type in range(n_camper_type):
            for i in range(camper_quantity_list[camper_type]):
                shape = (int(camper_type_list[camper_type,0]), int(camper_type_list[camper_type,1]))
                tol = int(camper_type_list[camper_type,2])
                camper = Camper(unique_id, self, shape, tol)
                self.schedule.add(camper)
                unique_id+=1
        return

    def step(self):
        self.timestep += 1
        self.schedule.step()
        #print(self.campground)
        self.campground_record = np.dstack([self.campground_record, self.campground])
