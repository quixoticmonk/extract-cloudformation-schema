#!/bin/bash

# Directory to search in (use current directory if not specified)
dir="${1:-.}"

# Output file
output_file="reference-resources.txt"

# Find all json files and process their names
for file in "$dir"/*.json; do
    # Get just the filename without the path
    basename=$(basename "$file")
    # Remove .json extension and replace _ with ::
    modified_name=$(echo "${basename%.json}" | tr '_' '::')
    # Add AWS:: prefix and append to output file
    echo "AWS::$modified_name" >> "$output_file"
done

# Sort the output file in place (optional)
sort -o "$output_file" "$output_file"
