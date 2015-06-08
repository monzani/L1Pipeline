import os

def copyFiles(files, inFileTypes, outFileTypes, workDir, **args):
    status = 0

    for ift in inFileTypes:
        oft = ift + 'NoQual'
        os.link(files[ift], files[oft])
        continue
    
    return status
