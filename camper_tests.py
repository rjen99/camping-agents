import numpy as np
from model import Camper, Campground
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Set campground info
height = 55
width = 50
num_campers = 200
num_steps = 750

print("--Running Test Code--")

# Create campground and campers
test_model = Campground.Campground(num_campers,height,width, manual=False)

camper_types = np.array([[2,3,6,0.5],[1,2,3,0.5]])
test_model.init_campers(camper_types)

# Run scenario
for i in range(num_steps):
    print("Step", i,"\n--------")
    test_model.step()

# Print last layout
print(test_model.campground_record[:,:,-1])

# Save info for plotting/visualing
filename = "shape_{0!s}_{1!s}_campers_{2!s}_2_3_step_{3!s}_3.npy".format(height,width,num_campers,num_steps)
np.save(filename, test_model.campground_record)

print(test_model.closest_dist_matrix)

filename_hap = "shape_{0!s}_{1!s}_campers_{2!s}_2_3_step_{3!s}_3_happiness.npy".format(height,width,num_campers,num_steps)
camper_happiness = []
camper_1 = []
camper_2 = []
for camper in test_model.schedule.agents:
    if camper.max_tol == 6:
        camper_1.append([camper.unique_id, camper.happiness, camper.time_placed])
    else:
        camper_2.append([camper.unique_id, camper.happiness, camper.time_placed])

    print("Camper", camper.unique_id, ":", camper.happiness)
    camper_happiness.append(camper.happiness)

camper_1 = np.array(camper_1)
camper_2 = np.array(camper_2)

count_1 = len(camper_1)
hap_mean_1 = np.mean(camper_1[:,1])
time_mean_1 = np.mean(camper_1[:,2])

count_2 = len(camper_2)
hap_mean_2 = np.mean(camper_2[:,1])
time_mean_2 = np.mean(camper_2[:,2])

print("Family\n------")
print("Mean Happiness:", hap_mean_1)
print("Mean Time Placed:", time_mean_1)

print("\nTeenagers\n---------")
print("Mean Happiness:", hap_mean_2)
print("Mean Time Placed:", time_mean_2)

np.save(filename_hap,camper_happiness)

# Animate tents being placed
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
