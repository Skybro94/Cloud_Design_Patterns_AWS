#!/bin/bash

echo "Initializing infrastructure setup..."

# Function to check if a command exists
check_command() {
    command -v "$1" &>/dev/null
}

# Determine Python executable
if check_command python3; then
    PYTHON_CMD="python3"
elif check_command python; then
    PYTHON_CMD="python"
else
    echo "Error: Python is not installed. Please install Python to proceed."
    exit 1
fi

echo "Using Python executable: $PYTHON_CMD"

# Check if cleanup argument is provided
if [ "$1" == "cleanup" ]; then
    echo "Running cleanup process..."
    $PYTHON_CMD main.py cleanup
else
    echo "Running deployment process..."
    $PYTHON_CMD main.py
fi

# Check for success or failure
if [ $? -eq 0 ]; then
    echo "Process completed successfully."
else
    echo "Error: Process failed. Please check the logs for details."
    exit 1
fi
