from nemomap.motifsdiscovery import getMotif,getMotifQuery
import json
import os


# function to write json files
def write_json(path, data, indent=4):
    with open(path, 'w') as file: 
        json.dump(data, file, indent=indent) 


# For which region networks do you want to discover motifs ?
region = input('Input region : vrancea / romania / california / italy / japan : ')


initialdir = os.getcwd()
motifStats={}



for motif in ['Triangles']:#,'Tetrahedrons1','Tetrahedrons2','Tetrahedrons3','Tetrahedrons4','Tetrahedrons5','Tetrahedrons6']:

    motifStats[motif]={}


    os.chdir('./nemomap')
    queryGraph = getMotifQuery(motif)
    os.chdir('..')


    os.chdir(f'./results/{region}/networks')

    if not os.path.exists(f'./motifs'):
        os.makedirs(f'motifs')



    for file in sorted(os.listdir()):
        if file.endswith(".txt"):    

            inputName = file
            print(inputName)


            stats = getMotif(inputName,motif,queryGraph)

            motifStats[motif][inputName]=stats

            write_json(f"./motifs/motifStats_{region}.json", motifStats)

    #if motif == 'Triangles':
    os.chdir(initialdir)



