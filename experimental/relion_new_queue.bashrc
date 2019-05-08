module switch intel/17.0.1 gnu/native
module load cuda/8.0.61

export PATH=/home/ufaserv1_k/fbscem/relion3/relion-3.0_beta/build/bin/:$PATH
export LD_LIBRARY_PATH=/home/ufaserv1_k/fbscem/relion3/relion-3.0_beta/build/lib/:$LD_LIBRARY_PATH

export RELION_QSUB_EXTRA_COUNT=2
export RELION_QSUB_COMMAND='bash'
export RELION_QUEUE_USE=True
export RELION_QSUB_TEMPLATE='/nobackup/fbsmi/relion_queue/bash_vers.sh'

export RELION_QSUB_EXTRA1='Email'
export RELION_QSUB_EXTRA1_DEFAULT="`whoami`@leeds.ac.uk"
export RELION_QSUB_EXTRA1_HELP='Enter your email address te be informed when the job has started and finished'

export RELION_QSUB_EXTRA2='Which Nodes'
export RELION_QSUB_EXTRA2_DEFAULT=''
export RELION_QSUB_EXTRA2_HELP='For automatic time estimation on the cryoEM nodes enter:\np100 or k80\nto manually specify a node choose from:\ncryoem p100\ncryoem p40, \ngeneral p100, \ngeneral k80\nand specify the runtime in the HH:MM:SS format: EX:\n general k80/48:00:00'
