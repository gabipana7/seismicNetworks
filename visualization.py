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


def visualize(quakes,region,withMap=False):

	# -------------------------SCALES FOR THE DOTS BASED ON MAG-----------------------------------#
	# Make scales for the dots changing with magnitude
	# Set scale for the colors of dots
	magnitudes=[int(x) for x in quakes['magnitude']]

	# Set scale for the sizes of dots
	mean = int(quakes['magnitude'].mean())
	max1 = int(quakes['magnitude'].max())
	min1 = int(quakes['magnitude'].min())
	magnitudesScale=[((x-mean)/(max1-min1))*250 for x in quakes['magnitude']]
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
		
		if region == 'romania':
			img = mpimg.imread('./maps/romania.png')
			# Create lists of points ranging from:
			# For x : longitude 19.8 - 30.2
			xx = np.linspace(19.8,30.2,img.shape[0])
			# For y : latitude 43.5941 - 48.4 
			yy = np.linspace(43.5941,48.4,img.shape[1])

			# Create the x component of the grid for the image plot
			x = np.ndarray((img.shape[0],1))
			# Create y component of the grid for the image plot
			y = np.ndarray((1,img.shape[1]))
			# Create the z component (choose at which depth the image is plotted)
			z = -196 * np.ones(x.shape)

		if region == 'vrancea':
			img = mpimg.imread('./maps/vrancea.png')
			# Create lists of points ranging from:
			# For x : longitude 26 - 27
			xx = np.linspace(26,27,img.shape[0])
			# For y : latitude 45 - 46 
			yy = np.linspace(45,46,img.shape[1])

			# Create the x component of the grid for the image plot
			x = np.ndarray((img.shape[0],1))
			# Create y component of the grid for the image plot
			y = np.ndarray((1,img.shape[1]))
			# Create the z component (choose at which depth the image is plotted)
			z = -200 * np.ones(x.shape)

		if region == 'california':
			img = mpimg.imread('./maps/california.png')
			# Create lists of points ranging from:
			# For x : longitude min max
			xx = np.linspace(-121.953,-114.026,img.shape[0])
			# For y : latitude min max
			yy = np.linspace(32,37,img.shape[1])

			# Create the x component of the grid for the image plot
			x = np.ndarray((img.shape[0],1))
			# Create y component of the grid for the image plot
			y = np.ndarray((1,img.shape[1]))
			# Create the z component (choose at which depth the image is plotted)
			z = -32 * np.ones(x.shape)

		if region == 'italy':
			img = mpimg.imread('./maps/italy.png')
			# Create lists of points ranging from:
			# For x : longitude min max
			xx = np.linspace(-6.08,36.02,img.shape[0])
			# For y : latitude min max
			yy = np.linspace(30.61,47.998,img.shape[1])

			# Create the x component of the grid for the image plot
			x = np.ndarray((img.shape[0],1))
			# Create y component of the grid for the image plot
			y = np.ndarray((1,img.shape[1]))
			# Create the z component (choose at which depth the image is plotted)
			z = -645  * np.ones(x.shape)

		if region == 'japan':
			img = mpimg.imread('./maps/japan.png')
			# Create lists of points ranging from:
			# For x : longitude min max
			xx = np.linspace(118.90483,156.68133,img.shape[0])
			# For y : latitude min max
			yy = np.linspace(17.40933,50.42683,img.shape[1])

			# Create the x component of the grid for the image plot
			x = np.ndarray((img.shape[0],1))
			# Create y component of the grid for the image plot
			y = np.ndarray((1,img.shape[1]))
			# Create the z component (choose at which depth the image is plotted)
			z = -700  * np.ones(x.shape)


		# Add any other region here by respecting the format:
			# read the image file using mpimg.imread('file.png')
			# Create lists of points in the shape of the image
			# x coordinate
			# y coordinate
			# z coordinate - the depth at which the 2D image will be displayed, preferably under the scatterplot


		# Assign x values (first component) the proper longitude
		for i in range(len(x)):
			x[i][0] = float(xx[i])

		# Assign y values (second component) the proper latitude
		for j in range(len(y[0])):
			y[0][j] = float(yy[j])


		# Plot the overlay with the map under the scattered eathquakes 
		ax.plot_surface(x,y,z, facecolors=img, rstride=1, cstride=1)


	return ax
