import numpy as np


# Define the positions of the 5 microphones
mic_positions = np.array(
    [
        [0.0, 0.0, 0.5],   # mic 1 (bottom left corner)
        [0.0, 4.8, 0.5],   # mic 2 (top left corner)
        [4.8, 4.8, 0.5],   # mic 3 (top right corner)
        [4.8, 0.0, 0.5],   # mic 4 (bottom right corner)
        [2.4, 4.8, 0.8]    # mic 5 (side)
    ]
)