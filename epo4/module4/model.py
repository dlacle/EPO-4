
speed = []
readings = []
distance = []

with open('data_speed165_break145.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip the header row
    for row in reader:
        speed.append(row[0])
        readings.append(row[1])
        distance.append(row[2])
speed = np.array(speed)
readings = np.array(readings)
print(len(readings))
distance = np.array(distance)

print(speed)
speed=np.array(speed)
print(type(readings))
print(max(readings))
fig = plt.figure()
axis = np.linspace(0, 1, len(readings))
speed_flat = speed.flatten()
# Plot the data
plt.fig(axis, speed, c="blue", marker="", label='speed')
#ax.plot(axis, readings/100, c="red", marker="", label='USR')
#ax.plot(axis, readings/100, c="green", marker="", label='USL')
plt.legend()
plt.show()
