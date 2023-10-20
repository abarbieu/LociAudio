import importlib
from termcolor import colored
import subprocess
import python_scripts.run_on_dir as run_on_dir
importlib.reload(run_on_dir)
import python_scripts.process_raw_audio as process_raw_audio
importlib.reload(process_raw_audio)

if __name__ == "__main__":
    base_dir_in = './PUT_AUDIO_DIR_HERE/'
    base_dir_out = './HERE_IS_YOUR_OUTPUT___DELETE_ME/'
    output = process_raw_audio.process_dir(base_dir_in, base_dir_out, recursive=True, verbose=True)


    model = "./whisper.cpp/models/ggml-small.en.bin"
    whisper_dir = "./whisper.cpp/"
    def file_func(file_path):
        subprocess.call([whisper_dir + 'main', '-m', model, '-f', file_path, '-ocsv'])
        sep =  colored('\n\n-----------------------------------\n\n', 'white')
        message = sep + colored(f'Transcribed! ', 'yellow') + f'{file_path}' + sep   

        return [None, message]

    run_on_dir.run_on_dir(base_dir_out, file_func=file_func, recursive=True, print_output=True)