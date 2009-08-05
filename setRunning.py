from java.util import HashMap

def setIfUnset(container, key, value):
    oldValue = container.get(key)
    if oldValue is None or oldValue == 'Unset':
        print 'Setting %s to %s.' % (key, value)
        container[key] = value
    else: print 'Current value of %s is %s, not changing it.' % (key, oldValue)
    return

print 'Setting L1RunStatus for run', runNumber, ' to ', l1RunStatus
runQuality.setL1RunStatus(runNumber, l1RunStatus)

reviewStatus = "Unset"
print 'Setting ReviewStatus for run', runNumber, ' to ', reviewStatus
runQuality.setReviewStatus(runNumber, reviewStatus)

newQuality = 'Good'
quality = runQuality.getRunQuality(runNumber)
print 'Current quality for run %s is %s.' % (runNumber, quality)
if quality is None or quality == 'Unset':
    print 'Setting quality for run %s to %s.' % (runNumber, newQuality)
    runQuality.setRunQuality(runNumber, newQuality)
    quality = newQuality
else: print 'Not changing run quality.'
pipeline.setVariable('runQuality', quality)    

fields = ['ACDQuality', 'CALQuality', 'GPSQuality', 'TRACKERQuality',
          'TRIGGERQuality']
metaData = runQuality.getMetaData(runNumber)
print 'old metaData:', metaData
for key in fields: setIfUnset(metaData, key, newQuality)
print 'new metadata:', metaData

runQuality.setOrUpdateMetaData(runNumber, metaData)
