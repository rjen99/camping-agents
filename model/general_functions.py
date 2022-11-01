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
    """
    valid_locations = np.transpose(np.where(closest_dist_matrix>=tol))
    if not np.any(valid_locations):
        return None
    #print(closest_dist_matrix)
    #print(valid_locations)
    location_dist = np.sum(valid_locations,1)
    closest = valid_locations[np.where(location_dist==np.min(location_dist))][0]
    return tuple(closest)