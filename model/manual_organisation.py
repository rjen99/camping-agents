import mesa
import numpy as np
from model.general_functions import closest_distance, find_closest
from model.Camper import Camper

class ManualCamper(Camper):

    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)
        self.happiness -= self.tol - 2      # reduce the starting happiness by how much closer the tents will be together by default
        self.tol = 2    # set tolerance low