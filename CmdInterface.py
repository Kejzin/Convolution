import argparse

def parse_argument():
    parser = argparse.ArgumentParser
    parser.add_argument("-i", " --input_files_paths", help="path to wave files")
    args = parser.parse_args()
    return args

