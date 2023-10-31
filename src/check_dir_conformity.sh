# Check if filenames conform to the required format
if [ -z "$1" ]; then
  echo "Usage: ./check_dir_conformity.sh <base_dir> [<file_extension>]"
  exit 1
fi

base_dir="$1"
file_extension="${2:-.*}"  # If no extension is provided, match any extension
non_conforming_files=()

for file in "$base_dir"/*; do
  if [ -f "$file" ]; then  # Check if it's a file and matches the extension
    filename=$(basename "$file")
    pattern="^[0-9]{6}_[0-9]{4}(-.+)?$file_extension$"
    if ! [[ $filename =~ $pattern ]]; then
      non_conforming_files+=("$file")
    fi
  fi
done

if [ ${#non_conforming_files[@]} -ne 0 ]; then
  echo "------------------------------------------------------------------"
  echo "The following files do not conform to the required format (YYMMDD_HHMM-title-here.$file_extension) and will be moved to a special directory:"
  echo "------------------------------------------------------------------"
  mkdir -p "$base_dir/NON_CONFORMING_FILES"
  for file in "${non_conforming_files[@]}"; do
    echo "-> $(basename "$file")"
    mv "$file" "$base_dir/NON_CONFORMING_FILES"
  done
  echo "------------------------------------------------------------------"
  echo "Please rename the files, move them to the base directory and run the script again."
  echo "...Continuing with the remaining files."
  echo "------------------------------------------------------------------"
fi