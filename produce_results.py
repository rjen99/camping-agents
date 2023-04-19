import numpy as np
from model import Camper, Campground
import matplotlib.pyplot as plt

def run_scenario(campsite_shape, camper_type_list, num_campers, num_steps, scenario_name="", verbose=False):
    print("--Running Scenario", scenario_name + "--")
    height = campsite_shape[0]
    width = campsite_shape[1]
    # Create campground and campers
    model = Campground.Campground(num_campers, height, width, verbose=verbose)
    model.init_campers(camper_type_list)

    # Run scenario
    for i in range(num_steps):

        print("Step", i, end='\r')
        model.step()
    
    return model

def format_for_save(model):
    campers = []
    for camper in model.schedule.agents:
        if camper.max_tol == 6:
            campers.append([camper.unique_id, 0, camper.happiness, camper.time_placed, camper.tol])
        else:
            campers.append([camper.unique_id, 1, camper.happiness, camper.time_placed, camper.tol])
    return campers

def save_scenario(model, campers, camper_filename, campsite_filename=None):
    # Save info for plotting/visualing
    if campsite_filename is not None:
        np.save(campsite_filename, model.campground_record)

    np.save(camper_filename,campers)

num_campers_50 = np.linspace(50, 400, num=10)
num_campers_100 = np.linspace(190, 1650, num=10)
num_campers_150 = np.linspace(450, 3750, num=10)
num_campers_list = [num_campers_50,num_campers_100,num_campers_150]
sizes = [(50,50),(100,100),(150,150)]

ratios = [0.25,0.5,0.75]
#capacity_list = [50,60,70,80,90,100]
capacity_list = [10,20,30,40,50,60,70,80,90,100]
#capacity_list=[40]
sep_sizes_list = [40,46,48]
seperated_size_ratio_list = [0.5,0.67,0.83]  # account for size difference
size = (50,50)
num_steps = 3330

for i in range(3):
    ratio = ratios[i]
    sep_size_1 = (size[0],sep_sizes_list[i])
    sep_size_2 = (size[0],50-sep_sizes_list[i])
    camper_type_1 = np.array([4,6,6,ratio,1])
    camper_type_2 = np.array([1,2,4,1-ratio,0])
    camper_types = np.array([camper_type_1, camper_type_2])
    camper_type_1[3] = 1
    camper_type_2[3] = 1

    for capacity in capacity_list:
        num_campers = ((capacity/100)*(size[0]*size[1]))/(ratio*24 + (1-ratio)*2)
        #num_steps = int(num_campers*10)

        for i in range(10):
            scenario_name = "- Camper Choice - Capacity {0!s} - Ratio {1!s}:{2!s} - Test {3!s}".format(capacity, int(ratio*100), int((1-ratio)*100), i)
            choice = run_scenario(size, camper_types, num_campers, num_steps, scenario_name)
            campers_choice_curr = format_for_save(choice)
            """im = choice.campground_record[:,:,-1]
            im[np.where(im>=1)] = 1
            plt.imshow(im)
            plt.xlabel("x")
            plt.ylabel("y")
            plt.show()"""
            
            scenario_name = "- Seperated 1 - Capacity {0!s} - Ratio {1!s}:{2!s} - Test {3!s}".format(capacity, int(ratio*100), int((1-ratio)*100), i)
            type_1 = run_scenario(sep_size_1, np.array([camper_type_1]), int(num_campers*ratio), num_steps, scenario_name)
            campers_type_1_curr = format_for_save(type_1)

            scenario_name = "- Seperated 2 - Capacity {0!s} - Ratio {1!s}:{2!s} - Test {3!s}".format(capacity, int(ratio*100), int((1-ratio)*100), i)
            type_2 = run_scenario(sep_size_2, np.array([camper_type_2]), int(num_campers*(1-ratio)), num_steps, scenario_name)
            campers_type_2_curr = format_for_save(type_2)

            if i == 0:
                campers_choice = np.array([campers_choice_curr])
                campers_type_1 = np.array([campers_type_1_curr])
                campers_type_2 = np.array([campers_type_2_curr])
            else:
                campers_choice = np.concatenate((campers_choice,[campers_choice_curr]),axis=0)
                campers_type_1 = np.concatenate((campers_type_1,[campers_type_1_curr]),axis=0)
                campers_type_2 = np.concatenate((campers_type_2,[campers_type_2_curr]),axis=0)
        filename = "same_num_steps/choice_size_50_cap_{0!s}_ratio_{1!s}_{2!s}.npy".format(capacity, int(ratio*100), int((1-ratio)*100))
        save_scenario(choice, campers_choice, filename)
        
        filename = "same_num_steps/seperated_1_size_50_cap_{0!s}_ratio_{1!s}_{2!s}.npy".format(capacity, int(ratio*100), int((1-ratio)*100))
        save_scenario(type_1, campers_type_1, filename)

        filename = "same_num_steps/seperated_2_size_50_cap_{0!s}_ratio_{1!s}_{2!s}.npy".format(capacity, int(ratio*100), int((1-ratio)*100))
        save_scenario(type_2, campers_type_2, filename)
        #print(campers_choice[:,0,:])
        #print(np.shape(campers_choice))

"""camper_types = np.array([[4,6,6,0.25,1],[1,2,4,1-0.25,0]])
scenario_name = "shape_{0!s}_campers_{1!s}_ratio_{2!s}_seperated_type2".format((25,50),167,int(0.25*100))
campers = np.array([camper_types[1,:]])
campers[0,3] = 1
seperated_2 = run_scenario((25,50), campers, int(167*(1-0.25)), int(167*3), scenario_name=scenario_name)
"""
"""
for size_index in range(len(sizes)):
    size = sizes[size_index]
    num_campers = num_campers_list[size_index]
    for ratio_index in range(len(ratios)):
        ratio = ratios[ratio_index]
        camper_types = np.array([[4,6,6,ratio,1],[1,2,4,1-ratio,0]])
        size_1 = (int(size[0]*seperated_size_ratio[ratio_index]), size[1])
        size_2 = (int(size[0]*(1-seperated_size_ratio[ratio_index])), size[1])
        for n in num_campers:
            num_steps = int(n*3)
            n=int(n)

            scenario_name = "shape_{0!s}_campers_{1!s}_ratio_{2!s}_camper_choice".format(size,n,int(ratio*100))
            camper_choice = run_scenario(size, camper_types, n, num_steps, scenario_name=scenario_name)
            filename = "new_data/" + scenario_name + ".npy"
            save_scenario(camper_choice, filename)

            scenario_name = "shape_{0!s}_campers_{1!s}_ratio_{2!s}_seperated_type1".format(size_1,n,int(ratio*100))
            campers = np.array([camper_types[0,:]])
            campers[0,3] = 1
            seperated_1 = run_scenario(size_1, campers, int(n*ratio), num_steps, scenario_name=scenario_name)
            filename = "new_data/" + scenario_name + ".npy"
            save_scenario(seperated_1, filename)
            
            scenario_name = "shape_{0!s}_campers_{1!s}_ratio_{2!s}_seperated_type2".format(size_2,n,int(ratio*100))
            campers = np.array([camper_types[1,:]])
            campers[0,3] = 1
            seperated_2 = run_scenario(size_2, campers, int(n*(1-ratio)), num_steps, scenario_name=scenario_name)
            filename = "new_data/" + scenario_name + ".npy"
            save_scenario(seperated_2, filename)
         
"""

height = 150
width = 150
num_campers = 100
num_steps = 200

"""
for i in range(10):
    scenario_name = "Corner " + str(i)
    model_corner = run_scenario((100,100), camper_types, num_campers, num_steps, scenario_name=scenario_name)
    filename_campsite = "data/shape_100_100_campers_100_corner_campsite_{0!s}.npy".format(i)
    filename_campers = "data/shape_100_100_campers_100_corner_campers_{0!s}.npy".format(i)
    #save_scenario(model_corner, filename_campsite, filename_campers)

    scenario_name = "Side " + str(i)
    model_side = run_scenario((100,100), camper_types, num_campers, num_steps, scenario_name=scenario_name)
    filename_campsite = "data/shape_100_100_campers_100_side_campsite.npy"
    filename_campers = "data/shape_100_100_campers_100_side_campers_{0!s}.npy".format(i)
    #save_scenario(model_side, filename_campsite, filename_campers)

    scenario_name = "Centre " + str(i)
    model_centre = run_scenario((100,100), camper_types, num_campers, num_steps, amenity_loc=(50,50), scenario_name=scenario_name)
    filename_campsite = "data/shape_100_100_campers_100_centre_campsite.npy"
    filename_campers = "data/shape_100_100_campers_100_centre_campers_{0!s}.npy".format(i)
    #save_scenario(model_centre, filename_campsite, filename_campers)
"""