'''
2D Navier-Stokes water CA simulation. Uses a MxN grid to simulate water flow in a 2D pipe.

Each cell uses the following parameters:
* Momentum tuple (U, V), defined by Navier-Stokes
* Pressure value (P), defined by Navier-Stokes
* Other water-related constants or behaviours found in research

These values change as mass is pushed through the pipe.
'''

from graphics import *
import numpy as np

# Grid for fluid simulation, containing momentum, pressure, and density
M = 40
N = 40
grid = np.zeros((M,N,3))



# Finds value of Poisson's equation. If x == 0, this becomes Laplace's equation.
def poisson(x):
	return (((p[i+1,j]+p[i-1,j])*dy**2) + ((p[i,j+1]+p[i,j-1])*dx**2) - (x*dx**2*dy**2))/(2*(dx**2 + dy**2))

# Discretized Navier-Stokes momentum/pressure equations. 'F' is a constant horizontal flow variable.
def navierStokes(F,i,j):
	grid[i,j,0] = grid[i,j,0] - (grid[i,j,0] * (dt / dx) * (grid[i,j,0] - grid[i-1,j,0])) -
				    (grid[i,j,1] * (dt / dy) * (grid[i,j,0] - grid[i,j-1,0])) -
				    ((dt / (2 * p * dx)) * (grid[i+1,j,2] - grid[i-1,j,2])) +
				    (v * ((dt/dx**2) * (grid[i+1,j,0] - 2 * grid[i,j,0] + grid[i-1,j,0])) +
					 ((dt/dy**2) * (grid[i,j+1,0] - 2 * grid[i,j,0] + grid[i,j-1,0])))+
				    dt * F
	grid[i,j,1] = grid[i,j,1] - (grid[i,j,0] * (dt / dx) * (grid[i,j,1] - grid[i-1,j,1])) -
				    (grid[i,j,1] * (dt / dy) * (grid[i,j,1] - grid[i,j-1,1])) -
				    ((dt / (2 * p * dy)) * (grid[i,j+1,2] - grid[i,j-1,2])) +
				    (v * ((dt/dx**2) * (grid[i+1,j,1] - 2 * grid[i,j,1] + grid[i-1,j,1])) +
					 ((dt/dy**2) * (grid[i,j+1,1] - 2 * grid[i,j,1] + grid[i,j-1,1])))
	grid[i,j,2] = ((dy**2 * (grid[i+1,j,2] + grid[i-1,j,2]) + dx**2 * (grid[i,j+1,2] + grid[i,j-1,2])) /
				(2 * (dx**2 + dy**2))) - (((p * (dx**2) * (dy**2))/ (2 * (dx**2 + dy**2))) *
				())

# Returns the dynamic viscosity of water, given a temperature value (in Celsius)
def viscosity(t):
	return 2.414e-5 * 10**(247.8/(t + 133.15))

# Returns water shade based on density value
def denToCol(d):

# Sets up graphics window
def setupGraphics():
	w = GraphWin(width=200, height=200)
