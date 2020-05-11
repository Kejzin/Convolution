import os
import logging
import ntpath
from CmdInterface import CmdInterface


class WaveFileSearcher:
    @staticmethod
    def find_wave_files_paths():
        """
        Find wave files under path given in cmd. Path must be a directory containing wav files and REFERENCE.wav file.
        Returns
        -------
           wave_files_and_reference_paths: [str]
                touple of two list. First is wave files paths to analize, second is reference file path.
        """
        path = CmdInterface.get_path_from_cmd()
        if os.path.isfile(path):
            raise NotADirectoryError('path is a file not a directory')
        elif os.path.isdir(path):
            path_content = os.listdir(path)
            wave_files_paths = ["{}/{}".format(path, file_path) for file_path in path_content if (".wav" in file_path
                                or ".WAV" in file_path)and("REFERENCE" not in file_path)]
        else:
            logging.error('{} is no valid path'.format(path))
            raise FileNotFoundError('{} is not a valid path'.format(path))

        assert wave_files_paths, 'there is no any wave file under given path'
        wave_files_names = [ntpath.basename(path) for path in wave_files_paths]

        print('I found {} files. Files names are: {}'.format(len(wave_files_names), wave_files_names))
        print('')

        wave_files_and_reference_paths = wave_files_paths
        return wave_files_and_reference_paths
