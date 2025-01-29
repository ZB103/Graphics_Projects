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
Pyramid = [bottompoly, frontpoly, rightpoly, backpoly, leftpoly]

# Definition of the Pyramid's underlying point cloud.  No structure, just the points.
PyramidPointCloud = [apex, base1, base2, base3, base4]
DefaultPyramidPointCloud = copy.deepcopy(PyramidPointCloud)

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
LCube = [ltoppoly, lbottompoly, lfrontpoly, lrightpoly, lbackpoly, lleftpoly]

# Definition of the Pyramid's underlying point cloud.  No structure, just the points.
LCubePointCloud = [lcube1,lcube2,lcube3,lcube4,lcube5,lcube6,lcube7,lcube8]
DefaultLCubePointCloud = copy.deepcopy(LCubePointCloud)

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
RCube = [rtoppoly, rbottompoly, rfrontpoly, rrightpoly, rbackpoly, rleftpoly]

# Definition of the Pyramid's underlying point cloud.  No structure, just the points.
RCubePointCloud = [rcube1,rcube2,rcube3,rcube4,rcube5,rcube6,rcube7,rcube8]
DefaultRCubePointCloud = copy.deepcopy(RCubePointCloud)



#************************************************************************************

# This function resets the pyramid to its original size and location in 3D space
def resetPyramid():
    for i in range(len(PyramidPointCloud)):
        for j in range(3):
            PyramidPointCloud[i][j] = DefaultPyramidPointCloud[i][j]

# This function resets the left cube to its original size and location in 3D space
def resetLCube():
    for i in range(len(LCubePointCloud)):
        for j in range(3):
            LCubePointCloud[i][j] = DefaultLCubePointCloud[i][j]
            
# This function resets the right cube to its original size and location in 3D space
def resetRCube():
    for i in range(len(RCubePointCloud)):
        for j in range(3):
            RCubePointCloud[i][j] = DefaultRCubePointCloud[i][j]


# This function translates an object by some displacement.  The displacement is a 3D
# vector so the amount of displacement in each dimension can vary.
def translate(object, displacement):
    #parsing the object at each polygon
    for polygon in range(len(object)):
        #parsing the polygon at each point
        for point in range(len(object[0])):
            #editing each point by amount specified
            object[polygon][point] += displacement[point]
    
# This function performs a simple uniform scale of an object assuming the object is
# centered at the origin.  The scalefactor is a scalar.
def scale(object,scalefactor):
    #centering the object at the origin
    #get center point
    p2 = len(object) - 1  #last point in list
    centerX = (object[0][0] + object[p2][0]) / 2
    centerY = (object[0][1] + object[p2][1]) / 2
    centerZ = (object[0][2] + object[p2][2]) / 2
    center = [centerX, centerY, centerZ]
    centeredObj = []
    #move object to origin based on center point
    for i in range(0, len(object)):
        centeredObj.append([])
        for j in range(0, len(object[0])):
            centeredObj[i].append(object[i][j] - center[j])
    
    #parsing the object at each polygon
    for i in range(0,len(object)):
        #parsing the polygon at each point
        for j in range(0,len(object[0])):
            #editing each point by amount specified and putting back
            centeredObj[i][j] *= scalefactor
            object[i][j] = centeredObj[i][j] + center[j]

# This function performs a rotation of an object about the Z axis (from +X to +Y)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CCW
# in a LHS when viewed from -Z [the location of the viewer in the standard postion]
def rotateZ(object,degrees):
    degrees = math.radians(degrees)
    #centering the object at the origin
    #get center point
    p2 = len(object) - 1  #last point in list
    centerX = (object[0][0] + object[p2][0]) / 2
    centerY = (object[0][1] + object[p2][1]) / 2
    centerZ = (object[0][2] + object[p2][2]) / 2
    center = [centerX, centerY, centerZ]
    centeredObj = []
    #move object to origin based on center point
    for i in range(0, len(object)):
        centeredObj.append([])
        for j in range(0, len(object[0])):
            centeredObj[i].append(object[i][j] - center[j])
    
    rotObj = []
    #parsing the object at each polygon
    for i in range(0,len(object)):
        #rotating object
        rotObj.append([])
        rotObj[i].append(centeredObj[i][0] * math.cos(degrees) - centeredObj[i][1] * math.sin(degrees))
        rotObj[i].append(centeredObj[i][0] * math.sin(degrees) + centeredObj[i][1] * math.cos(degrees))
        rotObj[i].append(centeredObj[i][2])
        #parsing the polygon at each point
        for j in range(0,len(object[0])):
            #putting object back
            object[i][j] = rotObj[i][j] + center[j]
    
# This function performs a rotation of an object about the Y axis (from +Z to +X)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CW
# in a LHS when viewed from +Y looking toward the origin.
def rotateY(object,degrees):
    degrees = math.radians(degrees)
    #centering the object at the origin
    #get center point
    p2 = len(object) - 1  #last point in list
    centerX = (object[0][0] + object[p2][0]) / 2
    centerY = (object[0][1] + object[p2][1]) / 2
    centerZ = (object[0][2] + object[p2][2]) / 2
    center = [centerX, centerY, centerZ]
    centeredObj = []
    #move object to origin based on center point
    for i in range(0, len(object)):
        centeredObj.append([])
        for j in range(0, len(object[0])):
            centeredObj[i].append(object[i][j] - center[j])
    
    rotObj = []
    #parsing the object at each polygon
    for i in range(0,len(object)):
        #rotating object
        rotObj.append([])
        rotObj[i].append(centeredObj[i][0] * math.cos(degrees) + centeredObj[i][2] * math.sin(degrees))
        rotObj[i].append(centeredObj[i][1])
        rotObj[i].append((-1)*centeredObj[i][0] * math.sin(degrees) + centeredObj[i][2] * math.cos(degrees))
        #parsing the polygon at each point
        for j in range(0,len(object[0])):
            #putting object back
            object[i][j] = rotObj[i][j] + center[j]

# This function performs a rotation of an object about the X axis (from +Y to +Z)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CW
# in a LHS when viewed from +X looking toward the origin.
def rotateX(object,degrees):
    degrees = math.radians(degrees)
    #centering the object at the origin
    #get center point
    p2 = len(object) - 1  #last point in list
    centerX = (object[0][0] + object[p2][0]) / 2
    centerY = (object[0][1] + object[p2][1]) / 2
    centerZ = (object[0][2] + object[p2][2]) / 2
    center = [centerX, centerY, centerZ]
    centeredObj = []
    #move object to origin based on center point
    for i in range(0, len(object)):
        centeredObj.append([])
        for j in range(0, len(object[0])):
            centeredObj[i].append(object[i][j] - center[j])
    
    rotObj = []
    #parsing the object at each polygon
    for i in range(0,len(object)):
        #rotating object
        rotObj.append([])
        rotObj[i].append(centeredObj[i][0])
        rotObj[i].append(centeredObj[i][1] * math.cos(degrees) - centeredObj[i][2] * math.sin(degrees))
        rotObj[i].append(centeredObj[i][1] * math.sin(degrees) + centeredObj[i][2] * math.cos(degrees))
        #parsing the polygon at each point
        for j in range(0,len(object[0])):
            #putting object back
            object[i][j] = rotObj[i][j] + center[j]

# The function will draw an object by repeatedly callying drawPoly on each polygon in the object
def drawObject(object,lineColor):
    #object: list of polygons
    for polygon in object:
        drawPoly(polygon,lineColor)

# This function will draw a polygon by repeatedly callying drawLine on each pair of points
# making up the object.  Remember to draw a line between the last point and the first.
def drawPoly(poly,lineColor):
    #poly: list of points
    #parse list of points to draw line
    for i in range(0, len(poly) - 1):
        drawLine(poly[i], poly[i+1],lineColor)
    #draw line from last point to first point
    drawLine(poly[len(poly)-1], poly[0],lineColor)

# Project the 3D endpoints to 2D point using a perspective projection implemented in 'project'
# Convert the projected endpoints to display coordinates via a call to 'convertToDisplayCoordinates'
# draw the actual line using the built-in create_line method
def drawLine(point1, point2,lineColor):
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
    if selectedObj == Pyramid:
        resetPyramid()
    elif selectedObj == LCube:
        resetLCube()
    elif selectedObj == RCube:
        resetRCube()
    drawAll()

def larger():
    w.delete(ALL)
    scale(selectedObjCloud,1.1)
    drawAll()

def smaller():
    w.delete(ALL)
    scale(selectedObjCloud,.9)
    drawAll()

def forward():
    w.delete(ALL)
    translate(selectedObjCloud,[0,0,5])
    drawAll()

def backward():
    w.delete(ALL)
    translate(selectedObjCloud,[0,0,-5])
    drawAll()

def left():
    w.delete(ALL)
    translate(selectedObjCloud,[-5,0,0])
    drawAll()

def right():
    w.delete(ALL)
    translate(selectedObjCloud,[5,0,0])
    drawAll()

def up():
    w.delete(ALL)
    translate(selectedObjCloud,[0,5,0])
    drawAll()

def down():
    w.delete(ALL)
    translate(selectedObjCloud,[0,-5,0])
    drawAll()

def xPlus():
    w.delete(ALL)
    rotateX(selectedObjCloud,5)
    drawAll()

def xMinus():
    w.delete(ALL)
    rotateX(selectedObjCloud,-5)
    drawAll()

def yPlus():
    w.delete(ALL)
    rotateY(selectedObjCloud,5)
    drawAll()

def yMinus():
    w.delete(ALL)
    rotateY(selectedObjCloud,-5)
    drawAll()

def zPlus():
    w.delete(ALL)
    rotateZ(selectedObjCloud,5)
    drawAll()

def zMinus():
    w.delete(ALL)
    rotateZ(selectedObjCloud,-5)
    drawAll()

#redraws all shapes
def drawAll():
    if selectedObj == Pyramid:
        drawObject(Pyramid,"red")
        drawObject(LCube,"black")
        drawObject(RCube,"black")
    elif selectedObj == LCube:
        drawObject(Pyramid,"black")
        drawObject(LCube,"red")
        drawObject(RCube,"black")
    elif selectedObj == RCube:
        drawObject(Pyramid,"black")
        drawObject(LCube,"black")
        drawObject(RCube,"red")



#switches the object highlighted to the one to its right
def switchTargetRight(event):
    global selectedObj
    global selectedObjCloud
    if selectedObj == LCube:
        selectedObj = Pyramid
        selectedObjCloud = PyramidPointCloud
    elif selectedObj == Pyramid:
        selectedObj = RCube
        selectedObjCloud = RCubePointCloud
    elif selectedObj == RCube:
        selectedObj = LCube
        selectedObjCloud = LCubePointCloud
    #redraw with new selection colored red
    w.delete(ALL)
    drawAll()
    
#switches the object highlighted to the one to its left
def switchTargetLeft(event):
    global selectedObj
    global selectedObjCloud
    if selectedObj == RCube:
        selectedObj = Pyramid
        selectedObjCloud = PyramidPointCloud
    elif selectedObj == LCube:
        selectedObj = RCube
        selectedObjCloud = RCubePointCloud
    elif selectedObj == Pyramid:
        selectedObj = LCube
        selectedObjCloud = LCubePointCloud
    #redraw with new selection colored red
    w.delete(ALL)
    drawAll()

root = Tk()
root.title("Wireframe Graphics")
outerframe = Frame(root)
outerframe.pack()

#creating default workspace
w = Canvas(outerframe, width=CanvasWidth, height=CanvasHeight)
#begins as selection
selectedObj = Pyramid
selectedObjCloud = PyramidPointCloud
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