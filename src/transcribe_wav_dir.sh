#!/bin/bash

# Check if the required arguments are provided
if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
  echo "Usage: ./transcribe_wav_dir.sh <input_wav_dir> <model_file> <transcript_dir> [other_params]"
  exit 1
fi

input_dir="$1"
model_file="$2"
transcript_dir="$3"
if [ -z "$4" ]; then
  other_params=""
else
other_params="$4"
fi

# Create output sub-directories under transcript_dir
json_dir="$transcript_dir/json"
df_dir="$transcript_dir/df"
stderr_dir="$transcript_dir/stderr"
stdout_dir="$transcript_dir/stdout"

# Validate input directory and model file
if [ ! -d "$input_dir" ] || [ ! -f "$model_file" ]; then
  echo "Invalid input directory or model file."
  exit 1
fi

mkdir -p "$json_dir" "$df_dir" "$stderr_dir" "$stdout_dir"

# Loop over each .wav file for transcription
for f in "$input_dir"/*.wav; do
  json_output="$json_dir/$(basename "${f%.*}").json"
  df_output="$df_dir/$(basename "${f%.*}").csv"
  stderr_output="$stderr_dir/$(basename "${f%.*}").ans"
  stdout_output="$stdout_dir/$(basename "${f%.*}").ans"
  txt_output="$transcript_dir/$(basename "${f%.*}").txt"
  
  # Print the file being processed
  echo "Now transcribing: $f with model: $model_file" | tee -a "$stdout_output"

  # Run the transcription and redirect outputs
  ./whisper.cpp/main -m "$model_file" -f "$f" -oj $other_params 2> "$stderr_output" | tee -a "$stdout_output"

  # Copy the stdout_output to a new txt file in $transcript_dir
  cp "$stdout_output" "$txt_output"

  # Create a .txt file without ANSI color codes
  txt_output="$transcript_dir/$(basename "${f%.*}").txt"
  perl -pe 's/\e\[?.*?[\@-~]//g' "$stdout_output" > "$txt_output"
  
  # Call the Python script to create a DataFrame from the JSON file
  python3 ./src/create_dataframe.py "${f}.json" "$df_dir"

  # Move the generated JSON file to the appropriate directory
  mv "${f}.json" "$json_output"
done
