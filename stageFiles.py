
"""@brief Manage staging of files to/from machine-local disk.

@author W. Focke <focke@slac.stanford.edu>
"""

import os

try:
    stageBase = os.environ['STAGEDIR']
except KeyError:
    stageBase = '/scratch'
    pass

class StageSet:

    """@brief Manage staging of files to/from machine-local disk.

    simple example:
    > stagedStuff = StageSet()
    > sIn = stagedStuff.stageIn(inFile)
    > sOut = stagedStuff.stageOut(outFile)
    > os.system('do_something < %s > %s' % (sIn, sOut))
    > stagedStuff.finish()
    instead of:
    > os.system('do_something < %s > %s' % (inFile, outFile))

    The values returned by stageIn and stageOut may be the same as
    their inputs if staging is not possible.

    @todo Implement staging functionality.

    @todo Write out a persistent representation so that multiple processes
    could use the same staging set, and only the last one to run would
    call finish().  Or maybe have some way that processes could register
    a "hold" on the set, and calls to finish would have no effect until all
    holds had been released.
    """


    def __init__(self):
        self.inFiles = {}
        self.outFiles = {}
        return

    def stageIn(self, inFile):
        """@brief Stage an input file.
        @param inFile real name of the input file
        @return name of the staged file
        """
        stageName = inFile
        return stageName
    
    def stageOut(self, outFile):
        """@brief Stage an output file.
        @param outFile real name of the output file
        @return name of the staged file
        """
        stageName = outFile
        return stageName

    def finish(self):
        """@brief Delete staged inputs, move outputs to final destination.
        """
        for stageName in self.inFiles.values():
            os.remove(stageName)
            pass
        for realName, stageName in self.outFiles.items():
            os.rename(stageName, realName)
            pass
        return
    
