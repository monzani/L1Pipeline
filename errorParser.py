#!/afs/slac/g/glast/isoc/flightOps/rhel6_gcc44/ISOC_PROD/bin/shisoc python2.6

import sys

import xml.dom.minidom as md

def parseErrorFile(inFile):
    return dict(
        (error.getAttribute('code'), int(error.getAttribute('quantity')))
        for error in md.parse(open(inFile)).getElementsByTagName('errorType')
        )

def writeXmlOutput(errorCountsDict, filename):
    # cadged from fastMon
    from pXmlWriter import pXmlWriter
    xmlWriter  = pXmlWriter(filename)
    xmlWriter.openTag('errorContribution')
    xmlWriter.indent()
    xmlWriter.writeComment('Summary by error code')
    xmlWriter.openTag('errorSummary')
    xmlWriter.indent()
    for (code, number) in errorCountsDict.items():
        xmlWriter.writeTag('errorType', {'code':code, 'quantity': number })
        continue
    xmlWriter.backup()
    xmlWriter.closeTag('errorSummary')
    xmlWriter.backup()
    xmlWriter.closeTag('errorContribution')
    xmlWriter.closeFile()
    return


def mergeFiles(outFile, inFiles):
    allErrors = {}
    for theseErrors in (parseErrorFile(inFile) for inFile in inFiles):
        for code, quant in theseErrors.items():
            allErrors[code] = allErrors.get(code, 0) + quant
            continue
        continue
    writeXmlOutput(allErrors, outFile)
    return


if __name__ == "__main__":

    import optparse
    parser = optparse.OptionParser()
    parser.add_option('-o', '--output-file', dest='outFile')
    parser.add_option('-i', '--input-file', dest='inFiles', action='append')
    options, args = parser.parse_args()

    mergeFiles(options.outFile, options.inFiles)
    
