#!/usr/bin/env python

#todo
#add helical and multibody - currently at 96:00:00

import subprocess
import sys

########polynomials
polys={
'Refine3D':[5.70156400945e-07, 0.388888018559, 123014.47594],
'Class3D':[3.37288748034e-06, 0.400375594628, 21750.3592438],
'Class2D':[-4.05542131513e-07, 0.475747768831, 29222.6171242]
}
####################
# originally wanted to do a dynamic menu system, but EOF errors with python raw_input

def node_menu(ninput):
    splitin = ninput.split('/')
    xnodes = {
        'cryoem_p100':('cryoEM p100','coproc_p100=4','#$ -P cryoem'),
        'cryoem_p40':('cryoEM p40','coproc_p40=2','#$ -P cryoem'),
        'general_k80':('General k80','coproc_k80=2',''),
        'general_p100':('General p100','coproc_p100=4','')}
    try:
        nodeout = xnodes[splitin[0]]
        timeout = splitin[1]
        return(nodeout,timeout)
    except:
        print("ERROR: {0} is not a valid node/time entry - see the notes in the relion help".format(ninput))
        sys.exit()
        
nodedic = {
    "p100":[('cryoEM p100','coproc_p100=4','#$ -P cryoem')],
    "p40":[('cryoEM p40','coproc_p40=2','#$ -P cryoem')],
    "P100":[('cryoEM p100','coproc_p100=4','#$ -P cryoem')],
    "P40":[('cryoEM p40','coproc_p40=2','#$ -P cryoem')]}

##################

# get relion variables
error =sys.argv[1]
outfile = sys.argv[2]
email = sys.argv[3]
node = sys.argv[4]
mpinodes = sys.argv[5]
command = ' '.join(sys.argv[6:])   

### choose which node to use:
try: 
    nodeinfo = nodedic[node]
    manual = False
except:
    nodeinfo = node_menu(node)
    manual = True


###calculate time needed
# get jobtype
splicom = command.split()
n=0
for i in splicom:
    if i == '--o':
        jobtype = splicom[n+1].split('/')[0]
        outdir = '/'.join(splicom[n+1].split('/')[:2])
        n=0
        break
    n+=1


# get number of particles
for i in splicom:
    if i == '--i':
        infile = splicom[n+1]
        n=0
        break
    n+=1

partsfile = open(infile,'r').readlines()
nparts = len(partsfile)

def calctimerec(type,nparts):
    if type not in polys:
        print('Not enough model data for jobtype {0} - using 48:00:00')
        return('48:00:00')
    time_s = polys[type][0]*(nparts^2)+polys[type][1]*nparts+polys[type][2]
    
    hours, remainder = divmod(time_s, 3600)
    minutes, seconds = divmod(remainder, 60)
    time= '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
    print('\nEstimated Job Length: {0}'.format(time))
    return(time)

if manual == False:
    timereq = calctimerec(jobtype,nparts)
else:
    timereq = nodeinfo[1]
    
runscript ='''#$ -cwd -V
#$ -l h_rt={6}     # specifiy max run time here
#$ -m be
#$ -e {0}
#$ -o {1}
{7}
#$  -M {2}    # put your email address here 
#$  -l {3}     # if coproc_p100=4 GPUS in relion should be left blank
 
## load modules 
module load cuda/8.0.61
module switch intel/17.0.1 gnu/native

## set library paths
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/home/ufaserv1_k/fbscem/Relion/relion/13Mar2018_2-1/lib/:$LD_LIBRARY_PATH

## print some diagnostic info 
module list
nvidia-smi -L
which relion_refine_mpi

## run relion
mpirun -n {4} {5}
'''.format(error,outfile,email,nodeinfo[0][1],mpinodes,command,timereq,nodeinfo[0][2])


print('wrote submission script to submit_script.sh'.format(outdir))
output=open('run_submit.sh','w')
output2=open('{0}/run_submit.sh'.format(outdir),'w')
output.write(runscript)
output2.write(runscript)
output.close()
output2.close()