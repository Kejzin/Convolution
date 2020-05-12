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
    norm = np.linalg.norm(np_array_to_normalize)
    normal_array = np_array_to_normalize / norm
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
    max_response_data = abs(limited_impulse_response_data).max()
    response_data_normalized = \
        [(normalized_data/max_response_data) * response_gain for normalized_data in limited_impulse_response_data]

    # Process a convolution on signal data using impulse response
    convolved = signal.convolve(limited_impulse_response_data, limited_signal_data_normalized)

    max_convolved_data = abs(convolved).max()
    # Normalize convolved data and expand its value to save as wave
    convolved_normalized = normalize_np_array(convolved)

    simplest_possible_plot(convolved_normalized, "convolved_normalized.png")

    convolved_to_wave = [data/2 for data in convolved]

    simplest_possible_plot(convolved_to_wave, "convolved_to_wave.png")

    wavfile.write(convolved_signal_file_path, signal_fs, np.array(convolved_to_wave))

    convolved_fs, read_convolved_data = wavfile.read(convolved_signal_file_path)

    max_convolved_value = abs(read_convolved_data).max()
    read_convolved_data = [(normalized_data / max_convolved_value) for normalized_data in read_convolved_data]

    simplest_possible_plot(read_convolved_data, "readed_convolved_data.png")

    recovered, remainder = signal.deconvolve(limited_impulse_response_data, read_convolved_data)

    simplest_possible_plot(recovered, "recovered.png")
    simplest_possible_plot(remainder, "remainder.png")

    recovered_deconvolved_to_wave = [data for data in recovered]
    wavfile.write(recovered_signal_path, signal_fs, np.array(recovered_deconvolved_to_wave))

    print("Tadam")
