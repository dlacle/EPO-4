from KITT import KITT
from epo4.Module2.Module2_mic_array.AudioBeacon import mic_recording
from epo4.Module2.Module2_mic_array.Deconvolution import *
#KITT.set_beacon() needs to be incluede when conecting with kitt
def get_stationary_location(N):
    data = mic_recording(N)
    locations = localization(data, xref, mic_positions_xy, Fs, eps, Vsound, len(xref), location_car,
                             threshold)
    location_stationary = IQR_average(locations)
    print(location_stationary)
    return location_stationary



