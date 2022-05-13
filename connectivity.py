import numpy as np
import matplotlib.pyplot as plt
import os


from scipy.optimize import curve_fit
from config.sqlcollect import getTable
from config.network import graphCreation
from config.cubes import makeCubes
from config.seismicZones import query
#from config.network import graphCreation3


# Power law used to fit the connectivity distribution
def power_law(x, a, b):
	return a*np.power(x, -b)



# For which region networks do you want to analyze motifs ?
region = input('Input region : vrancea / romania / california / italy / japan : ')

# Want to consider edgeWeight?
edgeWeight = input('Input if connectivity takes into account edge weight : True / False : ')


if not os.path.exists(f'./results/{region}/connectivity'):
	os.makedirs(f'results/{region}/connectivity')

plt.rcParams['text.usetex'] = True

connectivityData={}
connectivityData['5km']={}
connectivityData['10km']={}

sql_query= query(region)


for (magMin,magMax) in ((1,10),(2,10),(3,10),(1,3),(2,4),(4,10)):
	
	# Magnitude windows for the condition that collects the database through mySQL
	sql_query+=f" AND magnitude>={magMin} AND magnitude<={magMax}"

	# Collect the database and create the graph
	# Collect the earthquakes
	quakes = getTable(sql_query)


	for side in (5,10):

		# Make the Cubes
		quakes = makeCubes(quakes,region,side,energyRelease=True)

		realmagMax = max(quakes['magnitude'])

		# Process graph and its connectivity with edge weight
		if edgeWeight=='True':
			G = graphCreation(quakes,withEdgeWeight=True)
		
			# Degree
			degree_dict = dict(G.degree(G.nodes(),weight='weight'))
			connectivity=[]
			for item in degree_dict.values():
				connectivity.append(item)

		else:
			G = graphCreation(quakes)
			
			# Degree
			degree_dict = dict(G.degree(G.nodes()))
			connectivity=[]
			for item in degree_dict.values():
				connectivity.append(item)
		

		# hist and bins for the plots
		hist, bins = np.histogram(connectivity,bins=round(np.sqrt(len(connectivity))))
	
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
		pars, cov = curve_fit(f=power_law,xdata=x,ydata=y_norm,maxfev=5000)

		# Compute the chi_squared goodness of fit = sum( ( observed - expected )^2 / expected )
		chi_squared = np.sum((y_norm-power_law(x,*pars))**2/power_law(x,*pars))
		

		# APPEND RESULTS TO DATA
		connectivityData[f'{side}km'][f'{magMin}<magnitude<{magMax}']=[np.round(pars[1],4),np.round(chi_squared,4)]


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


		
		plt.setp(ax.get_xticklabels(), fontsize=26)
		plt.setp(ax.get_yticklabels(), fontsize=26)


		ax.tick_params(axis='both', which='major', pad=7)

		# Title of connectivity distribution ( data + fit )
		#ax.set_title(f'cube size = {side} km ', fontsize=26, fontweight='bold')

		# Magnitude range:
		ax.text(0.05,0.1, f'Magnitude Range:\n {magMin}'+r'$<$' + 'mag' + r'$<$' +f'{realmagMax}', fontsize=20,
		 		bbox=dict(facecolor='white', boxstyle='round', alpha=0.3),transform=ax.transAxes) 
				


		ax.set_xlabel(r'$\mathbf{k}$', fontsize=26,labelpad=20)
		ax.set_ylabel(r'$\mathbf{P_k}$', fontsize=26,labelpad=20)

		# Put a title and save the figure, depending on edgeWeight and the values of the different variables
		if edgeWeight=="True":
			fig.savefig(f'./results/{region}/connectivity/connectivityWeighted_network{region}_{side}km_{magMin}mag{magMax}.png',
						facecolor='white', transparent=False, bbox_inches='tight')  
		else:
			fig.savefig(f'./results/{region}/connectivity/connectivity_network{region}_{side}km_{magMin}mag{magMax}.png',
						facecolor='white', transparent=False, bbox_inches='tight')           


		plt.close();

		# Extract the magnitude restrictions from the condition 
		sql_query = sql_query.replace(f" AND magnitude>={magMin} AND magnitude<={magMax}", '');


		# Use break to get only the 5km sides
		break