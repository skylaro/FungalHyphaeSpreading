# -*- coding: utf-8 -*-
'''
Mushroom model from book, using absorbing, reflecting, and periodic boundary conditions.
S&S model was generated from information found in the following sources, which were also
utilized in this model to augment that of S&S.

References:
Blackwell, Meredith. 2011. “The Fungi: 1, 2, 3. . . 5.1 Million Species?” American
    Journal of Botany 98(3): 426–438.
Deacon, Jim. “The Microbial World—The Fungal Web.” Institute of Cell and Mo-
    lecular Biology and Biology Teaching Organization, University of Edinburgh.
    Archived. http://www.biology.ed.ac.uk/archive/jdeacon/microbes/fungalwe.htm
    (accessed January 1, 2013)
Gaylor, Richard J., and Kazume Nishidate. 1996. “Contagion in Excitable Media.”
    Modeling Nature: Cellular Automata Simulations with Mathematica. New York:
    TELOS/Springer-Verlag, pp. 155–171.
Illinois Extension Service. 1998. Department of Crop Sciences, University of Illi-
    nois– Urbana-Champaign. “Fairy Rings, Mushrooms and Puffballs.” Report on
    Plant Disease No. 403.
Kimball, John W. 2012. ”Fungi.” http://users.rcn.com/jkimball.ma.ultranet/Biology
    Pages/F/Fungi.html (accessed January 1, 2013)
Kruszelnicki, Karl S. “Great Moments in Science—Fairy Rings.” Karl S. Kruszel-
    nicki Pty Ltd. http://www.abc.net.au/science/k2/moments/s297489.htm (accessed
    January 1, 2013)
Lepp, Heino, and Murray Fagg. 2012. “The Mycelium.” Australian National Botanic
    Gardens. http://www.anbg.gov.au/fungi/mycelium.html (accessed January 1, 2013)
Rayner, Alan D. M. 1991. “Conflicting Flows: The Dynamics of Mycelial Territori-
    ality.” McIlvainea, 10: 24-3557-62.
'''

from graphics import *
import matplotlib.pyplot as plt
import numpy as np
import random
import time

# Cell States Constant
EMPTY = 0
SPORE = 1
YOUNG = 2
MATURING = 3
MUSHROOMS = 4
OLDER = 5
DECAYING = 6
DEAD1 = 7
DEAD2 = 8
INERT = 9

# Update Probabilities
probSporeToHyphae = 0.5
probMushroom = 0.5
probSpread = 0.5

# Grid initialization
winTitle = "Mushroom Simulation"
cellWidth = 15
m = 20
n = 20
winDims = (m, n)
win= GraphWin(width=winDims[0] * cellWidth, height=winDims[1] * cellWidth,title=winTitle)

# Probability of spawning a spore. Used when initializing the grid and then for spawning spores from mushrooms.
probSpore = 0.2

# Rule used for spawning new spores from a mushroom.
# 0 = All grid cells use probSpore, which is the mushroom coverage percentage.
# 1 = A single cell uses probSpore, which is calculated based on number of mushroom neighbors.
mushroomSporeSpawnRule = 0

# Used with spore spawn rule 0 after each timestep to calculate new probSpore value.
numMushrooms = 0


# Null grid has all -1s
grid = -1 * np.ones(winDims)

# Other adjustables properties
numTimeSteps = 15
numSimulations = 1
initRule = 1

# Method to initialize a starting grid
# RANDOM    = 0
# SINGLE    = 1
# DOUBLE    = 2
# BOUNDARY  = 3
def initGrid(t):

    # Randomly placed spores, using probSpore
    if t == 0:
        return np.random.choice(a=[SPORE, EMPTY], size=winDims, p=[probSpore, 1-probSpore])

    # Single spore in middle of grid
    elif t == 1:
        grid = np.ones(winDims) * EMPTY
        x = (int) (m / 2)
        y = (int) (n / 2)
        grid[x, y] = SPORE
        return grid

    # Two spores separating two quarters of the grid
    elif t == 2:
        grid = np.ones(winDims) * EMPTY
        x = (int) (m / 4)
        y = (int) (n / 2)
        grid[x, y] = SPORE
        grid[3 * x, y] = SPORE
        return grid

    # Single spore and impermeable barrier around grid
    elif t == 3:
        grid = np.ones(winDims) * EMPTY
        x = (int) (m / 2)
        y = (int) (n / 2)
        grid[x, y] = SPORE

        # Make inert grid around edges
        grid[:,0] = INERT
        grid[:,-1] = INERT
        grid[0,:] = INERT
        grid[-1,:] = INERT

        return grid

# Rather than using a spread constant, this method determines
# whether spread occurs by using a multi-branch random walk,
# similar to how mycelium actually spreads. 'dist' is the minimum
# linear distance required for spread from a center point.
# 'numTrials' is the number of random walks to generate before returning.
def randomSpread(dist, numTrials):
    sumDist = 0
    for i in range(numTrials):
        sumDist += 1
    return (sumDist / numTrials) >= dist

# State diagram on p. 717
def changeState(copyGrid, i, j):
    global probSpore
    global numMushrooms
    # Check if neighbor cells have mushrooms and update spore spawn probability.
    if mushroomSporeSpawnRule == 1 and copyGrid[i,j] != MUSHROOMS:
        probSpore = (copyGrid[i - 1:i + 1,j - 1:j + 1] == MUSHROOMS).sum() / 8

    if copyGrid[i,j] == SPORE:
        if random.random() < probSporeToHyphae:
            grid[i, j] = YOUNG

    # Modification of state diagram to include spawning of new spores on
    # any kind of ground except inert ground. Code branch applies to both
    # spore spawn rules.
    elif random.random() < probSpore and copyGrid[i,j] != INERT:
        grid[i,j] = SPORE

    # Turn all young hyphae into maturing hyphae after a single timestep
    elif copyGrid[i,j] == YOUNG:
        grid[i,j] = MATURING
    
    # A maturing hyphae has the chance of fruiting a mushroom. Otherwise, it ages.
    elif copyGrid[i,j] == MATURING:
        if random.random() < probMushroom:
            grid[i, j] = MUSHROOMS

            # Increment mushroom counter if spore spawning is based on mushroom count.
            if mushroomSporeSpawnRule == 0:
                numMushrooms = numMushrooms + 1

        else:
            grid[i, j] = OLDER

    # All mushrooms and old hyphae start to decay after one timestep.
    elif copyGrid[i,j] == MUSHROOMS or copyGrid[i,j] == OLDER:
        grid[i,j] = DECAYING
        # Decrement the number of mushrooms if a mushroom started decaying
        # and if spore spawning uses this rule
        if mushroomSporeSpawnRule == 0 and copyGrid[i,j] == MUSHROOMS:
            numMushrooms = numMushrooms - 1
    
    # All decaying hyphae will die after one timestep.
    elif copyGrid[i,j] == DECAYING:
        grid[i,j] = DEAD1
    
    # Do Project 1 so that the length of time the hyphae are dead is probabilistic;
    # and on the average, they are dead for two time steps.
    elif copyGrid[i,j] == DEAD1:
        grid[i,j] = DEAD2
        
    elif copyGrid[i,j] == DEAD2:
        grid[i,j] = EMPTY
    
    elif copyGrid[i,j] == EMPTY:
        if random.random() < isNeighborYoung(copyGrid,i,j):
            grid[i, j] = YOUNG

# Checks Moore neighborhood of cells for YOUNG values and returns new probSpread value.
# Modifies project in S&S to use a dynamic rather than constant probability.
# Assumes cell at [i, j] is already EMPTY
def isNeighborYoung(copyGrid,i, j):
    if copyGrid[i,j] != EMPTY:
        return 0
    #return (copyGrid[i - 1:i + 2,j - 1:j + 2] == YOUNG).sum() / 4.0
    if (copyGrid[i-1:i+2,j-1:j+2] == YOUNG).sum() > 0:
        return probSpread
    return 0

# Draw state to grid
def drawState(d, x, y):
	r = Point(cellWidth * x, cellWidth * y)
	s = Point(cellWidth * x + cellWidth, cellWidth * y + cellWidth)
	t = Rectangle(r,s)
	t.setFill(colorFromState(d))
	t.draw(win)

# EMPTY: Light Green
# SPORE: Black
# YOUNG: Dark Grey
# MATURING: Light Grey
# MUSHROOMS: White
# OLDER: Light Grey
# DECAYING: Tan
# DEAD1: Brown
# DEAD2: Dark Green
# INERT: Yellow
def colorFromState(state):
	if state == EMPTY:
		return color_rgb(0,255,0)
	if state == SPORE:
		return color_rgb(0,0,0)
	elif state == YOUNG:
		return color_rgb(64,64,64)
	elif state == MATURING or state == OLDER:
		return color_rgb(192,192,192)
	elif state == MUSHROOMS:
		return color_rgb(255,255,255)
	elif state == DECAYING:
		return color_rgb(255,255,128)
	elif state == DEAD1:
		return color_rgb(128,128,0)
	elif state == DEAD2:
		return color_rgb(0,128,0)
	elif state == INERT:
		return color_rgb(255,255,0)

# Main program

# Number of mushrooms at each step of each simulation
sims = np.zeros((numSimulations, numTimeSteps))
# Run 'numSimulations' sims
for s in range(numSimulations):
    grid = initGrid(initRule)
    numMushrooms = 0

    #Start by drawing initial state
    for i in range(m):
            for j in range(n):
                drawState(grid[i,j], i, j)

    # Configure spore spawning after initial grid is made
    probSpore = 0

    # Store the number of mushrooms at each time step
    mushrooms = np.zeros(numTimeSteps)

    # Draw each state change for k number of timesteps
    for k in range(numTimeSteps):
        copyGrid = np.copy(grid)
        for i in range(m):
            for j in range(n):
                changeState(copyGrid, i, j)
                drawState(grid[i,j], i, j)
        mushrooms[k] = numMushrooms


        # Calculate spore spawn probability and reset mushroom counter.
        # Only used with spore spawn rule 0
        if mushroomSporeSpawnRule == 0:
            probSpore = numMushrooms / (m * n)
            #numMushrooms = 0
    # Add current run to array of all sims
    sims[s] = mushrooms
    
# Mushroom count analysis
data = np.zeros(numTimeSteps)
# Get average number of mushrooms at each step across all sims
for i in range(numTimeSteps):
    data[i] = np.sum(sims[:,i]) / numSimulations

plt.plot(data)
plt.xlabel("Time step")
plt.ylabel("Number of mushrooms")
plt.text(0.75 * numTimeSteps, 0.1 * np.max(data), "t="+str(initRule))
plt.axes([0, numTimeSteps, 0, np.max(data)])
plt.show()