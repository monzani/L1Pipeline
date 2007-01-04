#!/usr/bin/env python


def expand(inFile, outFile, dic):
    inData = open(inFile).read()
    outData = inData % dic
    open(outFile, 'w').write(outData)
    return
