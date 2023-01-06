import os

# Set the directory you want to start from
rootDir = 'C:/Users/user/Downloads/P4Toolkit/brook'
i = 1

for dirName, subdirList, fileList in os.walk(rootDir):
    print('Found directory: %s' % dirName)
    for fname in fileList:
        if fname.endswith('.dae'):
            old_name = os.path.join(dirName, fname)
            new_name = os.path.join(dirName, 'bk_' + str(i) + '.dae')
            os.rename(old_name, new_name)
            i += 1