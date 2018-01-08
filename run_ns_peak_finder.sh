#!/bin/bash

list=$(ls outputs/cuts/ | grep .cut | cut -d'.' -f1)
for i in $list
do
python neighbour_signals_strict.py $i
done
