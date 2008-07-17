#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import config

import GPLinit

import fileNames

inList = sys.argv[1]
inFiles = [line.strip() for line in open(inList)]

sep = '/%s/' % config.stageBase

outFiles = []
for inFile in inFiles:
    oldBaseDir, junk, relativePath = inFile.partition(sep)[-1]
    newBaseDir = fileNames.stageBalance(relativePath)
    outFiles.append(os.path.join(newBaseDir, relativePath))
    continue
