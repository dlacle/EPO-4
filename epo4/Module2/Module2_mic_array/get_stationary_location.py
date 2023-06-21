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
# file_path_xref = r"C:\Users\ZA\Desktop\EPO-4\EPO-4-Python\epo4\Module2\Module2_mic_array\ref_sig_V1.8.txt"
# file_path_xref = r"Mic-Data/Mic-Data-V1/ref_sig_V1.8.txt"
# file_path_xref = r"C:\Users\ZA\Desktop\EPO-4\EPO-4-Python\epo4\Module2\Module2_mic_array\Mic-Data\Mic-Data-V1\ref_sig_V1.8.txt"
file_path_xref = r"C:\Users\rbjwe\PycharmProjects\EPO-4_GIT\epo4\Module2\Module2_mic_array\Mic-Data\Mic-Data-V1\ref_sig_V1.8.txt"
location_car = '80x400'
# Load data from the text file
xref = np.loadtxt(file_path_xref)

#set eps ch3 function
eps = 0.001

#set speed of sound
Vsound = 343.14 #speed of sound m/s 20 degree

#set treshold for find first peak channel response
threshold = 0.21
def get_stationary_location(N):
    max_retry = 3
    retry_count = 0

    while retry_count < max_retry:
        try:
            data = mic_recording(N)

            locations = localization(data, xref, mic_positions_xy, Fs, eps, Vsound, len(xref), location_car,
                                     threshold)
            location_stationary = IQR_average(locations)
            location_stationary = location_stationary / 100

            break  # If function call succeeds, exit the loop
        except Exception as e:
            print(f"Error occurred: {e}")
            retry_count += 1
            print(f"Retrying... (Attempt {retry_count})")

    if retry_count == max_retry:
        print("Function call unsuccessful after maximum retries.")
        location_stationary = [999,999] # error location not found

    print("location_stationary", location_stationary)
    return location_stationary

