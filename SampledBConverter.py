import sys
from pyfilterbank import splweighting
import numpy as np
from WaveReader import WaveReader
from acoustics import standards
from CmdInterface import CmdInterface
from scipy import signal


class DeconvolutionMaker:
    """Convert samples from given wave file to frequency and time weighted signal according to IEC 61672-1:2013"""

    def __init__(self, file_path):
        self.wave_reader_object = WaveReader(file_path)
        self.audio_samples_generator = self.wave_reader_object.read_audio_data_chunk()

    def convert_all_file_samples(self,):
        """Use convert_samples method to all samples in file.
        Returns
        -------
            all_converted_samples: [float]
        """
        all_converted_samples = []
        while True:
            try:
                all_converted_samples += next(self.deconvolve())
            except StopIteration:
                break
        return all_converted_samples

    def deconvolve(self, impulse_response):
        """
        Make full conversion from dynamic representation to frequency and time weighted samples according to IEC-61672.
        Returns
        -------
            db_fs_samples: [float]
                frequency and time weighted full scale level.
        """
        while True:
            try:
                samples = next(self.audio_samples_generator)
            except StopIteration:
                return
            recovered, remainder = signal.deconvolve(samples, impulse_response)
            yield recovered
