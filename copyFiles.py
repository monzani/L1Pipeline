#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os

def copyFiles(files, inFileTypes, outFileTypes, workDir, **args):
    status = 0

    for ift in inFileTypes:
        oft = ift + 'NoQual'
        os.link(files[ift], files[oft])
        continue
    
    return status
