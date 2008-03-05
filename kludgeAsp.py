#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Find new run directories.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys

import config

import GPLinit

import glastTime
import runner

status = 0

# dlRawDir = os.environ['DOWNLINK_RAWDIR']

# head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
# if not dlId: head, dlId = os.path.split(head)

# start = {}
# stop = {}
# boundaryFile = os.path.join(dlRawDir, 'event_times_%s.txt' % dlId)
# try:
#     lines = open(boundaryFile)
# except IOError:
#     print >> sys.stderr, "Couldn't open run boundary file %s" % boundaryFile
#     lines = []
#     pass
# for line in lines:
#     runId, tStart, tStop = line.strip().split()
#     start[runId] = glastTime.met(float(tStart))
#     stop[runId] = glastTime.met(float(tStop))
#     continue

# firstStart = min(start.values())
# lastStop = max(stop.values())

# print >> sys.stderr, "First run starts at %f" % firstStart
# print >> sys.stderr, "Last run stops at %f" % lastStop

# cmd = 'pipeline createStream --stream %s --define firstStart=%.17g --define lastStop=%.17g aspStart' % (dlId, firstStart, lastStop)

os.environ['nDownlink'] = os.environ['DOWNLINK_ID']
os.environ['folder'] = config.dataCatDir
cmd = config.aspLauncher

#print >> sys.stderr, "Not running [%s]" % cmd
status = runner.run(cmd)

sys.exit(status)
