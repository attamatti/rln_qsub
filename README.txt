$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
$  new submission script - simplified version 0.2  $
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

beta test directions

source /nobackup/fbsmi/relion_queue/relion_queue2_simple.bashrc

For the nodes field:
To use the cryoEM nodes with automatic runtime determination enter just the node name, either:

to specifiy and node and runtime use:

node_name/HH:MM:SS

the node names are:

cryoem_p100
cryoem_p40
general_k80
general_p100

so for example:

cryoem_p100/08:00:00

or

general_k80/14:30:00


Everything else should be set by default.


---------------
troubleshooting
---------------
please report any errors you get to Matt I.
The automatically set parameters should be as follows:
Queue submit command = bash
Standard submission script = /nobackup/fbsmi/relion_queue/bash_vers.sh