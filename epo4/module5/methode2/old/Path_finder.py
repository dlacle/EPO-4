import math

initial_orientation = 90 # with respect to x as
start_posx = 2
start_posy = 2
end_posx = 4
end_posy = 4
max_forward_radius = 1.5
max_backwards_radius = 1

x_center = start_posx + max_forward_radius*math.cos(math.radians(initial_orientation-90))
y_center = start_posy + max_forward_radius*math.sin(math.radians(initial_orientation-90))

displacement_vector = math.sqrt((x_center-end_posx)**2+(y_center-end_posy)**2)
l_straight_line = math.sqrt(displacement_vector**2-max_forward_radius**2)




