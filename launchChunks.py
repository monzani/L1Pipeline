#!/usr/bin/env python

"""@brief Launch chunk substreams.

@author W. Focke <focke@slac.stanford.edu>
"""

# Too bad we can't get the separator value from config
argList = chunkList.split('*')

# Launch a subStream for each run
for iStream, args in enumerate(argList):
    pipeline.createSubstream("doChunk", iStream+1, args)
    continue
