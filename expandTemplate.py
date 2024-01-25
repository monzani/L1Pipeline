#!/sdf/data/fermi/a/isoc/flightOps/rhel6_gcc44/ISOC_PROD/bin/shisoc python2.6


def expand(inFile, outFile, dic):
    inData = open(inFile).read()
    outData = inData % dic
    open(outFile, 'w').write(outData)
    return
