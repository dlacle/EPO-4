import numpy as np


# Define the positions of the 5 microphones
mic_positions = np.array(
    [
        [0  , 0  , 50],   # mic 1 (bottom left corner)
        [0  , 480, 50],   # mic 2 (top left corner)
        [480, 480, 50],   # mic 3 (top right corner)
        [480, 0  , 50],   # mic 4 (bottom right corner)
        [240, 480, 80]    # mic 5 (side)
    ]
)
for i, mic_position in enumerate(mic_positions):
    locals()[f'x{i+1}'] = mic_position

# test Print the variables
for i in range(1, len(mic_positions) + 1):
    print(f'x{i} = {locals()["x" + str(i)]}')
