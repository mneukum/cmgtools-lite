#!/bin/bash








model="ZprimeToZh"
model2="ZprimeZH"

#model="WprimeToWh"
#model2="WprimeWH"





 python checkSignalFits.py -s ${model} --fitResults "debug_JJ_Vjet_${model2}_2016_MJrandom_NP.json.root,debug_JJ_Hjet_${model2}_2016_MJrandom_NP.json.root"  -c "VV_HPHP"  -V "jj_l2_softDrop_mass" -m 55.0 -M 150.0 -e 0 --minMX 1200.0 --maxMX 7000.0 2016_new
 python checkSignalFits.py -s ${model} --fitResults "debug_JJ_Vjet_${model2}_2016_MJrandom_NP.json.root,debug_JJ_Hjet_${model2}_2016_MJrandom_NP.json.root"  -c "VH_HPHP"  -V "jj_l2_softDrop_mass" -m 55.0 -M 150.0 -e 0 --minMX 1200.0 --maxMX 7000.0 2016_new
 python checkSignalFits.py -s ${model} --fitResults "debug_JJ_Vjet_${model2}_2016_MJrandom_NP.json.root,debug_JJ_Hjet_${model2}_2016_MJrandom_NP.json.root"  -c "VH_LPHP"  -V "jj_l2_softDrop_mass" -m 55.0 -M 150.0 -e 0 --minMX 1200.0 --maxMX 7000.0 2016_new
 python checkSignalFits.py -s ${model} --fitResults "debug_JJ_Vjet_${model2}_2016_MJrandom_NP.json.root,debug_JJ_Hjet_${model2}_2016_MJrandom_NP.json.root"  -c "VH_HPLP"  -V "jj_l2_softDrop_mass" -m 55.0 -M 150.0 -e 0 --minMX 1200.0 --maxMX 7000.0 2016_new
 python checkSignalFits.py -s ${model} --fitResults "debug_JJ_Vjet_${model2}_2016_MJrandom_NP.json.root,debug_JJ_Hjet_${model2}_2016_MJrandom_NP.json.root"  -c "VV_HPLP"  -V "jj_l2_softDrop_mass" -m 55.0 -M 150.0 -e 0 --minMX 1200.0 --maxMX 7000.0 2016_new
 python checkSignalFits.py -s ${model} --fitResults "debug_JJ_Vjet_${model2}_2016_MJrandom_NP.json.root,debug_JJ_Hjet_${model2}_2016_MJrandom_NP.json.root"  -c "NP"  -V "jj_l2_softDrop_mass" -m 55.0 -M 150.0 -e 0 --minMX 1200.0 --maxMX 7000.0 2016_new
 
 
 python checkSignalFits.py -s ${model} --fitResults "debug_JJ_Vjet_${model2}_2016_MJrandom_NP.json.root,debug_JJ_Hjet_${model2}_2016_MJrandom_NP.json.root"  -c "VV_HPHP"  -V "jj_l2_softDrop_mass" -m 55.0 -M 150.0 -e 0 --minMX 1200.0 --maxMX 7000.0 2016_new -t 1
 python checkSignalFits.py -s ${model} --fitResults "debug_JJ_Vjet_${model2}_2016_MJrandom_NP.json.root,debug_JJ_Hjet_${model2}_2016_MJrandom_NP.json.root"  -c "VH_HPHP"  -V "jj_l2_softDrop_mass" -m 55.0 -M 150.0 -e 0 --minMX 1200.0 --maxMX 7000.0 2016_new -t 1
 python checkSignalFits.py -s ${model} --fitResults "debug_JJ_Vjet_${model2}_2016_MJrandom_NP.json.root,debug_JJ_Hjet_${model2}_2016_MJrandom_NP.json.root"  -c "VH_LPHP"  -V "jj_l2_softDrop_mass" -m 55.0 -M 150.0 -e 0 --minMX 1200.0 --maxMX 7000.0 2016_new -t 1
 python checkSignalFits.py -s ${model} --fitResults "debug_JJ_Vjet_${model2}_2016_MJrandom_NP.json.root,debug_JJ_Hjet_${model2}_2016_MJrandom_NP.json.root"  -c "VH_HPLP"  -V "jj_l2_softDrop_mass" -m 55.0 -M 150.0 -e 0 --minMX 1200.0 --maxMX 7000.0 2016_new -t 1
 python checkSignalFits.py -s ${model} --fitResults "debug_JJ_Vjet_${model2}_2016_MJrandom_NP.json.root,debug_JJ_Hjet_${model2}_2016_MJrandom_NP.json.root"  -c "VV_HPLP"  -V "jj_l2_softDrop_mass" -m 55.0 -M 150.0 -e 0 --minMX 1200.0 --maxMX 7000.0 2016_new -t 1
 python checkSignalFits.py -s ${model} --fitResults "debug_JJ_Vjet_${model2}_2016_MJrandom_NP.json.root,debug_JJ_Hjet_${model2}_2016_MJrandom_NP.json.root"  -c "NP"  -V "jj_l2_softDrop_mass" -m 55.0 -M 150.0 -e 0 --minMX 1200.0 --maxMX 7000.0 2016_new -t 1


 model="ZprimeToWW"
 model2="ZprimeWW"
 
#  model="BulkGravToWW"
#  model2="BulkGWW"
 
 model="BulkGravToZZ"
 model2="BulkGZZ"
 
model="WprimeToWZ" 
model2="WprimeWZ" 
# python checkSignalFits.py -s ${model} --fitResults "debug_JJ_${model2}_2016_MJrandom_NP.json.root"  -c "VV_HPHP"  -V "jj_l2_softDrop_mass" -m 55.0 -M 150.0 -e 0 --minMX 1200.0 --maxMX 7000.0 2016_new
# python checkSignalFits.py -s ${model} --fitResults "debug_JJ_${model2}_2016_MJrandom_NP.json.root"  -c "VH_HPHP"  -V "jj_l2_softDrop_mass" -m 55.0 -M 150.0 -e 0 --minMX 1200.0 --maxMX 7000.0 2016_new
# python checkSignalFits.py -s ${model} --fitResults "debug_JJ_${model2}_2016_MJrandom_NP.json.root"  -c "VH_LPHP"  -V "jj_l2_softDrop_mass" -m 55.0 -M 150.0 -e 0 --minMX 1200.0 --maxMX 7000.0 2016_new
# python checkSignalFits.py -s ${model} --fitResults "debug_JJ_${model2}_2016_MJrandom_NP.json.root"  -c "VH_HPLP"  -V "jj_l2_softDrop_mass" -m 55.0 -M 150.0 -e 0 --minMX 1200.0 --maxMX 7000.0 2016_new
# python checkSignalFits.py -s ${model} --fitResults "debug_JJ_${model2}_2016_MJrandom_NP.json.root"  -c "VV_HPLP"  -V "jj_l2_softDrop_mass" -m 55.0 -M 150.0 -e 0 --minMX 1200.0 --maxMX 7000.0 2016_new
# python checkSignalFits.py -s ${model} --fitResults "debug_JJ_${model2}_2016_MJrandom_NP.json.root"  -c "NP"  -V "jj_l2_softDrop_mass" -m 55.0 -M 150.0 -e 0 --minMX 1200.0 --maxMX 7000.0 2016_new


# python checkSignalFits.py -s ${model} --fitResults "debug_JJ_${model2}_2016_MJrandom_NP.json.root"  -c "VV_HPHP"  -V "jj_l2_softDrop_mass" -m 55.0 -M 150.0 -e 0 --minMX 1200.0 --maxMX 7000.0 2016_new -t 1
# python checkSignalFits.py -s ${model} --fitResults "debug_JJ_${model2}_2016_MJrandom_NP.json.root"  -c "VH_HPHP"  -V "jj_l2_softDrop_mass" -m 55.0 -M 150.0 -e 0 --minMX 1200.0 --maxMX 7000.0 2016_new -t 1
# python checkSignalFits.py -s ${model} --fitResults "debug_JJ_${model2}_2016_MJrandom_NP.json.root"  -c "VH_LPHP"  -V "jj_l2_softDrop_mass" -m 55.0 -M 150.0 -e 0 --minMX 1200.0 --maxMX 7000.0 2016_new -t 1
# python checkSignalFits.py -s ${model} --fitResults "debug_JJ_${model2}_2016_MJrandom_NP.json.root"  -c "VH_HPLP"  -V "jj_l2_softDrop_mass" -m 55.0 -M 150.0 -e 0 --minMX 1200.0 --maxMX 7000.0 2016_new -t 1
# python checkSignalFits.py -s ${model} --fitResults "debug_JJ_${model2}_2016_MJrandom_NP.json.root"  -c "VV_HPLP"  -V "jj_l2_softDrop_mass" -m 55.0 -M 150.0 -e 0 --minMX 1200.0 --maxMX 7000.0 2016_new -t 1
# python checkSignalFits.py -s ${model} --fitResults "debug_JJ_${model2}_2016_MJrandom_NP.json.root"  -c "NP"  -V "jj_l2_softDrop_mass" -m 55.0 -M 150.0 -e 0 --minMX 1200.0 --maxMX 7000.0 2016_new -t 1

