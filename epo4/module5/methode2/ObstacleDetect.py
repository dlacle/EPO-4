
def GetDistance():
    pass

def ObstacleDetect(total_distance, distance_driven):

    dL,dR = GetDistance()

    ObstacleDistance = 70

    # Check if there is an obstacle on the right (dR) or left (dL)
    # If either distance is less than the obstacle distance, consider it an obstacle
    if (dR < ObstacleDistance) or (dL < ObstacleDistance):
        # If there is an obstacle, set Obstacle variable to 1
        obstacle = True

        # If there is an obstacle but the destination is closer, neglect it
        difference = total_distance - distance_driven
        if difference < 60:
            obstacle = False
    else:
        # If no obstacle, set Obstacle variable to 0
        obstacle = False

    # Return the value of the Obstacle variable
    return obstacle