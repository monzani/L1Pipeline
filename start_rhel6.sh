#!/bin/sh

CONTAINERDIR=/sdf/group/fermi/sw/containers
apptainer shell -B /sdf \
                -B /sdf/group/fermi/a:/afs/slac/g/glast \
                -B $CONTAINERDIR/rhel6/opt/TWWfsw:/opt/TWWfsw \
                -B $CONTAINERDIR/rhel6/usr/local:/usr/local \
                $CONTAINERDIR/fermi-rhel6.20230922.sif
