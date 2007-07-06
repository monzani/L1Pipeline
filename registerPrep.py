

import os
import sys

import pipeline

def prep(fileType, fileName):
    """
    Deal with batch-side prep to register a file with the data catalog.
    Actual registration is done by a scriptlet (in registerStuff.py).
    This sets up some pipeline variables so the scriptlet knows what to do.
    """

    fileType = fileType.upper()
    junk, base = os.path.split(fileName)
    logipath = '/'.join(['/L1Proc', fileType, base])
    print >> sys.stderr, "logipath=[%s], filepath=[%s]" % (logipath, fileName)
    pipeline.setVariable('REGISTER_LOGIPATH', logipath)
    pipeline.setVariable('REGISTER_FILEPATH', fileName)

    return
