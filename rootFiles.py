#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Stuff to deal with ROOT files.

@author W. Focke <focke@slac.stanford.edu>
"""

import sys

import ROOT
ROOT.gSystem.Load('libcommonRootData.so')
ROOT.gSystem.Load('libdigiRootData.so')
ROOT.gSystem.Load('libreconRootData.so')


def getFileEvents(fileName, treeName='Digi'):

    from ROOT import TFile, TTree, TChain

    file = TFile(fileName)
    tree = file.Get(treeName)

    numEntries = tree.GetEntries()

    return numEntries


def concatenate_prune(outputFileName, fileNames, treeName='Digi', expectedEntries=None):

    from ROOT import TChain, gSystem
    
    c = TChain(treeName)
    c.SetMaxTreeSize(500000000000)

    if expectedEntries is not None:
        print >> sys.stderr, "Expect %d entries." % expectedEntries
        pass

    for name in fileNames:
        print >> sys.stderr, "Adding [%s] " % name
        addCode = c.Add(name, 0)
        if not addCode: # TChain.Add returns 1 for success, 0 for failure
            return 1
        pass
    
    numChainEntries = c.GetEntries()
    print >> sys.stderr, 'numChainEntries = ', numChainEntries
    if expectedEntries is not None:
        if numChainEntries != expectedEntries:
            print >> sys.stderr, "Bad # entries after chain creation."
            return 1
        pass
    
    gSystem.Load('libpipelineDatasets.so')


    from ROOT import pruneTuple

    print >> sys.stderr, "Merging..."

    pt = pruneTuple(c, outputFileName)

    # we don't really care if this succeeds or not...
    junk = pt.copyHeader(fileNames[0])

    retCode = pt.prune()

    numChainEntries = getFileEvents(outputFileName, treeName)
    print >> sys.stderr, 'numChainEntries = ', numChainEntries
    if expectedEntries is not None:
        if numChainEntries != expectedEntries:
            print >> sys.stderr, "Bad # entries after merge."
            return 1
        pass
    
    #print >> sys.stderr, outputFileName, ' created\n'

    return retCode


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print >> sys.stderr, 'usage: rootFiles.py treeName outFile inFile1 ...'
        sys.exit(1)
        pass
    
    treeName = sys.argv[1]
    outFile = sys.argv[2]
    inFiles = sys.argv[3:]
    
    concatenate_prune(outFile, inFiles, treeName)
    
