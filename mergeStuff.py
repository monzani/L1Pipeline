#!/usr/bin/env python

"""@brief Merge results of chunk or crumb processing.

@author W. Focke <focke@slac.stanford.edu>
"""

import glob
import os
env = os.environ
import re
import sys

#import runner

import config

import fileNames

# figure out what we're supposed to be doing from process name
taskName = env['PIPELINE_PROCESS']
taskRe = re.compile('^merge(.*)(Chunk|Crumb)s$')
match = taskRe.match(taskName)
if not match:
    print >> sys.stderr, "Bad task name %s" % taskName
    sys.exit(1)
    pass
fileType, level = match.groups()
level = level.lower()

# find input files
if level == 'chunk':
    chunkId = '*'
    crumbId = None
elif level == 'crumb':
    chunkId = env['CHUNKID']
    crumbId = '*'
else:
    print >> sys.stderr, 'Bad merge level %s' % level
    sys.exit(1)
    pass
files = fileNames.setup(env['DOWNLINK_ID'], chunkId, crumbId, createDirs=False)
pattern = files[fileType][level]
inFiles = glob.glob(pattern)

#env['outFile']="larry_recon.root"
#env['inFiles']="larry_recon_1.root larry_recon_2.root larry_recon_3.root"

##wbf## os.system(config.hadd+" "+env['outFile']+" "+env['inFiles'])
cmd = config.hadd+" "+env['outFile']+" "+env['inFiles']
#cmd = config.hadd + (' %s' % outFile) + ((' %s' * len(inFiles)) % tuple(inFiles))

status = runner.run(cmd)
sys.exit(status)
