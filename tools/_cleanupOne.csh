#!/bin/tcsh

echo ======================== start cleanup ========================

set localDisk=/scratch

if (! { test -d $localDisk })  then
	echo No scratch dir to clean out.
	echo ======================== finish cleanup ========================
	exit
endif

cd $localDisk
df -h .
ls -l

set dirs=`ls -l | awk '$3=="glastraw" && / [0-9]+$/{print $NF}'`

echo dirs=$dirs

if ({ test -z "$dirs" }) then
	echo Nothing to remove.
	echo ======================== finish cleanup ========================
	exit
endif

foreach dir ($dirs)
	if ({ ps uwww $dir }) then
		echo Process still active, not removing $dir
	else
		echo Removing $dir
		rm -rf $dir
	endif
end

df -h .

echo ======================== finish cleanup ========================
