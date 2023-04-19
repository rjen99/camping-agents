import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

filename = "data/shape_50_50_campers_100_centre_campsite.npy"
campground_record = np.load(filename)
height = 50
width = 50

num_campers = 100
num_steps = 200

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