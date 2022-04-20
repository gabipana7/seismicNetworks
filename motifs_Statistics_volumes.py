import matplotlib.pyplot as plt
import os

from sqlcollect import getTable
from seismicZones import query

import networkx as nx
from network import graphCreation

from cubes import makeCubes


import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

from motifs_areasVolumesEnergy import*
from seismicZones import query
from network import graphCreation3



# For which region networks do you want to analyze motifs ?
region = 'vrancea'

# What motifs do you want to discover ?
motif = 'Tetrahedrons3'



if not os.path.exists(f'./results/{region}/motifStatistics'):
    os.makedirs(f'results/{region}/motifStatistics')


sql_query= query(region)

for mag in (1,2,3):
    
    # Magnitude windows for the condition that collects the database through mySQL
    sql_query+=f" AND magnitude>={mag}"
    

    for side in (5,10):
        # Collect the database and create the graph
        # Magnitude window for the query that collects the database through mySQL


        # Collect the earthquakes
        quakes = getTable(sql_query)

        # Make the Cubes
        quakes = makeCubes(quakes,region,side,energyRelease=True)

        # Make the network
        G = graphCreation3(quakes)
        
        motifNodes,energyMotif = totalMeanEnergyMotif(region,side,mag,motif,G,quakes)
        
        volumesWeightTotalMag,volumesWeightMeanMag = volumesInSquares(motifNodes,energyMotif,G,quakes)
        hist, bins = np.histogram(volumesWeightTotalMag,bins=round(math.sqrt(len(volumesWeightTotalMag))))
        
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

        y_norm = [float(i)/sum(y) for i in y]

        pars, cov = curve_fit(f=power_law,xdata=x,ydata=y_norm,maxfev=5000)

        # Compute the chi_squared goodness of fit = sum( ( observed - expected )^2 / expected )
        chi_squared = np.sum((y_norm-power_law(x,*pars))**2/power_law(x,*pars))
        
        if side == 5:
            # Plot the results
            fig, ax = plt.subplots(1,2,figsize=(15,5))

            # The data, scattered
            ax[0].scatter(x,y_norm)
            ax[0].set_xscale('log')
            ax[0].set_yscale('log')
            # The fit
            ax[0].plot(x,power_law(x,*pars),
                       label=f'$\gamma$ = {np.round(pars[1],4)}\n$\chi^2$ = {np.round(chi_squared,4)}',
                       color='red')


            # Legend : gamma coefficient of fit and chi_squared goodness of fit
            ax[0].legend(loc='upper right',fontsize=16,frameon=True)

            # Title of connectivity distribution ( data + fit )
            ax[0].set_title('cube size = 5 km ')
            ax[0].set_xlabel(r'$V_{TE}$')
            ax[0].set_ylabel(r'$P(V_{TE})$')

        if side == 10 :
            # Connectivity distribution ( data + fit)
            # The data, scattered
            ax[1].scatter(x,y_norm)
            ax[1].set_xscale('log')
            ax[1].set_yscale('log')
            # The fit
            ax[1].plot(x,power_law(x,*pars),
                       label=f'$\gamma$ = {np.round(pars[1],4)}\n$\chi^2$ = {np.round(chi_squared,4)}',
                       color='red')


            # Legend : gamma coefficient of fit and chi_squared goodness of fit
            ax[1].legend(loc='upper right',fontsize=16,frameon=True)

            # Title of connectivity distribution ( data + fit )
            ax[1].set_title('cube size = 10 km')
            ax[1].set_xlabel(r'$V_{TE}$')
            ax[1].set_ylabel(r'$P(V_{TE})$')
            
            #plt.suptitle(f'Volume distributions in {region} - magnitude>{mag}',fontsize=18)
            fig.savefig(f'./results/{region}/motifStatistics/motifs{motif}_network{region}_totalEnergy_{mag}mag.png')
        
            #fig.savefig(f'./motifs{region}Statistics/quakes{region}_totalEnergy_{mag}mag_squaresVolumes.png')

            
        # MEAN ENERGY MOTIFS
        #fig.clear()
        hist, bins = np.histogram(volumesWeightMeanMag,bins=round(math.sqrt(len(volumesWeightMeanMag))))
        
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

        y_norm = [float(i)/sum(y) for i in y]

        pars, cov = curve_fit(f=power_law,xdata=x,ydata=y_norm,maxfev=5000)

        # Compute the chi_squared goodness of fit = sum( ( observed - expected )^2 / expected )
        chi_squared = np.sum((y_norm-power_law(x,*pars))**2/power_law(x,*pars))
        
        if side == 5:
            # Plot the results
            fig2, ax2 = plt.subplots(1,2,figsize=(15,5))

            # The data, scattered
            ax2[0].scatter(x,y_norm)
            ax2[0].set_xscale('log')
            ax2[0].set_yscale('log')
            # The fit
            ax2[0].plot(x,power_law(x,*pars),
                       label=f'$\gamma$ = {np.round(pars[1],4)}\n$\chi^2$ = {np.round(chi_squared,4)}',
                       color='red')


            # Legend : gamma coefficient of fit and chi_squared goodness of fit
            ax2[0].legend(loc='upper right',fontsize=16,frameon=True)

            # Title of connectivity distribution ( data + fit )
            ax2[0].set_title('cube size = 5 km ')
            ax2[0].set_xlabel(r'$V_{ME}$')
            ax2[0].set_ylabel(r'$P(V_{ME})$')

        if side == 10 :
            # Connectivity distribution ( data + fit)
            # The data, scattered
            ax2[1].scatter(x,y_norm)
            ax2[1].set_xscale('log')
            ax2[1].set_yscale('log')
            # The fit
            ax2[1].plot(x,power_law(x,*pars),
                       label=f'$\gamma$ = {np.round(pars[1],4)}\n$\chi^2$ = {np.round(chi_squared,4)}',
                       color='red')

            # Legend : gamma coefficient of fit and chi_squared goodness of fit
            ax2[1].legend(loc='upper right',fontsize=16,frameon=True)

            # Title of connectivity distribution ( data + fit )
            ax2[1].set_title('cube size = 10 km')
            ax2[1].set_xlabel(r'$V_{ME}$')
            ax2[1].set_ylabel(r'$P(V_{ME})$')
            
            #plt.suptitle(f'Volume distributions in {region} - magnitude>{mag}',fontsize=18)
            fig2.savefig(f'./results/{region}/motifStatistics/motifs{motif}_network{region}_meanEnergy_{mag}mag.png')

            #fig2.savefig(f'./motifs{region}Statistics/quakes{region}_meanEnergy_{mag}mag_squaresVolumes.png')
    # Extract the magnitude restrictions from the condition 
    sql_query = sql_query.replace(f" AND magnitude>={mag}", '')