from nemomap.motifsdiscovery import getMotif,getMotifQuery
import json
import os


# function to add to JSON
def write_json(path,new_data,inputName,motif):
    with open(path,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data[motif][inputName] = new_data
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)


# # function to write json files
# def write_json(path, data, indent=4):
#     with open(path, 'a') as file: 
#         json.dump(data, file, indent=indent) 


# For which region networks do you want to discover motifs ?
region = input('Input region : vrancea / romania / california / italy / japan : ')


initialdir = os.getcwd()
#motifStats={}


# What motifs do you want to discover ?
motif = input('Input motif: Triangles / Tetrahedrons : ')


#for motif in ['Triangles']:#,'Tetrahedrons1','Tetrahedrons2','Tetrahedrons3','Tetrahedrons4','Tetrahedrons5','Tetrahedrons6']:

#motifStats[motif]={}


os.chdir('./nemomap')
queryGraph = getMotifQuery(motif)
os.chdir(initialdir)


os.chdir(f'./results/{region}/networks')

if not os.path.exists(f'./motifs'):
    os.makedirs(f'motifs')



statsPath = f"./motifs/motifsStats_{region}.json"

file_exists = os.path.exists(statsPath)


if file_exists:
    with open(statsPath, 'r+') as file:
        file_data = json.load(file)
        file_data[motif] = {}
        file.seek(0)
        json.dump(file_data, file, indent = 4)
else:
     with open(statsPath, 'a+') as file:
        json.dump({motif:{}}, file, indent=4)


        
    


# THE STATS ARE NOT CORRECT. THINK LATER

if region == 'vrancea':

    for file in sorted(os.listdir()):

        if file.endswith(".txt"):    

            inputName = file
            print(inputName)


            stats = getMotif(inputName,motif,queryGraph)

            #motifStats[motif].append({inputName=stats})

            write_json(statsPath, stats, inputName, motif)

    os.chdir(initialdir)



elif region == 'japan':
    # Select the cube side length in km: ( 5 / 10 km)
    for side in (5,10):

        if motif == 'Triangles':
            # Select desired magnitude filter 
            for mag in (5,4,3):

                inputName = f'network{region}_{side}km_{mag}mag.txt'
                stats = getMotif(inputName,motif,queryGraph)

                #motifStats[motif][inputName]=stats

                write_json(statsPath, stats, inputName, motif)

        else:
            # Select desired magnitude filter 
            for mag in (3,4,5):

                inputName = f'network{region}_{side}km_{mag}mag.txt'
                stats = getMotif(inputName,motif,queryGraph)

                #motifStats[motif][inputName]=stats

                write_json(statsPath, stats, inputName, motif)


    os.chdir(initialdir)


#elif region == 'california' or region == 'italy':
else:
    if motif == 'Triangles':

        for file in sorted(os.listdir()):

            if file.endswith(".txt"):    

                inputName = file
                print(inputName)


                stats = getMotif(inputName,motif,queryGraph)

                #motifStats[motif][inputName]=stats

                write_json(statsPath, stats, inputName, motif)
    
        #os.chdir(initialdir)


    else:
        for side in (5,10):
            # Select desired magnitude filter 
            for mag in (4,3,2):

                inputName = f'network{region}_{side}km_{mag}mag.txt'
                stats = getMotif(inputName,motif,queryGraph)

                #motifStats[motif][inputName]=stats

                write_json(statsPath, stats, inputName, motif)

        #os.chdir(initialdir)


    #os.chdir(initialdir)



