#!/usr/bin/env bash

rm out/*
rm err/*

##### this is only for testing on HPC, tag level
foreach VAR (ant camel ivy jedit log4j lucene poi synapse velocity)
  bsub -W 1200 -o ./out/$VAR.out.%J -e ./err/$VAR.err.%J /share3/wfu/miniconda/bin/python2.7 run.py start /share3/wfu/Caret/$VAR
end