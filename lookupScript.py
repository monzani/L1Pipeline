nameManglingPrefix = 'L1'
location = 'SLAC_XROOT'

def setVar(fileType, name, value):
    mangledName = '_'.join([nameManglingPrefix, fileType, name])
    value = pipeline.setVariable(mangledName, value)
    return value

typeList = fileTypes.split(',')

for fileType in typeList:
    uType = fileType.upper()
    print 'type:', uType
    # DatasetList getDatasets(String logicalFolderPath, boolean recurseFolders, boolean searchFolders, String datasetGroupName, boolean searchGroups, String searchCriteria, String sites[], String metaFieldsToRetrieve[], String sortFields[])
    dsList = datacatalog.getDatasets( # DatasetList getDatasets(...)
        "/Data/Flight/Level1/" + DATASOURCE, # String logicalFolderPath
        0, #  boolean recurseFolders
        0, # boolean searchFolders
        uType, # String datasetGroupName
        1, # boolean searchGroups
        'Name=="' + RUNID + '"', # String searchCriteria
        [location], # String sites[]
        [], # String metaFieldsToRetrieve[]
        [] # String sortFields[]
        )
    print 'dsList:', dsList
    # dsList = [x for x in dsList.iterator()]
    # print 'dsList:', dsList
    # assert len(dsList) == 1
    ds = dsList.get(0)
    print 'ds:', ds
    loc = ds.getLocations()
    print 'loc:', loc
    for key in loc.keySet():
        print 'key:', key
        value = loc[key]
        print 'value:', value
        print 'path:', value.getPath()
    #path = loc.getPath()
    #print 'path:', path
    #setVar(fileType, 'fileName', path)
    continue
