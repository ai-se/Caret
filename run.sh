#! /bin/tcsh

rm out/*
rm err/*

###### this is only for testing on HPC, normal test
#foreach goal (precision f1 auc)
#  foreach r (true false)
#    bsub -W 1200 -o ./out/${goal}_${r}.out.%J -e ./err/${goal}_${r}.err.%J /share3/wfu/miniconda/bin/python2.7 run.py run $goal $r
#  end
#end


##### this is only for testing on HPC, exhuastive grid search
foreach goal (precision f1 auc)
  foreach r (false)
    bsub -W 1200 -o ./out/${goal}_${r}.out.%J -e ./err/${goal}_${r}.err.%J /share3/wfu/miniconda/bin/python2.7 run.py run $goal $r
  end
end