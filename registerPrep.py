

import os
import sys

import fileNames
import pipeline

def prep(fileType, fileName):
    """
    Deal with batch-side prep to register a file with the data catalog.
    Actual registration is done by a scriptlet (in registerStuff.py).
    This sets up some pipeline variables so the scriptlet knows what to do.
    """

    logiPath = fileNames.dataCatName(fileType, fileName)
    filePath = fileNames.sitedName(fileName)
    print >> sys.stderr, "logipath=[%s], filepath=[%s]" % (logiPath, filePath)
    pipeline.setVariable('REGISTER_LOGIPATH', logiPath)
    pipeline.setVariable('REGISTER_FILEPATH', filePath)

    return
