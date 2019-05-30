from graphics import *
import time

#User-adjustable parameters
winTitle = "Water Simulation"

cellWidth = 15
winDims = (80,20)

# Object variables
win= GraphWin(width=winDims[0] * cellWidth, height=winDims[1] * cellWidth,title=winTitle)
win.setBackground('black')

# Draws cell density to display. The shade of blue is given by the cell's normalized density value (0 to 1.0).
def drawDensity(d, x, y):
	eps = 1e-6
	if d < eps:	return
	r = Point(cellWidth * x, cellWidth * y)
	s = Point(cellWidth * x + cellWidth, cellWidth * y + cellWidth)
	t = Rectangle(r,s)
	t.setFill(color_rgb(0,0,d * 255.0))
	t.draw(win)

# Draws momentum vectors at a cell. Multiplier used might be inaccurate.
def drawMomentums(u, v, x, y):
	q = 2.0
	r = Point((cellWidth * x) - (cellWidth / 2.0), (cellWidth * y) - (cellWidth / 2.0))
	s = Point(r.getX() + (q * u), r.getY() + (q * v))
	l = Line(r, s)
	l.setArrow('last')
	l.setOutline('white')
	l.draw(win)

# Draws mass at a given coordinate.
def drawMass(mass, x, y):
	return

# Runs an animation given a timestep value
def animate(t):
	while(True):
		start = time.time()

		end = time.time()
		time.sleep(t - (end - start))
	return