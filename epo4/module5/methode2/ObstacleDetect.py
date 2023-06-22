


def GetDistance():
    distance = []
    for i in range(5):  # doing 20 measurements
        time.sleep(0.5)  # wait 0.2 second per measurement
        status = kitt.get_status("dist")
        distance.append(status)
    print(distance)


def ObstacleDetect(x0,x1):
    status = kitt.get_status("dist")

    dL = status[0]
    dR = status[1]

    ObstacleDistance = 70

    # Check if there is an obstacle on the right (dR) or left (dL)
    # If either distance is less than the obstacle distance, consider it an obstacle
    if (dR < ObstacleDistance) or (dL < ObstacleDistance):
        # If there is an obstacle, set Obstacle variable to 1
        obstacle = True

        # If there is an obstacle but the destination is closer, neglect it
        distance_point = np.sqrt((x0[0]-x1[1])**2 + (x1[0]-x1[1])**2)
        if distance_point < ObstacleDistance:
            obstacle = False
    else:
        # If no obstacle, set Obstacle variable to 0
        obstacle = False

    # Return the value of the Obstacle variable
    return obstacle
# kitt = KITT('com5')
#
# GetDistance()
#
# del kitt # disconnect from kitt
