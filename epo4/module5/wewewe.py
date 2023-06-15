import numpy as np
# def relative_loc(x0, x1, orientation):
#     dx_vector = np.array([x1[0] - x0[0], x1[1] - x0[1]])  # distance/direction vector between location 0 and 1
#     dx = np.sqrt(pow(dx_vector[0], 2) + pow(dx_vector[1], 2))  # distance to location 1
#     dx_angle = beta(x0[0], x0[1], x1[0], x1[1])  # angle between dx_vector and positive x-axis
#     print('dx_vector', dx_angle)
#     omega = dx_angle - orientation  # angle between dx_vector and alpha
#     print('omega',omega)
#
#     omega = call_angle(omega)
#     return dx, omega
#
# def beta(x0, y0, x1, y1):
#     dx = np.array([x1 - x0, y1 - y0])  # distance/direction vector between location 0 and 1
#     dx_angle = np.arctan2(dx[1] , dx[0])  # angle of dx vector with positive x-axis (requested direction)
#     print('dx_vector beta function', dx_angle)
#     dx_angle = call_angle(dx_angle)
#     return dx_angle
#
#
# # set angle in range -pi to pi
# def call_angle(angle):
#     angle = angle % (2*np.pi)
#     print('angle afer mapping call_angle', angle)
#     if angle > np.pi:
#         angle = angle - 2*np.pi
#         print('angle afer mapping angle> pi call_angle', angle)
#     return angle
#
# x0 = np.array([int(100) / 100, int(100) / 100])  # [x0,y0] starting location
# print('x0:',x0)
# orientation = np.radians(int(225))  # starting orientation angle with x-axis
# print('orient rad:',orientation)
# orientation = orientation % (2*np.pi)
# print('orient rad:',orientation)
# d0 = np.array([np.cos(orientation), np.sin(orientation)])  # starting orientation vector
# x1 = np.array([int(300) / 100, int(300) / 100])  # [x1, y1] end location
#
# relative location of  car and end-location x1
orientation = np.radians(int(0))  # starting orientation angle with x-axis
print('orient rad:',orientation)
orientation = orientation % (2*np.pi)
print('orient rad:',orientation)

orientation = orientation + np.pi  # orientation for backwards driving
orientation = orientation % (2 * np.pi)
print(orientation)