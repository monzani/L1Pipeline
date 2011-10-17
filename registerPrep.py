
import os
import sys

import config

import datacatalog
import fileNames
import variables

def oldAndBroken(fileType, fileName):
    """
    Deal with batch-side prep to register a file with the data catalog.
    Actual registration is done by a scriptlet (in registerStuff.py).
    This sets up some pipeline variables so the scriptlet knows what to do.
    """

    taskName = os.environ['L1_TASK_NAME']
    taskVersion =  os.environ['PIPELINE_TASKVERSION']
    creator = '-'.join([taskName, taskVersion])

    fileVersion = fileNames.version(fileName)

    variables.setVar(fileType, 'format', fileNames.fileTypes[fileType])
    variables.setVar(fileType, 'dcType', fileNames.dataCatType(fileType))
    # variables.setVar(fileType, 'path', config.dataCatDir) # remove me!
    variables.setVar(fileType, 'group', fileNames.dataCatGroup(fileType))
    variables.setVar(fileType, 'site', fileNames.getSite(fileName))
    variables.setVar(fileType, 'fileName', fileName)
    variables.setVar(fileType, 'ver', fileVersion)
    # variables.setVar(fileType, 'creator', creator) # remove me!

    return


def theNewHotness(fileType, fileName):
    """
    This is not complete, don't try to use it yet.
    
    Deal with batch-side prep to register a file with the data catalog.
    Actual registration is done during stageOut finalization.
    This sets up some data structures so stageOut knows what to do.
    """

    taskName = os.environ['L1_TASK_NAME']
    taskVersion =  os.environ['PIPELINE_TASKVERSION']
    creator = '-'.join([taskName, taskVersion])

    ds = datacatalog.NewDataset(os.environ['RUNID'],
                                fileNames.fileTypes[fileType],
                                fileNames.dataCatType(fileType),
                                os.environ['dataCatDir'],
                                fileNames.dataCatGroup(fileType),
                                fileNames.getSite(fileName),
                                fileName)
    ds.setVersionId(fileNames.version(fileName))

    attr = {'sCreator': creator,
            'sDataSource': os.environ['DATASOURCE'],
            'nDownlink': os.environ['DOWNLINK_ID'],
            'sIntent': os.environ[''],
            'nMetStart': os.environ[''],
            'nMetStop': os.environ[''],
            'nMootKey': os.environ[''],
            'nRun': os.environ['runNumber']}

    return ds, attr


prep = oldAndBroken
