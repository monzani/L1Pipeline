#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Do TKR analysis.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys

if __name__ == "__main__":
    print >> sys.stderr, "This module is not supported as main script"
    sys.exit(1)

import config

import runner


def tkrAnalysis(files, workDir, **args):
    status = 0

    stagedDigiFile = files['digi']
    stagedReconFile = files['recon']

    stagedOutFile = files['tkrAnalysis']

    # do the work
    app = config.apps['tkrAnalysis']
    cmtScript = config.packages['calibTkrUtil']['setup']

    cmd = """
cd %(workDir)s
source %(cmtScript)s
%(app)s %(stagedDigiFile)s %(stagedReconFile)s %(stagedOutFile)s
""" % locals()

    status |= runner.run(cmd)

    return status
