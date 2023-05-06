import os
import re

# List of words to search for in the .opl files
search_words = ["hash", "end", "grge", "cars", "tcyc", "mlop", "lodm", "slow", "blok", "versio", "Binary", "version 3", "inst"]

# Create a list of all ".opl" files in the current working directory
opl_files = [f for f in os.listdir('.') if f.endswith('.opl')]

# Create a regular expression pattern to search for the specified words
pattern = re.compile(r'\b(?:' + '|'.join(search_words) + r')\b')

# Iterate over each ".opl" file
for opl_file in opl_files:
    # Read the lines of the .opl file
    with open(opl_file, 'r') as infile:
        lines = infile.readlines()

    # Write only the lines that don't contain any of the specified words or are empty
    with open(opl_file, 'w') as outfile:
        for line in lines:
            if not pattern.search(line) and not line.strip() == "":
                outfile.write(line)
