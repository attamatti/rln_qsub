#!/usr/bin/env python
# Matt I's simplified all-purpose ARC3 submission script
# vers 0.2 2019-05-08

import sys

####################
def node_menu(ninput,info):
    
    """ returns the values neeed for each node and time requested in the format [(node name, coproc command, extra ino),HH:MM:SS]
    if run with the info = True flag just outputs the available node names to screen"""
    
    xnodes = {
        'cryoem_p100':('cryoEM p100','coproc_p100=4','#$ -P cryoem'),
        'cryoem_p40':('cryoEM p40','coproc_p40=2','#$ -P cryoem'),
        'general_k80':('General k80','coproc_k80=2',''),
        'general_p100':('General p100','coproc_p100=4','')}
    try:
        splitin = ninput.split('/')
        nodeout = xnodes[splitin[0]]
        timeout = splitin[1]
        return(nodeout,timeout)
    except:
        if info == False:
            print("ERROR: {0} is not a valid node/time entry - see the notes in the relion help".format(ninput))
        print("\nEnter the node and time in the format: Node_Name/HH:MM:SS")
        print("Currently available nodes are: {0}".format(','.join(xnodes)))
        
        sys.exit()
##################

# if in information mode print the node info then exit
if '--nodeinfo' in sys.argv:
    node_menu(False,True)

## otherwise do a submission
# get relion variables
error =sys.argv[1]
outfile = sys.argv[2]
email = sys.argv[3]
node = sys.argv[4]
mpinodes = sys.argv[5]
command = ' '.join(sys.argv[6:])   


nodeinfo = node_menu(node,False)
timereq = nodeinfo[1]


###calculate time needed
# get jobtype
splicom = command.split()
n=0
for i in splicom:
    if i == '--o':
        outdir = '/'.join(splicom[n+1].split('/')[:2])
        n=0
        break
    n+=1

#### here is the actual submit script
# {0} = relion error file (job.err) for screen display
# {1} = relion output file (job.out) for screen display
# {2} = user entered email address
# {3} = coproc for specificing which GPUS, item[1] in the xnodes dic
# {4} = the number of MPIs
# {5} = the rest of the relion command
# {6} = requested run time (HH:MM:SS)
# {7} = extra info if required for cryoem nodes, item[2] in the xnodes dic, left blank forthe general nodes

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

## write the scripts and give the user feedback
print('job will be run on a {0} node'.format(nodeinfo[0][0]))
print('wrote submission script to {0}/submit_script.sh'.format(outdir))
output=open('run_submit.sh','w')
output2=open('{0}/run_submit.sh'.format(outdir),'w')
output.write(runscript)
output2.write(runscript)
output.close()
output2.close()
