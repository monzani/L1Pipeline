#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import sys

import xml.dom.minidom as md

inFile = sys.argv[1]

doc = md.parse(inFile)

processes = set(element.getAttribute('name')
                for element in doc.getElementsByTagName('process'))

afters = set(element.getAttribute('process')
             for element in doc.getElementsByTagName('after'))

orphans = afters - processes

for orph in sorted(orphans): print orph
