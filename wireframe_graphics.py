# Ani Baker | 103-98-202
# CSC 470 | Assignment #1
# 12/18/2024
# Description: A program that implements a small world of three wireframe
# objects using tkinter

import math
import copy
from tkinter import *

CanvasWidth = 600
CanvasHeight = 600
d = 500

#Class that holds each of the objects in a more object-oriented approach
class Shape:
    # Object's polygons
    polys = {}
    # Object's underlying points, no structure
    pointCloud = {}
    # Point cloud to reset object to
    defaultPointCloud = {}
    
    #constructor
    def __init__(self, pol, pc):
        self.polys = pol
        self.pointCloud = pc
        self.defaultPointCloud = copy.deepcopy(self.pointCloud)
    
    # This function resets the pyramid to its original size and location in 3D space
    def resetObject(self):
        for i in range(len(self.pointCloud)):
            for j in range(3):
                self.pointCloud[i][j] = self.defaultPointCloud[i][j]
    
    #centering the object at the origin
    def centerObj(self):
        #get center point
        p2 = len(self.pointCloud) - 1  #last point in list
        centerX = (self.pointCloud[0][0] + self.pointCloud[p2][0]) / 2
        centerY = (self.pointCloud[0][1] + self.pointCloud[p2][1]) / 2
        centerZ = (self.pointCloud[0][2] + self.pointCloud[p2][2]) / 2
        center = [centerX, centerY, centerZ]
        centeredObj = []
        #move object to origin based on center point
        for i in range(0, len(self.pointCloud)):
            centeredObj.append([])
            for j in range(0, len(self.pointCloud[0])):
                centeredObj[i].append(self.pointCloud[i][j] - center[j])
        return centeredObj, center

    # This function translates an object by some displacement.  The displacement is a 3D
    # vector so the amount of displacement in each dimension can vary.
    def translate(self, displacement):
        #parsing the object at each polygon
        for polygon in range(len(self.pointCloud)):
            #parsing the polygon at each point
            for point in range(len(self.pointCloud[0])):
                #editing each point by amount specified
                self.pointCloud[polygon][point] += displacement[point]
        
    # This function performs a simple uniform scale of an object assuming the object is
    # centered at the origin.  The scalefactor is a scalar.
    def scale(self, scalefactor):
        #center obj at origin
        centeredObj, center = self.centerObj()
        
        #parsing the object at each polygon
        for i in range(0,len(self.pointCloud)):
            #parsing the polygon at each point
            for j in range(0,len(self.pointCloud[0])):
                #editing each point by amount specified and putting back
                centeredObj[i][j] *= scalefactor
                self.pointCloud[i][j] = centeredObj[i][j] + center[j]
    
    # This function performs a rotation of an object about the Z axis (from +X to +Y)
    # by 'degrees', assuming the object is centered at the origin.  The rotation is CCW
    # in a LHS when viewed from -Z [the location of the viewer in the standard postion]
    def rotateZ(self, degrees):
        radians = math.radians(degrees)
        #center obj at origin
        centeredObj, center = self.centerObj()
        
        rotObj = []
        #parsing the object at each polygon
        for i in range(0,len(self.pointCloud)):
            #rotating object
            rotObj.append([])
            rotObj[i].append(centeredObj[i][0] * math.cos(radians) - centeredObj[i][1] * math.sin(radians))
            rotObj[i].append(centeredObj[i][0] * math.sin(radians) + centeredObj[i][1] * math.cos(radians))
            rotObj[i].append(centeredObj[i][2])
            #parsing the polygon at each point
            for j in range(0,len(self.pointCloud[0])):
                #putting object back
                self.pointCloud[i][j] = rotObj[i][j] + center[j]
    
    # This function performs a rotation of an object about the Y axis (from +Z to +X)
    # by 'degrees', assuming the object is centered at the origin.  The rotation is CW
    # in a LHS when viewed from +Y looking toward the origin.
    def rotateY(self, degrees):
        radians = math.radians(degrees)
        #center obj at origin
        centeredObj, center = self.centerObj()
        
        rotObj = []
        #parsing the object at each polygon
        for i in range(0,len(self.pointCloud)):
            #rotating object
            rotObj.append([])
            rotObj[i].append(centeredObj[i][0] * math.cos(radians) + centeredObj[i][2] * math.sin(radians))
            rotObj[i].append(centeredObj[i][1])
            rotObj[i].append((-1)*centeredObj[i][0] * math.sin(radians) + centeredObj[i][2] * math.cos(radians))
            #parsing the polygon at each point
            for j in range(0,len(self.pointCloud[0])):
                #putting object back
                self.pointCloud[i][j] = rotObj[i][j] + center[j]

    # This function performs a rotation of an object about the X axis (from +Y to +Z)
    # by 'degrees', assuming the object is centered at the origin.  The rotation is CW
    # in a LHS when viewed from +X looking toward the origin.
    def rotateX(self, degrees):
        radians = math.radians(degrees)
        #center obj at origin
        centeredObj, center = self.centerObj()
        
        rotObj = []
        #parsing the object at each polygon
        for i in range(0,len(self.pointCloud)):
            #rotating object
            rotObj.append([])
            rotObj[i].append(centeredObj[i][0])
            rotObj[i].append(centeredObj[i][1] * math.cos(radians) - centeredObj[i][2] * math.sin(radians))
            rotObj[i].append(centeredObj[i][1] * math.sin(radians) + centeredObj[i][2] * math.cos(radians))
            #parsing the polygon at each point
            for j in range(0,len(self.pointCloud[0])):
                #putting object back
                self.pointCloud[i][j] = rotObj[i][j] + center[j]

# ***************************** Initialize Pyramid Object ***************************
# Definition  of the five underlying points
apex = [0,50,100]
base1 = [50,-50,50]
base2 = [50,-50,150]
base3 = [-50,-50,150]
base4 = [-50,-50,50]

# Definition of the five polygon faces using the meaningful point names
# Polys are defined in clockwise order when viewed from the outside
frontpoly = [apex,base1,base4]
rightpoly = [apex,base2,base1]
backpoly = [apex,base3,base2]
leftpoly = [apex,base4,base3]
bottompoly = [base1,base2,base3,base4]

# Definition of the object
Pyramid = Shape([bottompoly, frontpoly, rightpoly, backpoly, leftpoly], [apex, base1, base2, base3, base4])

# ***************************** Initialize Cube 1 Object ***************************
# Definition  of the eight underlying points
lcube1 = [-150,150,25]
lcube2 = [-150,125,25]
lcube3 = [-125,150,25]
lcube4 = [-125,125,25]
lcube5 = [-150,150,50]
lcube6 = [-150,125,50]
lcube7 = [-125,150,50]
lcube8 = [-125,125,50]

# Definition of the six polygon faces using the meaningful point names
# Polys are defined in clockwise order when viewed from the outside
lfrontpoly = [lcube1,lcube3,lcube4,lcube2]
lrightpoly = [lcube7,lcube3,lcube4,lcube8]
lbackpoly = [lcube5,lcube7,lcube8,lcube6]
lleftpoly = [lcube1,lcube5,lcube7,lcube3]
ltoppoly = [lcube5,lcube7,lcube3,lcube1]
lbottompoly = [lcube2,lcube4,lcube8,lcube6]

# Definition of the object
LCube = Shape([ltoppoly, lbottompoly, lfrontpoly, lrightpoly, lbackpoly, lleftpoly], [lcube1,lcube2,lcube3,lcube4,lcube5,lcube6,lcube7,lcube8])

# ***************************** Initialize Cube 2 Object ***************************
# Definition  of the eight underlying points
rcube1 = [150,150,25]
rcube2 = [150,125,25]
rcube3 = [125,150,25]
rcube4 = [125,125,25]
rcube5 = [150,150,50]
rcube6 = [150,125,50]
rcube7 = [125,150,50]
rcube8 = [125,125,50]

# Definition of the six polygon faces using the meaningful point names
# Polys are defined in clockwise order when viewed from the outside
rfrontpoly = [rcube1,rcube3,rcube4,rcube2]
rrightpoly = [rcube7,rcube3,rcube4,rcube8]
rbackpoly = [rcube5,rcube7,rcube8,rcube6]
rleftpoly = [rcube1,rcube5,rcube7,rcube3]
rtoppoly = [rcube5,rcube7,rcube3,rcube1]
rbottompoly = [rcube2,rcube4,rcube8,rcube6]

# Definition of the object
RCube = Shape([rtoppoly, rbottompoly, rfrontpoly, rrightpoly, rbackpoly, rleftpoly], [rcube1,rcube2,rcube3,rcube4,rcube5,rcube6,rcube7,rcube8])



#**************************************drawing functions**********************************************

#redraws all shapes
def drawAll():
    drawObject(0)
    drawObject(1)
    drawObject(2)

# The function will draw an object by repeatedly callying drawPoly on each polygon in the object
def drawObject(objectNum):
    #object: list of polygons
    #deciding line color, red for selected shape
    lineColor = ""
    if(objectNum == currObj):
        lineColor = "red"
    else:
        lineColor = "black"
    #draw polygons
    for polygon in objList[objectNum].polys:
        drawPoly(polygon, lineColor)

# This function will draw a polygon by repeatedly callying drawLine on each pair of points
# making up the object.  Remember to draw a line between the last point and the first.
def drawPoly(poly, lineColor):
    #poly: list of points
    #parse list of points to draw line
    for i in range(0, len(poly) - 1):
        drawLine(poly[i], poly[i+1], lineColor)
    #draw line from last point to first point
    drawLine(poly[len(poly)-1], poly[0],lineColor)

# Project the 3D endpoints to 2D point using a perspective projection implemented in 'project'
# Convert the projected endpoints to display coordinates via a call to 'convertToDisplayCoordinates'
# draw the actual line using the built-in create_line method
def drawLine(point1, point2, lineColor):
    #point: list of coordinates
    #converting points and drawing line between them
    projectedStart = project(point1)
    projectedEnd = project(point2)
    w.create_line(projectedStart[0], projectedStart[1], projectedEnd[0], projectedEnd[1],fill=lineColor)

# This function converts from 3D to 2D (+ depth) using the perspective projection technique.  Note that it
# will return a NEW list of points.  We will not want to keep around the projected points in our object as
# they are only used in rendering
def project(point):
    #point: list of coordinates
    #point[0] = X
    #point[1] = Y
    #point[2] = Z
    
    #convert X with projection equation
    projectedX = d * (point[0] / (d + point[2]))
    
    #convert Y with projection equation
    projectedY = d * (point[1] / (d + point[2]))
    
    #convert Z with projection equation (used
    #for overlapping objects; not used during this project)
    projectedZ = d * (point[2] / (d + point[2]))
    
    #turn point into array and return
    ps = convertToDisplayCoordinates([projectedX, projectedY, projectedZ])
    return ps

# This function converts a 2D point to display coordinates in the tk system.  Note that it will return a
# NEW list of points.  We will not want to keep around the display coordinate points in our object as 
# they are only used in rendering.
def convertToDisplayCoordinates(point):
    # original system: +X right, +Y up, +Z in, origin center
    # display system: +X right, +Y down, +Z out, origin top left corner
    #point[0] = X
    #point[1] = Y
    #point[2] = Z
    
    #x does not change
    newX = float(point[0])
    #y becomes inverted sign
    newY = point[1] * -1
    #z becomes inverted sign
    newZ = point[2] * -1
    #move x and y to origin
    newX = newX + CanvasWidth / 2
    newY = newY + CanvasHeight / 2
    
    #turn point into array and return
    displayXY = [newX, newY, newZ]
    return displayXY
    

# **************************************************************************
# Everything below this point implements the interface
def reset():
    w.delete(ALL)
    objList[currObj].resetObject()
    drawAll()

def larger():
    w.delete(ALL)
    objList[currObj].scale(1.1)
    drawAll()

def smaller():
    w.delete(ALL)
    objList[currObj].scale(.9)
    drawAll()

def forward():
    w.delete(ALL)
    objList[currObj].translate([0,0,5])
    drawAll()

def backward():
    w.delete(ALL)
    objList[currObj].translate([0,0,-5])
    drawAll()

def left():
    w.delete(ALL)
    objList[currObj].translate([-5,0,0])
    drawAll()

def right():
    w.delete(ALL)
    objList[currObj].translate([5,0,0])
    drawAll()

def up():
    w.delete(ALL)
    objList[currObj].translate([0,5,0])
    drawAll()

def down():
    w.delete(ALL)
    objList[currObj].translate([0,-5,0])
    drawAll()

def xPlus():
    w.delete(ALL)
    objList[currObj].rotateX(5)
    drawAll()

def xMinus():
    w.delete(ALL)
    objList[currObj].rotateX(-5)
    drawAll()

def yPlus():
    w.delete(ALL)
    objList[currObj].rotateY(5)
    drawAll()

def yMinus():
    w.delete(ALL)
    objList[currObj].rotateY(-5)
    drawAll()

def zPlus():
    w.delete(ALL)
    objList[currObj].rotateZ(5)
    drawAll()

def zMinus():
    w.delete(ALL)
    objList[currObj].rotateZ(-5)
    drawAll()

#switches the object highlighted to the one to its right
def switchTargetRight(event):
    global currObj
    currObj += 1
    #loop to top of list
    if currObj == 3:
        currObj = 0
    #redraw with new selection colored red
    w.delete(ALL)
    drawAll()
    
#switches the object highlighted to the one to its left
def switchTargetLeft(event):
    global currObj
    currObj -= 1
    #loop to top of list
    if currObj == -1:
        currObj = 2
    #redraw with new selection colored red
    w.delete(ALL)
    drawAll()

root = Tk()
root.title("Wireframe Graphics")
outerframe = Frame(root)
outerframe.pack()

#creating default workspace
w = Canvas(outerframe, width=CanvasWidth, height=CanvasHeight)
#creating list of objects
            #0      1       2
objList = [LCube, Pyramid, RCube]
#begins as selection
currObj = 1 #Pyramid
drawAll()
w.pack()

controlpanel = Frame(outerframe)
controlpanel.pack()

#buttons on bottom of screen
resetcontrols = Frame(controlpanel, height=100, borderwidth=2, relief=RIDGE)
resetcontrols.pack(side=LEFT)

resetcontrolslabel = Label(resetcontrols, text="Reset")
resetcontrolslabel.pack()

resetButton = Button(resetcontrols, text="Reset", fg="green", command=reset)
resetButton.pack(side=LEFT)

scalecontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
scalecontrols.pack(side=LEFT)

scalecontrolslabel = Label(scalecontrols, text="Scale")
scalecontrolslabel.pack()

largerButton = Button(scalecontrols, text="Larger", command=larger)
largerButton.pack(side=LEFT)

smallerButton = Button(scalecontrols, text="Smaller", command=smaller)
smallerButton.pack(side=LEFT)

translatecontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
translatecontrols.pack(side=LEFT)

translatecontrolslabel = Label(translatecontrols, text="Translation")
translatecontrolslabel.pack()

forwardButton = Button(translatecontrols, text="FW", command=forward)
forwardButton.pack(side=LEFT)

backwardButton = Button(translatecontrols, text="BK", command=backward)
backwardButton.pack(side=LEFT)

leftButton = Button(translatecontrols, text="LF", command=left)
leftButton.pack(side=LEFT)

rightButton = Button(translatecontrols, text="RT", command=right)
rightButton.pack(side=LEFT)

upButton = Button(translatecontrols, text="UP", command=up)
upButton.pack(side=LEFT)

downButton = Button(translatecontrols, text="DN", command=down)
downButton.pack(side=LEFT)

rotationcontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
rotationcontrols.pack(side=LEFT)

rotationcontrolslabel = Label(rotationcontrols, text="Rotation")
rotationcontrolslabel.pack()

xPlusButton = Button(rotationcontrols, text="X+", command=xPlus)
xPlusButton.pack(side=LEFT)

xMinusButton = Button(rotationcontrols, text="X-", command=xMinus)
xMinusButton.pack(side=LEFT)

yPlusButton = Button(rotationcontrols, text="Y+", command=yPlus)
yPlusButton.pack(side=LEFT)

yMinusButton = Button(rotationcontrols, text="Y-", command=yMinus)
yMinusButton.pack(side=LEFT)

zPlusButton = Button(rotationcontrols, text="Z+", command=zPlus)
zPlusButton.pack(side=LEFT)

zMinusButton = Button(rotationcontrols, text="Z-", command=zMinus)
zMinusButton.pack(side=LEFT)

#arrow keys change selected object and highlight it red
root.bind('<Left>', switchTargetLeft)
root.bind('<Right>', switchTargetRight)

root.mainloop()