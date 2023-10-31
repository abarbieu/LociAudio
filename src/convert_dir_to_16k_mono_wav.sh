#!/bin/bash

# Initialize log file
if [ -z "$1" ]; then
  echo "Usage: ./convert_dir_to_16k_mono_wav.sh <input_dir>"
  exit 1
fi

if [ ! -d "$1" ]; then
  echo "Error: Invalid directory $1"
  exit 1
fi

if ! command -v ffmpeg &> /dev/null; then
  echo "Error: ffmpeg not found. Please install ffmpeg."
  exit 1
fi

# Navigate to input directory
base_dir="$1"

# Create the directories if they don't exist
mkdir -p "$base_dir/wavs" "$base_dir/raw" "$base_dir/wav_temp"

# Enable nullglob
shopt -s nullglob

cd "$base_dir"

# Loop through audio files
for f in *.mp3 *.wav *.m4a *.WAV *.ogg; do
  output_file="./wav_temp/${f%.*}.wav"
  printf "Converting \e[32m%s\e[0m to 16kHz Mono Wav\n" "$f"
  ffmpeg -v quiet -stats -i "$f" -ar 16000 -ac 1 -c:a pcm_s16le "$output_file" -y
  printf "\n"
  mv "$f" ./raw/
done

# Disable nullglob
shopt -u nullglob