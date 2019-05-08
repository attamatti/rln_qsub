#!/usr/bin/env python

## to add
# check if using only local searches
# make sure job isn't a continuations

import glob
import os
#get the arc jobs
files = glob.glob('*/job*/run.out')
goodfiles = []
for i in files:
    if i.split('/')[0] in ('Class3D','Class2D','Refine3D'):
        goodfiles.append(i)

def check_file(rlnfile):
    data = open(rlnfile,'r').readlines()
    for j in data:
        if 'Master  (0) runs on host' in j:
            host = j.split('=')[-1].split('.')[1]
    if host == 'arc3':
        return(True)

filestorunon = []
for i in goodfiles:
    if check_file(i) ==True:
        filestorunon.append(i)
        
#get the stats for each arc job
def get_params(rlnjobfile):
    jobdata = open(rlnjobfile,'r').readlines()
    helical = '0'
    nclasses = '1'
    for i in jobdata:
        line = i.split('==')
        if line[0] == 'Do helical reconstruction? ':
            if line[1] == 'Yes':
                helical = line[1]
            else:
                helical= 'False'
        elif line[0] == 'Number of classes: ':
            nclasses = line[1].replace('\n','')
        elif line[0] == 'Mask diameter (A): ':
            diameter = line[1].replace('\n','')
        elif line[0] == 'Number of MPI procs: ':
            nprocs = line[1].replace('\n','')
        elif line[0] == 'Number of threads: ':
            nthreads = line[1].replace('\n','')
        elif line[0]== 'Local searches from auto-sampling: ':
            lss = line[1].split()[0].replace('\n','')
        elif line[0] == 'Initial angular sampling: ':
            ias = line[1].split()[0].replace('\n','')
        elif line[0] == 'is_continue ':
            conti = line[1].replace('\n','')
        elif line[0] == 'Perform local angular searches? ':
            c3dlas = line[1].replace('\n','')
        elif line[0] == 'Number of iterations: ':
            niter = line[-1].replace('\n','')
    # get the number of particles
    dir = '/'.join(jobfile.split('/')[0:-1])
    partsdata = open('{0}/run_submit.script'.format(dir),'r').readlines()
    n=0
    nodetype = partsdata[7].split()[2]
    for i in partsdata[-2].split():
        if i == '--i':
            partsfile = partsdata[-2].split()[n+1]
            break
        if i == '--continue':
            partsfile = partsdata[-2].split()[n+1]  
            break
        n+=1
    try:
        str(lss)
        str(ias)
    except:
        lss = '0'
        ias = '1'
    try:
        str(c3dlas)
    except:
        c3dlas = ' No'
    try:
        str(niter)
    except:
        niter = '-1'
    try:
        str(helical)
    except:
        helical = 'False'
    try:
        nparts = len(open(partsfile,'r').readlines())
    except:
        nparts = 0
    
    return([helical,str(nparts),nclasses,diameter,nprocs,nthreads,nodetype,lss,ias,conti,c3dlas,niter])

def get_times(rlnrunfile,iters):
    tottime = 0
    tmult = {'sec':1.0,'min':60.0,'hrs':3600.0}
    rundata = open(rlnrunfile,'r').readlines()
    for i in rundata:
        if i.split(',_,')[-1] == '">\n':
            rtime = i.split('/')[-1].split()[0:2]
            time = float(rtime[0])*tmult[rtime[1]]
            tottime += time
     #check if the job actually finished...
    if rundata[-1] == ' Auto-refine: + But you may want to run relion_postprocess to mask the unfil.mrc maps and calculate a higher resolution FSC\n' or rundata[-4] ==' Expectation iteration {0} of {0}\n'.format(iters):
        finished = 'True'
    else:
        finished = 'False'
    return(str(tottime),finished)

finalout = open('/fbs/emsoftware2/LINUX/fbsmi/scripts/workshop/rln_queuefix/data/arcstats_{0}.csv'.format(os.getcwd().split('/')[-1]),'w')
finalout.write('dir,jobfile,outfile,helical,nparts,nclasses,diameter,nprocs,nthreads,nodetype,lss,ias,conti,c3dlas,niter,TIME(s),Finished?\n')
for i in filestorunon:
    print i
    try:
        dir = '/'.join(i.split('/')[:-1])
        jobfile ='{0}/run.job'.format(dir)
        runfile ='{0}/run.out'.format(dir)
        finalout.write('{0},'.format(os.getcwd()))
        finalout.write('{0},{1},'.format(i,jobfile))
        params = get_params(jobfile)
        finalout.write('{0},'.format(','.join(params)))
        finalout.write('{0}\n'.format(','.join(get_times(runfile,params[-1].strip(' ')))))
        print i,jobfile
        print params
        print get_times(runfile,params[-1].strip(' '))
    except:
        print"Error on {0} -- ask Matt... ".format(i)