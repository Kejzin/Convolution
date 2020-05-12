from scipy.io import wavfile
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

signal_wave_file_path = r".\Test_signals\dummy.wav"
impulse_response_wav_file_path = r".\Test_signals\RESPONSE.wav"
convolved_signal_file_path = r".\created_signals\convolved.wav"
recovered_signal_path = r".\created_signals\deconvolved.wav"


def simplest_possible_plot(data_to_plot, plot_name):
    x_axis = np.arange(0, len(data_to_plot))
    fig, ax = plt.subplots()
    ax.plot(x_axis, data_to_plot)
    ax.grid()
    plt.savefig(f"plots\\{plot_name}")


def normalize_np_array(np_array_to_normalize):
    try:
        max_value = max(np_array_to_normalize.min(), np_array_to_normalize.max(), key=abs)
        normal_array = np_array_to_normalize / max_value
    except AttributeError:
        print("empty array or other Atribute Error")
        normal_array = np.array([0,0])
    return normal_array


if __name__ == "__main__":
    # Read signal and impulse response valuse
    signal_fs, signal_data = wavfile.read(signal_wave_file_path)
    response_fs, impulse_response_data = wavfile.read(impulse_response_wav_file_path)

    simplest_possible_plot(signal_data, "signal.png")
    simplest_possible_plot(impulse_response_data, "response.png")

    response_length = len(impulse_response_data)
    signal_length = len(signal_data)


    # Limit response and signal length to optimize computing time for testing
    limited_impulse_response_data = impulse_response_data[0:int(response_length/2)]
    limited_signal_data = signal_data[0:int(signal_length/4)]

    simplest_possible_plot(limited_signal_data, "limited_signal.png")
    simplest_possible_plot(limited_impulse_response_data, "limited_response.png")

    # Normalize signal data
    limited_signal_data_normalized = normalize_np_array(limited_signal_data)

    # Normalize impulse response data and adjust it's gain. It is extremely overload
    response_gain = 1/1000
    response_data_normalized = normalize_np_array(limited_impulse_response_data)

    simplest_possible_plot(response_data_normalized, "normalized_response_data.png")
    # Process a convolution on signal data using impulse response
    convolved = signal.convolve(limited_signal_data_normalized, limited_impulse_response_data,)

    max_convolved_data = abs(convolved).max()
    # Normalize convolved data and expand its value to save as wave
    convolved_normalized = normalize_np_array(convolved)

    simplest_possible_plot(convolved_normalized, "normalized_convolved.png")

    wavfile.write(convolved_signal_file_path, signal_fs, convolved_normalized)

    convolved_fs, read_convolved_data = wavfile.read(convolved_signal_file_path)

    read_convolved_data_normalized = normalize_np_array(read_convolved_data)

    simplest_possible_plot(read_convolved_data_normalized, "normalized_read_convolved_data.png")

    recovered, remainder = signal.deconvolve(limited_impulse_response_data, read_convolved_data)

    recovered_normalized = normalize_np_array(recovered)
    remainder_normalized = normalize_np_array(remainder)

    simplest_possible_plot(recovered_normalized, "normalized_recovered.png")
    simplest_possible_plot(remainder_normalized, "normalized_remainder.png")

    wavfile.write(recovered_signal_path, signal_fs, recovered_normalized)

    print("Tadam")
