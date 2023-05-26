import numpy as np

x0 = np.array([int(input('x: ')), int(input('y: '))])
a = int(input('a: '))
d0 = np.array([np.cos(a), np.sin(a)])
v = int(input('v: '))
L = 0.335
Theta = 0
phi = int(input('steering angle phi: '))
v1 = (v/100)*np.cos(phi)
print('v1: ', v1)
R = int(input('estimation of R: '))
drive_time = int(input('drive_time: '))

delta_Theta = v1*np.sin(phi)/L
Theta = Theta + delta_Theta * drive_time
d1 = np.array([np.cos(a-Theta), np.sin(a+Theta)])
x1 = np.array([R*(np.sin(a)*np.cos(Theta)+np.sin(Theta)*np.cos(a)), R*(np.cos(a)*(1-np.cos(Theta))+np.sin(a)*np.cos(Theta))])
print('new orientation: ', d1)
print('new location: ', x1)
