# make tree containing genweight, other event weights, as well as is jet H/ V jet, what category is the event classified in, what V/Htag has each jet -> for each signal sample!
#use this as input for the migrationUncertainties.py script
import ROOT
import os, sys, re, optparse,pickle,shutil,json
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
from array import array
ROOT.gROOT.ProcessLine("struct rootint { Int_t ri;};")
from ROOT import rootint
ROOT.gROOT.ProcessLine("struct rootfloat { Float_t rf;};")
from ROOT import rootfloat
ROOT.gROOT.ProcessLine("struct rootlong { Long_t li;};")
from ROOT import rootlong
import cuts
from rootpy.tree import CharArrayCol



parser = optparse.OptionParser()
parser.add_option("-y","--year",dest="year",default='2016',help="year of data taking")
parser.add_option("-s","--signal",dest="signal",help="signal to categorise",default='ZprimeToZh')
parser.add_option("-d","--directory",dest="directory",help="directory with signal samples",default='2016_new/')

(options,args) = parser.parse_args()


def getSamplelist(directory,signal):
    samples =[]
    for filename in os.listdir(directory):
      if filename.find(signal)!=-1 and filename.find('root')!=-1:
        if filename.find("VBF")!=-1 and signal.find("VBF")==-1: continue  
        samples.append(directory+filename)
    print samples
    return samples



def selectSignalTree(cs,sample):
    rfile = ROOT.TFile(sample,'READ')
    tree = rfile.Get('AnalysisTree')
    outfile = ROOT.TFile('tmp.root','RECREATE')
    finaltree = tree.CopyTree(cs['common']+'*'+cs['acceptance'])
    print 'overall entries in tree '+str(tree.GetEntries())
    print 'entries after analysis selections '+str(finaltree.GetEntries())
    signaltree_VH_HPHP = finaltree.CopyTree(cs['VH_HPHP'])
    signaltree_VV_HPHP = finaltree.CopyTree(cs['VV_HPHP'])#all other categories before are explicitly removed so that each event can only live in one category!!
    signaltree_VH_LPHP = finaltree.CopyTree(cs['VH_LPHP'])
    signaltree_VH_HPLP = finaltree.CopyTree(cs['VH_HPLP'])
    signaltree_VV_HPLP = finaltree.CopyTree(cs['VV_HPLP'])
    rest = finaltree.CopyTree('!('+cs['VV_HPLP']+')*!('+cs['VH_LPHP']+')*!('+cs['VH_HPLP']+')*!('+cs['VH_HPHP']+')*!('+cs['VV_HPHP']+')')
    print ' #event VH_HPHP '+str(signaltree_VH_HPHP.GetEntries())+' #event VV_HPHP '+str(signaltree_VV_HPHP.GetEntries())+' #event VH_LPHP '+str(signaltree_VH_LPHP.GetEntries())+' #event VH_LPHP '+str(signaltree_VH_LPHP.GetEntries())+' #event VV_HPLP '+str(signaltree_VV_HPLP.GetEntries())
    print '#event no category '+str(rest.GetEntries())
    sumcat = signaltree_VH_HPHP.GetEntries()+signaltree_VV_HPHP.GetEntries()+signaltree_VH_LPHP.GetEntries()+signaltree_VH_HPLP.GetEntries()+signaltree_VV_HPLP.GetEntries()
    print 'sum '+str(sumcat)
    print 'overall signal efficiency after selection cut '+str(finaltree.GetEntries()/float(tree.GetEntries()))
    print 'signal efficiency after category cuts '+str(sumcat/float(tree.GetEntries()))
    print 'efficiency of all category cuts '+str(sumcat/float(finaltree.GetEntries()))
    #inversetree = tree.CopyTree('!('+cuts['common']+'*'+cuts['acceptance']+')')
    #print inversetree.GetEntries()
    #print inversetree.GetEntries()+finaltree.GetEntries()
    signaltree_VH_HPHP.SetName('VH_HPHP')
    signaltree_VV_HPHP.SetName('VV_HPHP')
    signaltree_VH_LPHP.SetName('VH_LPHP')
    signaltree_VH_HPLP.SetName('VH_HPLP')
    signaltree_VV_HPLP.SetName('VV_HPLP')
    
    signaltree_VH_HPHP.Write()
    signaltree_VV_HPHP.Write()
    signaltree_VH_LPHP.Write()
    signaltree_VH_HPLP.Write()
    signaltree_VV_HPLP.Write()
    outfile.Close()

class myTree:
    
    run = rootint()
    lumi = rootint()
    puWeight  = rootfloat()
    genWeight = rootfloat()
    xsec      = rootfloat()
    evt       = rootlong()
    
    jj_l1_mergedVTruth           = rootint()
    jj_l2_mergedVTruth           = rootint()
    
    jj_l1_mergedHTruth           = rootint()
    jj_l2_mergedHTruth           = rootint()
    
    jj_l1_mergedZbbTruth           = rootint()
    jj_l2_mergedZbbTruth           = rootint()
    
    jj_l1_jetTag           = bytearray(6)
    jj_l2_jetTag           = bytearray(6)
    
    category               =  bytearray(7)
    newTree = None
    File = None
    
    def __init__(self, treename,outfile):
        self.File = outfile
        self.File.cd()
    #ROOT.gROOT.ProcessLine("struct string { TString s;};")
    #from ROOT import string
        self.newTree = ROOT.TTree(treename,treename)
        
        self.newTree.Branch("run",self.run,"run/i")
        self.newTree.Branch("lumi",self.lumi,"lumi/i")
        self.newTree.Branch("evt",self.evt,"evt/l")
        self.newTree.Branch("xsec",(self.xsec),"xsec/F")        
        self.newTree.Branch("puWeight",(self.puWeight),"puWeight/F")                 
        self.newTree.Branch("genWeight",(self.genWeight),"genWeight/F")
   
        self.newTree.Branch("jj_l1_mergedVTruth",self.jj_l1_mergedVTruth,"jj_l1_mergedVTruth/i")
        self.newTree.Branch("jj_l2_mergedVTruth",self.jj_l2_mergedVTruth,"jj_l2_mergedVTruth/i")
        self.newTree.Branch("jj_l1_mergedHTruth",self.jj_l1_mergedHTruth,"jj_l1_mergedHTruth/i")
        self.newTree.Branch("jj_l2_mergedHTruth",self.jj_l2_mergedHTruth,"jj_l2_mergedHTruth/i")
        
        self.newTree.Branch("jj_l1_mergedZbbTruth",self.jj_l1_mergedZbbTruth,"jj_l1_mergedZbbTruth/i")
        self.newTree.Branch("jj_l2_mergedZbbTruth",self.jj_l2_mergedZbbTruth,"jj_l2_mergedZbbTruth/i")
   
        self.newTree.Branch("jj_l1_jetTag",self.jj_l1_jetTag,"jj_l1_jetTag[6]/C")
        self.newTree.Branch("jj_l2_jetTag",self.jj_l1_jetTag,"jj_l2_jetTag[6]/C")
     
        self.newTree.Branch("category",self.category,"category[7]/C")
        
    def setOutputTreeBranchValues(self,cat,ctx):
        rf = ROOT.TFile('tmp.root','READ')
        cattree = rf.Get(cat)
        ZHbb_branch_l1 = cattree.GetBranch(ctx.varl1Htag)
        ZHbb_leaf_l1 = ZHbb_branch_l1.GetLeaf(ctx.varl1Htag)
        W_branch_l1 = cattree.GetBranch(ctx.varl1Wtag)
        W_leaf_l1 = W_branch_l1.GetLeaf(ctx.varl1Wtag)
        ZHbb_branch_l2 = cattree.GetBranch(ctx.varl2Htag)
        ZHbb_leaf_l2 = ZHbb_branch_l2.GetLeaf(ctx.varl2Htag)
        W_branch_l2 = cattree.GetBranch(ctx.varl2Wtag)
        W_leaf_l2 = W_branch_l2.GetLeaf(ctx.varl2Wtag)
        
        
        WPHP_ZHbb_branch_l1 = cattree.GetBranch(ctx.WPHPl1Htag)
        WPHP_ZHbb_leaf_l1 = WPHP_ZHbb_branch_l1.GetLeaf(ctx.WPHPl1Htag)
        WPHP_W_branch_l1 = cattree.GetBranch(ctx.WPHPl1Wtag)
        WPHP_W_leaf_l1 = WPHP_W_branch_l1.GetLeaf(ctx.WPHPl1Wtag)
        
        WPHP_ZHbb_branch_l2 = cattree.GetBranch(ctx.WPHPl2Htag)
        WPHP_ZHbb_leaf_l2 = WPHP_ZHbb_branch_l2.GetLeaf(ctx.WPHPl2Htag)
        WPHP_W_branch_l2 = cattree.GetBranch(ctx.WPHPl2Wtag)
        WPHP_W_leaf_l2 = WPHP_W_branch_l2.GetLeaf(ctx.WPHPl2Wtag)
        
        
        WPLP_ZHbb_branch_l1 = cattree.GetBranch(ctx.WPLPl1Htag)
        WPLP_ZHbb_leaf_l1 = WPLP_ZHbb_branch_l1.GetLeaf(ctx.WPLPl1Htag)
        WPLP_W_branch_l1 = cattree.GetBranch(ctx.WPLPl1Wtag)
        WPLP_W_leaf_l1 = WPLP_W_branch_l1.GetLeaf(ctx.WPLPl1Wtag)
        
        WPLP_ZHbb_branch_l2 = cattree.GetBranch(ctx.WPLPl2Htag)
        WPLP_ZHbb_leaf_l2 = WPLP_ZHbb_branch_l2.GetLeaf(ctx.WPLPl2Htag)
        WPLP_W_branch_l2 = cattree.GetBranch(ctx.WPLPl2Wtag)
        WPLP_W_leaf_l2 = WPLP_W_branch_l2.GetLeaf(ctx.WPLPl2Wtag)
        
        
        for event in cattree:
            self.puWeight.rf       = event.puWeight 
            self.genWeight.rf      = event.genWeight
            self.xsec.rf           = event.xsec     
            self.evt.rl            = event.evt                  
            self.lumi.ri           = event.lumi
            self.run.ri = event.run 
            
            self.jj_l1_mergedVTruth.ri = event.jj_l1_mergedVTruth
            self.jj_l2_mergedVTruth.ri = event.jj_l2_mergedVTruth
            self.jj_l1_mergedHTruth.ri = event.jj_l1_mergedHTruth
            self.jj_l2_mergedHTruth.ri = event.jj_l2_mergedHTruth
            self.jj_l1_mergedZbbTruth.ri = event.jj_l1_mergedZbbTruth
            self.jj_l2_mergedZbbTruth.ri = event.jj_l2_mergedZbbTruth
            self.category[:7] = cat 
            # this depends now on the actual cuts in the analysis!!
            
            if ZHbb_leaf_l1.GetValue() > WPHP_ZHbb_leaf_l1.GetValue():
                self.jj_l1_jetTag[:6] = 'HPHtag'
            elif W_leaf_l1.GetValue() > WPHP_W_leaf_l1.GetValue():
                self.jj_l1_jetTag[:6] = 'HPVtag'
            elif ZHbb_leaf_l1.GetValue() > WPLP_ZHbb_leaf_l1.GetValue():
                self.jj_l1_jetTag[:6] = 'LPHtag'
            elif W_leaf_l1.GetValue() > WPLP_W_leaf_l1.GetValue():
                self.jj_l1_jetTag[:6] = 'LPVtag'
            else:
                self.jj_l1_jetTag[:6] = 'Notag'
                
            #print   WPLP_W_leaf_l1.GetValue()  
            if ZHbb_leaf_l2.GetValue() > WPHP_ZHbb_leaf_l2.GetValue():
                self.jj_l2_jetTag[:6] = 'HPHtag'
            elif W_leaf_l2.GetValue() > WPHP_W_leaf_l2.GetValue():
                self.jj_l2_jetTag[:6] = 'HPVtag'
            elif ZHbb_leaf_l2.GetValue() > WPLP_ZHbb_leaf_l2.GetValue():
                self.jj_l2_jetTag[:6] = 'LPHtag'
            elif W_leaf_l2.GetValue() > WPLP_W_leaf_l2.GetValue():
                self.jj_l2_jetTag[:6] = 'LPVtag'
            else:
                self.jj_l2_jetTag[:6] = 'Notag'
                    
           
            
            #print self.jj_l1_jetTag
            self.newTree.Fill()
        print 'number of events in this category '+str(self.newTree.GetEntries())

    def test(self):
        for event in self.newTree:
            print event.jj_l1_mergedVTruth
    def write(self):
        self.File.cd()
        self.newTree.Write()

if __name__=='__main__':
    outfile = ROOT.TFile('migrationunc/'+options.signal+'_'+options.year+'.root','RECREATE')
    if options.directory.find(options.year)== -1: print 'ATTENTION: are you sure you are using the right directory for '+options.year+' data?'    
    ctx  = cuts.cuts("init_VV_VH.json",int(options.year),"random_dijetbins")
    samplelist= getSamplelist(options.directory,options.signal)
    for sample in samplelist:
        print sample
        print 'init new tree'
        outtree = myTree(sample.split('.root')[0].replace(options.directory,''),outfile)
        print 'select common cuts signal tree' 
        selectSignalTree(ctx.cuts,sample)
        
        #for t in signaltrees:
        outtree.setOutputTreeBranchValues('VH_HPHP',ctx)
        outtree.setOutputTreeBranchValues('VV_HPHP',ctx)
        outtree.setOutputTreeBranchValues('VH_LPHP',ctx)
        outtree.setOutputTreeBranchValues('VH_HPLP',ctx)
        outtree.setOutputTreeBranchValues('VV_HPLP',ctx)
        
        #outtree.test()
        outfile.cd()
        outtree.write()
        #tree.Write(outfile.GetName())
        
        
        