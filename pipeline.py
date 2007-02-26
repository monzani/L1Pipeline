#!/usr/bin/env python

"""@brief interface to pipeline functions.
"""

def setVariable(varName, value):
    # muck about with pipeline summary file
    line = 'pipeline.%s: %s\n' % (varName, value)
    ofp = open('pipeline_summary', 'a')
    ofp.write(line)
    ofp.close()
    return
