
"""@brief Manage staging of files to/from machine-local disk.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import shutil
import sys

import runner

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

        print >> sys.stderr, \
              "Attempting to set up staging area [%s]" \
              % self.stageDir
        try:
            os.mkdir(self.stageDir)
            self.staged = True
            print >> sys.stderr, "Success!"
        except OSError:
            print >> sys.stderr, "Failed!"
            self.staged = False
            # override some methods so they don't have to be full of
            # tedious condition checks
            self.stageIn = self.noOp
            self.stageOut = self.noOp
            self.stagedName = self.noOp                        
            pass

        self.inFiles = {}
        self.outFiles = {}
        
        return

    def stageIn(self, inFile):
        """@brief Stage an input file.
        @param inFile real name of the input file
        @return name of the staged file
        """
        stageName = self.stagedName(inFile)
        print >> sys.stderr, \
              "Attempting to stage [%s] to [%s]" \
              % (inFile, stageName)
        try:
            shutil.copy(inFile, stageName)
            self.inFiles[inFile] = stageName
            print >> sys.stderr, "Success!"
            os.system('ls -l %s/*' % self.stageDir)
        except OSError:
            print >> sys.stderr, "Failed!  Forging ahead with unstaged file."
            stageName = inFile
        return stageName
    
    def stageOut(self, outFile):
        """@brief Stage an output file.
        @param outFile real name of the output file
        @return name of the staged file
        """
        stageName = self.stagedName(outFile)
        print >> sys.stderr, \
              "Expecting output file [%s], will move to [%s]" \
              % (stageName, outFile)
        self.outFiles[outFile] = stageName
        return stageName

    def finish(self):
        """@brief Delete staged inputs, move outputs to final destination.
        """
        for stageName in self.inFiles.values():
            print >> sys.stderr, "Deleting [%s]" % stageName
            os.remove(stageName)
            pass
        for realName, stageName in self.outFiles.items():
            print >> sys.stderr, "Moving [%s] to [%s]" % (stageName, realName)
            shutil.move(stageName, realName)
            pass
        if self.staged:
            print >> sys.stderr, "Deleting [%s]" % self.stageDir
            try:
                os.rmdir(self.stageDir)
            except OSError:
                print >> sys.stderr, "Terrible hack for staging issue! FIX ME!"
                os.system('ls -lah %s/*' % self.stageDir)
                runner.run('rm -rf %s' % self.stageDir)
                pass
            pass
        return
    
    def stagedName(self, fileName):
        """@brief Generate names of staged files.
        @param fileName Real name of file.
        @return Name of staged file.
        """
        base = os.path.basename(fileName)
        stageName = os.path.join(self.stageDir, base)
        return stageName

    def noOp(self, input):
        return input
    
