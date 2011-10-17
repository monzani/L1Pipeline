creator = pipeline.getTaskVersionPath()
currentStream = pipeline.getCurrentStream()
btiProcess = currentStream.getProcessInstance(btiProcess)
badRanges = btiProcess.getVariable("badRanges")
ranges = []
if badRanges == 'x':
    pass
else:
    lines = badRanges.split(',')
    for line in lines:
        fields = line.split(":")
        start = int(round(float(fields[0])))
        stop = int(round(float(fields[1])))
        qual = int(fields[2])
        ranges.append(((start, stop), qual))
        continue
    ranges.sort()
    pass
print 'ranges:', ranges

if ranges:
    theSet = runQuality.createBadTimeIntervalSetForRun(runNumber, creator)
    setId = theSet.getId()

    for (start, stop), qual in ranges:
        iv = runQuality.createBadTimeIntervalForSet(setId, creator)
        iv.setSuggestedStartPeriod(start)
        iv.setSuggestedEndPeriod(stop)
        iv.setDataQual(qual)
        runQuality.updateBadTimeInterval(iv)
        continue

    runQuality.updateBadTimeIntervalSet(theSet)
    pass
