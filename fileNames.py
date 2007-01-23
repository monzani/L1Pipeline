"""@brief Conventions for naming files.

@author W. Focke <focke@slac.stanford.edu>
"""

import os


headFields = 3

def baseHead(inFile):
    """@brief Parses out the portion of a filename that does not depend on
    the file type.
    """

    inDir, inName = os.path.split(inFile)

    cut = inName.rindex('.')
    inBase = inName[:cut]
    allFields = inBase.split('_')

    goodFields = allFields[:headFields]
    head = '_'.join(goodFields)

    return head

def join(parts, ext):
    return '_'.join(parts) + '.' + ext
