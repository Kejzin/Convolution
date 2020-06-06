from scipy.io import wavfile
from scipy import signal, fft
import numpy as np
import matplotlib.pyplot as plt
import math

signal_wav_file_path = r"E:\Kejzin\Documents\PWR\Master_Thesis\Sygnaly testowe\Czyste\Klasyka2.wav"
impulse_response_wav_file_path = r".\Test_signals\Big_Hall_E001_M2S.wav"
convolved_signal_file_path = r"E:\Kejzin\Documents\PWR\Master_Thesis\Sygnaly testowe\poglos\Klasyka2_conv.wav"
recovered_signal_path = r".\created_signals\deconvolved.wav"
remainder_signal_path = r".\created_signals\remainder.wav"



def simplest_possible_plot(data_to_plot, plot_name):
    """Create very simple plot of np.array()given for testing purposes.

     Construct linear x_axis to mach length of given data. Save it in working directory, in "plots/" subfolder
     """
    x_axis = np.arange(0, len(data_to_plot))
    fig, ax = plt.subplots()
    ax.plot(x_axis, data_to_plot)
    ax.grid()
    plt.savefig(f"plots\\{plot_name}")


def normalize_np_array(np_array_to_normalize):
    """Normalize numpy array to get a values in range [-1,1]. Return empty array if meets attribute error"""
    try:
        max_value = max(np_array_to_normalize.min(), np_array_to_normalize.max(), key=abs)
        normal_array = (np_array_to_normalize / max_value)

    except AttributeError:
        print("empty array or other Attribute Error")
        normal_array = np.array([0])*1000
    return normal_array


if __name__ == "__main__":
    # Read signal and impulse response value
    signal_fs, signal_data = wavfile.read(signal_wav_file_path)
    response_fs, impulse_response_data = wavfile.read(impulse_response_wav_file_path)

    simplest_possible_plot(signal_data, "original_signal.png")
    simplest_possible_plot(impulse_response_data, "original_response.png")

    response_length = len(impulse_response_data)
    signal_length = len(signal_data)

    desired_response_length = int(4096)*4
    desired_signal_length = int(4096)*8

    # Limit response and signal length to optimize computing time for testing
    timelimited_impulse_response_data = impulse_response_data# [0:desired_response_length]
    timelimited_signal_data = signal_data

    simplest_possible_plot(timelimited_signal_data, "timelimited_signal.png")
    simplest_possible_plot(timelimited_impulse_response_data, "timelimited_response.png")

    # Normalize signals data
    timelimited_signal_data_normalized = normalize_np_array(timelimited_signal_data)
    timelimited_response_data_normalized = normalize_np_array(timelimited_impulse_response_data)

    simplest_possible_plot(timelimited_response_data_normalized, "timelimited_normalized_response_data.png")
    simplest_possible_plot(timelimited_signal_data_normalized, "timelimited_normalized_signal_data.png")

    # Process a convolution on signal data using impulse response
    convolved = signal.convolve(timelimited_signal_data_normalized, timelimited_impulse_response_data,)

    # Normalize convolved data
    convolved_normalized = normalize_np_array(convolved)
    simplest_possible_plot(convolved_normalized, "normalized_convolved.png")

    # Save normalized convolved data as wav file.
    wavfile.write(convolved_signal_file_path, signal_fs, convolved_normalized)

    # Read convolved data from wav file. It is simulation of real-life usage when we have convoluted signal and
    # impulse response, not pure input signal.
    convolved_fs, read_convolved_data = wavfile.read(convolved_signal_file_path)

    read_convolved_data_normalized = normalize_np_array(read_convolved_data)
    timelimited_read_convolved_data_normalized = read_convolved_data_normalized[0:desired_response_length]
    simplest_possible_plot(timelimited_read_convolved_data_normalized, "normalized_read_convolved_data.png")


    print("Tadam")
