import numpy as np

def closest_distance(campground, dist='manhattan'):
    """
    Create an array of each square's distance from the closest camper. For campers choosing where to go
    Parameters
    ----------
    campground: array of int
                array of camper locations
    dist: str
          Euclidian or Manhattan distance
    Outputs
    -------
    closest_dist_matrix: array of float
                         array of each square's distance from the closest camper
    """
    closest_dist_matrix = np.empty_like(campground, dtype=float)
    camper_locations = np.transpose(np.nonzero(campground))
    height, width = np.shape(closest_dist_matrix)
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
    
    return closest_dist_matrix

def find_closest(closest_dist_matrix, tol=3):
    """
    Find the closest space that meets the camper's tolerated distance
    Parameters
    ----------
    closest_dist_matrix: array of float
                         array of each square's distance from the closest camper
    tol: int
         current camper's tolerated distance (doesn't want to camp any closer to another camper)
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
    
    location_dist = np.transpose(np.sum(valid_locations,1))

    ordered_locations = []
    for i in range(len(valid_locations)):
        ordered_locations.append([tuple(valid_locations[i]), location_dist[i]])
    ordered_locations.sort(key=lambda x:x[1])
    
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