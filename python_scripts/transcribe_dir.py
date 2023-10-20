import os
import argparse
import subprocess
import process_raw_audio
from tqdm import tqdm

from termcolor import colored

if __name__ == "__main__":
    default_model = 'large'
    default_input = './data/to_transcribe_raw'

    parser = argparse.ArgumentParser(description='Convert and transcribe audio files.')
    parser.add_argument('-i', '--input', type=str, default=default_input, help='Path to the input folder')
    parser.add_argument('-o', '--output_path', type=str, help='Path to the output folder (if not specified, will be the same as input folder)')
    parser.add_argument('-r', '--recursive', action='store_true', help='Run recursively on subdirectories')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print output')
    parser.add_argument('-m', '--model', type=str, default=default_model, help='Whisper model to use for transcription')

    args = parser.parse_args()

    if args.verbose:
        print("Input: {}".format(args.input))
        print("Output: {}".format(args.output_path))
        print("Recursive: {}".format(args.recursive))
        print("Model: {}".format(args.model))
    
    if args.output_path is None:
        args.output_path = args.input

    if os.path.isdir(args.input):
        if args.verbose:
            print("Converting files to wav etc...")
        processed_files = process_raw_audio.process_dir(args.input, args.output_path, recursive=args.recursive, verbose=args.verbose, return_flat=True)
    else:
        print("Input must be a directory.")