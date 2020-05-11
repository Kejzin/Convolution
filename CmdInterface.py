import sys
import logging


class CmdInterface:
    @staticmethod
    def get_path_from_cmd():
        """
        get firs argument from cmd. In use case it should be wave files path
        Returns
        -------
            path: str
                first argument from cmd, should be path to wave files
        """
        try:
            path = sys.argv[1]
        except IndexError:
            logging.error('Path not entered. Please enter path to wave files')
            sys.exit()
        return path
