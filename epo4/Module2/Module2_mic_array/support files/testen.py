# import numpy as np
import math
# from scipy import stats
#
# locations = [[1, 2],
#              [2, 2],
#              [3, 2],
#              [4, 2]]
#
# locations_array = np.array(locations)
#
# x_iqr = stats.iqr(locations_array[:, 0])
# y_iqr = stats.iqr(locations_array[:, 1])
#
# x_lower_bound = np.percentile(locations_array[:, 0], 25) - (1.5 * x_iqr)
# x_upper_bound = np.percentile(locations_array[:, 0], 75) + (1.5 * x_iqr)
#
# y_lower_bound = np.percentile(locations_array[:, 1], 25) - (1.5 * y_iqr)
# y_upper_bound = np.percentile(locations_array[:, 1], 75) + (1.5 * y_iqr)
#
# filtered_locations = locations_array[(locations_array[:, 0] >= x_lower_bound) &
#                                      (locations_array[:, 0] <= x_upper_bound) &
#                                      (locations_array[:, 1] >= y_lower_bound) &
#                                      (locations_array[:, 1] <= y_upper_bound)]
#
# average_location = np.mean(filtered_locations, axis=0)
#
# print("Average location (x, y) within IQR range:", average_location)

#absolute error
point1 = (120, 320)
point2 = (163.30619954,301.22708675)

x1, y1 = point1
x2, y2 = point2

absolute_error = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

print("Absolute Error:", absolute_error)