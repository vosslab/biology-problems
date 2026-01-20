#!/bin/bash

# Function to process a single file
process_file() {
    local input_file=$1

    # Check if the file exists and is readable
    if [ ! -f "$input_file" ] || [ ! -r "$input_file" ]; then
        echo "File does not exist or is not readable: $input_file"
        return 1
    fi

    # Read and process each line in the file
    while read -r line; do
        # Convert the line to lowercase
        line=$(echo "$line" | tr '[:upper:]' '[:lower:]')

        # Remove all non-letter characters from the line
        line=$(echo "$line" | sed 's/[^a-zA-Z ]//g')

        # Split the line into words
        for word in $line; do
            # Get the length of the word
            len=${#word}

            # Check if the word's length is between 3 and 6
            if [ "$len" -ge 3 ] && [ "$len" -le 6 ]; then
                echo "$word"
            fi
        done
    done < "$input_file"
}

# Main part of the script

# If a directory is provided, loop over all .yml files in that directory
if [ -d "$1" ]; then
    for file in "$1"/*.yml; do
        process_file "$file"
    done | sort | uniq
# If a single file is provided, just process that file
elif [ -f "$1" ]; then
    process_file "$1" | sort | uniq
# If neither a valid directory nor file is provided
else
    echo "Usage: $0 <filename or directory>"
    exit 1
fi
