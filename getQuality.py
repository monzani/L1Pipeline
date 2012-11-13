runNumber = int(RUNID[1:])
quality = runQuality.getRunQuality(runNumber)
print 'q:', quality
pipeline.setVariable('runQuality', quality)
