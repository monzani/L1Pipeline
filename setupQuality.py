theSet = runQuality.getMostRecentSubmittedTimeIntervalSet(runNumber, creator)

if theSet:
    intervals = theSet.getActiveIntervals()
    print intervals

    lines = []
    for interval in intervals:
        start = interval.getRequestedStartPeriod()
        stop = interval.getRequestedEndPeriod()
        qual = interval.getDataQual()
        print start, stop, qual
        lines.append("%s:%s:%s" % (start, stop, qual))
        continue

    rangeStr = ",".join(lines)

else:
    rangeStr = "x"
    pass

print "rangeStr:", rangeStr
pipeline.setVariable("badRanges", rangeStr)

#print "Failing on purpose for debugging."
#raise SystemExit
