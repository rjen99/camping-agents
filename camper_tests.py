import numpy as np
from model import Camper, Campground
import matplotlib.pyplot as plt
import matplotlib.animation as animation



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
test_model = Campground.Campground(15,10,10)
for i in range(10):
    test_model.step()
    #print(test_model.campground)

#print(test_model.campground_record[:,:,0])
#print(test_model.campground_record[:,:,9])

fig, ax = plt.subplots()

ims = []
for i in range(10):
    curr_im = test_model.campground_record[:,:,i]
    curr_im[np.where(curr_im>=1)] = 1
    im = ax.imshow(curr_im, animated=True)
    if i == 0:
        ax.imshow(test_model.campground_record[:,:,i])  # show an initial one first
    ims.append([im])

ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=1000)
plt.show()


#test_array = np.array([[1,0,0,1],[2,1,1,2],[3,2,2,3],[4,3,3,4]])
#print(test_array)
#locs = np.transpose(np.where(test_array>=3))
#print(locs)
#loc_dist = np.sum(locs,1)
#closest = locs[np.where(loc_dist==np.min(loc_dist))][0]
#print(closest)