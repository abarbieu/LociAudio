#!/bin/bash

pause_length=$1
input_dir=$2

if [ "$#" -ne 2 ]; then
  echo "Usage: ./remove_silence_dir.sh <pause_length> <input_dir>"
  exit 1
fi

if [ ! -d "$input_dir" ]; then
  echo "Error: Directory $input_dir does not exist."
  exit 1
fi

for file in "$input_dir"/*.wav; do
  sox "$file" temp.wav silence -l 1 0.1 1% -1 $pause_length 1%
  mv temp.wav "$file"
done