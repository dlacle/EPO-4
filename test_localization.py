import numpy as np

def difference_to_location_xy(diff_peak, mic_positions_xy, Fs,Vsound):#Algorith neglect height
    # diff_to_distance = [x * Vsound/ Fs for x in diff_peak]
    diff_to_distance = diff_peak

    # Ensure range_diff and receiver_positions have the correct dimensions
    assert len(diff_to_distance) == 10, "Invalid range difference input"
    assert mic_positions_xy.shape == (5, 2), "Invalid receiver positions input"

    x1, y1 = mic_positions_xy[0]
    x2, y2 = mic_positions_xy[1]
    x3, y3 = mic_positions_xy[2]
    x4, y4 = mic_positions_xy[3]
    x5, y5 = mic_positions_xy[4]

    #define r_ij (Range difference)
    r12 = diff_to_distance[0]
    r13 = diff_to_distance[1]
    r14 = diff_to_distance[2]
    r15 = diff_to_distance[3]
    r23 = diff_to_distance[4]
    r24 = diff_to_distance[5]
    r25 = diff_to_distance[6]
    r34 = diff_to_distance[7]
    r35 = diff_to_distance[8]
    r45 = diff_to_distance[9]

    # define matrix A
    A = np.array([
        [2 * (x2 - x1), 2 * (y2 - y1), -2 * r12, 0, 0, 0],
        [2 * (x3 - x1), 2 * (y3 - y1), 0, -2 * r13, 0, 0],
        [2 * (x4 - x1), 2 * (y4 - y1), 0, 0, -2 * r14, 0],
        [2 * (x5 - x1), 2 * (y5 - y1), 0, 0, 0, -2 * r15],
        [2 * (x3 - x2), 2 * (y3 - y2), 0, -2 * r23, 0, 0],
        [2 * (x4 - x2), 2 * (y4 - y2), 0, 0, -2 * r24, 0],
        [2 * (x5 - x2), 2 * (y5 - y2), 0, 0, 0, -2 * r25],
        [2 * (x4 - x3), 2 * (y4 - y3), 0, 0, -2 * r34, 0],
        [2 * (x5 - x3), 2 * (y5 - y3), 0, 0, 0, -2 * r35],
        [2 * (x5 - x4), 2 * (y5 - y4), 0, 0, 0, -2 * r45]
    ])

    # magnitude / length
    l1 = np.linalg.norm(mic_positions_xy[0])
    l2 = np.linalg.norm(mic_positions_xy[1])
    l3 = np.linalg.norm(mic_positions_xy[2])
    l4 = np.linalg.norm(mic_positions_xy[3])
    l5 = np.linalg.norm(mic_positions_xy[4])

    #define matrix B
    B = np.array([
        [r12**2-l1**2+l2**2],
        [r13**2-l1**2+l3**2],
        [r14**2-l1**2+l4**2],
        [r15**2-l1**2+l5**2],
        [r23**2-l2**2+l3**2],
        [r24**2-l2**2+l4**2],
        [r25**2-l2**2+l5**2],
        [r34**2-l3**2+l4**2],
        [r35**2-l3**2+l5**2],
        [r45**2-l4**2+l5**2]
    ])

    # A*y=B solving for y:
    y = np.matmul(np.linalg.pinv(A),B)
    location = y[:2]
    return location

def difference_to_location_xyz(diff_peak, mic_positions_xyz, Fs,Vsound):
    # diff_to_distance = [x * Vsound / Fs for x in diff_peak]
    diff_to_distance = diff_peak
    # Ensure range_diff and receiver_positions have the correct dimensions
    assert len(diff_to_distance) == 10, "Invalid range difference input"
    assert mic_positions_xyz.shape == (5, 3), "Invalid receiver positions input"

    # # #
    # x1, y1, z1 = mic_positions_xyz[0]
    # x2, y2, z2 = mic_positions_xyz[1]
    # x3, y3, z3 = mic_positions_xyz[2]
    # x4, y4, z4 = mic_positions_xyz[3]
    # x5, y5, z5 = mic_positions_xyz[4]
    #
    # # define r_ij (Range difference)
    # r12 = diff_to_distance[0]
    # r13 = diff_to_distance[1]
    # r14 = diff_to_distance[2]
    # r15 = diff_to_distance[3]
    # r23 = diff_to_distance[4]
    # r24 = diff_to_distance[5]
    # r25 = diff_to_distance[6]
    # r34 = diff_to_distance[7]
    # r35 = diff_to_distance[8]
    # r45 = diff_to_distance[9]
    #
    # # define matrix A
    # A = np.array([
    #     [2 * (x2 - x1),2 * (y2 - y1),2 * (z2 - z1), 2 * r12],
    #     [2 * (x3 - x1),2 * (y3 - y1),2 * (z3 - z1), 2 * r13],
    #     [2 * (x4 - x1),2 * (y4 - y1),2 * (z4 - z1), 2 * r14],
    #     [2 * (x5 - x1),2 * (y5 - y1),2 * (z5 - z1), 2 * r15]
    # ])
    #
    # # magnitude / length
    # l1 = np.linalg.norm(mic_positions_xyz[0])
    # l2 = np.linalg.norm(mic_positions_xyz[1])
    # l3 = np.linalg.norm(mic_positions_xyz[2])
    # l4 = np.linalg.norm(mic_positions_xyz[3])
    # l5 = np.linalg.norm(mic_positions_xyz[4])
    #
    # # define matrix B
    # B = np.array([
    #     [-r12**2 + (x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2],
    #     [-r13**2 + (x3 - x1)**2 + (y3 - y1)**2 + (z3 - z1)**2],
    #     [-r14**2 + (x4 - x1)**2 + (y4 - y1)**2 + (z4 - z1)**2],
    #     [-r15**2 + (x5 - x1)**2 + (y5 - y1)**2 + (z5 - z1)**2]
    #
    # ])
    #
    # # A*y=B solving for y:
    # y = np.linalg.pinv(A)*B
    # location = y
    # return location

    x1, y1, z1 = mic_positions_xyz[0]
    x2, y2, z2 = mic_positions_xyz[1]
    x3, y3, z3 = mic_positions_xyz[2]
    x4, y4, z4 = mic_positions_xyz[3]
    x5, y5, z5 = mic_positions_xyz[4]

    # define r_ij (Range difference)
    r12 = diff_to_distance[0]
    r13 = diff_to_distance[1]
    r14 = diff_to_distance[2]
    r15 = diff_to_distance[3]
    r23 = diff_to_distance[4]
    r24 = diff_to_distance[5]
    r25 = diff_to_distance[6]
    r34 = diff_to_distance[7]
    r35 = diff_to_distance[8]
    r45 = diff_to_distance[9]

    # define matrix A
    A = np.array([
        [2 * (x2 - x1), 2 * (y2 - y1), 2 * (z2 - z1), -2 * r12, 0, 0, 0],
        [2 * (x3 - x1), 2 * (y3 - y1), 2 * (z3 - z1), 0, -2 * r13, 0, 0],
        [2 * (x4 - x1), 2 * (y4 - y1), 2 * (z4 - z1), 0, 0, -2 * r14, 0],
        [2 * (x5 - x1), 2 * (y5 - y1), 2 * (z5 - z1), 0, 0, 0, -2 * r15],
        [2 * (x3 - x2), 2 * (y3 - y2), 2 * (z3 - z2), 0, -2 * r23, 0, 0],
        [2 * (x4 - x2), 2 * (y4 - y2), 2 * (z4 - z2), 0, 0, -2 * r24, 0],
        [2 * (x5 - x2), 2 * (y5 - y2), 2 * (z5 - z2), 0, 0, 0, -2 * r25],
        [2 * (x4 - x3), 2 * (y4 - y3), 2 * (z4 - z3), 0, 0, -2 * r34, 0],
        [2 * (x5 - x3), 2 * (y5 - y3), 2 * (z5 - z3), 0, 0, 0, -2 * r35],
        [2 * (x5 - x4), 2 * (y5 - y4), 2 * (z5 - z4), 0, 0, 0, -2 * r45]
    ])

    # magnitude / length
    l1 = np.linalg.norm(mic_positions_xyz[0])
    l2 = np.linalg.norm(mic_positions_xyz[1])
    l3 = np.linalg.norm(mic_positions_xyz[2])
    l4 = np.linalg.norm(mic_positions_xyz[3])
    l5 = np.linalg.norm(mic_positions_xyz[4])

    # define matrix B
    B = np.array([
        [(r12 ** 2) - (l1 ** 2) + (l2 ** 2)],
        [(r13 ** 2) - (l1 ** 2) + (l3 ** 2)],
        [(r14 ** 2) - (l1 ** 2) + (l4 ** 2)],
        [(r15 ** 2) - (l1 ** 2) + (l5 ** 2)],
        [(r23 ** 2) - (l2 ** 2) + (l3 ** 2)],
        [(r24 ** 2) - (l2 ** 2) + (l4 ** 2)],
        [(r25 ** 2) - (l2 ** 2) + (l5 ** 2)],
        [(r34 ** 2) - (l3 ** 2) + (l4 ** 2)],
        [(r35 ** 2) - (l3 ** 2) + (l5 ** 2)],
        [(r45 ** 2) - (l4 ** 2) + (l5 ** 2)]
    ])

    # A*y=B solving for y:
    y = np.matmul(np.linalg.pinv(A),B)
    location = y[:3]
    return location
'''''''''''''''''''''''''''''
extended iriterative version of the manual
'''''''''''''''''''''''''''''
    # #Localisation algorithm
    # b = np.zeros(10)
    # A = np.zeros([10,7])
    # r = 0
    #
    # for i in range(5):
    #     for j in range(i+1,5):
    #         A[r, 0] = 2*(mic_positions_xyz[j,0] - mic_positions_xyz[i,0]).T
    #         A[r, 1] = 2*(mic_positions_xyz[j,1] - mic_positions_xyz[i,1]).T
    #         A[r, 2] = 2 * (mic_positions_xyz[j, 2] - mic_positions_xyz[i, 2]).T
    #         A[r , j + 2 ] = -(2 * diff_to_distance[i]) #abs?
    #         r += 1
    #
    # r = 0
    # for i in range(5):
    #     for j in range(i + 1, 5):
    #         diff_to_distance[i, j] < 5:
    #         b[k] = (diff_to_distance[i] ** 2 - np.norm(mic_positions_xyz[i]) ** 2 + np.norm(mic_positions_xyz[j]) ** 2)
    #         elif distmat[i, j] > 5:
    #             b[k] = (distmat[j, i] ** 2 - norm(micloc[i]) ** 2 + norm(micloc[j]) ** 2)
    #         k += 1

'''''''''''''''''''''''''''''
hh
'''''''''''''''''''''''''''''
    # N = len(mic_positions)  # Number of microphones
    #
    # # Compute pairwise range differences
    # r_ij = np.zeros((N, N))
    # for i in range(N):
    #     for j in range(i + 1, N):
    #         r_ij[i, j] = diff_peak[i * (N - 1) - (i * (i - 1) // 2) + (j - i - 1)]
    #         r_ij[j, i] = -r_ij[i, j]
    #
    # # Compute matrix A and vector b
    # A = np.zeros((N * (N - 1) // 2, N + 1))
    # b = np.zeros((N * (N - 1) // 2,))
    # row = 0
    # for i in range(N):
    #     for j in range(i + 1, N):
    #         A[row, :2] = 2 * (mic_positions[j, :] - mic_positions[i, :])
    #         A[row, -1] = -2 * r_ij[i, j]
    #         b[row] = r_ij[i, j] ** 2 - np.linalg.norm(mic_positions[i, :]) ** 2 + np.linalg.norm(
    #             mic_positions[j, :]) ** 2
    #         row += 1
    #
    # # Compute pseudoinverse of A and solve for unknowns
    # A_inv = np.linalg.pinv(A)
    # solution = np.dot(A_inv, b)
    # car_location = solution[:2]  # (x, y) location of the car
    # d = solution[2:]  # Nuisance parameters (distances)
    #
    # # Compute z-coordinate (assuming car is always at z = 0)
    # z = np.zeros_like(car_location[0])

    # return np.array([car_location[0], car_location[1], z])
    # diff_to_distance = [x * Vsound/Fs for x in diff_peak]
    #
    # # TDOA measurements
    # rij = np.array(diff_to_distance)
    # xi = mic_positions
    #
    # # Constructing the coefficient matrix A
    # A = np.zeros((10, 5))
    # for i in range(4):
    #     A[i, :3] = 2 * (xi[i + 1] - xi[0])
    #     A[i, 3] = -2 * rij[i]
    #
    # for i in range(3):
    #     A[i + 4, :3] = 2 * (xi[i + 2] - xi[i + 1])
    #     A[i + 4, 3] = -2 * rij[i + 4]
    #
    # for i in range(2):
    #     A[i + 7, :3] = 2 * (xi[i + 3] - xi[i + 1])
    #     A[i + 7, 3] = -2 * rij[i + 7]
    #
    # A[9, :3] = 2 * (xi[4] - xi[3])
    # A[9, 4] = -2 * rij[9]
    #
    # # Constructing the known vector b
    # b = np.zeros(10)
    # for i in range(4):
    #     b[i] = np.linalg.norm(xi[0]) ** 2 - np.linalg.norm(xi[i + 1]) ** 2 + rij[i] ** 2
    #
    # for i in range(3):
    #     b[i + 4] = np.linalg.norm(xi[i + 1]) ** 2 - np.linalg.norm(xi[i + 2]) ** 2 + rij[i + 4] ** 2
    #
    # for i in range(2):
    #     b[i + 7] = np.linalg.norm(xi[i + 1]) ** 2 - np.linalg.norm(xi[i + 3]) ** 2 + rij[i + 7] ** 2
    #
    # b[9] = np.linalg.norm(xi[3]) ** 2 - np.linalg.norm(xi[4]) ** 2 + rij[9] ** 2
    #
    # # Computing the pseudo-inverse of A
    # A_pseudo_inv = np.linalg.pinv(A)
    #
    # # Solving for the unknown vector y
    # y = np.dot(A_pseudo_inv, b)
    #
    # # Extracting the car's location x and nuisance parameters d2, d3, d4, d5
    # location = y[:3]
    # # d2, d3, d4, d5 = y[3:]
    #
    # # Printing the results
    # # print("Car Location (x, y, z):", location)
    # # print("Nuisance Parameters (d2, d3, d4, d5):", d2, d3, d4, d5)
    # return location

# def Average_location(x,y,n_locations = 1):

mic_positions_xy = np.array(
        [
            [0, 480],  # mic 1 (bottom left corner)
            [480, 480],  # mic 2 (top left corner)
            [480, 0],  # mic 3 (top right corner)
            [0, 0], # mic 4 (bottom right corner)
            [0, 240]  # mic 5 (side)
        ]
    )

mic_positions_xyz = np.array(
    [
        [0, 480, 50],  # mic 1 (bottom left corner)
        [480, 480, 50],  # mic 2 (top left corner)
        [480, 0, 50],  # mic 3 (top right corner)
        [0, 0, 50],  # mic 4 (bottom right corner)
        [0, 240, 80]  # mic 5 (side)
    ]
)


def test_localization_xy(kitt_test_location_xy):
    '''
        Generate a TDOA distance matrix based on a known location (x,y) of the KITT car (specifically the beacon)
        Used to test localization algorithm on known locations
    '''
    # If an incorrect number dimensions was given, give an error
    if len(kitt_test_location_xy) != 2: raise ValueError("Give an appropriate number of dimensions")
    # A list of known microphone coordinates
    mic_positions_xy = np.array(
        [
            [0, 480],  # mic 1 (bottom left corner)
            [480, 480],  # mic 2 (top left corner)
            [480, 0],  # mic 3 (top right corner)
            [0, 0], # mic 4 (bottom right corner)
            [0, 240]  # mic 5 (side)
        ]
    )
    range_diff = []
    for i in range(4):
        for j in range(i + 1, 5):
            # Using the known coordinates, use the Pythagorean theorem to determine the distance between KITT
            # and each microphone
            disti = np.sqrt(np.sum((mic_positions_xy[i] - kitt_test_location_xy) ** 2))
            distj = np.sqrt(np.sum((mic_positions_xy[j] - kitt_test_location_xy) ** 2))
            range_diff.append(distj - disti)
    print(range_diff)
    '''
       range diff matrix
       '''
    # # Container to generate TDOA distance matrix
    # dist = np.zeros([5, 5])
    #
    # range_diff = []
    # for i in range(5):
    #     for j in range(5):
    #         # Using the known coordinates, use the pythagorean theorem to determine the distance between KITT
    #         # and each microphone
    #         disti = np.sqrt(np.sum((mic_positions_xy[i] - kitt_test_location_xy) ** 2))
    #         distj = np.sqrt(np.sum((mic_positions_xy[j] - kitt_test_location_xy) ** 2))
    #         dist[i, j] = distj - disti  #range difference
    #         range_diff.append(dist[i, j])
    #
    # print(range_diff)
    return range_diff

# print(test_localization_xy([80,400]))#[240,240],80,400],[240,120]
def test_localization_xyz(kitt_test_location_xyz):
    '''
        Generate a TDOA distance matrix based on a known location (x,y,z) of the KITT car (specifically the beacon)
        Used to test localization algorithm on known locations
    '''
    # If a 2D coordinate is given, add a z coordinate (26cm)
    if len(kitt_test_location_xyz) == 2: kitt_test_location_xyz.append(0.26)
    # If an incorrect number dimensions was given, give an error
    if len(kitt_test_location_xyz) != 3: raise ValueError("Give an appropriate number of dimensions")
    # A list of known microphone coordinates
    mic_positions_xyz = np.array(
        [
            [0, 480, 50],  # mic 1 (bottom left corner)
            [480, 480, 50],  # mic 2 (top left corner)
            [480, 0, 50],  # mic 3 (top right corner)
            [0, 0, 50],  # mic 4 (bottom right corner)
            [0, 240, 80]  # mic 5 (side)
        ]
    )

    range_diff = []
    for i in range(4):
        for j in range(i + 1, 5):
            # Using the known coordinates, use the Pythagorean theorem to determine the distance between KITT
            # and each microphone
            disti = np.sqrt(np.sum((mic_positions_xyz[i] - kitt_test_location_xyz) ** 2))
            distj = np.sqrt(np.sum((mic_positions_xyz[j] - kitt_test_location_xyz) ** 2))
            range_diff.append(distj - disti)
    '''
    range diff matrix
    '''
    # # Container to generate TDOA distance matrix
    # dist = np.zeros([5, 5])

    # range_diff = []
    # for i in range(5):
    #     for j in range(5):
    #         # Using the known coordinates, use the pythagorean theorem to determine the distance between KITT
    #         # and each microphone
    #         disti = np.sqrt(np.sum((mic_positions_xyz[i] - kitt_test_location_xyz) ** 2))
    #         distj = np.sqrt(np.sum((mic_positions_xyz[j] - kitt_test_location_xyz) ** 2))
    #         dist[i, j] = distj - disti  #range difference
    #         range_diff.append(dist[i, j])
    #
    # print(range_diff)
    return range_diff

# print(test_localization_xyz([240,240]))#[240,240],[80,400],[240,120]

'''
Test localization 
'''
location = [240,120]
diff = [12, 230, 218, 224, 218, 206, 212, -12, -6, 6]
diff = [x * 343.14/ 48000 for x in diff] #240x120
#xy
print('generated rangediff:',difference_to_location_xy(test_localization_xy(location),mic_positions_xy,48000,343.14))
print('real range diff:',difference_to_location_xy(diff,mic_positions_xy,48000,343.14))
#xyz
print('generated rangediff:',difference_to_location_xyz(test_localization_xyz(location),mic_positions_xyz,48000,343.14))
print('real range diff:',difference_to_location_xyz(diff,mic_positions_xyz,48000,343.14))