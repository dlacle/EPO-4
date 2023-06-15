import numpy as np
import math


def difference_to_location_xy(r_ij_vec, mic_positions, Fs, Vsound):

    # Ensure r_ij and receiver_positions have the correct dimensions
    # assert len(r_ij_vec) == 10, "Invalid range difference input"
    # assert mic_positions.shape == (5, 2), "Invalid receiver positions input"

    x1, y1 = mic_positions[0]
    x2, y2 = mic_positions[1]
    x3, y3 = mic_positions[2]
    x4, y4 = mic_positions[3]

    # define r_ij (Range difference)
    r12 = r_ij_vec[0]
    r13 = r_ij_vec[1]
    r14 = r_ij_vec[2]
    r23 = r_ij_vec[3]
    r24 = r_ij_vec[4]
    r34 = r_ij_vec[5]

    # define matrix A
    A = np.array([
        [2 * (x2 - x1), 2 * (y2 - y1), -2 * r12, 0, 0],
        [2 * (x3 - x1), 2 * (y3 - y1), 0, -2 * r13, 0],
        [2 * (x4 - x1), 2 * (y4 - y1), 0, 0, -2 * r14],
        [2 * (x3 - x2), 2 * (y3 - y2), 0, -2 * r23, 0],
        [2 * (x4 - x2), 2 * (y4 - y2), 0, 0, -2 * r24],
        [2 * (x4 - x3), 2 * (y4 - y3), 0, 0, -2 * r34],
    ])

    # magnitude / length
    l1 = np.linalg.norm(mic_positions[0])
    l2 = np.linalg.norm(mic_positions[1])
    l3 = np.linalg.norm(mic_positions[2])
    l4 = np.linalg.norm(mic_positions[3])

    # define matrix B
    B = np.array([
        [r12**2 - l1**2 + l2**2],
        [r13**2 - l1**2 + l3**2],
        [r14**2 - l1**2 + l4**2],
        [r23**2 - l2**2 + l3**2],
        [r24**2 - l2**2 + l4**2],
        [r34**2 - l3**2 + l4**2],
    ])
    A[A == 0] = 1e-12

    # A*y=B solving for y:
    y = np.matmul(np.linalg.pinv(A), B)
    location = y[:2]
    return location


# A list of known microphone coordinates
mic_positions_xy = np.array(
    [
        [0, 480],  # mic 1 (bottom left corner)
        [480, 480],  # mic 2 (top left corner)
        [480, 0],  # mic 3 (top right corner)
        [0, 0],  # mic 4 (bottom right corner)
        [0, 240]  # mic 5 (side)
    ]
)

mic_positions_xy_only_4_mics = np.array(
    [
        [0, 480],  # mic 1 (bottom left corner)
        [480, 480],  # mic 2 (top left corner)
        [480, 0],  # mic 3 (top right corner)
        [0, 0]  # mic 4 (bottom right corner)
    ]
)


def test_localization_xy(kitt_test_location_xy):
    """
    Generate a TDOA distance matrix based on a known location (x,y) of the KITT car (specifically the beacon)
    Used to test localization algorithm on known locations
    """

    # If an incorrect number dimensions was given, give an error
    if len(kitt_test_location_xy) != 2:
        raise ValueError("Give an appropriate number of dimensions")

    r_ij = []
    for i in range(4):
        for j in range(i + 1, 4):
            # Using the known coordinates, use the Pythagorean theorem to determine the distance between KITT
            # and each microphone
            d_i = math.dist(mic_positions_xy_only_4_mics[i], kitt_test_location_xy)
            d_j = math.dist(mic_positions_xy_only_4_mics[j], kitt_test_location_xy)
            r_ij.append(d_i - d_j)
    r_ij = np.array(r_ij)
    print(f'r_ij:\n'
          f'{r_ij}\n')

    '''
       range diff matrix
       '''
    # # Container to generate TDOA distance matrix
    # dist = np.zeros([5, 5])
    #
    # r_ij = []
    # for i in range(5):
    #     for j in range(5):
    #         # Using the known coordinates, use the pythagorean theorem to determine the distance between KITT
    #         # and each microphone
    #         d_i = np.sqrt(np.sum((mic_positions_xy[i] - kitt_test_location_xy) ** 2))
    #         d_j = np.sqrt(np.sum((mic_positions_xy[j] - kitt_test_location_xy) ** 2))
    #         dist[i, j] = d_j - d_i  #range difference
    #         r_ij.append(dist[i, j])
    #
    # print(r_ij)
    return r_ij


def main():
    Fs = 48e3
    v_sound = 343.14

    # KITT location
    location = [240, 120]

    # Measured range value r_ij from deconvolution func
    diff = [12, 230, 218, 218, 206, -12] # 240x120
    # diff =[-398, -675, -410, -277, -12, 265] #80X400
    diff_calc = [x * 343.14 / 48000 for x in diff]

    # Computed location
    location_comp = difference_to_location_xy(test_localization_xy(location), mic_positions_xy_only_4_mics, Fs, v_sound)
    print(f'Computed location (x,y) [cm]:\n'
          f'{location_comp}'
          f'\n')

    # Actual location
    location_actual = difference_to_location_xy(diff_calc, mic_positions_xy_only_4_mics, Fs, v_sound)
    print(f'Actual location (x,y) [cm]:\n'
          f'{location_actual}'
          f'\n')

    # Error margin
    error_margin = abs(location_comp - location_actual)
    print(f'Error margin (x,y) [cm]:\n'
          f'{error_margin[0][0], error_margin[1][0]}'
          f'\n')

    return

main()