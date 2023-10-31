# Automated Transcription Pipeline (Whisper cpp)

This repo contains code for the automated transcription of diverse audiofiles. As of writing this it:

- Checks audio filename format conformity
- Converts (wav, m4a, mp3) into 16Khz single channel wav (combines stereo) via `fmmpeg` 
- Removes silence via `sox`
- Transcribes audio locally using `whisper.cpp` (Mac Metal compatible) 
- Manages files and folders automatically

## Instructions

1. Create a directory containing the raw audio files to be transcribed
2. Update config.yaml:
    - Set `base_dir` to your audio directory
    - Ensure you have the git `whisper.cpp` submodule cloned
    - Ensure `whisper_models_dir` contains built whisper models ([refer to whisper.cpp](https://github.com/ggerganov/whisper.cpp))
    - Define `model_names` to contain the models you wish to use (ggml indicates built for Mac Metal)
    - Update any whisper parameters via `other_params`
3. Run ./update.sh

You should then find a set of self-descriptive directories in your audio folder

You can also run scripts in `./src` after transcription to avoid repeated work