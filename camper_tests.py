import numpy as np
from model import Camper, Campground
import matplotlib.pyplot as plt

campground = np.zeros((5,5))
x=2
y=2
unique_id = 2
if campground[x,y] == 0:
    location = (x,y)
    campground[x-1:x+2,y-1:y+2] = -1     # Set surrounding area to -1 (not campable on)
    campground[x,y] = unique_id

#print(campground)

print("running test code")
test_model = Campground.Campground(10,5,5)
for i in range(10):
    test_model.step()
    print(test_model.campground)
#

#test_array = np.array([[1,0,0,1],[2,1,1,2],[3,2,2,3],[4,3,3,4]])
#print(test_array)
#locs = np.transpose(np.where(test_array>=3))
#print(locs)
#loc_dist = np.sum(locs,1)
#closest = locs[np.where(loc_dist==np.min(loc_dist))][0]
#print(closest)