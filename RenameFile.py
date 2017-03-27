import os

path = r'pages/'

def renameAll(path):
    filelist = os.listdir(path)
    for file in filelist:
        filename = file
        oldpath = os.path.join(path, filename)

        # print(filename)

        if filename.find('_') >= 0:
            filename = filename.replace('_', '')

        if filename.find('-') >= 0:
            filename = filename.replace('-', '')

        # print(filename + '\n')

        newpath = os.path.join(path, filename)
        if not os.path.isfile(newpath):
            os.rename(oldpath, newpath)
    print('complete')


renameAll(path)