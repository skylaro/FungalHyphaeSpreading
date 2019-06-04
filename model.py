# -*- coding: utf-8 -*-
'''
Mushroom model from book.

Projects:
Develop the simulation of this module using absorbing boundary conditions.
Include a function to show the situation aboveground. Run the simulation
employing various initial grids, as follows:
    a.  As described in the module with various values of probSpore. Describe
        the results.
    b.  With exactly one spore in the middle. Verify that the figure seems to agree
        with Figure 14.5.1.
    c.  With exactly two spores that are several cells apart toward the middle.
        Verify that the rings merge into the figure-eight pattern observed in na-
        ture, as in Figure 14.5.2.
    d.  With exactly one spore and a barrier. Verify that the results appear to
        agree with the growth pattern in Figure 14.5.3.

Do Project 1 where the probability of young hyphae spreading into a site is
proportional to the number of neighbors that contain young hyphae.

Adjust the simulation of this module so that new spores can form when
mushrooms are present. Consider the following two possibilities:
    a.  The probability that a cell can obtain a spore at the next time period is
        equal to the percentage of mushrooms in the grid.
    b.  A cell can obtain a spore at the next time period with a specified probabil-
        ity provided one of its neighbors contains a mushroom.

Do Project 1 so that the length of time the hyphae are dead is probabilistic;
and on the average, they are dead for two time steps.

Do Project 1 using periodic boundary conditions.

Do Project 1 using reflecting boundary conditions.

Do Project 1, where the neighbors of a cell include those cells to the north-
east, southeast, southwest, and northwest.

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

import numpy as np
import random
import time
import sim_graph as g

#import matplotlib.pyplot as plt

# Cell States
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
probSpore = 0.5
m = 30
n = 30
grid = np.random.choice(a=[SPORE, EMPTY], size=(m, n), p=[probSpore, 1-probSpore])

'''
the 3 dimension is to store the (state, R, G, B)
grid = np.zeros((m,n,4))

grid[:,:,2] = 1
grid[int(m/2),int(n/2),:] = 0
grid[int(m/2),int(n/2),0] = 1
'''

# Other adjustables properties
animationTimestep = 0.1
numTimeSteps = 400

# State diagram on p. 717
def changeState(i, j):
    if grid[i,j] == SPORE:
        if random.random() < probSporeToHyphae:
            grid[i, j] = YOUNG

            '''DarkGrey 51,51,51
            grid[i, j,1] = .20
            grid[i, j,2] = .20
            grid[i, j,3] = .20
            '''         
    elif grid[i,j] == YOUNG:
        grid[i,j] = MATURING
        
        '''Light Grey 178,178,178
        grid[i, j,1] = .7
        grid[i, j,2] = .7
        grid[i, j,3] = .7
        '''    
    elif grid[i,j] == MATURING:
        if random.random() < probMushroom:
            grid[i, j] = MUSHROOMS

            '''White 255,255,255
            grid[i, j,1] = 1
            grid[i, j,2] = 1
            grid[i, j,3] = 1
            '''
        else:
            grid[i, j] = OLDER
            
            '''Light Grey 178,178,178
            grid[i, j,1] = .7
            grid[i, j,2] = .7
            grid[i, j,3] = .7
            '''
    elif grid[i,j] == MUSHROOMS or grid[i,j] == OLDER:
        grid[i,j] = DECAYING
        
        '''Tan ---- 204,127,51
        grid[i, j,1] = .80
        grid[i, j,2] = .50
        grid[i, j,3] = .2
        '''
    elif grid[i,j] == DECAYING:
        grid[i,j] = DEAD1
        
        '''Brown ---- 178,51,0
        grid[i, j,1] = .70
        grid[i, j,2] = .20
        grid[i, j,3] = .1
        '''
    elif grid[i,j] == DEAD1:
        grid[i,j] = DEAD2
        
        '''Dark Green ----0 102 0
        grid[i, j,1] = 0
        grid[i, j,2] = .4
        grid[i, j,3] = 0
        '''
    elif grid[i,j] == DEAD2:
        grid[i,j] = EMPTY
        
        '''light Green 0,255,0
        grid[i, j,1] = 0
        grid[i, j,2] = 1
        grid[i, j,3] = 0
        '''
    elif grid[i,j] == EMPTY:
        if (random.random() < probSpread) and isNeighborYoung(i,j):
            grid[i, j] = YOUNG
            
            '''DarkGrey 51,51,51
            grid[i, j,1] = .20
            grid[i, j,2] = .20
            grid[i, j,3] = .20
            '''

# Checks Moore neighborhood of cells for YOUNG values.
# Assumes cell at [i, j] is already EMPTY
def isNeighborYoung(i, j):
    return YOUNG in grid[i - 1:i + 1,j - 1:j + 1]

# Main program

#Start by drawing initial state
for i in range(m):
        for j in range(n):
            g.drawState(grid[i,j], i, j)

# Draw each state change for k number of timesteps
for k in range(numTimeSteps):
    start = time.time()
    for i in range(m):
        for j in range(n):
            changeState(i,j)
            g.drawState(grid[i,j], i, j)
    end = time.time()
    time.sleep(animationTimestep - (end - start))

#drive for the simulation 
#for efficiency i commented out the plotting 
'''                                                            
def simDrive():
    simDuration = 40
    timeStep = []
    gridCopy = np.copy(grid)
    #print(gridCopy[:,:,0])
    img, ax = show_grid(grid)
    for  ith in range(simDuration):
        for i in range(m):
            for j in range(n):
                changeState(gridCopy, i,j)
                
        #print(ith)
        #print(grid[:,:,0])
        #print(gridCopy[:,:,0])
        
        
        gridCopy = np.copy(grid)
        img, ax = show_grid(grid, img , ax)        
        
        #currentGrid = np.copy(grid)
        timeStep.append(gridCopy)
        #interface.animate(currentGrid)
        #print(grid[:,:,0])
def show_grid(gridField, img = None, ax = None):
    """ This is the animation of the CA for fluid dynamics.
    in this method we make a 14 by 14 figure that is the shape of the channel. From our
    research on the Navier Equations we use U to show the what the current state of the water motion it is in.
    Gray means close to zero V.
    
    
    
    """
    length = m
    width = n
    data = np.zeros((length, width, 3), dtype='f')

    color = np.array([[0,255,0],[0,0,0],[25,25,25],[105,105,105],[255,255,255],[105,105,105],[245,245,220],[165,42,42],[0,100,0],[255,255,0]])
    #- Create figure and axes:

    


    #- Set first display data values:
    data[:,:, 0] = color[0,0] /255       
    data[:,:, 1] = color[0,1] /255     
    data[:,:, 2] = color[0,2] /255      
    
    #if the img is not set yet display initial values of no motion
    if img is None:
        fig = plt.figure()
        ax = fig.add_axes( (0, 0, .5, .5), frameon=False )

        #- Draw image:

        img = ax.imshow(data, interpolation='none',
                extent=[0, width, 0, length],
                aspect="auto",
                zorder=0)

        plt.pause(2)

    
    #- Draw image:
    data[:,:,:] = grid[:,:,1:]
    img = ax.imshow(data, interpolation='none',
                extent=[0, width, 0, length],
                aspect="auto",
                zorder=0)

    img.set_data(data)

    ax.axis('off')
    plt.show()
    plt.pause(1)
    return img, ax


simDrive()
'''