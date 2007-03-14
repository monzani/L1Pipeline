#!/usr/bin/env python

"""@brief Launch cleanup for newly-retired runs.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys

import config
import fileNames
import pipeline

dlDir = os.environ['DOWNLINK_RAWDIR']

# the name of this file is a contract with the halfpipe
retireFile = os.path.join(dlDir, 'retired_runs.txt')

# set up a subStream for each run
for iRun, line in open(retireFile):

    runId, runStatus = line.split()

    if runStatus not in ['COMPLETE', 'INCOMPLETE']:
        print >> sys.stderr, "Bad status %s for run %s, not cleaning up" % (runStatus, runId)
        continue
    
    args = "RUNID=%(runId)s" % locals()
    pipeline.createSubStream("cleanupRun", iRun, args)
    continue
