import os

def write_wpfl_data(filename, output_file):
    with open(filename, 'rb') as f:
        # HEADER 1
        offset1 = int.from_bytes(f.read(4), byteorder='little', signed=False)
        padding1 = f.read(4)
        offset2 = int.from_bytes(f.read(4), byteorder='little', signed=False)
        offset3 = int.from_bytes(f.read(4), byteorder='little', signed=False)
        padding2 = f.read(4)
        offset4 = int.from_bytes(f.read(4), byteorder='little', signed=False)
        offset5 = int.from_bytes(f.read(4), byteorder='little', signed=False)
        long_val = int.from_bytes(f.read(4), byteorder='little', signed=False)
        
        # HEADER 2
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
        
        
        long_list_size = word2
        long_list = []
        for i in range(long_list_size):
            long_val = int.from_bytes(f.read(4), byteorder='little', signed=False)
            long_list.append(long_val)
        # PADDING
        padding5 = f.read(long_list_size % 4)
        if padding5 != b'\xcd' * (long_list_size % 4):
            print(f"Warning: padding after long list is {padding5.hex()}")



        
        # OFFSET
        offset_list_size = word4
        offset_list = []
        for i in range(offset_list_size):
            offset_val = int.from_bytes(f.read(4), byteorder='little', signed=False)
            offset_list.append(offset_val)
        # PADDING
        padding6 = f.read(offset_list_size % 4)
        if padding6 != b'\xcd' * (offset_list_size % 4):
            print(f"Warning: padding after offset list is {padding6.hex()}")

        
        with open(output_file, 'a') as out:
            out.write(f"{filename}\n")
            out.write(f"Offset 1: {offset1}\n")
            out.write(f"Padding 1: {padding1.hex()}\n")
            out.write(f"Offset 2: {offset2}\n")
            out.write(f"Offset 3: {offset3}\n")
            out.write(f"Padding 2: {padding2.hex()}\n")
            out.write(f"Offset 4: {offset4}\n")
            out.write(f"Offset 5: {offset5}\n")
            out.write(f"Long value: {long_val}\n")
            out.write(f"Long value 2: {long_val2}\n")
            out.write(f"Padding 3: {padding3.hex()}\n")
            out.write(f"Padding 4: {padding4.hex()}\n")
            out.write(f"Long value 3: {long_val3}\n")
            out.write(f"Offset 6: {offset6}\n")
            out.write(f"Word 1: {word1}\n")
            out.write(f"Word 2: {word2}\n")
            out.write(f"Offset 7: {offset7}\n")
            out.write(f"Word 3: {word3}\n")
            out.write(f"Word 4: {word4}\n")
            out.write(f"Long list: {long_list}\n")
            out.write(f"Offset list: {offset_list}\n")
            out.write("\n")

 
wpfl_files = [f for f in os.listdir() if os.path.isfile(f) and f.endswith('.wpfl')]

        
with open('output.txt', 'a') as out:
    for filename in wpfl_files:
        write_wpfl_data(filename, 'output.txt')
       
