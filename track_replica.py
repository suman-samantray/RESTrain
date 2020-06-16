# track_replica
#
# script to track replicas during REMD/REST simulation

#!/opt/local/bin/python

import sys

inf=open(sys.argv[1],'r')
ouf=open(sys.argv[2],'w')

nreplica=int(sys.argv[3])

replica=[i for i in range(nreplica)]


## find where we expect data
pos_replica=[9+5*i for i in range(nreplica)]

## find where we expect xs
pos_x_replica=[11+5*i for i in range(nreplica-1)]

iframe=0
print >> ouf, "%12d " % (iframe),
for r in replica:
    print >> ouf, "%4d " % (r),
print >> ouf

for line in inf.readlines():
    if line[:7]!='Repl ex':
        continue
    iframe+=1
    # check for swaps
    for i in range(nreplica-1):
        px=pos_x_replica[i]
        if line[px]=='x':
            replica[i],replica[i+1]=replica[i+1],replica[i]

    print >> ouf, "%12d " % (iframe),
    for r in replica:
        print >> ouf, "%4d " % (r),
    print >> ouf
