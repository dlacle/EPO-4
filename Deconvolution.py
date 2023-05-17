import time
import serial
import pyaudio
import numpy as np
import matplotlib.pyplot as plt

# Reference signal
ref_sig = np.loadtxt('Mic-Data/data_mics_kitt_carrier_2250_bit_3k_ref.txt')

# Field locations
data_80x400 = np.loadtxt('Mic-Data/data_mics_kitt_mic_80x400.txt')
data_140x320 = np.loadtxt('Mic-Data/data_mics_kitt_mic_140x320.txt')
