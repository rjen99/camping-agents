import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

filename = "shape_50_50_campers_100_2_3_step_500.npy"
campground_record = np.load(filename)
height = int(filename[6:8])
width = int(filename[9:11])

num_campers = int(filename[20:23])
num_steps = int(filename[-7:-4])

fig, ax = plt.subplots()

ims = []
for i in range(num_steps):
    curr_im = campground_record[:,:,i]
    curr_im[np.where(curr_im>=1)] = 1
    im = ax.imshow(curr_im, animated=True)
    if i == 0:
        ax.imshow(campground_record[:,:,i])  # show an initial one first
    ims.append([im])

ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=1000)
plt.show()