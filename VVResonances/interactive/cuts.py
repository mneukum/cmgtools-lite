
# class to initialize all analysis cuts
# init_ VV_VH.json contains all analysis cuts! -> need category import this file
import json
import ast

class cuts():
    lumi = 1.
    yeartag = "16"
    HPSF = 1.
    LPSF = 1.
    
    minMJ = 0.
    maxMJ = 0.
    binsMJ = 0.
    
    minMVV = 0.0
    maxMVV = 0.0
    binsMVV = 0.
    
    minMX = 0.
    maxMX = 0.
    
    HCALbinsMVV  =" --binsMVV "
    HCALbinsMVVSignal= " --binsMVV "
    
    fixParsSig = {}
    fixParsSigMVV ={}
    catVtag = {}
    catHtag = {}
    

    
    cuts={}
    
    
    def __init__(self,jsonfile,year,options):
        
        with open(jsonfile) as json_file:
                     
            
            data = json.load(json_file)
            ##### load binning and cut offs
            self.minMJ = data["ranges_and_binning"]["minMJ"]
            self.maxMJ = data["ranges_and_binning"]["maxMJ"]
            self.binsMJ = data["ranges_and_binning"]["binsMJ"]
            
            self.minMVV = data["ranges_and_binning"]["minMVV"]
            self.maxMVV = data["ranges_and_binning"]["maxMVV"]
            self.binsMVV = data["ranges_and_binning"]["binsMVV"]
            
            self.minMX = data["ranges_and_binning"]["minMX"]
            self.maxMX = data["ranges_and_binning"]["maxMX"]
            
            ## load SF for the different years 
            if year==2016:
                self.yeartag = "16"
            elif year==2017:
                self.yeartag = "17"
            elif year==2018:
                self.yeartag = "18"
                print " attention  lumi to be checked #to be checked! https://twiki.cern.ch/twiki/bin/view/CMS/PdmV2018Analysis"
            else: print "no such data taking year -> running with default values on 2016 data"
    
            self.lumi = data["lumi"+self.yeartag]

            self.fixParsSigMVV = data["fixParsSigMVV"]
            self.fixParsSig = data["fixParsSig"]
            self.HPSF = data['HPSF'+self.yeartag]
            self.LPSF = data['LPSF'+self.yeartag]
            self.catVtag['HP1'] = '('+data["tagging_variables_and_wp"]["varl1Wtag"]+'>'+ data["tagging_variables_and_wp"]["l1Wtag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_HP_Wtag"+self.yeartag])+')' 
            self.catVtag['HP2'] = '('+data["tagging_variables_and_wp"]["varl2Wtag"]+'>'+ data["tagging_variables_and_wp"]["l2Wtag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_HP_Wtag"+self.yeartag])+')' 
            self.catVtag['LP1'] = '(('+ data["tagging_variables_and_wp"]["varl1Wtag"]+'<'+ data["tagging_variables_and_wp"]["l1Wtag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_HP_Wtag"+self.yeartag]) +')&&('+ data["tagging_variables_and_wp"]["varl1Wtag"] +'>'+ data["tagging_variables_and_wp"]["l1Wtag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_LP_Wtag"+self.yeartag]) +'))' 
            self.catVtag['LP2'] = '(('+ data["tagging_variables_and_wp"]["varl2Wtag"]+'<'+ data["tagging_variables_and_wp"]["l2Wtag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_HP_Wtag"+self.yeartag]) +')&&('+ data["tagging_variables_and_wp"]["varl2Wtag"] +'>'+ data["tagging_variables_and_wp"]["l2Wtag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_LP_Wtag"+self.yeartag]) +'))'
            self.catVtag['NP1'] =  '('+data["tagging_variables_and_wp"]["varl1Wtag"] +'<' +data["tagging_variables_and_wp"]["l1Wtag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_LP_Wtag"+self.yeartag]) + ')' 
            self.catVtag['NP2'] =  '('+data["tagging_variables_and_wp"]["varl2Wtag"] +'<' +data["tagging_variables_and_wp"]["l2Wtag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_LP_Wtag"+self.yeartag]) + ')' 
            
            
            self.catHtag['HP1'] = '('+data["tagging_variables_and_wp"]["varl1Htag"]+'>'+ data["tagging_variables_and_wp"]["l1Htag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_HP_Htag"+self.yeartag])+')' 
            self.catHtag['HP2'] = '('+data["tagging_variables_and_wp"]["varl2Htag"]+'>'+ data["tagging_variables_and_wp"]["l2Htag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_HP_Htag"+self.yeartag])+')' 
            self.catHtag['LP1'] = '(('+ data["tagging_variables_and_wp"]["varl1Htag"]+'<'+ data["tagging_variables_and_wp"]["l1Htag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_HP_Htag"+self.yeartag]) +')&&('+ data["tagging_variables_and_wp"]["varl1Htag"] +'>'+ data["tagging_variables_and_wp"]["l1Htag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_LP_Htag"+self.yeartag]) +'))' 
            self.catHtag['LP2'] = '(('+ data["tagging_variables_and_wp"]["varl2Htag"]+'<'+ data["tagging_variables_and_wp"]["l2Htag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_HP_Htag"+self.yeartag]) +')&&('+ data["tagging_variables_and_wp"]["varl2Htag"] +'>'+ data["tagging_variables_and_wp"]["l2Htag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_LP_Htag"+self.yeartag]) +'))'
            self.catHtag['NP1'] =  '('+data["tagging_variables_and_wp"]["varl1Htag"] +'<' +data["tagging_variables_and_wp"]["l1Htag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_LP_Htag"+self.yeartag]) + ')' 
            self.catHtag['NP2'] =  '('+data["tagging_variables_and_wp"]["varl2Htag"] +'<' +data["tagging_variables_and_wp"]["l2Htag"+self.yeartag].replace("XX", data["tagging_variables_and_wp"]["WP_LP_Htag"+self.yeartag]) + ')' 
            
            selections = ["common","common_VV","common_VBF","NP","res","nonres","resTT","acceptance","acceptanceMJ","acceptanceMVV","acceptanceGEN","looseacceptanceMJ"]
            for sel in selections:
                self.cuts[sel] = data["selection_cuts"][sel]
                self.cuts[sel] = self.cuts[sel].replace("minMJ",str(self.minMJ))
                self.cuts[sel] = self.cuts[sel].replace("maxMJ",str(self.maxMJ))
                self.cuts[sel] = self.cuts[sel].replace("minMVV",str(self.minMVV))
                self.cuts[sel] = self.cuts[sel].replace("maxMVV",str(self.maxMVV))
            if options.find('dijetbins')!=-1:
                print "use dijet binning! "
                alldijetbins =  data["ranges_and_binning"]["dijetbins"]
                dijetbins = []
                for b in alldijetbins:
                    if b > self.maxMVV: continue
                    if b < self.minMVV: continue
                    dijetbins.append(b)
                
                
                self.HCALbinsMVV += ','.join(str(e) for e in dijetbins)

                self.minMVV = float(dijetbins[0])
                self.maxMVV = float(dijetbins[-1])
                self.binsMVV= len(dijetbins)-1
                
                dijetbins = []
                for b in alldijetbins:
                    if b > self.maxMX: continue
                    if b < self.minMX: continue
                    dijetbins.append(b)
                
                
                self.HCALbinsMVVSignal += ','.join(str(e) for e in dijetbins)
            else:
                self.HCALbinsMVV=""
                self.HCALbinsMVVSignal=""
            if options.find('random')!=-1:
                print "Use random sorting!"
                print "ortoghonal VV + VH"
                catsAll = {}
                #scheme 2: improves VV HPHP (VH_HPHP -> VV_HPHP -> VH_LPHP,VH_HPLP -> VV_HPLP) 
                #at least one H tag HP (+ one V/H tag HP)                                                                                                                                                                                                                                     
                catsAll['VH_HPHP'] = '('+'&&'.join([self.catVtag['HP1'],self.catHtag['HP2']])+')'
                catsAll['HV_HPHP'] = '('+'&&'.join([self.catHtag['HP1'],self.catVtag['HP2']])+')'
                catsAll['HH_HPHP'] = '('+'&&'.join([self.catHtag['HP1'],self.catHtag['HP2']])+')'
                self.cuts['VH_HPHP'] = '('+'||'.join([catsAll['VH_HPHP'],catsAll['HV_HPHP'],catsAll['HH_HPHP']])+')'

                # two V tag HP                                                                                                                                                                                                                                                                
                self.cuts['VV_HPHP'] = '('+'!'+self.cuts['VH_HPHP']+'&&'+'(' +  '&&'.join([self.catVtag['HP1'],self.catVtag['HP2']]) + ')' + ')'

                #at least one H-tag HP (+one V OR H-tag LP)                                                                                                                                                                                                                                   
                catsAll['VH_LPHP'] = '('+'&&'.join([self.catVtag['LP1'],self.catHtag['HP2']])+')'
                catsAll['HV_HPLP'] = '('+'&&'.join([self.catHtag['HP1'],self.catVtag['LP2']])+')'
                catsAll['HH_HPLP'] = '('+'&&'.join([self.catHtag['HP1'],self.catHtag['LP2']])+')'
                catsAll['HH_LPHP'] = '('+'&&'.join([self.catHtag['LP1'],self.catHtag['HP2']])+')'
                self.cuts['VH_LPHP'] = '('+'('+'!'+self.cuts['VH_HPHP']+'&&!'+self.cuts['VV_HPHP']+')&&('+'||'.join([catsAll['VH_LPHP'],catsAll['HV_HPLP'],catsAll['HH_HPLP'],catsAll['HH_LPHP']])+')'+')'

                #at least one V-tag HP (+ one H-tag LP)                                  
                catsAll['VH_HPLP'] = '('+'&&'.join([self.catVtag['HP1'],self.catHtag['LP2']])+')'
                catsAll['HV_LPHP'] = '('+'&&'.join([self.catHtag['LP1'],self.catVtag['HP2']])+')'
                self.cuts['VH_HPLP'] = '('+'('+'!'+self.cuts['VH_LPHP']+'&&!'+self.cuts['VH_HPHP']+'&&!'+self.cuts['VV_HPHP']+')&&('+'||'.join([catsAll['VH_HPLP'],catsAll['HV_LPHP']])+')'+')'

                self.cuts['VH_all'] =  '('+  '||'.join([self.cuts['VH_HPHP'],self.cuts['VH_LPHP'],self.cuts['VH_HPLP']]) + ')'

                self.cuts['VV_HPLP'] = '(' +'('+'!'+self.cuts['VH_all']+') &&' + '(' + '('+  '&&'.join([self.catVtag['HP1'],self.catVtag['LP2']]) + ')' + '||' + '(' + '&&'.join([self.catVtag['HP2'],self.catVtag['LP1']]) + ')' + ')' + ')'
            else:
                print "Use b-tagging sorting"
                self.cuts['VH_HPHP'] = '('+  '&&'.join([self.catHtag['HP1'],self.catVtag['HP2']]) + ')'
                self.cuts['VH_HPLP'] = '('+  '&&'.join([self.catHtag['HP1'],self.catVtag['LP2']]) + ')'
                self.cuts['VH_LPHP'] = '('+  '&&'.join([self.catHtag['LP1'],self.catVtag['HP2']]) + ')'
                self.cuts['VH_LPLP'] = '('+  '&&'.join([self.catHtag['LP1'],self.catVtag['LP2']]) + ')'
                self.cuts['VH_all'] =  '('+  '||'.join([self.cuts['VH_HPHP'],self.cuts['VH_HPLP'],self.cuts['VH_LPHP'],self.cuts['VH_LPLP']]) + ')'
                self.cuts['VV_HPHP'] = '(' + '!' + self.cuts['VH_all'] + '&&' + '(' + '&&'.join([self.catVtag['HP1'],self.catVtag['HP2']]) + ')' + ')'
                self.cuts['VV_HPLP'] = '(' + '!' + self.cuts['VH_all'] + '&&' + '(' + '('+  '&&'.join([self.catVtag['HP1'],self.catVtag['LP2']]) + ')' + '||' + '(' + '&&'.join([self.catVtag['HP2'],self.catVtag['LP1']]) + ')' + ')' + ')'



if __name__ == "__main__":
    c = cuts("init_VV_VH.json",2016,"dijetbins_random")
    print c.HPSF
    print c.LPSF
    print c.minMJ
    print c.catVtag['LP1']
    
    print c.catHtag['LP1']
    print c.maxMX
    print c.HCALbinsMVV 
    print c.HCALbinsMVVSignal 
    
    print c.cuts["VV_HPHP"]
    
    selections = ["common","common_VV","common_VBF","NP","res","nonres","resTT","acceptance","acceptanceMJ","acceptanceMVV","acceptanceGEN","looseacceptanceMJ"]
    
    for sel in selections:
        print c. cuts[sel]
    
    
    print c.fixParsSig["ZprimeWW"]['NP']