#!/usr/bin/env python

"""@brief Delete no-longer-needed directories and their contents.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys

import procDirs
import runner

runId = os.environ['RUNID']

try:
    chunkId = os.environ['CHUNK_ID']
    dlId = os.environ['DOWNLINK_ID']
    level = 'crumb'
except KeyError:
    chunkId = None
    dlId = '*'
    level = 'chunk'
    pass

goners = procDirs.findPieceDirs(dlId, runId, chunkId)

for goner in goners:
    print >> sys.stderr, "NOT running: 'rm -rf %s'." % goner
    #runner.run('rm -rf %s' % goner)
    print >> sys.stderr, '%s has left the building.' % goner
    continue
