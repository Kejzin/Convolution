from WaveReader import WaveReader, WaveWriter
from WaveFileSearcher import WaveFileSearcher
from WaveReader import WaveReader
import CmdInterface as cmd
from SampledBConverter import DeconvolutionMaker
import wave
from WaveReader import WaveWriter
import os


if __name__ == "__main__":
    def main():
        wave_file_searcher = WaveFileSearcher()
        wave_files_paths = wave_file_searcher.find_wave_files_paths()
        cmd_args = cmd.parse_argument()
        response_file_path = cmd_args.inpulse_response
        print(response_file_path)
        for path in wave_files_paths:
            reader = WaveReader(response_file_path)
            response = reader.read_all_audio_data()
            print("HALO")
            # print("RESPONSE", response)
            print(path)
            deconvolutor = DeconvolutionMaker(path)
            deconvoluted = deconvolutor.deconvolve(response)
            print(deconvoluted)
            audio_file = wave.open(path, 'rb')
            params = audio_file.getparams()
            frames_and_params = (deconvoluted, params)
            WaveWriter.write_defined_frames(os.getcwd(), frames_and_params)

        return deconvoluted
    main()
