#bin/bash!
models=("BGZZ" "WprimeWZ" "ZprimeWW" "BGWW"  "ZprimeZH" "WprimeWH")
models=("BGZZ")

# 
# for model in ${models[@]}
# do
#     python makeInputs.py --signal ${model} --run signalnorm --batch False
#     python makeInputs.py --signal ${model} --run signalmvv
#     python makeInputs.py --signal ${model} --run signalmj
#     cp JJ_${model}*.root results_2016/
#     cp JJ_${model}*.json results_2016/
# done



# 
# python drawFittedParameters.py results_2016/
# cp results_2016/Signal_mjet2016_NP_*.pdf /home/dschaefer/Documents/AnalysisNotes2/AN-19-131/figures/signal/
# 
# 
# python plotSignalShapesFromJSON.py  --category NP -o results_2016/
# cp results_2016/signalShapes_mVV_NP_2016_All_test.pdf /home/dschaefer/Documents/AnalysisNotes2/
# 
# python plotSignalShapesFromJSON.py --var mJ --category NP -o results_2016/
# cp results_2016/signalShapes_mJ_NP_2016_All_test.pdf /home/dschaefer/Documents/AnalysisNotes2/
# 

# # now make the signal only cards !!!!
# python /work/dschaefer/DiBoson3D/makePseudoData.py --which sigonly
#  models=("BulkGZZ"  "WprimeWZ" "ZprimeWW" "BulkGWW"  "ZprimeZH" "WprimeWH")
#  category=( "VV_HPHP"  "VH_HPHP" "VH_HPLP" "VH_LPHP" "VV_HPLP")
#  models=("BulkGZZ")
# 
#  for model in ${models[@]}
#  do
#    for c in ${category[@]}
#    do
#        python makeCard.py --outlabel "sigonly_M4000" --pseudodata $model --signal $model --category $c --period "2016"
#   
#     python makeCard.py --outlabel "sigonly_M2000" --pseudodata $model --signal $model --category $c --period "2016"
#    done 
#  done


# masses=(4000  2000)
# 
# mkdir postfitplots/
# 
# 
# models=("BulkGWW" "WprimeWZ" "ZprimeWW" "BulkGZZ" "ZprimeZH" "WprimeWH")
# models=("BulkGZZ")
# 
# 
# for model in ${models[@]}
# do
#   for c in ${category[@]}
#   do
#     for m in ${masses[@]}
#     do
#     python runFitPlots_vjets_signal_oneyear_splitRes.py -n workspace_JJ_${model}_${c}_13TeV_2016sigonly_M${m}.root  -l nominal -i  results_2016/JJ_2016_nonRes_${c}.root -M $m -s --xrange 65,105 -o postfitplots/ --channel $c -l sigonly_${model}_${c}_M${m} --doFit False
#     
#     python runFitPlots_vjets_signal_oneyear_splitRes.py -n workspace_JJ_${model}_${c}_13TeV_2016sigonly_M${m}.root  -l nominal -i  results_2016/JJ_2016_nonRes_${c}.root -M $m -s --xrange 85,105 -o postfitplots/ --channel $c -l sigonly_${model}_${c}_M${m} --doFit False
#     
#     python runFitPlots_vjets_signal_oneyear_splitRes.py -n workspace_JJ_${model}_${c}_13TeV_2016sigonly_M${m}.root  -l nominal -i  results_2016/JJ_2016_nonRes_${c}.root -M $m -s --xrange 105,150 -o postfitplots/ --channel $c -l sigonly_${model}_${c}_M${m} --doFit False
#     
#     
#     python runFitPlots_vjets_signal_oneyear_splitRes.py -n workspace_JJ_${model}_${c}_13TeV_2016sigonly_M${m}.root  -l nominal -i  results_2016/JJ_2016_nonRes_${c}.root -M $m -s --xrange 65,105 --xrange 65,105 -o postfitplots/ --channel $c -l sigonly_${model}_${c}_M${m} --doFit False
#     
#     
#     
#     python runFitPlots_vjets_signal_oneyear_splitRes.py -n workspace_JJ_${model}_${c}_13TeV_2016sigonly_M${m}.root  -l nominal -i  results_2016/JJ_2016_nonRes_${c}.root -M $m -s --xrange 65,85 --yrange 65,85 -o postfitplots/ --channel $c -l sigonly_${model}_${c}_M${m} --doFit False
#     
#     python runFitPlots_vjets_signal_oneyear_splitRes.py -n workspace_JJ_${model}_${c}_13TeV_2016sigonly_M${m}.root  -l nominal -i  results_2016/JJ_2016_nonRes_${c}.root -M $m -s --xrange 105,150 --yrange 105,150 -o postfitplots/ --channel $c -l sigonly_${model}_${c}_M${m} --doFit False
#     
#     python runFitPlots_vjets_signal_oneyear_splitRes.py -n workspace_JJ_${model}_${c}_13TeV_2016sigonly_M${m}.root  -l nominal -i  results_2016/JJ_2016_nonRes_${c}.root -M $m -s --xrange 65,105 --yrange 105,150 -o postfitplots/ --channel $c -l sigonly_${model}_${c}_M${m} --doFit False
#     
#     
#     python runFitPlots_vjets_signal_oneyear_splitRes.py -n workspace_JJ_${model}_${c}_13TeV_2016sigonly_M${m}.root  -l nominal -i  results_2016/JJ_2016_nonRes_${c}.root -M $m -s --xrange 65,85 --yrange 105,150 -o postfitplots/ --channel $c -l sigonly_${model}_${c}_M${m} --doFit False
#     
#     python runFitPlots_vjets_signal_oneyear_splitRes.py -n workspace_JJ_${model}_${c}_13TeV_2016sigonly_M${m}.root  -l nominal -i  results_2016/JJ_2016_nonRes_${c}.root -M $m -s --xrange 65,85 --yrange 85,105 -o postfitplots/ --channel $c -l sigonly_${model}_${c}_M${m} --doFit False
#     
#     python runFitPlots_vjets_signal_oneyear_splitRes.py -n workspace_JJ_${model}_${c}_13TeV_2016sigonly_M${m}.root  -l nominal -i  results_2016/JJ_2016_nonRes_${c}.root -M $m -s --xrange 85,105 --yrange 85,105 -o postfitplots/ --channel $c -l sigonly_${model}_${c}_M${m} --doFit False
#     
#     
#     python runFitPlots_vjets_signal_oneyear_splitRes.py -n workspace_JJ_${model}_${c}_13TeV_2016sigonly_M${m}.root  -l nominal -i  results_2016/JJ_2016_nonRes_${c}.root -M $m -s -o postfitplots/ --channel $c -l sigonly_${model}_${c}_M${m} --doFit False
# 
#     done
#   done
# done






mkdir postfitplots/


models=("ZprimeZH")
category=( "VH_HPLP" "VH_LPHP" "VH_HPHP" "VV_HPLP" "VV_HPHP")


for model in ${models[@]}
do
  for c in ${category[@]}
  do
    
     python runFitPlots_vjets_signal_bigcombo_splitRes.py -n workspace_JJ_${model}_${c}_13TeV_2016ttbar.root  -i  ttbarmodeling/JJ_2016_nonRes_${c}.root -M 2000  -o postfitplots/ --channel ${c} -l ttbar_${c} --doVjets --addTop --doFit False --zrange 1200,1600
    python runFitPlots_vjets_signal_bigcombo_splitRes.py -n workspace_JJ_${model}_${c}_13TeV_2016ttbar.root  -i  ttbarmodeling/JJ_2016_nonRes_${c}.root -M 2000  -o postfitplots/ --channel ${c} -l ttbarFit_${c} --doVjets --addTop --zrange 1200,1600
    
    
     python runFitPlots_vjets_signal_bigcombo_splitRes.py -n workspace_JJ_${model}_${c}_13TeV_2016ttbar.root  -i  ttbarmodeling/JJ_2016_nonRes_${c}.root -M 2000  -o postfitplots/ --channel ${c} -l ttbar_${c} --doVjets --addTop --doFit False --zrange 1600,2000
    python runFitPlots_vjets_signal_bigcombo_splitRes.py -n workspace_JJ_${model}_${c}_13TeV_2016ttbar.root  -i  ttbarmodeling/JJ_2016_nonRes_${c}.root -M 2000  -o postfitplots/ --channel ${c} -l ttbarFit_${c} --doVjets --addTop --zrange 1600,2000
    
    python runFitPlots_vjets_signal_bigcombo_splitRes.py -n workspace_JJ_${model}_${c}_13TeV_2016ttbar.root  -i  ttbarmodeling/JJ_2016_nonRes_${c}.root -M 2000  -o postfitplots/ --channel ${c} -l ttbar_${c} --doVjets --addTop --doFit False --zrange 2000,5000
    python runFitPlots_vjets_signal_bigcombo_splitRes.py -n workspace_JJ_${model}_${c}_13TeV_2016ttbar.root  -i  ttbarmodeling/JJ_2016_nonRes_${c}.root -M 2000  -o postfitplots/ --channel ${c} -l ttbarFit_${c} --doVjets --addTop --zrange 2000,5000
    
    
     python runFitPlots_vjets_signal_bigcombo_splitRes.py -n workspace_JJ_${model}_${c}_13TeV_2016ttbar.root  -i  ttbarmodeling/JJ_2016_nonRes_${c}.root -M 2000  -o postfitplots/ --channel ${c} -l ttbar_${c} --doVjets --addTop --doFit False --xrange 65,105
    python runFitPlots_vjets_signal_bigcombo_splitRes.py -n workspace_JJ_${model}_${c}_13TeV_2016ttbar.root  -i  ttbarmodeling/JJ_2016_nonRes_${c}.root -M 2000  -o postfitplots/ --channel ${c} -l ttbarFit_${c} --doVjets --addTop --xrange 65,105
    
    
    python runFitPlots_vjets_signal_bigcombo_splitRes.py -n workspace_JJ_${model}_${c}_13TeV_2016ttbar.root  -i  ttbarmodeling/JJ_2016_nonRes_${c}.root -M 2000  -o postfitplots/ --channel ${c} -l ttbar_${c} --doVjets --addTop --doFit False --xrange 105,215
    python runFitPlots_vjets_signal_bigcombo_splitRes.py -n workspace_JJ_${model}_${c}_13TeV_2016ttbar.root  -i  ttbarmodeling/JJ_2016_nonRes_${c}.root -M 2000  -o postfitplots/ --channel ${c} -l ttbarFit_${c} --doVjets --addTop --xrange 105,215
    
    
     python runFitPlots_vjets_signal_bigcombo_splitRes.py -n workspace_JJ_${model}_${c}_13TeV_2016ttbar.root  -i  ttbarmodeling/JJ_2016_nonRes_${c}.root -M 2000  -o postfitplots/ --channel ${c} -l ttbar_${c} --doVjets --addTop --doFit False --xrange 65,105 --yrange 65,105
    python runFitPlots_vjets_signal_bigcombo_splitRes.py -n workspace_JJ_${model}_${c}_13TeV_2016ttbar.root  -i  ttbarmodeling/JJ_2016_nonRes_${c}.root -M 2000  -o postfitplots/ --channel ${c} -l ttbarFit_${c} --doVjets --addTop --xrange 65,105 -yrange 65,105
    
    
    python runFitPlots_vjets_signal_bigcombo_splitRes.py -n workspace_JJ_${model}_${c}_13TeV_2016ttbar.root  -i  ttbarmodeling/JJ_2016_nonRes_${c}.root -M 2000  -o postfitplots/ --channel ${c} -l ttbar_${c} --doVjets --addTop --doFit False --xrange 105,215 --yrange 105,215
    python runFitPlots_vjets_signal_bigcombo_splitRes.py -n workspace_JJ_${model}_${c}_13TeV_2016ttbar.root  -i  ttbarmodeling/JJ_2016_nonRes_${c}.root -M 2000  -o postfitplots/ --channel ${c} -l ttbarFit_${c} --doVjets --addTop --xrange 105,215 --yrange 105,215
    
    python runFitPlots_vjets_signal_bigcombo_splitRes.py -n workspace_JJ_${model}_${c}_13TeV_2016ttbar.root  -i  ttbarmodeling/JJ_2016_nonRes_${c}.root -M 2000  -o postfitplots/ --channel ${c} -l ttbar_${c} --doVjets --addTop --doFit False --xrange 105,215 --yrange 65,105
    python runFitPlots_vjets_signal_bigcombo_splitRes.py -n workspace_JJ_${model}_${c}_13TeV_2016ttbar.root  -i  ttbarmodeling/JJ_2016_nonRes_${c}.root -M 2000  -o postfitplots/ --channel ${c} -l ttbarFit_${c} --doVjets --addTop --xrange 105,215 --yrange 65,105
    
    
    python runFitPlots_vjets_signal_bigcombo_splitRes.py -n workspace_JJ_${model}_${c}_13TeV_2016ttbar.root  -i  ttbarmodeling/JJ_2016_nonRes_${c}.root -M 2000  -o postfitplots/ --channel ${c} -l ttbar_${c} --doVjets --addTop --doFit False
    python runFitPlots_vjets_signal_bigcombo_splitRes.py -n workspace_JJ_${model}_${c}_13TeV_2016ttbar.root  -i  ttbarmodeling/JJ_2016_nonRes_${c}.root -M 2000  -o postfitplots/ --channel ${c} -l ttbarFit_${c} --doVjets --addTop
    
  done
done

