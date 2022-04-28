import vtk
import networkx as nx

import os 

import ast
import numpy as np

from config.writeMotifs import writeNetworksMotifs


# ---------------------------SETUP AND COLLECTION OF QUAKES------------------------------------#
# Which region do you want to analyze ?
region = input('Input region : vrancea / romania / california / italy / japan : ')

# The side of the cubes that you split the region in 
side = int(input('Input side of the cube split in km 5 / 10 / 20 - recommended = 5 : '))

# Select desired magnitude threshold
mag = int(input('Select desired magnitude threshold - recommended = 4 : '))

G = nx.read_gexf(f'./results/{region}/networks/view/network{region}_{side}km_{mag}mag.gexf')


motif = input('Input motif: Triangles (for areas) / Tetrahedrons 1/3 (for volumes) : ')


#---------------------------------------MOTIFS-----------------------------------------#

# Use readlines() to open the 
fileMotif = open(f'./results/{region}/networks/motifs/motifs{motif}_network{region}_{side}km_{mag}mag.txt', 'r')
linesMotif = fileMotif.readlines()

# Properly evaluate the Lines to get the Lists
motifNodes=[]
for item in linesMotif:
    motifNodes.append(ast.literal_eval(item))


if motif == 'Triangles':    
    # Graph containing triangles only
    H = nx.Graph()
    for item in motifNodes:
        H.add_edge(int(item[0]),int(item[1]))
        H.add_edge(int(item[1]),int(item[2]))
        H.add_edge(int(item[0]),int(item[2]))

else:
    # Graph containing squares only
    H = nx.Graph()
    for item in motifNodes:
        H.add_edge(int(item[0]),int(item[1]))
        H.add_edge(int(item[1]),int(item[2]))
        H.add_edge(int(item[2]),int(item[3]))
        H.add_edge(int(item[0]),int(item[3]))

    
# Set the triangle attribute = 0 to each edge
nx.set_edge_attributes(G, 0, name=motif)

G = nx.convert_node_labels_to_integers(G,first_label=1)

# Iterate through our triangle only network edges
for (u,v) in H.edges():
    # Assign to original network edges the attribute triangle = 1
    G[u][v][motif] = 1


# Get attributes that go into VTK function

# X Y Z coords
lat =[]
long = []
depth =[]
for n in G.nodes():
    lat.append(int(G.nodes[n]['quake_xLatitude']))
    long.append(int(G.nodes[n]['quake_yLongitude']))
    depth.append(int(G.nodes[n]['quake_zDepth']))

minLat = min(lat)
maxLat = max(lat)
minLong = min(long)
maxLong = max(long)
minDepth = min(depth)
maxDepth = max(depth)
maxDimension = max(maxLat,maxLong,maxDepth)


coords=[]
for n in G.nodes():
    coords.append([ np.float32(round((int(G.nodes[n]['quake_xLatitude']) - minLat)*(maxLat/maxDimension)/(maxLat-minLat),3)),
                    np.float32(round((int(G.nodes[n]['quake_yLongitude']) - minLong)*(maxLong/maxDimension)/(maxLong-minLong),3)),
                    np.float32(round((int(G.nodes[n]['quake_zDepth']) - minDepth)*(maxDepth/maxDimension)/(maxDepth-minDepth),3))])
  
# Degree of nodes edges    
degree = [d for n, d in G.degree()]

# Weight of edges
weights = []
for (i,j) in G.edges():
    weights.append(G[i][j]['weight'])
    
# Triangle quality of edges
motifs = []
for (i,j) in G.edges():
    motifs.append(G[i][j][motif])



if not os.path.exists(f'./results/{region}/networksview'):
    os.makedirs(f'./results/{region}/networksview')
os.chdir(f'./results/{region}/networksview')



# Write the VTK file that goes in Paraview
# The network
writeNetworksMotifs(nodeCoords=coords,
                motifCoords=motifNodes,
                edges=G.edges(),
                scalar=degree, name='degree',
                scalar2=weights, name2='weight',
                escalar2=motifs, ename2=motif,
#               nodeLabel=nodeLabel,
                fileout=f'network{region}_{side}km_{mag}mag_{motif}')
