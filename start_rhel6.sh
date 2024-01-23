#!/bin/sh

CONTAINERDIR=/sdf/group/fermi/sw/containers
apptainer shell -B /sdf \
                -B /sdf/data/fermi/a:/afs/slac.stanford.edu/g/glast \
		-B /sdf/group/fermi/sw/package:/afs/slac.stanford.edu/package \
                -B $CONTAINERDIR/rhel6/opt/TWWfsw:/opt/TWWfsw \
                -B $CONTAINERDIR/rhel6/usr/local:/usr/local \
                $CONTAINERDIR/fermi-rhel6.20230922.sif
