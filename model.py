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
probSporeToHyphae = 0
probMushroom = 0
probSpread = 0

# Grid initialization
probSpore = 0.5
m = 20
n = 20
grid = np.random.choice(a=[SPORE, EMPTY], size=(m, n), p=[probSpore, 1-probSpore])

# State diagram on p. 717
def changeState(i, j):
    if grid[i,j] == SPORE:
        if random.random() < probSporeToHyphae:
            grid[i, j] = YOUNG
    elif grid[i,j] == YOUNG:
        grid[i,j] = MATURING
    elif grid[i,j] == MATURING:
        if random.random() < probMushroom:
            grid[i, j] = MUSHROOMS
        else:
            grid[i, j] = OLDER
    elif grid[i,j] == MUSHROOMS or grid[i,j] == OLDER:
        grid[i,j] = DECAYING
    elif grid[i,j] == DECAYING:
        grid[i,j] = DEAD1
    elif grid[i,j] == DEAD1:
        grid[i,j] = DEAD2
    elif grid[i,j] == DEAD2:
        grid[i,j] = EMPTY
    elif grid[i,j] == EMPTY:
        neighborIsYoung = grid[i-1 : i+1, j-1 : j+1]
        if random.random() < probSpread and neighborIsYoung:
            grid[i, j] = YOUNG