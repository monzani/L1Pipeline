runNumber = int(RUNID[1:])
quality = runQuality.getRunQuality(runNumber)
pipeline.setVariable('runQuality', quality)
