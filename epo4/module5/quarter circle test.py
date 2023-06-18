import numpy as np

new_or = 180
phase_v = 20

quarter_circle_count = 0  # Initialize the quarter circle counter
alpha = 0

while abs(phase_v - new_or) > 90:
    alpha += np.deg2rad(90)
    new_or -= np.rad2deg(alpha)
    quarter_circle_count += 1  # Increment the quarter circle counter

print("new_or",new_or)
print("Quarter circle turns performed:", quarter_circle_count)
print("Performing a regular turn.")