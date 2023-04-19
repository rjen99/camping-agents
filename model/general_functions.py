import numpy as np

def update_closest_dist_matrix(campground, closest_dist_matrix, loc, max_dist=10):
    # get campground sub-matrix (21x21), do the closest dist stuff on it, slot it into the closest_dist_matrix
    height = np.size(campground,0)
    width = np.size(campground,1)
    if loc[0] < max_dist:
        lower_height_bound = 0
    else:
        lower_height_bound = loc[0]-max_dist
    if height-loc[0] < max_dist:
        upper_height_bound = height
    else:
        upper_height_bound = loc[0]+max_dist
    
    if loc[1] < max_dist:
        lower_width_bound = 0
    else:
        lower_width_bound = loc[1]-max_dist
    if width-loc[1] < max_dist:
        upper_width_bound = width
    else:
        upper_width_bound = loc[1]+max_dist
    
    campground_update = campground[lower_height_bound:upper_height_bound+1,lower_width_bound:upper_width_bound+1]
    camper_locations = np.transpose(np.nonzero(campground_update))
    centre_x = int((upper_width_bound-lower_width_bound)/2)
    centre_y = int((upper_height_bound-lower_height_bound)/2)
    #print(campground_update)
    closest_dist_matrix_update = closest_dist_matrix[lower_height_bound:upper_height_bound+1,lower_width_bound:upper_width_bound+1]
    #print(closest_dist_matrix_update)
    for m in range(np.size(campground_update,0)):
        for n in range(np.size(campground_update,1)):
            for location in camper_locations:
                
                # calculate manhattan distance
                distance = abs(m-location[0]) + abs(n-location[1])

                # current camper is closer than previous ones, update the array
                if distance < closest_dist_matrix_update[m,n]:
                    closest_dist_matrix_update[m,n] = distance
            #if campground_update[m,n] != 0:
            #    distance = abs(m-centre_y) + abs(n-centre_x)
            #    
            #    if distance < closest_dist_matrix_update[centre_y,centre_x]:
            #        closest_dist_matrix_update[centre_y,centre_x] = distance
    #print(campground_update)
    #print(closest_dist_matrix_update)
    closest_dist_matrix[lower_height_bound:upper_height_bound+1,lower_width_bound:upper_width_bound+1] = closest_dist_matrix_update
    return closest_dist_matrix

def closest_distance(campground, max_dist=10, dist='manhattan'):
    """
    Create an array of each square's distance from the closest camper. For campers choosing where to go
    Parameters
    ----------
    campground: array of int
                array of camper locations
    max_dist: int
              Maximum distance from nearby tents recorded (e.g. if closest is 15m away, recorded as 10m)
    dist: str
          Euclidian or Manhattan distance
    Outputs
    -------
    closest_dist_matrix: array of float
                         array of each square's distance from the closest camper
    """
    closest_dist_matrix = np.empty_like(campground, dtype=float)
    #camper_locations = np.transpose(np.nonzero(campground))
    height, width = np.shape(closest_dist_matrix)

    for i in range(height):
        for j in range(width):
            closest_dist_matrix[i,j] = max_dist
            if i < max_dist:
                lower_height_bound = 0
            else:
                lower_height_bound = i-max_dist
            if height-i < max_dist:
                upper_height_bound = height
            else:
                upper_height_bound = i+max_dist
            
            if j < max_dist:
                lower_width_bound = 0
            else:
                lower_width_bound = j-max_dist
            if width-j < max_dist:
                upper_width_bound = width
            else:
                upper_width_bound = j+max_dist

            """surrounding = campground[lower_height_bound:upper_height_bound,lower_width_bound:upper_width_bound]
            camper_locations = np.transpose(np.nonzero(surrounding))
            print(camper_locations)
            for location in camper_locations:
                distance = abs(location[0]-i) + abs(location[1]-j)
                
                if distance < closest_dist_matrix[i,j]:
                    closest_dist_matrix[i,j] = distance"""

            for m in range(lower_height_bound,upper_height_bound):
                for n in range(lower_width_bound,upper_width_bound):
                    if campground[m,n] != 0:
                        distance = abs(m-i) + abs(n-j)
                        
                        if distance < closest_dist_matrix[i,j]:
                            closest_dist_matrix[i,j] = distance

    #print(camper_locations)
    """
    for i in range(height):
        for j in range(width):
            closest_dist_matrix[i,j] = np.inf   # set closest to infinity
            
            # find closest camper
            for location in camper_locations:

                if dist == 'euclid':
                    # calculate euclidian distance
                    distance = np.sqrt(np.sum(np.subtract((i,j),location)**2))   
                elif dist == 'manhattan':
                    # calculate manhattan distance
                    distance = np.sum(abs(np.subtract((i,j),location)))
                
                # current camper is closer than previous ones, update the array
                if distance < closest_dist_matrix[i,j]:
                    closest_dist_matrix[i,j] = distance
    """
    return closest_dist_matrix

def find_closest(closest_dist_matrix, amenity_loc=(0,0), tol=3, priority='closest'):
    """
    Find the closest space that meets the camper's tolerated distance
    Parameters
    ----------
    closest_dist_matrix: array of float
                         array of each square's distance from the closest camper
    amenity_loc: tuple/coordinates
                 location of the camper's preferred amenity
    tol: int
         current camper's tolerated distance (doesn't want to camp any closer to another camper)
    priority: str
              whether to order list by 'closest' space or 'largest' space (highest distance from closest tent)
    Output
    ------
    closest: tuple/co-ordinates
             co-ordinates of the closest space that meets the tolerance
    ordered_locations: list of [tuple, int]
                       list of all locations meeting the tolerance and their distance. Ordered by distance
    """
    valid_locations = np.transpose(np.where(closest_dist_matrix>=tol))

    if not np.any(valid_locations):
        return None
    #print(closest_dist_matrix)
    dist_from_amenity = [abs(amenity_loc[0]-loc[0])+abs(amenity_loc[1]-loc[1]) for loc in valid_locations]
    if priority == 'closest':
        ordered_locations = []
        for i in range(len(valid_locations)):
            ordered_locations.append([tuple(valid_locations[i]), dist_from_amenity[i]])
        ordered_locations.sort(key=lambda x:x[1])

    elif priority == 'largest':
        close_index = np.where(np.array(dist_from_amenity)<=10)
        far_index = np.where(np.array(dist_from_amenity)>10)
        #print(far_index)
        ordered_close = []
        ordered_far = []
        for i in close_index[0]:
            ordered_close.append([tuple(valid_locations[i]), closest_dist_matrix[tuple(valid_locations[i])]])
        for i in far_index[0]:
            #print(i)
            ordered_far.append([tuple(valid_locations[i]), closest_dist_matrix[tuple(valid_locations[i])]])
        #print(ordered_far)
        ordered_locations = ordered_close + ordered_far
        # get index for close and far (within 10m for now), order each list by largest, then put together

    # USE FOR CLOSEST
    # ORDER BY, SPLIT INTO 'NEAR' AND 'FAR', THEN ORDER EACH BY DISTANCE FOR LARGEST
    #if priority == 'closest':
    #    order_by_values = np.transpose(np.sum(valid_locations,1))
    #elif priority == 'largest':
    #    order_by_values = [closest_dist_matrix[tuple(i)] for i in valid_locations]

    #ordered_locations = []
    #for i in range(len(valid_locations)):
    #    ordered_locations.append([tuple(valid_locations[i]), order_by_values[i]])
    #ordered_locations.sort(key=lambda x:x[1])
    
    return ordered_locations

def create_tol_neighbourhood(max_tol):
    tol_dict = dict()
    for i in range(2,max_tol+1):
        tol_dict[i]=[]

    upper_left =  [[ 1,0], [0,-1]]
    upper_right = [[ 1,0], [0, 1]]
    lower_left =  [[-1,0], [0,-1]]
    lower_right = [[-1,0], [0, 1]]
    corners = [upper_left, upper_right, lower_left, lower_right]

    old_distance = [[1,0], [0,-1]]
    for k in range(4):
        corner = corners[k]
        old_distance = corners[k]
        for i in range(2,max_tol+1):
            new_dist = []
            for direction in corner:
                for distance in old_distance:
                    new_dist.append(np.add(direction, distance))
            tol_dict[i].append(np.unique(new_dist,axis=0))
            old_distance = new_dist
    
    return tol_dict

def within_bounds(height,width, co_ord):
    if co_ord[0] >= 0 and co_ord[0] < height and co_ord[1] >= 0 and co_ord[1] < width:
        return True
    else:
        return False

"""tents = [[0,0],[0,4],[0,5],[0,10],[0,15],[1,0],[1,4],[1,15],[6,0],[6,4],[6,5],[6,10],[6,15],[7,0],[7,4],[7,15],[15,0],[15,4],[15,5],[15,10],[15,15]]

matrix = np.zeros((16,16))
for i in tents:
    matrix[i[0],i[1]] = 1
close_matrix = closest_distance(matrix, max_dist=5)
print(close_matrix)
print(matrix)

matrix[1,8] = 2
print(update_closest_dist_matrix(matrix,close_matrix,(1,8),5))
print(matrix)"""