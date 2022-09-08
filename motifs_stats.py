import numpy as np
import matplotlib.pyplot as plt
import os


from scipy.optimize import curve_fit
from config.sqlcollect import getTable
#from config.network import graphCreation
from config.cubes import makeCubes
from config.seismicZones import query
from config.network import graphCreation3


from motifs_areas_volumes_energy import*


# For which region networks do you want to analyze motifs ?
region = input('Input region : vrancea / romania / california / italy / japan : ')

# What motifs do you want to discover ?
motif = input('Input motif: Triangles (for areas) / Tetrahedrons (for volumes) : ')


# # For which region networks do you want to analyze motifs ?
# region = 'italy'

# # What motifs do you want to discover ?
# motif = 'Tetrahedrons1'


if not os.path.exists(f'./results/{region}/motifStatistics'):
    os.makedirs(f'results/{region}/motifStatistics')


plt.rcParams['text.usetex'] = True

sql_query= query(region)


for mag in (3,5):
    
    # Magnitude windows for the condition that collects the database through mySQL
    sql_query+=f" AND magnitude>={mag}"

    # Collect the database and create the graph
    # Collect the earthquakes
    quakes = getTable(sql_query)


    for side in (5,10):

        # Make the Cubes
        quakes = makeCubes(quakes,region,side,energyRelease=True)

        # Get maximum magnitude for displaying on the plot
        realmagMax = max(quakes['magnitude'])

        # Make the network
        quakesGraph = graphCreation3(quakes)


        # Get the motif nodes and the energy in motifs    
        motifNodes,energyMotif = totalMeanEnergyMotif(region,side,mag,motif,quakesGraph,quakes)
        
        # TRIANGLES 
        if motif == 'Triangles':
            motifTotalEnergy,motifMeanEnergy = areasInTriangles(motifNodes,energyMotif,quakesGraph,quakes)
        # TETRAHEDRONS
        else:
            motifTotalEnergy,motifMeanEnergy = volumesInSquares(motifNodes,energyMotif,quakesGraph,quakes)


        # TOTAL ENERGY / MEAN ENERGY PLOTS
        for motifstats in [motifTotalEnergy,motifMeanEnergy]:

            # hist and bins for the plots
            hist, bins = np.histogram(motifstats,bins=round(np.sqrt(len(motifstats))))
        
            # Create the x as hist with zeros, force into floats ! 
            x = np.zeros_like(hist.astype(float))
            for i in range(1,len(bins)):
                x[i-1]=((bins[i]+bins[i-1])/2)

            for i in range(len(hist)):
                if hist[i]==0:
                    y=np.array(hist[:i])
                    x=np.array(x[:i])
                    break
                else:
                    y=hist

            # normalize y axis 
            y_norm = [float(i)/sum(y) for i in y]

            # the curve fit of the data
            pars, cov = curve_fit(f=power_law,xdata=x,ydata=y_norm,maxfev=10000)

            # Compute the chi_squared goodness of fit = sum( ( observed - expected )^2 / expected )
            chi_squared = np.sum((y_norm-power_law(x,*pars))**2/power_law(x,*pars))
            

            # Plot the results
            fig = plt.figure(figsize=(15,10))
            ax = fig.add_subplot(111)

            # The data, scattered
            ax.scatter(x,y_norm)
            ax.set_xscale('log')
            ax.set_yscale('log')

            # The fit
            ax.plot(x,power_law(x,*pars),
                        label=f'$\gamma$ = {np.round(pars[1],4)}\n$\chi^2$ = {np.round(chi_squared,4)}',
                        color='red')

            # Legend : gamma coefficient of fit and chi_squared goodness of fit
            plt.legend(loc='upper right',fontsize=26, frameon=True)

            #r'$\mathbf{Longitude}$'

            
            plt.setp(ax.get_xticklabels(), fontsize=26)
            plt.setp(ax.get_yticklabels(), fontsize=26)


            ax.tick_params(axis='both', which='major', pad=7)

            # Title of connectivity distribution ( data + fit )
            #ax.set_title(f'cube size = {side} km ', fontsize=26, fontweight='bold')

            # Magnitude range:
            ax.text(0.05,0.1, f'Magnitude Range:\n {mag}'+r'$<$' + 'mag' + r'$<$' +f'{realmagMax}', fontsize=20,
                    bbox=dict(facecolor='white', boxstyle='round', alpha=0.3),transform=ax.transAxes) 


            # TOTAL MAGNITUDE IN MOTIF
            if motifstats == motifTotalEnergy:

                # TRIANGLES LABELS
                if motif == "Triangles":
                    ax.set_xlabel(r'$\mathbf{S_{TE}}$', fontsize=26,labelpad=20)
                    ax.set_ylabel(r'$\mathbf{P(S_{TE})}$', fontsize=26,labelpad=20)
                # TETRAHEDRONS LABELS
                else:
                    ax.set_xlabel(r'$\mathbf{V_{TE}}$', fontsize=26,labelpad=20)
                    ax.set_ylabel(r'$\mathbf{P(V_{TE})}$', fontsize=26,labelpad=20)


                fig.savefig(f'./results/{region}/motifStatistics/motif{motif}_TotalEnergy_network{region}_{side}km_{mag}mag.png',
                            facecolor='white', transparent=False, bbox_inches='tight')           

            # MEAN MAGNITUDE IN MOTIF
            else:

                # TRIANGLE LABELS
                if motif == "Triangles":
                    plt.xlabel(r'$\mathbf{S_{ME}}$', fontsize=26,labelpad=20)
                    plt.ylabel(r'$\mathbf{P(S_{ME})}$', fontsize=26,labelpad=20)
                # TETRAHEDRONS LABELS
                else:
                    plt.xlabel(r'$\mathbf{V_{ME}}$', fontsize=26,labelpad=20)
                    plt.ylabel(r'$\mathbf{P(V_{ME})}$', fontsize=26,labelpad=20)


                fig.savefig(f'./results/{region}/motifStatistics/motif{motif}_MeanEnergy_network{region}_{side}km_{mag}mag.png',
                                facecolor='white', transparent=False, bbox_inches='tight')

            plt.close();

        # Extract the magnitude restrictions from the condition 
        sql_query = sql_query.replace(f" AND magnitude>={mag}", '');

        # Use break to get only the 5km sides
        break