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

height = 55
width = 50
num_campers = 238
num_steps = 750

print("running test code")
test_model = Campground.Campground(num_campers,height,width, manual=False)

for i in range(num_steps):
    print("Step", i,"\n--------")
    test_model.step()
    #print(test_model.campground)

#print(test_model.campground_record[:,:,0])
print(test_model.campground_record[:,:,-1])

filename = "shape_{0!s}_{1!s}_campers_{2!s}_2_3_step_{3!s}_3.npy".format(height,width,num_campers,num_steps)
filename_hap = "shape_{0!s}_{1!s}_campers_{2!s}_2_3_step_{3!s}_3_happiness.npy".format(height,width,num_campers,num_steps)
np.save(filename, test_model.campground_record)
print(test_model.closest_dist_matrix)
camper_happiness = []
for i in test_model.schedule.agents:
    print("Camper", i.unique_id, ":", i.happiness)
    camper_happiness.append(i.happiness)
np.save(filename_hap,camper_happiness)
fig, ax = plt.subplots()

ims = []
for i in range(num_steps):
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