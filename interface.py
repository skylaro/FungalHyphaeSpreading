from graphics import *
import time

#User-adjustable parameters
winTitle = "Mushroom Simulation"

cellWidth = 15
winDims = (80,20)

# Object variables
win= GraphWin(width=winDims[0] * cellWidth, height=winDims[1] * cellWidth,title=winTitle)
win.setBackground('green')

# Draw state to grid
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
def drawState(d, x, y):
	r = Point(cellWidth * x, cellWidth * y)
	s = Point(cellWidth * x + cellWidth, cellWidth * y + cellWidth)
	t = Rectangle(r,s)
	t.setFill(color_rgb(0,0,d * 255.0))
	t.draw(win)

# Draws momentum vectors at a cell. Multiplier used might be inaccurate.
'''
def drawMomentums(u, v, x, y):
	q = 2.0
	r = Point((cellWidth * x) - (cellWidth / 2.0), (cellWidth * y) - (cellWidth / 2.0))
	s = Point(r.getX() + (q * u), r.getY() + (q * v))
	l = Line(r, s)
	l.setArrow('last')
	l.setOutline('white')
	l.draw(win)
'''


# Runs an animation given a timestep value
def animate(t):
	while(True):
		start = time.time()

		end = time.time()
		time.sleep(t - (end - start))
	return