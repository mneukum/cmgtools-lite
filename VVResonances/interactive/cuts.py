# contains all analysis cuts! -> need category import this file




#scale factors to be updated!
HPSF16 = 0.937
LPSF16 = 1.006
HPSF17 = 0.955
LPSF17 = 1.003

#ranges and binning
minMJ=55.0
maxMJ=215.0
binsMJ=80

widerMVV=False
minMVV=838.00
maxMVV=6000.0
if widerMVV: maxMVV=7600.0

binsMVV=100

minMX=1200.0

maxMX=6000.0    

#gen level cuts for templates    
minGenMJ=20.
maxGenMJ=300.
minGenMVV=800.0
maxGenMVV=6000.0
if widerMVV: maxGenMVV=8000.0


    
HCALbinsMVVSignal=" --binsMVV 1,3,6,10,16,23,31,40,50,61,74,88,103,119,137,156,176,197,220,244,270,296,325,354,386,419,453,489,526,565,606,649,693,740,788,838,890,944,1000,1058,1126,1181,1246,1313,1383,1455,1530,1607,1687,1770,1856,1945,2037,2132,2231,2332,2438,2546,2659,2775,2895,3019,3147,3279,3416,3558,3704,3854,4010,4171,4337,4509,4686,4869,5058,5253,5500,5663,5877,6099,6328,6564,6808"
#dijetbins = [1126,1181,1246,1313,1383,1455,1530,1607,1687,1770,1856,1945,2037,2132,2231,2332,2438,2546,2659,2775,2895,3019,3147,3279,3416,3558,3704,3854,4010,4171,4337,4509,4686,4869,5058,5253,5500] # ,7060,7320,7589]
dijetbins = [1126,1181,1246,1313,1383,1455,1530,1607,1687,1770,1856,1945,2037,2132,2231,2332,2438,2546,2659,2775,2895,3019,3147,3279,3416,3558,3704,3854,4010,4171,4337,4509,4686,4869,5058,5253,5455,5663,5877,6099,6328,6564,6808,7060,7320,7589]
HCALbinsMVV  =" --binsMVV "
HCALbinsMVV += ','.join(str(e) for e in dijetbins)

minMVV = float(dijetbins[0])
maxMVV = float(dijetbins[-1])
binsMVV= len(dijetbins)-1
    
  
  
    
catVtag = {}
catHtag = {}


#MassDecorrelatedDeepBoosted_WvsQCD with fixed mistag rate 
print "################     you are using DeepAK8 WvsQCD with fixed mistag rate !! !!!!! #########"        
catVtag['HP1'] = '(jj_l1_DeepBoosted_WvsQCD>jj_l1_DeepBoosted_WvsQCD__0p05_default_16)'                                                                                           
catVtag['HP2'] = '(jj_l2_DeepBoosted_WvsQCD>jj_l2_DeepBoosted_WvsQCD__0p05_default_16)'                                                                                           
catVtag['LP1'] = '((jj_l1_DeepBoosted_WvsQCD<jj_l1_DeepBoosted_WvsQCD__0p05_default_16)&&(jj_l1_DeepBoosted_WvsQCD>jj_l1_DeepBoosted_WvsQCD__0p10_default_16))'                                                       
catVtag['LP2'] = '((jj_l2_DeepBoosted_WvsQCD<jj_l2_DeepBoosted_WvsQCD__0p05_default_16)&&(jj_l2_DeepBoosted_WvsQCD>jj_l2_DeepBoosted_WvsQCD__0p10_default_16))'                                                       
catVtag['NP1'] = '(jj_l1_DeepBoosted_WvsQCD<jj_l1_DeepBoosted_WvsQCD__0p10_default_16)'                                                                                           
catVtag['NP2'] = '(jj_l2_DeepBoosted_WvsQCD<jj_l2_DeepBoosted_WvsQCD__0p10_default_16)'



print "################     you are using DeepAK8 ZHbbvsQCD  with fixed mistag rate !!  !!!!! #########"  
catHtag['HP1'] = '(jj_l1_DeepBoosted_ZHbbvsQCD>jj_l1_DeepBoosted_ZHbbvsQCD__0p02_default_16)' 
catHtag['HP2'] = '(jj_l2_DeepBoosted_ZHbbvsQCD>jj_l2_DeepBoosted_ZHbbvsQCD__0p02_default_16)' 
catHtag['LP1'] = '(jj_l1_DeepBoosted_ZHbbvsQCD<jj_l1_DeepBoosted_ZHbbvsQCD__0p02_default_16&&jj_l1_DeepBoosted_ZHbbvsQCD>jj_l1_DeepBoosted_ZHbbvsQCD__0p10_default_16)' 
catHtag['LP2'] = '(jj_l2_DeepBoosted_ZHbbvsQCD<jj_l2_DeepBoosted_ZHbbvsQCD__0p02_default_16&&jj_l2_DeepBoosted_ZHbbvsQCD>jj_l2_DeepBoosted_ZHbbvsQCD__0p10_default_16)'
catHtag['NP1'] = '(jj_l1_DeepBoosted_ZHbbvsQCD<jj_l1_DeepBoosted_ZHbbvsQCD__0p10_default_16)' 
catHtag['NP2'] = '(jj_l2_DeepBoosted_ZHbbvsQCD<jj_l2_DeepBoosted_ZHbbvsQCD__0p10_default_16)'
cuts={}

cuts['common'] = '((HLT_JJ)*(run>500) + (run<500))*(passed_METfilters&&passed_PVfilter&&njj>0&&jj_LV_mass>700&&abs(jj_l1_eta-jj_l2_eta)<1.3&&jj_l1_softDrop_mass>0.&&jj_l2_softDrop_mass>0.&&TMath::Log(jj_l1_softDrop_mass**2/jj_l1_pt**2)<-1.8&&TMath::Log(jj_l2_softDrop_mass**2/jj_l2_pt**2)<-1.8)'
cuts['common_VV'] = '((HLT_JJ)*(run>500) + (run<500))*(passed_METfilters&&passed_PVfilter&&njj&&!njj_vbf&&jj_LV_mass>700&&abs(jj_l1_eta-jj_l2_eta)<1.3&&jj_l1_softDrop_mass>0.&&jj_l2_softDrop_mass>0.&&TMath::Log(jj_l1_softDrop_mass**2/jj_l1_pt**2)<-1.8&&TMath::Log(jj_l2_softDrop_mass**2/jj_l2_pt**2)<-1.8)'
cuts['common_VBF'] = '((HLT_JJ)*(run>500) + (run<500))*(passed_METfilters&&passed_PVfilter&&njj_vbf&&jj_LV_mass>700&&abs(jj_l1_eta-jj_l2_eta)<1.3&&jj_l1_softDrop_mass>0.&&jj_l2_softDrop_mass>0.&&TMath::Log(jj_l1_softDrop_mass**2/jj_l1_pt**2)<-1.8&&TMath::Log(jj_l2_softDrop_mass**2/jj_l2_pt**2)<-1.8)'

cuts['NP']='1.'


#these will probably change to use mergedHTruth as well? do we need a mergedTopTruth?
cuts['nonres'] = '1'
cuts['res'] = '(jj_l1_mergedVTruth==1&&jj_l1_softDrop_mass>60&&jj_l1_softDrop_mass<120)'
cuts['resTT'] = '(jj_l1_mergedVTruth==1&&jj_l1_softDrop_mass>140&&jj_l1_softDrop_mass<200)'

cuts['acceptance']= "(jj_LV_mass>{minMVV}&&jj_LV_mass<{maxMVV}&&jj_l1_softDrop_mass>{minMJ}&&jj_l1_softDrop_mass<{maxMJ}&&jj_l2_softDrop_mass>{minMJ}&&jj_l2_softDrop_mass<{maxMJ})".format(minMVV=minMVV,maxMVV=maxMVV,minMJ=minMJ,maxMJ=maxMJ)
cuts['acceptanceMJ']= "(jj_l1_softDrop_mass>{minMJ}&&jj_l1_softDrop_mass<{maxMJ}&&jj_l2_softDrop_mass>{minMJ}&&jj_l2_softDrop_mass<{maxMJ})".format(minMJ=minMJ,maxMJ=maxMJ)
cuts['acceptanceMVV'] = "(jj_LV_mass>{minMVV}&&jj_LV_mass<{maxMVV})".format(minMVV=minMVV,maxMVV=maxMVV)
cuts['acceptanceGEN']='(jj_l1_gen_softDrop_mass>{minGenMJ}&&jj_l2_gen_softDrop_mass>{minGenMJ}&&jj_l1_gen_softDrop_mass<{maxGenMJ}&&jj_l2_gen_softDrop_mass<{maxGenMJ}&&jj_gen_partialMass>{minGenMVV}&&jj_gen_partialMass<{maxGenMVV}&&TMath::Log(jj_l1_gen_softDrop_mass**2/jj_l1_gen_pt**2)<-1.5&&TMath::Log(jj_l2_gen_softDrop_mass**2/jj_l2_gen_pt**2)<-1.5)'.format(minGenMVV=minGenMVV,maxGenMVV=maxGenMVV,minGenMJ=minGenMJ,maxGenMJ=maxGenMJ)
cuts['looseacceptanceMJ']= "(jj_l1_softDrop_mass>35&&jj_l1_softDrop_mass<300&&jj_l2_softDrop_mass>35&&jj_l2_softDrop_mass<300)"


print "Use random sorting!"
print "ortoghonal VV + VH"
catsAll = {}
#scheme 2: improves VV HPHP (VH_HPHP -> VV_HPHP -> VH_LPHP,VH_HPLP -> VV_HPLP) 
#at least one H tag HP (+ one V/H tag HP)                                                                                                                                                                                                                                     
catsAll['VH_HPHP'] = '('+'&&'.join([catVtag['HP1'],catHtag['HP2']])+')'
catsAll['HV_HPHP'] = '('+'&&'.join([catHtag['HP1'],catVtag['HP2']])+')'
catsAll['HH_HPHP'] = '('+'&&'.join([catHtag['HP1'],catHtag['HP2']])+')'
cuts['VH_HPHP'] = '('+'||'.join([catsAll['VH_HPHP'],catsAll['HV_HPHP'],catsAll['HH_HPHP']])+')'

# two V tag HP                                                                                                                                                                                                                                                                
cuts['VV_HPHP'] = '('+'!'+cuts['VH_HPHP']+'&&'+'(' +  '&&'.join([catVtag['HP1'],catVtag['HP2']]) + ')' + ')'

#at least one H-tag HP (+one V OR H-tag LP)                                                                                                                                                                                                                                   
catsAll['VH_LPHP'] = '('+'&&'.join([catVtag['LP1'],catHtag['HP2']])+')'
catsAll['HV_HPLP'] = '('+'&&'.join([catHtag['HP1'],catVtag['LP2']])+')'
catsAll['HH_HPLP'] = '('+'&&'.join([catHtag['HP1'],catHtag['LP2']])+')'
catsAll['HH_LPHP'] = '('+'&&'.join([catHtag['LP1'],catHtag['HP2']])+')'
cuts['VH_LPHP'] = '('+'('+'!'+cuts['VH_HPHP']+'&&!'+cuts['VV_HPHP']+')&&('+'||'.join([catsAll['VH_LPHP'],catsAll['HV_HPLP'],catsAll['HH_HPLP'],catsAll['HH_LPHP']])+')'+')'

#at least one V-tag HP (+ one H-tag LP)                                  
catsAll['VH_HPLP'] = '('+'&&'.join([catVtag['HP1'],catHtag['LP2']])+')'
catsAll['HV_LPHP'] = '('+'&&'.join([catHtag['LP1'],catVtag['HP2']])+')'
cuts['VH_HPLP'] = '('+'('+'!'+cuts['VH_LPHP']+'&&!'+cuts['VH_HPHP']+'&&!'+cuts['VV_HPHP']+')&&('+'||'.join([catsAll['VH_HPLP'],catsAll['HV_LPHP']])+')'+')'

cuts['VH_all'] =  '('+  '||'.join([cuts['VH_HPHP'],cuts['VH_LPHP'],cuts['VH_HPLP']]) + ')'

cuts['VV_HPLP'] = '(' +'('+'!'+cuts['VH_all']+') &&' + '(' + '('+  '&&'.join([catVtag['HP1'],catVtag['LP2']]) + ')' + '||' + '(' + '&&'.join([catVtag['HP2'],catVtag['LP1']]) + ')' + ')' + ')'

