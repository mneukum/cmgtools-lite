
#!/usr/bin/env python
import os, re
import commands
import math, time
import sys
import random

def makeSubmitFileCondor(exe,jobname,jobflavour):
    print "make options file for condor job submission "
    submitfile = open("submit.sub","w")
    submitfile.write("executable  = "+exe+"\n")
    submitfile.write("arguments             = $(ClusterID) $(ProcId)\n")
    submitfile.write("output                = "+jobname+".$(ClusterId).$(ProcId).out\n")
    submitfile.write("error                 = "+jobname+".$(ClusterId).$(ProcId).err\n")
    submitfile.write("log                   = "+jobname+".$(ClusterId).log\n")
    submitfile.write('+JobFlavour           = "'+jobflavour+'"\n')
    submitfile.write("queue")
    submitfile.close()    
    
print 
print 'START'
print 
########   YOU ONLY NEED TO FILL THE AREA BELOW   #########
########   customization  area #########
NumberOfJobs= 100 # number of jobs to be submitted
queue = "8nh" # give bsub queue -- 8nm (8 minutes), 1nh (1 hour), 8nh, 1nd (1day), 2nd, 1nw (1 week), 2nw 
mydir = os.getcwd()
tmpdir = "tmp_mlfit_combo_m1200_pythia_2/"
jobdir = "/eos/cms/store/cmst3/group/exovv/bias_test_new/res_mlfit_combo_m1200_pythia_2/"
tmpdir2 = "/eos/cms/store/cmst3/group/exovv/bias_test_new/tmp_mlfit_combo_m1200_pythia_2/"
########   customization end   #########

path = os.getcwd()
workspace = path+"/workspace.root"
print
print 'do not worry about folder creation:'
os.system("rm -r %s"%tmpdir)
os.system("mkdir %s"%tmpdir)
os.system("rm -r %s"%tmpdir2)
os.system("mkdir %s"%tmpdir2)
os.system("mkdir %s"%jobdir)
print

##### loop for creating and sending jobs #####
for x in range(1, int(NumberOfJobs)+1):
   ##### creates directory and file list for job #######
   os.system("mkdir %s/job%i"%(tmpdir,x))
   os.system("mkdir %s/job%i"%(tmpdir2,x))
   os.chdir("%s/job%i"%(tmpdir,x))
   path = os.getcwd()
   
   ##### creates jobs #######
   with open('job.sh', 'w') as fout:
      fout.write("#!/bin/sh\n")
      fout.write("echo\n")
      fout.write("echo\n")
      fout.write("echo 'START---------------'\n")
      fout.write("echo 'WORKDIR ' ${PWD}\n")
      fout.write("source /afs/cern.ch/cms/cmsset_default.sh\n")
      fout.write("cd "+str(path)+"\n")
      fout.write("cmsenv\n")
      fout.write("python %s/run_mlfit_jobs_bigcombo_forCondor.py --k1 2016/save_new_shapes_pythia_HPHP_3D.root --k2 2016/save_new_shapes_pythia_HPLP_3D.root --mc pythia --i1 2016/JJ_nonRes_HPHP.root --i2 2016/JJ_nonRes_HPLP.root -t 5 -l job%i -w %s -d %s --mass 1200 --expectedSignal 40.0 --tmpdir %s\n"%(mydir,x,mydir,jobdir,tmpdir2+"/job"+str(x)))
      fout.write("echo 'STOP---------------'\n")
      fout.write("echo\n")
      fout.write("echo\n")
   os.system("chmod 755 job.sh")
   
   ###### sends bjobs ######
   makeSubmitFileCondor("job.sh","job","workday")
   os.system("condor_submit submit.sub")
   print "job nr " + str(x) + " submitted"
   
   os.chdir("../..")
   
print
print "your jobs:"
os.system("condor_q")
print
print 'END'
print
