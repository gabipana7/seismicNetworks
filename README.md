# seismic-networks

# Tools for Earthquakes Visualization and Earthquake Networks creation

In this repository you will find the necessary tools for:


## Visualization

* earthquakes epicenter visualization as 3D scatterplots on latitude, longitude and depth dimensions;
* the scatterplot points sizes and color vary according to the magnitude of the earthquakes;
* possibility to add a 2D map as a projection on the 3D plot, under the scatterplot.
### *Vrancea Seismic Region with 2D map (thousands of earthquakes)*:
![vrancea_2mag_map](https://user-images.githubusercontent.com/72228598/189355345-89e3eac3-2573-4b39-9c90-6a6653e1f119.png)

### *Japan Seismic Region with 2D map (millions of earthquakes)*
![japan_2mag_map](https://user-images.githubusercontent.com/72228598/189359558-c8b7dd91-9bc8-4be2-a623-98414922173a.png)

## Network creation

* using graphs, seismic networks are created;

### *split the seismic region in cubes*
![vrancea_2mag_cubes_map](https://user-images.githubusercontent.com/72228598/189355552-bf607acd-477f-4d63-946a-1fc92c5a9410.png)
### *draw lines from earthquake to earthquake cronollogicaly to create a network*
![vrancea_2mag_cubes_graph1000](https://user-images.githubusercontent.com/72228598/189355810-017a9668-d3db-4ec9-a849-47dd8aedbcae.png)
**control the size of network by modifying cube sizes - bigger size, more earthquakes fit in a cube**

* centrality measures such as connectivity (weighted/unweighted).

### *Conncetivity in Vrancea Seismic Network ___(power law)___*
![connectivity_networkvrancea_5km_1mag10](https://user-images.githubusercontent.com/72228598/189356153-8d3ee58d-c15f-4368-8bf7-28e5baeac9db.png)


---
## Motifs

* fundamental building blocks of graphs;
* motif detection using a slightly modified version of NemoMapPy - https://github.com/zicanl/NemoMapPy;
* motif visualization using Paraview. <br />
### *Vrancea Triangles Visualization*
![networkvrancea_5km_4mag_Triangles](https://user-images.githubusercontent.com/72228598/189356447-bdededd1-08e3-4689-ad5d-11949d510073.png)
### *California Triangles Visualization*
![networkcalifornia_5km_4mag_Triangles](https://user-images.githubusercontent.com/72228598/189357417-350d517d-43ed-40b6-bdda-b8a624ef214c.png)
* motif connectivity analysis;
* motif areas and volumes distributions, weighted by total energy and mean energy released in motif;<br />
### *California Motifs Distribution - Triangles areas weighted by total energy released in motif ___(power law)___*
![motifTriangles_TotalEnergy_networkcalifornia_5km_1mag](https://user-images.githubusercontent.com/72228598/189357247-286415c0-78bb-4420-ba44-4ab8c31efe6a.png)


---
---
# COMING SOON
## Autocorrelations

* spatial autocorrelations;
* temporal autocorrelations.


## Miscellaneous

* waiting times;
* energy release distribution.
