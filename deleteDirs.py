#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Delete no-longer-needed directories and their contents.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys

import fileNames
import runner

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)

runId = os.environ.get('RUNID')
if runId is not None:
    runStatus = os.environ['RUNSTATUS']

    chunkId = os.environ.get('CHUNK_ID')
    if chunkId is not None:
        level = 'chunk'
    else:
        level = 'run'
        dlId = '*'
        pass
else:
    level = 'downlink'
    chunkId = None
    pass

# This decision should be made at a higher level.
if level == 'run' and runStatus not in ['COMPLETE', 'INCOMPLETE']:
    print >> sys.stderr, 'Run %s has status %s, not deleting chunks.' \
          % (runId, runStatus)
    sys.exit(0)
    pass

goners = fileNames.findPieces(None, dlId, runId, chunkId)

for goner in goners:
    print >> sys.stderr, "Deleting %s." % goner
    cmd = 'rm -rf %(goner)s' % locals()
    runner.run(cmd)
    print >> sys.stderr, '%s has left the building.' % goner
    continue
