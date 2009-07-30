#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import numpy as N
import pyfits

clobber = True


def mergeFiles(outFile, inFiles):
    status = 0

    files = [pyfits.open(inFile) for inFile in inFiles]
    if not checkFiles(files):
        print >> sys.stderr, "Files don't match."
        return 1

    primary = files[0][0]
    pHead = primary.header
    outBase = os.path.basename(outFile)
    pHead.update('FILENAME', outBase)
    del pHead['CHECKSUM']

    copyKeyWords(pHead, files[-1][0].header)
    
    hduList = pyfits.HDUList([primary])

    nHdu = len(files[0])
    for iHdu in range(1, nHdu):
        hduList.append(mergeHdus([xx[iHdu]  for xx in files]))
        continue
    
    hduList.writeto(outFile, clobber=clobber)

    return status


def checkFiles(inputs):
    status = True
    baseline = len(inputs[0])
    for input in inputs: status &= (len(input) == baseline)
    return status


def mergeHdus(inputs):
    if not checkHdus(inputs): raise ValueError, "HDUs don't match."

    header = inputs[0].header
    del header['CHECKSUM']
    del header['DATASUM']

    copyKeyWords(header, inputs[-1].header)

    columns = inputs[0].columns

    nRows = 0
    for hdu in inputs: nRows += hdu.data.shape[0]

    newHdu = pyfits.new_table(columns, header=header, nrows=nRows)
    for name in columns.names:
        newColumn = N.concatenate([hdu.data.field(name) for hdu in inputs ])
        newHdu.data.field(name)[:] = newColumn
        continue

    return newHdu


def checkHdus(inputs):
    status = True
    baseline = inputs[0].columns
    #for hdu in inputs[1:]: status &= (hdu.columns == baseline)
    return status


kwToCopy = ['DATE-END', 'TSTOP']
def copyKeyWords(target, source):
    for kw in kwToCopy:
        target.update(kw, source[kw])
        continue
    return


def main():
    outFile = sys.argv[1]
    inFiles = sys.argv[2:]
    mergeFiles(outFile, inFiles)
    return


if __name__ == "__main__":
    main()
    
