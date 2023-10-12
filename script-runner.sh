#!/bin/bash

# Change directory to the 'scripts' directory or exit if unsuccessful
cd "$(dirname "$0")/scripts" || exit 1

# Check if the script file path is provided as an argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <script_file_path>"
    exit 1
fi

# Get the script file path from the argument
script_file_path="$1"

# Check if the script file exists
if [ ! -f "$script_file_path" ]; then
    echo "Error: Script file not found!"
    exit 1
fi

# Run the Python script
python3 "$script_file_path"
