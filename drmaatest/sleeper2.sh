#!/bin/sh
#
# Usage: sleeper.sh [time]]
#        default for time is 60 seconds

# -- our name ---
#$ -N Sleeper1
#$ -S /bin/sh
# Make sure that the .e and .o file arrive in the
# working directory
#$ -cwd
#Merge the standard out and standard error to one file
#$ -j y
/bin/echo Here I am: `hostname`. Sleeping now at: `date`
/bin/echo Running on host: `hostname`.
/bin/echo In directory: `pwd`
/bin/echo Starting on: `date`
# Send mail at submission and completion of script
#$ -m be
#$ -M deadline@kronos
time=60
if [ $# -ge 1 ]; then
   time=$1
fi
sleep $time

echo Now it is: `date`
