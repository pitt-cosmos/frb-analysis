#!/bin/bash

list=$(ls outputs/cuts/ | grep .cut | cut -d'.' -f1)
for i in $list
do
python coincident_signals_filter.py $i
done
