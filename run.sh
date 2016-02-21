#! /bin/tcsh

rm out/*
rm err/*

##### this is only for testing on HPC, tag level
foreach goal (precision f1 auc )
  foreach r (true false)
    bsub -W 1200 -o ./out/$VAR.out.%J -e ./err/$VAR.err.%J /share3/wfu/miniconda/bin/python2.7 run.py run goal r
end