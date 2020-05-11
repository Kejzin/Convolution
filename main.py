from WaveReader import WaveReader, WaveWriter
from WaveFileSearcher import WaveFileSearcher
import CmdInterface as cmd


if __name__ == "__main__":
    def main():
        wave_file_searcher = WaveFileSearcher()
        wave_files_paths = wave_file_searcher.find_wave_files_paths()
        cmd_args = cmd.parse_argument()
        response_file_path = cmd_args.inpulse_response
        print(response_file_path)
        return wave_files_paths
    main()
