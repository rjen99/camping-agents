import mesa
import numpy as np

class Camper(mesa.Agent):

    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)
        self.location = None
        self.width = 1
        self.height = 1
        print("Camper", self.unique_id)

    def step(self):
        if not self.location:
            x = np.random.randint(self.model.width)
            y = np.random.randint(self.model.height)
            if self.model.campground[x,y] == 0:
                print("Camper", self.unique_id, "at position", (x,y))
                self.location = (x,y)
                if x == 0:
                    x_start = x
                    x_end = x+2
                elif x == self.model.width-1:
                    x_start = x-1
                    x_end = x+1
                else:
                    x_start = x-1
                    x_end = x+2

                if y == 0:
                    y_start = y
                    y_end = y+2
                elif y == self.model.height-1:
                    y_start = y-1
                    y_end = y+1
                else:
                    y_start = y-1
                    y_end = y+2
                
                self.model.campground[x_start:x_end,y_start:y_end] = -1     # Set surrounding area to -1 (not campable on)
                self.model.campground[x,y] = self.unique_id     # Set actual location to ID

