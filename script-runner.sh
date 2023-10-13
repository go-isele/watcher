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

# Check if the script is a FastAPI application (assuming it's in the format of 'uvicorn main:app')
if grep -q "uvicorn main:app" "$script_file_path"; then
    # Start the FastAPI application using uvicorn in the background
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload &

    # Run the Python script
    python3 "$script_file_path"

    # Optionally, you can add a command to stop the FastAPI application when the Python script exits
    # For example, you can use 'pkill' to stop the uvicorn process:
    # pkill -f "uvicorn main:app --host 0.0.0.0 --port 8000"
else
    # Run the non-API Python script
    python3 "$script_file_path"
fi
