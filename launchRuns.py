#!/usr/bin/env python

"""@brief Find new run directories.

@author W. Focke <focke@slac.stanford.edu>
"""

dlId = os.environ['DOWNLINK_ID']
dlRawDir = os.environ['DOWNLINK_RAWDIR']

# Too bad we can't get the separator value from config
argList = runList.split('*')

# Launch a subStream for each run
for iStream, args in enumerate(argList):
    pipeline.createSubstream("doRun", iStream+1, args)
    continue
