'''
2D Navier-Stokes water CA simulation. Uses a MxN grid to simulate water flow in a 2D pipe.

Each cell uses the following parameters:
* Momentum tuple (U, V), defined by Navier-Stokes
* Pressure value (P), defined by Navier-Stokes
* Fractional Density value (D), defined by SOLA-VOF

These values change as mass is pushed through the pipe.
'''
import numpy as np

# Grid for fluid simulation, containing momentum, pressure, and density
M = 40
N = 40
grid = np.zeros((M,N,3))

# Fluid constants
flowRate = 1.0
dx = 
dy = 
dt = 
T = 10
d = 
v = viscosity(T)

# Boundary conditions (for walls, masses. etc.)


# Finds value of Poisson's equation. If x == 0, this becomes Laplace's equation.
def poisson(x):
	return (((p[i+1,j]+p[i-1,j])*dy**2) + ((p[i,j+1]+p[i,j-1])*dx**2) - (x*dx**2*dy**2))/(2*(dx**2 + dy**2))

# Discretized Navier-Stokes momentum/pressure equations. 'F' is a constant horizontal flow variable.
def navierStokes(i,j):
	grid[i,j,0] = grid[i,j,0] - (grid[i,j,0] * dt / dx) * (grid[i,j,0] - grid[i-1,j,0])) -
				    (grid[i,j,1] * (dt / dy) * (grid[i,j,0] - grid[i,j-1,0])) -
				    ((dt / (2 * p * dx)) * (grid[i+1,j,2] - grid[i-1,j,2])) +
				    (v * ((dt/dx**2) * (grid[i+1,j,0] - 2 * grid[i,j,0] + grid[i-1,j,0])) +
					 ((dt/dy**2) * (grid[i,j+1,0] - 2 * grid[i,j,0] + grid[i,j-1,0])))+
				    dt * flowRate
	grid[i,j,1] = grid[i,j,1] - (grid[i,j,0] * (dt / dx) * (grid[i,j,1] - grid[i-1,j,1])) -
				    (grid[i,j,1] * (dt / dy) * (grid[i,j,1] - grid[i,j-1,1])) -
				    ((dt / (2 * p * dy)) * (grid[i,j+1,2] - grid[i,j-1,2])) +
				    (v * ((dt/dx**2) * (grid[i+1,j,1] - 2 * grid[i,j,1] + grid[i-1,j,1])) +
					 ((dt/dy**2) * (grid[i,j+1,1] - 2 * grid[i,j,1] + grid[i,j-1,1])))
	grid[i,j,2] = ((dy**2 * (grid[i+1,j,2] + grid[i-1,j,2]) + dx**2 * (grid[i,j+1,2] + grid[i,j-1,2])) /
				(2 * (dx**2 + dy**2))) - (((p * (dx**2) * (dy**2))/ (2 * (dx**2 + dy**2))) *
				())

# Returns the kinematic viscosity of water, given a temperature value (in Celsius) and a density value
def viscosity(density, t):
	return (2.414e-5 * 10**(247.8/(t + 133.15))) / density

# Water density given a Celsius temperature (DIPPR105 equation)
def density(t):
	return 0.14395 / 0.0112 ** (1 + (1 - ((t + 273.15) / 649.727)) ** 0.05107)

# Simulates fluid density using the SOLA-VOF algorithm
# Each cell has a fractional (0-1.0) density and is considered empty if density == 0
# Free surface cells have density > 0 and density < 1
# Must run after Navier-Stokes velocity/pressure simulation
def fracVOF():
	# dF/dT + drFu/dX + dFv/dY = 0
	# dF = min(flux(A,D) * abs(V) + max(0, (1 - flux(A,D)) * abs(V) - (1 - flux(D)) * dX), flux(D) * dX)