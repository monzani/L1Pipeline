#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Delete no-longer-needed directories and their contents.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys

import config

import fileOps
import fileNames
import runner

status = 0

dlRawDir = os.environ['DOWNLINK_RAWDIR']
head, dlId = os.path.split(dlRawDir)
if not dlId: head, dlId = os.path.split(head)

runId = os.environ.get('RUNID')
if runId is not None:
    # runStatus = os.environ['RUNSTATUS']

    chunkId = os.environ.get('CHUNK_ID')
    if chunkId is not None:
        level = 'chunk'
    else:
        level = 'run'
        dlId = '*'
        pass

    # check if mergeStuff has supressed cleanup due to missing files
    mergeLock = fileNames.checkMergeLock(runId)
    if mergeLock:
        print >> sys.stderr, '''Cleanup is supressed by %s''' % mergeLock
        sys.exit(1)
        pass
    
else:
    level = 'downlink'
    chunkId = None
    pass

goners = fileNames.findPieces(None, dlId, runId, chunkId)

if level == 'downlink':
    if config.saveDl:
        dest = fileNames.dlDirectory(dlRawDir)
        if os.path.isdir(dest):
            print >> sys.stderr, '%(dlRawDir)s has already ben saved, deleting.' % locals()
            goners.append(dlRawDir)
        elif os.path.isdir(dlRawDir):
            fileOps.mkdirFor(dest)
            cmd = 'mv %(dlRawDir)s %(dest)s' % locals()
            status |= runner.run(cmd)
            pass
    else:
        goners.append(dlRawDir)
        pass
    pass
elif level == 'run':
    goners.append(fileNames.tokenDir(head, runId))
    pass

totG = len(goners)
for ig, goner in enumerate(goners):
    if config.doCleanup:
        print >> sys.stderr, "Deleting %s. (%d/%d)" % (goner, ig+1, totG)
        status |= fileOps.rmtree(goner)
        print >> sys.stderr, '%s has left the building.' % goner
    else:
        print >> sys.stderr, "NOT Deleting %s." % goner
        pass
    continue

sys.exit(status)
