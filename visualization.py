# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg

from pylab import *
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.cbook import get_sample_data

plt.rcParams['text.usetex'] = True

# Set the style of the plots to a more beautiful format
#az.style.use('arviz-darkgrid')


def visualize(quakes,region,withMap=False,mapcoords={}):

	# -------------------------SCALES FOR THE DOTS BASED ON MAG-----------------------------------#
	# Make scales for the dots changing with magnitude
	# Set scale for the colors of dots
	magnitudes=[float(x) for x in quakes['magnitude']]

	# Set scale for the sizes of dots
	mean = int(quakes['magnitude'].mean())
	max1 = int(quakes['magnitude'].max())
	min1 = int(quakes['magnitude'].min())
	magnitudesScale=[((x-mean)/(max1-min1))*150 for x in quakes['magnitude']]
	# ----------------------------------------------------------------------------------------------#


	# ----------------------------------------PLOTS------------------------------------------------#
	# 3D Scatter plot of earthquakes locations
	# Initialize figure and 3D axes
	fig = plt.figure(figsize=(10,10))
	ax = Axes3D(fig,auto_add_to_figure=False)
	fig.add_axes(ax)
	ax.set_proj_type('ortho')

	# Scatter the earthquakes and use scales to customize the dots
	im = ax.scatter(quakes['longitude'], quakes['latitude'],-quakes['depth'],
			s=magnitudesScale ,c=magnitudes, cmap='Greens', marker='o',
			edgecolor='black', linewidth=0.2, alpha=0.8)

	# Label the axes
	ax.set_xlabel(r'$\mathbf{Longitude}$', fontsize=20, fontweight='bold',labelpad=25)
	ax.set_ylabel(r'$\mathbf{Latitude}$',fontsize=20, fontweight='bold',labelpad=25)
	ax.set_zlabel(r'$\mathbf{Depth}$', fontsize=20, fontweight='bold',labelpad=20)

	plt.rcParams['text.usetex'] = True
	plt.setp(ax.get_xticklabels(), fontsize=16)
	plt.setp(ax.get_yticklabels(), fontsize=16)
	plt.setp(ax.get_zticklabels(), fontsize=16)



	# Remove z-axis
	#ax.w_zaxis.line.set_lw(0.)
	#ax.set_zticks([])

	# Adjust plot view
	#ax.view_init(elev=60, azim=225)
	#ax.dist=11

	ax.tick_params(axis='both', which='major', pad=7)

	# Show the colorbar used on the magnitude scale
	cbar = fig.colorbar(im, ax=ax, orientation='vertical',fraction=0.046, pad=0.12, shrink=0.65)
	# Label the colorbar
	cbar.set_label(r'$\mathbf{Magnitude}$',fontsize=20, fontweight='bold',labelpad=15)
	#cbar.ax.yaxis.set_label_position('left')



	if withMap == 'True':

		# Remove gray panes and axis grid
		ax.xaxis.pane.fill = False
		ax.xaxis.pane.set_edgecolor('white')
		ax.yaxis.pane.fill = False
		ax.yaxis.pane.set_edgecolor('white')
		ax.zaxis.pane.fill = False
		ax.zaxis.pane.set_edgecolor('white')
		ax.grid(False)


		img = mpimg.imread(f'./maps/{region}.png')
		# Create lists of points ranging from:
		# For x : longitude 
		xx = np.linspace(mapcoords['minLon'],mapcoords['maxLon'],img.shape[0])
		# For y : latitude 
		yy = np.linspace(mapcoords['minLat'],mapcoords['maxLat'],img.shape[1])

		# Create the x component of the grid for the image plot
		x = np.ndarray((img.shape[0],1))
		# Create y component of the grid for the image plot
		y = np.ndarray((1,img.shape[1]))
		# Create the z component (choose at which depth the image is plotted)
		z = -mapcoords['maxDepth'] * np.ones(x.shape)


		# Assign x values (first component) the proper longitude
		for i in range(len(x)):
			x[i][0] = float(xx[i])

		# Assign y values (second component) the proper latitude
		for j in range(len(y[0])):
			y[0][j] = float(yy[j])


		# Plot the overlay with the map under the scattered eathquakes 
		ax.plot_surface(x,y,z, facecolors=img, rstride=1, cstride=1)


	return ax
