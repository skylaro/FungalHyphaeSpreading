from graphics import *
import model

#User-adjustable parameters
winTitle = "Mushroom Simulation"
cellWidth = 15
winDims = (model.m, model.n)

# Object variables
win= GraphWin(width=winDims[0] * cellWidth, height=winDims[1] * cellWidth,title=winTitle)

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
	if state == model.EMPTY:
		return color_rgb(0,1,0)
	if state == model.SPORE:
		return color_rgb(0,0,0)
	elif state == model.YOUNG:
		return color_rgb(0.4,0.4,0.4)
	elif state == model.MATURING or state == model.OLDER:
		return color_rgb(0.8,0.8,0.8)
	elif state == model.MUSHROOMS:
		return color_rgb(1,1,1)
	elif state == model.DECAYING:
		return color_rgb(1,1,0.5)
	elif state == model.DEAD1:
		return color_rgb(.5,.5,0)
	elif state == model.DEAD2:
		return color_rgb(0,0.5,0)
	elif state == model.INERT:
		return color_rgb(1,1,0)