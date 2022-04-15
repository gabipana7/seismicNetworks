import time
import os
from .GraphProcessor import GraphProcessor
from .Utility import Utility
from .RandomGraphGenerator import RandomGraphGenerator

from statistics import pstdev



def getMotif(region,motif):
    stats={}
#for motif in ['Triangles','Tetrahedrons']:
    queryName = 'query' + motif + '.txt'

#for queryName in ['queryTriangles.txt','queryTetrahedrons.txt']:
    print(queryName)

    '''Create Graphs'''
    myGP = GraphProcessor()

    cwd = os.getcwd()
    print(cwd)
    
    os.chdir('./nemomap')
    queryGraph = myGP.loadGraph(queryName, directed=True)
    os.chdir('..')

    os.chdir(f'./results/{region}/networks')



    for file in os.listdir():
        if file.endswith(".txt"):
            inputName = file
            print(inputName)
            stats[str(inputName)]={}


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

        if not os.path.exists(f'./motifs'):
            os.makedirs(f'motifs')



        
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
        stats[str(inputName)]['Nodes'] = inputGraph.getNumberofVertices()
        stats[str(inputName)]['Edges'] = inputGraph.getNumberofEdges()

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
            stats[str(inputName)]['Mappings'] = totalMappings

            print("Average of Mapping in Random Graphs: {}".format(avgFRm))
            stats[str(inputName)]['AvgMap'] = avgFRm


            #print("Standard Deviation of Mapping in Random Graphs: {}".format(stdFRm))
            if stdFRm == 0.0:
                zScore = "undefined"
            else:
                zScore = (totalMappings - avgFRm) / stdFRm
            timeEnd = time.time()

            print("\nP value: ", pValue)
            print("Z Score: ", zScore)
            print("Time taken: %s seconds" % (timeEnd - timeStart))
            stats[str(inputName)]['Time'] = (timeEnd - timeStart)



        os.chdir('./motifs')

        old_name = "output.txt"
        new_name = "motifs" + motif + '_' + inputName

        os.rename(old_name, new_name)
        os.chdir('..')

    return stats

