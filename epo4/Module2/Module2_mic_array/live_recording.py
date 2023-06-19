
import numpy as np
from epo4.Module2.Module2_mic_array.AudioBeacon import mic_recording
from epo4.Module2.Module2_mic_array.Deconvolution import localization
# #KITT.set_beacon() needs to be incluede when conecting with kitt

mic_positions_xy = np.array(
    [
        [0  ,480],   # mic 1 (bottom left corner)
        [480,480],   # mic 2 (top left corner)
        [480,0  ],   # mic 3 (top right corner)
        [0  ,0  ],   # mic 4 (bottom right corner)
        [0  ,240]    # mic 5 (side)
    ]
)
Fs = 48000

# File path ref signal
# file_path_xref = r"C:\Users\ZA\Desktop\EPO-4\EPO-4-Python\epo4\Module2\Module2_mic_array\ref_sig_V1.8.txt"
# file_path_xref = r"Mic-Data/Mic-Data-V1/ref_sig_V1.8.txt"
file_path_xref = r"C:\Users\ZA\Desktop\EPO-4\EPO-4-Python\epo4\Module2\Module2_mic_array\Mic-Data\Mic-Data-V1\ref_sig_V1.8.txt"

# Load data from the text file
xref = np.loadtxt(file_path_xref)

#set eps ch3 function
eps = 0.001

#set speed of sound
Vsound = 343.14 #speed of sound m/s 20 degree

#set treshold for find first peak channel response
threshold = 0.21
def live_recording(S):
    data = mic_recording(S)
    locations = localization(data, xref, mic_positions_xy, Fs, eps, Vsound, len(xref), location_car,
                                 threshold)

    recorded_orientation = calculate_line_angle(locations)
    print("Angle of the line:", recorded_orientation)

    return recorded_orientation

def calculate_line_angle(locations, threshold=3):
    x = [location[0] for location in locations]  # Extract x-coordinates
    y = [location[1] for location in locations]  # Extract y-coordinates

    delta_x = np.diff(x)  # Differences between x-coordinates
    delta_y = np.diff(y)  # Differences between y-coordinates

    angle = np.arctan2(delta_y, delta_x)
    angle = np.rad2deg(angle)
    angle = angle % 360
    angle = np.mean(angle)
    return angle

