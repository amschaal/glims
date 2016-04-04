#!/bin/bash 
printenv

echo "Hi!"
wget $1
sleep 10s
wget $2
echo "Bye world!"