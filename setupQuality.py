intervals = runQuality.getBadTimeIntervalsForRun(runNumber)
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
print rangeStr
pipeline.setVariable("badRanges", rangeStr)

#print "Failing on purpose for debugging."
#raise SystemExit
