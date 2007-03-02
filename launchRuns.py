#!/usr/bin/env python

"""@brief Launch run substreams.

@author W. Focke <focke@slac.stanford.edu>
"""

# Too bad we can't get the separator value from config
argList = runList.split('*')

# Launch a subStream for each run
for iStream, args in enumerate(argList):
    pipeline.createSubstream("doRun", iStream, args)
    continue
