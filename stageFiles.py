
"""@brief Manage staging of files to/from machine-local disk.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import shutil

try:
    defaultStageArea = os.environ['STAGEDIR']
except KeyError:
    defaultStageArea = '/scratch'
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


    def __init__(self, stageName=None, stageArea=None):
        """@brief Set up a staging area.
        @param [stageName] Name of directory where staged copies are kept.
        @param [stageArea] Parent of directory where staged copies are kept.
        """
        
        if stageArea is None:
            stageArea = defaultStageArea
            pass
        if stageName is None:
            stageName = `os.getpid()`
            pass
        self.stageDir = os.path.join(stageArea, stageName)
        os.mkdir(self.stageDir)

        self.inFiles = {}
        self.outFiles = {}
        
        return

    def stageIn(self, inFile):
        """@brief Stage an input file.
        @param inFile real name of the input file
        @return name of the staged file
        """
        stageName = self.stagedName(inFile)
        try:
            shutil.copy(inFile, stageName)
        except OSError:
            stageName = inFile
        return stageName
    
    def stageOut(self, outFile):
        """@brief Stage an output file.
        @param outFile real name of the output file
        @return name of the staged file
        """
        stageName = self.stagedName(outFile)
        return stageName

    def finish(self):
        """@brief Delete staged inputs, move outputs to final destination.
        """
        for stageName in self.inFiles.values():
            os.remove(stageName)
            pass
        for realName, stageName in self.outFiles.items():
            shutil.move(stageName, realName)
            pass
        os.rmdir(self.stageDir)
        return
    
    def stagedName(self, fileName):
        """@brief Generate names of staged files.
        @param fileName Real name of file.
        @return Name of staged file.
        """
        base = os.path.basename(fileName)
        stageName = os.path.join(self.stageDir, base)
        return stageName
