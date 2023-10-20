#!/bin/bash

# Command Check: yq
if ! command -v yq &> /dev/null; then
  echo "Error: yq is not installed. Please install yq."
  exit 1
fi

# Read Config
base_dir=$(yq eval '.base_dir' config.yaml)
whisper_models_dir=$(yq eval '.whisper_models_dir' config.yaml)
model_names=$(yq eval '.model_names[]' config.yaml)
use_preconverted=$(yq eval '.use_preconverted' config.yaml)
preconverted_dir=$(yq eval '.preconverted_dir' config.yaml)
other_params=$(yq eval '.other_params' config.yaml)
IFS=$'\n' read -rd '' -a models <<<"$model_names"

# Validate models
models_full_path=()
for model_name in "${models[@]}"; do
  model_path="$whisper_models_dir/$model_name.bin"
  if [ -f "$model_path" ]; then
    models_full_path+=("$model_path")
  else
    printf "\e[31mWarning: Model $model_path not found. Skipping.\e[0m\n"
  fi
done

# Conversion step
if [ "$use_preconverted" = "true" ]; then
  if [ -d "$preconverted_dir" ]; then
    echo "Using pre-converted files from $preconverted_dir."
    wav_dir_to_use="$preconverted_dir"
  else
    echo "Error: Pre-converted directory $preconverted_dir does not exist."
    exit 1
  fi
else
  echo "Step 1: Converting audio files."
  if ./convert_dir_to_16k_mono_wav.sh "$base_dir"; then
    echo "Step 1: Complete."
    wav_dir_to_use="$base_dir/wav_temp"
  else
    echo "Error: Conversion failed."
    exit 1
  fi
fi

echo "Step 2: Transcription."
# Loop over each model for transcription
for model_path in "${models_full_path[@]}"; do
  echo "Transcribing with model: $(basename "$model_path")"
  echo "Parameters: "$other_params""
  model_name=$(basename "$model_path" .bin)
  transcript_dir="$base_dir/transcripts_$model_name"
  mkdir -p "$transcript_dir"

  if ./transcribe_wav_dir.sh "$wav_dir_to_use" "$model_path" "$transcript_dir" "$other_params"; then
    echo "Transcription complete for model: $model_name."
  else
    echo "Error: Transcription failed for model: $model_name."
    exit 1
  fi
done

# Final Cleanup
if [ "$use_preconverted" != "true" ]; then
  echo "Step 3: Final Cleanup."
  mkdir -p "$base_dir/wavs"
  mv "$base_dir/wav_temp"/* "$base_dir/wavs"
  rm -rf "$base_dir/wav_temp/*"
fi
echo "All steps completed successfully."
