import numpy as np


# Define the positions of the 5 microphones x,y,z
mic_positions = np.array(
    [
        [0  ,480, 50],   # mic 1 (bottom left corner)
        [480,480, 50],   # mic 2 (top left corner)
        [480,0  , 50],   # mic 3 (top right corner)
        [0  ,0  , 50],   # mic 4 (bottom right corner)
        [0  ,240, 80]    # mic 5 (side)
    ]
)
