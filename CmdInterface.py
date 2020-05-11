import argparse

def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file", help="path to wave files")
    parser.add_argument("-r", "--inpulse_response", help="inpulse response of room")
    args = parser.parse_args()
    return args

