$$$$$$$$$$$$$$$$$$$$$$$$$$$
$  new submission script  $
$$$$$$$$$$$$$$$$$$$$$$$$$$$

beta test directions

source /nobackup/fbsmi/relion_queue/relion_new_queue.bashrc

For the nodes field:
To use the cryoEM nodes with automatic runtime determination enter just the node name, either:

p100
p40

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

The script automatically calculates the appropriate runtime for the job for Class2D, Class3D, and Refine3D jobs.
Other job types will just be given 48:00:00 until there is enough data to model their runtimes.
Runtime is determined solely on particle number but generously padded and relatively independent of box size.
The only possiility I see for problems is doing classifications with really large number of classes or very fine angular sampling, but then just specifiy a runtime manually.

Remember the general nodes can't see cryoem-gui, the data actually need to be on nobackup for these ones.

---------------
troubleshooting
---------------
please report any errors you get to Matt I.
The automatically set parameters should be as follows:
Queue submit command = bash
Standard submission script = /nobackup/fbsmi/relion_queue/bash_vers.sh


-----
to do
-----

write program for finding outliers and removing them - needs to be done manually
Data model only uses jobs that were completed, not continuations and didn't use local angle searches.  will therefore overestimate teh amount of time needed to do refinements with locla searchs turned on.