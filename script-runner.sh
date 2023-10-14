#!/bin/bash

# Navigate to the scripts directory
cd scripts || exit 1

# Get the script name as the first argument
script_name="$1"

# Check if a valid script name is provided
if [ -z "$script_name" ]; then
    echo "Error: Please provide a valid script name (cleaner.py, compresser.py, or db_logger.py)."
    exit 1
fi

# Check the provided script name and execute the corresponding Python script
case "$script_name" in
    "cleaner.py" | "compressor.py")
        python "$script_name"
        ;;
    "db_logger.py")
        # Run FastAPI application using uvicorn
        uvicorn main:app --host 0.0.0.0 --port 8000 --reload
        ;;
    *)
        echo "Error: Invalid script name. Please provide a valid script name (cleaner.py, compresser.py, or db_logger.py)."
        exit 1
        ;;
esac

# Exit the script
exit 0
