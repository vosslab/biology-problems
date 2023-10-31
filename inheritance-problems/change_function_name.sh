#!/bin/bash

# Iterate over all Python files in the current directory
for file in t*_test-cross_*.py unordered*.py; do
    #echo $file
    # Create a temporary file
    temp_file=$(mktemp)

    # Use sed to find and replace the function call and store in temporary file
    cp "$file" "$temp_file"
    # Use sed to find and replace the function calls and update the temp file
    gsed -e 's/invertType(/ptcl.invert_genotype(/' \
        -e 's/flipGene(/ptcl.flip_gene_by_letter(/' \
        -e 's/getPhenotype(/ptcl.get_phenotype_name(/' \
        -e 's/getGeneOrder(/ptcl.get_random_gene_order(/' \
        -i "$temp_file"

    # Get the number of lines in the original and temporary files
    original_lines=$(wc -l < "$file")
    temp_lines=$(wc -l < "$temp_file")

    # Compare the temporary file with the original file
    if ! cmp -s "$file" "$temp_file"; then
        # Check if temp_file has the same number of lines as the original file
        if [ "$original_lines" -eq "$temp_lines" ]; then
            # Files are different, but have the same number of lines, so update the original file
            mv "$temp_file" "$file"
            # Output the name of the file that got modified
            echo "Modified $file"
        else
            # Output a message if the number of lines do not match, indicating an issue
            echo "Line count mismatch for $file and its temporary file, skipping. $original_lines vs. $temp_lines"
        fi
    else
        # Files are the same, so remove the temporary file
        rm "$temp_file"
    fi
done

echo "Finished updating Python files."
