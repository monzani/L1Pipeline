"""@brief Make SVAC tuple.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys

if __name__ == "__main__":
    print >> sys.stderr, "This module is not supported as main script"
    sys.exit(1)

import config

import fileNames
import runner


def svacTuple(files, idArgs, workDir, **args):
    status = 0

    stagedDigiFile = files['digi']
    stagedReconFile = files['recon']

    stagedSvacFile = files['svac']

    realHistFile = fileNames.fileName('svacHist', *idArgs)
    stagedHistFile = os.path.join(workDir, os.path.basename(realHistFile))

    # make an empty file to use as dummy MC
    mcFile = os.path.join(workDir, 'emptyFile')
    open(mcFile, 'w').close()

    # contents of JO file
    options = \
"""%(mcFile)s
%(stagedDigiFile)s
%(stagedReconFile)s
%(stagedSvacFile)s
%(stagedHistFile)s
""" \
    % locals()

    # write JO file
    optionFile = os.path.join(workDir, 'jobOptions.txt')
    open(optionFile, 'w').write(options)

    # do the work
    svacTupleApp = config.apps['svacTuple']
    l1Setup = config.l1Setup
    instDir = config.L1Build
    glastExt = config.glastExt

    cmd = """
    cd %(workDir)s
    export INST_DIR=%(instDir)s 
    export GLAST_EXT=%(glastExt)s
    source %(l1Setup)s
    %(svacTupleApp)s %(optionFile)s
    """ % locals()

    status |= runner.run(cmd)

    return status
