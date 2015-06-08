#!/afs/slac/g/glast/isoc/flightOps/rhel5_gcc41/ISOC_PROD/bin/shisoc python2.6


def expand(inFile, outFile, dic):
    inData = open(inFile).read()
    outData = inData % dic
    open(outFile, 'w').write(outData)
    return
