#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if pidstat command exists
if ! command_exists pidstat; then
    echo "pidstat command not found. Attempting to install sysstat package..."

    # Check the package manager and install sysstat
    if command_exists apt-get; then
        sudo apt-get update
        sudo apt-get install -y sysstat
    elif command_exists yum; then
        sudo yum install -y sysstat
    else
        echo "Error: Unsupported package manager. Please install sysstat manually."
        exit 1
    fi

    # Recheck if pidstat is now available
    if ! command_exists pidstat; then
        echo "Failed to install sysstat or pidstat command. Exiting."
        exit 1
    fi
fi

# Get disk usage statistics for processes
pidstat -d 1 1 | awk '{if (NR > 3) { pid=$1; read_bytes=$3; write_bytes=$4; for(i=12;i<=NF;i++){if($i!=""){process_name=$i;break;}} print "{ \"pid\": \""pid"\", \"process_name\": \""process_name"\", \"read_bytes\": "read_bytes", \"write_bytes\": "write_bytes" }," }}' | sed '$ s/,$//'
