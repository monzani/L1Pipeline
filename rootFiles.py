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
    # Or maybe we do.  Check it out.
    print >> sys.stderr, 'Result of header copy: %s' % junk

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


def concatenate(outputFileName, fileNames, treeName='Digi', expectedEntries=None, basketSize=None):

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
    
    print >> sys.stderr, 'Creating output file ...'
    otf = ROOT.TFile.Open(outputFileName, "RECREATE")

    mergeOptions = ['keep']
    if basketSize is None:
        mergeOptions.append('fast')
        basketSize = 0
        print >> sys.stderr, 'Using fast merge.'
    else:
        print >> sys.stderr, 'Changing basket size to %d.' % basketSize       
        pass
    option = ','.join(mergeOptions)
    
    print >> sys.stderr, "Merging ..."
    nFiles = c.Merge(otf, basketSize, option)
    retCode = nFiles != 1

    now = time.time()
    print >> sys.stderr, 'End merge at', time.ctime(now), '(%f elapsed)' % (now - then)
    then = now

    print >> sys.stderr, 'Copying header ...'
    nBytes = copyHeader(fileNames[0], otf)
    print >> sys.stderr, 'wrote %d bytes' % nBytes

    print >> sys.stderr, 'Creating index ...'
    indexEntries = buildIndex(otf, treeName, "m_runId", "m_eventId")
    print >> sys.stderr, '%d entries' % indexEntries
    if indexEntries and indexEntries != expectedEntries:
        print >> sys.stderr, "Bad # entries after indexing."
        return 1
    
    otf.Close()

    print >> sys.stderr, outputFileName, ' created'

    numChainEntries = getFileEvents(outputFileName, treeName)
    print >> sys.stderr, 'numChainEntries = ', numChainEntries
    if numChainEntries != expectedEntries:
        print >> sys.stderr, "Bad # entries after merge."
        return 1

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
    #option = ''
    option = 'fast'
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
    if not header:
        print >> sys.stderr, 'Input file %s has no header.' % inFileName
        inTFile.Close()
        return 0
    outTFile.cd()
    nBytes = header.Write(headerName)
    inTFile.Close()
    return nBytes


def buildIndex(tFile, treeName, major, minor):
    tree = tFile.Get(treeName)
    if not tree:
        print >> sys.stderr, 'TFile %s has no tree %s' % (tFile, treeName)
        return -1
    for branchName in major, minor:
        branch = tree.GetBranch(branchName)
        if not branch:
            print >> sys.stderr, "Tree %s has no branch %s, can't build index" \
                  % (treeName, branchName)
            return 0 # this is not really an error
        continue
    indexEntries = tree.BuildIndex(major, minor)
    return indexEntries


def hSplit(inFile, treeName, crumbData):

    selection = ""
    option = "fast"

    for outFile, numEvents, firstEvent in crumbData:

        # ROOT 5.18 used to let us do these outside the loop
        # but with 5.20, they have to be in here
        oldFP = ROOT.TFile(inFile)
        oldTree = oldFP.Get(treeName)
        
        print >> sys.stderr, outFile, numEvents, firstEvent,
        start = time.time()

        newFP = ROOT.TFile(outFile, "recreate")
        newTree = oldTree.CopyTree(selection, option, numEvents, firstEvent)
        newTree.AutoSave();
        newFP.Close()

        print >> sys.stderr, time.time() - start

        continue

    return


def filter(inFile, treeName, outFile, cut):

    status = 0

    option = "fast"

    oldFP = ROOT.TFile(inFile)
    oldTree = oldFP.Get(treeName)
    
    newFP = ROOT.TFile(outFile, "recreate")
    newTree = oldTree.CopyTree(cut, option, sys.maxint, 0)
    newTree.AutoSave();
    newFP.Close()

    return status


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print >> sys.stderr, 'usage: rootFiles.py treeName outFile inFile1 ...'
        sys.exit(1)
        pass
    
    treeName = sys.argv[1]
    outFile = sys.argv[2]
    inFiles = sys.argv[3:]
    
    concatenate_prune(outFile, inFiles, treeName)
    
