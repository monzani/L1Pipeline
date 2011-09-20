from java.sql import Timestamp

creator = pipeline.getTaskVersionPath()
theSet = runQuality.getMostRecentSubmittedTimeIntervalSet(runNumber, creator)
ivs = []

if theSet:
    intervals = theSet.getActiveIntervals()
    for interval in intervals:
        range = ((interval.getRequestedStartPeriod(), interval.getRequestedEndPeriod()), interval.getDataQual())
        ivs.append((range, interval))
        continue
    ivs.sort()
    pass
print 'ivs:', ivs

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

if len(ivs) != len(ranges):
    print "Flagged and requested interval lists have different lengths!"
    raise SystemExit

stuff = zip(ranges, ivs)
# # This fails if the interval overlaps the start or end of a run
# # or a gap, probably
# for (range, iv) in stuff:
#     ((ft2Start, ft2Stop), ft2Qual) = range
#     ((reqStart, reqStop), reqQual) = iv[0]
#     if not ((ft2Start <= reqStart) and (ft2Stop >= reqStop) and (ft2Qual == reqQual)):
#         print "Interval mismatch!"
#         raise SystemExit
#     continue

for (range, iv) in stuff:
    ((start, stop), qual) = range
    interval = iv[1]
    
    interval.setFt2StartPeriod(start)
    interval.setFt2EndPeriod(stop)
    continue

exportProcess = currentStream.getProcessInstance("exportFT2")
exportTime = exportProcess.getVariable("exportTime")
millis = long(float(exportTime) * 1000)
print millis
exportTime = Timestamp(millis)

if theSet:
    theSet.setExportTime(exportTime)
    theSet.setStreamId(pipeline.getStream())
    theSet.setTaskName(creator)
    runQuality.updateBadTimeIntervalSet(theSet)
    pass
