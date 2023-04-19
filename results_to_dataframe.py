import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import pandas as pd

ratios = [0.25,0.5,0.75]
capacity_list = [10,20,30,40,50,60,70,80,90,100]
size = (50,50)
ratio = 0.25

capacity_all = []
ratio_list = []
type_list = []
tol_list = []
happiness_list = []
time_placed_list = []
method_list = []
run_id_list = []

for ratio in ratios:
    ratio_str = str(int(ratio*100)) + ":" + str(int((1-ratio)*100))
    print(ratio_str)
    for capacity in capacity_list:
        print(capacity)
        num_campers = int(((capacity/100)*(size[0]*size[1]))/(ratio*24 + (1-ratio)*2))

        filename = "yet_more_data/choice_size_50_cap_{0!s}_ratio_{1!s}_{2!s}.npy".format(capacity, int(ratio*100), int((1-ratio)*100))
        campers = np.load(filename)

        for i in range(10):
            
            #type_list = np.concatenate((type_list,campers[i,:,1]))
            tol_list = np.concatenate((tol_list,campers[i,:,4]))
            happiness_list = np.concatenate((happiness_list,campers[i,:,2]))
            time_placed_list = np.concatenate((time_placed_list,campers[i,:,3]))

            for j in campers[i,:,:]:
                run_id_list = np.concatenate((run_id_list,[i]))
                capacity_all = np.concatenate((capacity_all,[capacity]))
                ratio_list = np.concatenate((ratio_list,[ratio_str]))
                method_list = np.concatenate((method_list,["choice"]))
                if j[1] == 0:
                    type_list = np.concatenate((type_list,["family"]))
                elif j[1] == 1:
                    type_list = np.concatenate((type_list,["single person"]))
        
    for capacity in capacity_list:
        print(capacity)
        num_campers = int(((capacity/100)*(size[0]*size[1]))/(ratio*24 + (1-ratio)*2))

        filename = "yet_more_data/seperated_1_size_50_cap_{0!s}_ratio_{1!s}_{2!s}.npy".format(capacity, int(ratio*100), int((1-ratio)*100))
        campers = np.load(filename)

        for i in range(10):
            
            #type_list = np.concatenate((type_list,campers[i,:,1]))
            tol_list = np.concatenate((tol_list,campers[i,:,4]))
            happiness_list = np.concatenate((happiness_list,campers[i,:,2]))
            time_placed_list = np.concatenate((time_placed_list,campers[i,:,3]))

            for j in campers[i,:,:]:
                run_id_list = np.concatenate((run_id_list,[i]))
                capacity_all = np.concatenate((capacity_all,[capacity]))
                ratio_str = str(int(ratio*100)) + ":" + str(int((1-ratio)*100))
                ratio_list = np.concatenate((ratio_list,[ratio_str]))
                method_list = np.concatenate((method_list,["segregated"]))
                if j[1] == 0:
                    type_list = np.concatenate((type_list,["family"]))
                elif j[1] == 1:
                    type_list = np.concatenate((type_list,["single person"]))

    for capacity in capacity_list:
        print(capacity)
        num_campers = int(((capacity/100)*(size[0]*size[1]))/(ratio*24 + (1-ratio)*2))

        filename = "yet_more_data/seperated_2_size_50_cap_{0!s}_ratio_{1!s}_{2!s}.npy".format(capacity, int(ratio*100), int((1-ratio)*100))
        campers = np.load(filename)

        for i in range(10):
            
            #type_list = np.concatenate((type_list,campers[i,:,1]))
            tol_list = np.concatenate((tol_list,campers[i,:,4]))
            happiness_list = np.concatenate((happiness_list,campers[i,:,2]))
            time_placed_list = np.concatenate((time_placed_list,campers[i,:,3]))

            for j in campers[i,:,:]:
                run_id_list = np.concatenate((run_id_list,[i]))
                capacity_all = np.concatenate((capacity_all,[capacity]))
                ratio_str = str(int(ratio*100)) + ":" + str(int((1-ratio)*100))
                ratio_list = np.concatenate((ratio_list,[ratio_str]))
                method_list = np.concatenate((method_list,["segregated"]))
                if j[1] == 0:
                    type_list = np.concatenate((type_list,["family"]))
                elif j[1] == 1:
                    type_list = np.concatenate((type_list,["single person"]))



print(np.shape(np.array(type_list)),np.shape(tol_list),np.shape(happiness_list),np.shape(time_placed_list),np.shape(capacity_all))#,np.shape(c_type_placed),np.shape(c_type_placed2))

results = pd.DataFrame({"capacity":capacity_all, "ratio":ratio_list, "method":method_list, "type": type_list, "run_id": run_id_list,"happiness":happiness_list,"tol":tol_list,"time":time_placed_list})
results.to_csv("new_results_all.csv")

print(results)

plt.figure()
sns.lineplot(data=results, x="capacity", y="happiness", hue="type", style="method")
plt.figure()
sns.lineplot(data=results, x="capacity", y="tol", hue="type", style="method")
plt.figure()
sns.lineplot(data=results, x="capacity", y="time", hue="type", style="method")
plt.show()