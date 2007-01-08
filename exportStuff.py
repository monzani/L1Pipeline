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
