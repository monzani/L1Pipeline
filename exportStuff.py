#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

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

import config

import GPLinit

import fileNames
import runner
import stageFiles

# Where do we send the data?
if config.testMode:
    # send = ""             # noop
    send = "--send LISOC" # loopback test
else:
    # send = "--send GSSC"  # the real deal
    send = "--send LISOC" # always test mode for now
pass

staged = stageFiles.StageSet()

files = fileNames.setup(os.environ['DOWNLINK_ID'], os.environ['RUNID'])
exportFile = files['run'][os.environ['fileType']]

stagedFile = staged.stageIn(exportFile)

args = stagedFile

isocBin = config.isocBin

cmd = """eval `%(isocBin)s/isoc env --add-env=flightops`
FASTCopy.py %(send)s %(args)s
""" % locals()

status = runner.run(cmd)

status |= staged.finish()

sys.exit(status)
