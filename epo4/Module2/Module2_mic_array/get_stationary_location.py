from KITT import KITT
import numpy as np
from epo4.Module2.Module2_mic_array.AudioBeacon import mic_recording
from epo4.Module2.Module2_mic_array.Deconvolution import localization, IQR_average
#KITT.set_beacon() needs to be incluede when conecting with kitt

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
file_path_xref = r"C:\Users\Sam\PycharmProjects\EPO-4\epo4\Module2\Module2_mic_array\ref_sig_V1.8.txt"
location_car = '80x400'
# Load data from the text file
xref = np.loadtxt(file_path_xref)

#set eps ch3 function
eps = 0.001

#set speed of sound
Vsound = 343.14 #speed of sound m/s 20 degree

#set treshold for find first peak channel response
threshold = 0.25
def get_stationary_location(N):
    data = mic_recording(N)

    locations = localization(data, xref, mic_positions_xy, Fs, eps, Vsound, len(xref), location_car,
                             threshold)
    location_stationary = IQR_average(locations)
    print(location_stationary)
    return location_stationary


if __name__ == '__main__':
    get_stationary_location(10000)