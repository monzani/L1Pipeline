#!/usr/bin/env python

"""@brief Stuff to deal with ROOT files.

@author W. Focke <focke@slac.stanford.edu>
"""

from os import environ
import config

environ['ROOTSYS']=config.rootSys

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
