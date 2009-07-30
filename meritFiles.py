#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import ROOT

def startAndStop(fileName, treeName='MeritTuple'):
    from ROOT import TFile, TTree, TChain

    file = TFile(fileName)
    tree = file.Get(treeName)
    numEntries = tree.GetEntries()

    vals = []
    for pos in (0, numEntries-1):
        iEntry = tree.LoadTree(pos)
        if iEntry < 0: raise IndexError, 'Bad LoadTree'
        bytes = tree.GetEntry(pos)
        if bytes <= 0: raise IOError, 'Bad GetEntry'
        vals.append(tree.EvtElapsedTime)
        continue
    return tuple(vals)


def main():
    import sys
    fileNames = sys.argv[1:]
    for fileName in fileNames:
        start, stop = startAndStop(fileName)
        print "%s %.17f %.17f" % (fileName, start, stop)
        continue
    return

if __name__ == "__main__":
    main()
    
