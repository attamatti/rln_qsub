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

export RELION_QSUB_EXTRA2='Node_Name/HH:MM:SS'
export RELION_QSUB_EXTRA2_DEFAULT=''
export RELION_QSUB_EXTRA2_HELP='Choose from:\ncryoem_p100\ncryoem p40, \ngeneral_p100, \ngeneral k80\nand_specify the runtime in the HH:MM:SS format: EX:\n general_k80/48:00:00'
