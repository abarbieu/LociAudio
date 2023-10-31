#!/bin/bash

# Check if the required arguments are provided
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: ./make_dfs.sh <input_json_dir> <output_dir>"
  exit 1
fi

input_dir="$1"
output_dir="$2"

./src/check_dir_conformity.sh "$input_dir" "json"

# Validate input directory
if [ ! -d "$input_dir" ]; then
  echo "Invalid input directory."
  exit 1
fi

# Loop over each .json file for conversion
for f in "$input_dir"/*.json; do
  # Print the file being processed
  echo "Converting to df: $f"
  
  # Call the Python script to create a DataFrame from the JSON file
  python3 ./src/create_dataframe.py "$f" "$output_dir"
done