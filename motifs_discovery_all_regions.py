
from nemomap.motifsdiscovery import getMotif
import json
import os


# For which region networks do you want to discover motifs ?
region = input('Input region : vrancea / romania / california / italy / japan : ')


initialdir = os.getcwd()
motifStats={}


for motif in ['Triangles','Tetrahedrons']:
    stats = getMotif(region,motif)
    motifStats[motif]=stats
    if motif == 'Triangles':
        os.chdir(initialdir)



with open(f"./motifs/motifStats_{region}.json","w") as f:
    json.dump(motifStats,f)