import numpy as np
import matplotlib.pyplot as plt

filename = "shape_55_50_campers_238_2_3_step_750_happiness.npy"
happiness_6 = np.load(filename)
filename = "shape_55_50_campers_238_2_3_step_750_4_happiness.npy"
happiness_4 = np.load(filename)
filename = "shape_55_50_campers_238_2_3_step_750_3_happiness.npy"
happiness_3 = np.load(filename)

print(happiness_4)
avg_happiness_3 = np.mean(happiness_3-3)
avg_happiness_4 = np.mean(happiness_4-2)
avg_happiness_6 = np.mean(happiness_6)

#plt.plot([3,4,6],[avg_happiness_3,avg_happiness_4,avg_happiness_6])
#plt.xlabel("Tolerance")
#plt.ylabel("Mean happiness")
hist_bins = [-12,-10,-8,-6,-4,-2,0,2,4,6,8,10]

#fig,ax = plt.subplots(1,3)
#ax[0].hist(happiness_3-3, bins=hist_bins)
#ax[1].hist(happiness_4-2, bins=hist_bins)
#ax[2].hist(happiness_6, bins=hist_bins)
plt.hist([happiness_3-3,happiness_4-2,happiness_6], bins=hist_bins)
plt.legend(["Tolerance=3","Tolerance=4","Tolerance=6"])
plt.xlabel("Happiness value")
plt.ylabel("Number of campers")
plt.show()