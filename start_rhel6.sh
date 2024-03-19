#!/bin/sh

CONTAINERDIR=/sdf/group/fermi/sw/containers
#-B $CONTAINERDIR/rhel6/afs/slac.stanford.edu/package/perl:/afs/slac.stanford.edu/package/perl \
apptainer shell -B /sdf:/sdf \
		-B /sdf/group/fermi/a:/afs/slac/g/glast \
		-B /sdf/group/fermi/a:/afs/slac.stanford.edu/g/glast \
		-B /sdf/group/fermi/sw/package:/afs/slac/package \
		-B /sdf/group/fermi/sw/package:/afs/slac.stanford.edu/package \
		-B $CONTAINERDIR/rhel6/opt/TWWfsw:/opt/TWWfsw \
                -B $CONTAINERDIR/rhel6/usr/local:/usr/local \
                $CONTAINERDIR/fermi-rhel6.20230922.sif
