import os
import argparse
# from pydub import AudioSegment
from termcolor import colored
import importlib
import subprocess
import python_scripts.run_on_dir as run_on_dir
importlib.reload(run_on_dir)


def process_file(file_path, base_dir, base_dir_out=None):
    message = ""
    accepted_formats = ['.mp3', '.m4a', '.flac', '.wav']
    if file_path.endswith(tuple(accepted_formats)):
        relative_path = os.path.relpath(file_path, base_dir)
        base_name = os.path.splitext(relative_path)[0] # remove extension
        if base_dir_out is None:
            base_dir_out = base_dir
            out_file_path = os.path.join(base_dir_out, base_name + '_c.wav')
        else:
            out_file_path = os.path.join(base_dir_out, base_name + '.wav')
        os.makedirs(os.path.dirname(out_file_path), exist_ok=True)
        subprocess.call(['ffmpeg', '-y', '-i', file_path, '-ar', '16000', '-ac', '1', '-c:a', 'pcm_s16le', out_file_path])
        message = colored('\n\n-----------------------------------\n', 'black') + \
            colored(f'Converted! ', 'yellow') + f'{file_path} -> {out_file_path}' + \
            '\n-----------------------------------\n\n'
        return [out_file_path, message]
    
def process_dir(base_dir, base_dir_out=None, recursive=False, verbose=False, return_flat=True):
    file_func = lambda file_path: process_file(file_path, base_dir, base_dir_out)
    return run_on_dir.run_on_dir(base_dir, file_func=file_func, recursive=recursive, print_output=verbose,return_flat=return_flat)


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='Convert audio files to WAV format.')
#     parser.add_argument('input', type=str, help='Path to the input file or folder')
#     parser.add_argument('-o', '--output_path', type=str, default=None, help='Path to the output folder (optional)')
#     parser.add_argument('-d', '--duration', type=int, default=None, help='Duration in minutes to extract from the beginning of the audio file (optional)')
#     parser.add_argument('-r', '--recursive', action='store_true', help='Run recursively on subdirectories')
#     parser.add_argument('-v', '--verbose', action='store_true', help='Print output')
#     args = parser.parse_args()

#     if os.path.isdir(args.input):
#         process_dir(args.input, args.output_path, args.duration, args.recursive, args.verbose)
#     else:
#         if args.output_path is None:
#             output_path = os.path.splitext(args.input)[0] + '-converted.wav'
#         else:
#             output_path = os.path.join(args.output_path, os.path.basename(args.input))
#         convert_to_wav(args.input, output_path, args.duration)

#     process_dir('../data/test_raw/', recursive=True,
#                                            output_path="../temp/test_proc/", verbose=True)
