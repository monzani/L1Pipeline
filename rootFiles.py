#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Stuff to deal with ROOT files.

@author W. Focke <focke@slac.stanford.edu>
"""

import sys
import time

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

    now = time.time()
    print >> sys.stderr, 'Start scan at', time.ctime(now)
    then = now

    scanEntries = 0
    for iFile, name in enumerate(fileNames):
        print >> sys.stderr, "Adding %d [%s]" % (iFile, name),
        fileEntries = getFileEvents(name, treeName)
        print >> sys.stderr, "%d entries." % fileEntries
        scanEntries += fileEntries
        addCode = c.Add(name, 0)
        if not addCode: # TChain.Add returns 1 for success, 0 for failure
            return 1
        pass

    now = time.time()
    print >> sys.stderr, 'End scan at', time.ctime(now), '(%f elapsed)' % (now - then)
    then = now

    print >> sys.stderr, 'scanEntries = ', scanEntries
    if expectedEntries is not None:
        if scanEntries != expectedEntries:
            print >> sys.stderr, "Bad # entries after input scan."
            return 1
        pass
    expectedEntries = scanEntries
    
    numChainEntries = c.GetEntries()
    print >> sys.stderr, 'numChainEntries = ', numChainEntries
    if numChainEntries != expectedEntries:
        print >> sys.stderr, "Bad # entries after chain creation."
        return 1
    
    gSystem.Load('libpipelineDatasets.so')
    from ROOT import pruneTuple

    print >> sys.stderr, "Merging..."

    pt = pruneTuple(c, outputFileName)

    # we don't really care if this succeeds or not...
    junk = pt.copyHeader(fileNames[0])

    # Here's where the real work happens
    retCode = pt.prune()

    now = time.time()
    print >> sys.stderr, 'End merge at', time.ctime(now), '(%f elapsed)' % (now - then)
    then = now

    numChainEntries = getFileEvents(outputFileName, treeName)
    print >> sys.stderr, 'numChainEntries = ', numChainEntries
    if numChainEntries != expectedEntries:
        print >> sys.stderr, "Bad # entries after merge."
        return 1
    
    print >> sys.stderr, outputFileName, ' created\n'

    return retCode


def concatenate_cal(outputFileName, fileNames, treeName='Digi', expectedEntries=None):

    from ROOT import TChain, gSystem
    
    c = TChain(treeName)
    c.SetMaxTreeSize(500000000000)

    if expectedEntries is not None:
        print >> sys.stderr, "Expect %d entries." % expectedEntries
        pass

    scanEntries = 0
    for iFile, name in enumerate(fileNames):
        print >> sys.stderr, "Adding %d [%s]" % (iFile, name),
        fileEntries = getFileEvents(name, treeName)
        print >> sys.stderr, "%d entries." % fileEntries
        scanEntries += fileEntries
        addCode = c.Add(name, 0)
        if not addCode: # TChain.Add returns 1 for success, 0 for failure
            return 1
        pass
    print >> sys.stderr, 'scanEntries = ', scanEntries
    if expectedEntries is not None:
        if scanEntries != expectedEntries:
            print >> sys.stderr, "Bad # entries after input scan."
            return 1
        pass
    expectedEntries = scanEntries
    
    numChainEntries = c.GetEntries()
    print >> sys.stderr, 'numChainEntries = ', numChainEntries
    if numChainEntries != expectedEntries:
        print >> sys.stderr, "Bad # entries after chain creation."
        return 1
    
    print >> sys.stderr, "Merging..."

    #basketSize = 32000 # default
    basketSize = 1000000 # recommended by Rene
    option = ''
    #option = 'fast'
    otf = ROOT.TFile.Open(outputFileName, "RECREATE")
    nFiles = c.Merge(otf, basketSize, option)
    retCode = nFiles != 1

    numChainEntries = getFileEvents(outputFileName, treeName)
    print >> sys.stderr, 'numChainEntries = ', numChainEntries
    if numChainEntries != expectedEntries:
        print >> sys.stderr, "Bad # entries after merge."
        return 1
    
    #print >> sys.stderr, outputFileName, ' created\n'

    return retCode


def copyHeader(inFileName, outTFile):
    headerName = 'header'
    inTFile = ROOT.TFile.Open(inFileName)
    header = inTFile.Get(headerName)
    outTFile.cd()
    header.Write(headerName)
    return


def hSplit(inFile, treeName, crumbData):

    selection = ""
    option = "fast"

    oldFP = ROOT.TFile(inFile)
    oldTree = oldFP.Get(treeName)

    for outFile, numEvents, firstEvent in crumbData:

        print >> sys.stderr, outFile, numEvents, firstEvent,
        start = time.time()

        newFP = ROOT.TFile(outFile, "recreate")
        newTree = oldTree.CopyTree(selection, option, numEvents, firstEvent)
        newTree.AutoSave();
        newFP.Close()

        print >> sys.stderr, time.time() - start

        continue

    return


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print >> sys.stderr, 'usage: rootFiles.py treeName outFile inFile1 ...'
        sys.exit(1)
        pass
    
    treeName = sys.argv[1]
    outFile = sys.argv[2]
    inFiles = sys.argv[3:]
    
    concatenate_prune(outFile, inFiles, treeName)
    
