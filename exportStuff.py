#!/afs/slac/g/glast/isoc/flightOps/rhel6_gcc44/ISOC_PROD/bin/shisoc python2.6

"""@brief Export completed runs to SSC.

This should run after the FT1 files from all runs in a downlink have been
registered with the data server.  It will export FT1 files for all runs which
are done to the SSC.  "Done," in this context, means:

either

We have recieved and processed all data from the run.

or

We know that we will not receive any more data for the run (probably because
the run is missing data and it has been over a week since it was taken).

This will require keeping track either of which runs have been sent or
(probably more efficient) which ones are "in process."

@todo Write the code.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys
import time

import config

import GPLinit

import fileNames
import runner
import pipeline
import stageFiles


head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']
fileType = os.environ['fileType']

# Where do we send the data?
if config.testMode:
    # send = ""             # noop
    send = "--send LISOC" # loopback test
else:
    send = "--send GSSC"  # the real deal
    # send = "--send LISOC" # always test mode for now
pass

staged = stageFiles.StageSet(excludeIn=config.excludeIn)
finishOption = config.finishOption

inputFile = fileNames.fileName(fileType, dlId, runId)
stagedInFile = staged.stageIn(inputFile)
args = stagedInFile

isocBin = config.isocBin
outCfg = config.fastCopyCfg

cmd = """eval `%(isocBin)s/isoc env --add-env=flightops`
ISOC_SITEDEP=%(outCfg)s FASTCopy.py %(send)s %(args)s
""" % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

exportTime = time.time()
pipeline.setVariable("exportTime", exportTime)

status |= staged.finish(finishOption)

sys.exit(status)
