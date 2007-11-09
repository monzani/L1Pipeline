
import itertools
import os
import random
import sys

import config

import procDirs

dlId = os.environ['DOWNLINK_ID']

def balance(pieces, runId, chunkId=None):
    if chunkId is None:
        level = 'run'
    else:
        level = 'chunk'
        pass
    
    stageBases = list(config.stageDirs)
    random.shuffle(stageBases)
    for piece, stageBase in zip(pieces, itertools.cycle(stageBases)):
        if level == 'run':
            dirs = procDirs.setup(dlId, runId, piece)
            link = dirs['chunk']
            stageDir = procDirs.getStageDir(stageBase, runId, piece)
        else:
            dirs = procDirs.setup(dlId, runId, chunkId, piece)
            link = dirs['crumb']
            stageDir = procDirs.getStageDir(stageBase, runId, chunkId, piece)
            pass

        procDirs.mkdir(stageDir)
        
        if os.path.exists(link):
            try:
                os.remove(link)
            except OSError:
                os.rmdir(link)
                pass
            pass
        else:
            procDirs.mkdir(link)
            os.rmdir(link)
            pass

        print >> sys.stderr, 'Linking %s to %s' % (stageDir, link)
        os.symlink(stageDir, link)
        continue
    return
