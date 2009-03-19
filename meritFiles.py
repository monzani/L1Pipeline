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
