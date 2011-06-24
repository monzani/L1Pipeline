from java.sql import Timestamp

intervals = list(runQuality.getBadTimeIntervalsForRun(runNumber))
ivs = []
for interval in intervals:
    range = ((interval.getRequestedStartPeriod(), interval.getRequestedEndPeriod()), interval.getDataQual())
    ivs.append((range, interval))
    continue
ivs.sort()
print ivs

flagProcess = pipeline.getProcessInstance("flagFT2")
badRanges = flagProcess.getVariable("badRanges")
lines = badRanges.split(',')
ranges = []
for line in lines:
    fields = line.split(":")
    start = int(round(float(fields[0])))
    stop = int(round(float(fields[1])))
    qual = int(fields[2])
    ranges.append(((start, stop), qual))
    continue
ranges.sort()
print ranges

if len(ivs) != len(ranges):
    print "Flagged and requested interval lists have different lengths!"
    raise SystemExit

stuff = zip(ranges, ivs)
for (range, iv) in stuff:
    ((ft2Start, ft2Stop), ft2Qual) = range
    ((reqStart, reqStop), reqQual) = iv[0]
    if not ((ft2Start <= reqStart) and (ft2Stop >= reqStop) and (ft2Qual == reqQual)):
        print "Interval mismatch!"
        raise SystemExit
    continue

exportProcess = pipeline.getProcessInstance("exportFT2")
exportTime = exportProcess.getVariable("exportTime")
millis = long(float(exportTime) * 1000)
print millis
exportTime = Timestamp(millis)

for (range, iv) in stuff:
    ((start, stop), qual) = range
    interval = iv[1]
    
    interval.setFt2StartPeriod(start)
    interval.setFt2EndPeriod(stop)
    interval.setFt2Export(exportTime)
    runQuality.updateBadTimeInterval(interval)    
    continue
