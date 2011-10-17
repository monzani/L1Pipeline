
import os
import xml.etree.ElementTree as et

import config

import pipeline

defQual = config.solarFlareFlag


def getRangesXml(inFile, qual=None):
    if qual is None: qual = defQual
    
    tree = et.parse(inFile)
    ivs = tree.findall('badIntervals/interval')
    ranges = [((int(round(float(iv.attrib['start_met']))),
                int(round(float(iv.attrib['end_met'])))),
               qual) for iv in ivs]
    return ranges


def getRangesVar():
    rangeStr = os.environ['badRanges']
    if rangeStr == 'x': return []
    lines = rangeStr.split(',')
    ranges = []
    for line in lines:
        fields = line.split(':')
        start = float(fields[0])
        stop = float(fields[1])
        qual = int(fields[2])
        range = ((start, stop), qual)
        ranges.append(range)
        continue
    return ranges


def getRangesText():
    timeFile = os.path.join(runDir , 'timeFile')

    lines = open(timeFile)
    ranges = []
    for line in lines:
        fields = line.split()
        start = float(fields[0])
        stop = float(fields[1])
        qual = int(fields[2])
        range = ((start, stop), qual)
        ranges.append(range)
    return ranges


def setRangesVar(ranges):
    if not ranges:
        rangeStr = 'x'
    else:
        lines = []
        for ((start, stop), qual) in ranges:
            line = "%s:%s:%s" % (start, stop, qual)
            lines.append(line)
            continue
        rangeStr = ','.join(lines)
        pass
    pipeline.setVariable("badRanges", rangeStr)
    return
