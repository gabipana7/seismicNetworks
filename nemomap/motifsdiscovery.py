import time
import os
from .GraphProcessor import GraphProcessor
from .Utility import Utility
from .RandomGraphGenerator import RandomGraphGenerator

from statistics import pstdev


def getMotifQuery(motif):
    queryName = 'query' + motif + '.txt'
    print(queryName)

    '''Create Graphs'''
    myGP = GraphProcessor()

    queryGraph = myGP.loadGraph(queryName, directed=True)
    
    return queryGraph


def getMotif(inputName, motif, queryGraph):
    stats={}


    '''
#for motif in ['Triangles','Tetrahedrons']:
    queryName = 'query' + motif + '.txt'

#for queryName in ['queryTriangles.txt','queryTetrahedrons.txt']:
    print(queryName)

    
    

    cwd = os.getcwd()
    print(cwd)
    
    os.chdir('./nemomap')
    queryGraph = myGP.loadGraph(queryName, directed=True)
    os.chdir('..')
    '''



    myGP = GraphProcessor()
    
    inputGraph = myGP.loadGraph(inputName, directed=True)
    
    myUtility = Utility()
    randomGenerator = RandomGraphGenerator()
    """
    main output
    print stats
    """
    print("\n")
    print("Input Graph: Nodes - %d; Edges - %d" % (inputGraph.getNumberofVertices(), inputGraph.getNumberofEdges()))
    print("Query Graph: Nodes - %d; Edges - %d" % (queryGraph.getNumberofVertices(), queryGraph.getNumberofEdges()))
    stats['Nodes'] = inputGraph.getNumberofVertices()
    stats['Edges'] = inputGraph.getNumberofEdges()

    print("\nQuery Graph (sub-graph) Edges: ")
    for item in queryGraph.getEdgeList():
        print(item)

    h = queryGraph.getNodesSortedByDegree(0)
    h1 = h[-1]
    print("\nH node = [ %d ]" % h1)

    '''run the nemomap alg'''
    timeStart = time.time()
    totalMappings = myUtility.algorithm2_modified(queryGraph, inputGraph, h1, 0)

    print("\nMapping: %d" % totalMappings)

    zScore = None
    pValue = None
    countN = 0
    randomMappingList = []
    numberOfIterations = 1
    for i in range(numberOfIterations):
        randomGraph = randomGenerator.generate(inputGraph)
        #for edge in randomGraph.edgeList:
            #print(edge[0], edge[1])
        
        randomMappings = myUtility.algorithm2_modified(queryGraph, randomGraph,
                                                    queryGraph.getNodesSortedByDegree(0)[-1], 1)
        randomMappingList.append(randomMappings)

        if randomMappings >= totalMappings:
            countN += 1
    if numberOfIterations > 0:
        print("\ncountN: ", countN)
        pValue = countN / numberOfIterations

        stdFRm = pstdev(randomMappingList)
        avgFRm = sum(randomMappingList) / (len(randomMappingList))

        print("\nMapping: {}".format(totalMappings))
        stats['Mappings'] = totalMappings

        print("Average of Mapping in Random Graphs: {}".format(avgFRm))
        stats['AvgMap'] = avgFRm


        #print("Standard Deviation of Mapping in Random Graphs: {}".format(stdFRm))
        if stdFRm == 0.0:
            zScore = "undefined"
        else:
            zScore = (totalMappings - avgFRm) / stdFRm
        timeEnd = time.time()

        print("\nP value: ", pValue)
        print("Z Score: ", zScore)
        print("Time taken: %s seconds" % (timeEnd - timeStart))
        stats['Time'] = (timeEnd - timeStart)



    os.chdir('./motifs')

    old_name = "output.txt"
    new_name = "motifs" + motif + '_' + inputName

    os.rename(old_name, new_name)
    os.chdir('..')


    return stats


# '''Get File names and see if they can be opened'''
# inputName = input("Input Graph: ")
# queryName = input("Query Graph: ")


    '''
    goodInput = True

    try:
        open(inputName, "r")
    except IOError:
        print("Input File Error - check spelling and that file exists")
        goodInput = False
    try:
        open(queryName, "r")
    except IOError:
        print("Query File Error -  check spelling and that file exists")
        goodInput = False


    if goodInput:
    '''

    



