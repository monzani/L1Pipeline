#!/usr/bin/env python

"""@brief interface to pipeline functions.
"""

import runner

def setVariable(varName, value):
    # use bash function
    cmd = 'pipelineSet %s %s' % (varName, value)
    status = runner.run(cmd)
    return status

def createSubStream(subTask, stream=0, args=''):
    cmd = 'pipelineCreateStream %s %s %s' % (subTask, stream, args)
    status = runner.run(cmd)
    return status
