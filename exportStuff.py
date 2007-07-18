#!/usr/bin/env python

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

import fileNames
import runner
import stageFiles

# Where do we send the data?
# Should select this based on test or prod mode.
#send = ""             # noop
#send = "--send LISOC" # loopback test
send = "--send GSSC"  # the real deal

staged = stageFiles.StageSet()

files = fileNames.setup(os.environ['DOWNLINK_ID'], os.environ['RUNID'])
exportFile = files['run'][os.environ['fileType']]

stagedFile = staged.stageIn(exportFile)

args = stagedFile

cmd = """. /u/gl/glastops/isoc_config_devel.sh
FASTCopy.py %(send)s %(args)s
""" % locals()

runner.run(cmd)

staged.finish()
