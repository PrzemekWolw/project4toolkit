import os

# Get a list of all .odd files in the current directory
odd_files = [f for f in os.listdir('.') if f.endswith('.odd')]

# Iterate over the .odd files
for odd_file in odd_files:
    # Open the .odd file for reading
    with open(odd_file, 'r') as f:
        # Read the contents of the file into a string
        contents = f.read()

    # Split the contents of the file into a list of blocks based on the gtaDrawable keyword
    blocks = contents.split('gtaDrawable')

    # Iterate over the blocks
    for block in blocks:
        # Check if the block contains the desired text
        if 'lodgroup' in block:
            # Extract the drawable name from the block
            drawable_name = block.split('\n')[0].strip()
            
            # Create a new .odd file for the drawable
            with open(f'{drawable_name}.odr', 'w') as f:
                # Write the block to the new file
                f.write(f'gtaDrawable {block}')
                
exec(open("P4Toolkit.py").read())