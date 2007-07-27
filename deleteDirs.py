#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Delete no-longer-needed directories and their contents.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys

import procDirs
import runner

runId = os.environ['RUNID']
runStatus = os.environ['RUNSTATUS']

try:
    chunkId = os.environ['CHUNK_ID']
    dlId = os.environ['DOWNLINK_ID']
    level = 'crumb'
except KeyError:
    chunkId = None
    dlId = '*'
    level = 'chunk'
    pass

if level == 'chunk' and runStatus not in ['COMPLETE', 'INCOMPLETE']:
    print >> sys.stderr, 'Run %s has status %s, not deleting chunks.' \
          % (runId, runStatus)
    sys.exit(0)
    pass

goners = procDirs.findPieceDirs(dlId, runId, chunkId)

for goner in goners:
    print >> sys.stderr, "Running: 'rm -rf %s'." % goner
    runner.run('rm -rf %s' % goner)
    print >> sys.stderr, '%s has left the building.' % goner
    continue
