import os

def extract_text_strings(filename, output_file):
    with open(filename, 'rb') as f:
        # Read the first header
        offset1 = int.from_bytes(f.read(4), byteorder='little', signed=False)
        padding1 = f.read(4)
        offset2 = int.from_bytes(f.read(4), byteorder='little', signed=False)
        offset3 = int.from_bytes(f.read(4), byteorder='little', signed=False)
        padding2 = f.read(4)
        offset4 = int.from_bytes(f.read(4), byteorder='little', signed=False)
        offset5 = int.from_bytes(f.read(4), byteorder='little', signed=False)
        long_val = int.from_bytes(f.read(4), byteorder='little', signed=False)
        
        # Read the second header
        long_val2 = int.from_bytes(f.read(4), byteorder='little', signed=False)
        padding3 = f.read(4)
        padding4 = f.read(4)
        long_val3 = int.from_bytes(f.read(4), byteorder='little', signed=False)
        offset6 = int.from_bytes(f.read(4), byteorder='little', signed=False)
        word1 = int.from_bytes(f.read(2), byteorder='little', signed=False)
        word2 = int.from_bytes(f.read(2), byteorder='little', signed=False)
        offset7 = int.from_bytes(f.read(4), byteorder='little', signed=False)
        word3 = int.from_bytes(f.read(2), byteorder='little', signed=False)
        word4 = int.from_bytes(f.read(2), byteorder='little', signed=False)
        
        # Read the list of LONG values
        long_list_size = word2
        long_list = []
        for i in range(long_list_size):
            long_val = int.from_bytes(f.read(4), byteorder='little', signed=False)
            long_list.append(long_val)
        # Check for padding
        padding5 = f.read(long_list_size % 4)
        if padding5 != b'\xcd' * (long_list_size % 4):
            print(f"Warning: padding after long list is {padding5.hex()}, expected {b'\\\\xcd' * (long_list_size % 4)}")

        # Read the list of offsets
        offset_list_size = word4
        offset_list = []
        for i in range(offset_list_size):
            offset_val = int.from_bytes(f.read(4), byteorder='little', signed=False)
            offset_list.append(offset_val)
        # Check for padding
        padding6 = f.read(offset_list_size % 4)
        if padding6 != b'\xcd' * (offset_list_size % 4):
            print(f"Warning: padding after offset list is {padding6.hex()}, expected {b'\\\\xcd' * (offset_list_size % 4)}")

        # Read the plain text strings
        for i, offset in enumerate(offset_list):
            if offset == 0:
                continue
            f.seek(offset)
            text_string = ''
            byte = f.read(1)
            while byte != b'\x00':
                text_string += byte.decode('ascii')
                byte = f.read(1)
                
            # Get a list of all .wpfl files in the current working directory
        wpfl_files = [f for f in os.listdir() if os.path.isfile(f) and f.endswith('.wpfl')]

        # Open the output file and write the data sets for each .wpfl file
        with open('output.txt', 'a') as out:
            for filename in wpfl_files:
                out.write(f"Text String {i}: {text_string} (Offset: {offset})\n")