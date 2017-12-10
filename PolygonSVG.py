#  This code will take an SVG, which was generated by Inkscape from another image type.
#  Then extract each component object, writing a csv of polygon data which can be visualized in Tableau.
#  The program will also write a csv with Tableau color palette information.
#
#  Written by Ken Flerlage, December, 2017
#
#  This code is in the public domain

from xml.dom import minidom
from base64 import b16encode
import math
import sys
import os
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
 
# Prompt for the input file.
def get_file():
    root = Tk()
    root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select File",filetypes = (("Scalable Vector Graphic","*.svg"),("All Files","*.*")))
    root.withdraw()

    return root.filename 

# Convert RGB Color Values to Hex.
def convertRGBtoHex (Red, Green, Blue):
    triplet = (Red, Green, Blue)
    colorHex = b'#'+ b16encode(bytes(triplet))
    colorHex = str(colorHex)
    colorHex = colorHex[2:len(colorHex)-1]
    
    return colorHex;

# Get the Hex color from the fill color string for the svg object.
def getColorHex (RGBString):
    RGBString = RGBString[4:len(RGBString)-1]
    rgbList = RGBString.split(',')
    Red = int(rgbList[0])
    Green = int(rgbList[1])
    Blue = int(rgbList[2])
    colorHex = str(convertRGBtoHex(Red, Green, Blue))
    
    return colorHex;

#---------------------------------------------------------------------------------------
# Main processing routine.
# Prompt for SVG file.
xmlin = get_file()
if xmlin == "":
    messagebox.showinfo("Error", "No file selected. Program will now quit.")
    sys.exit()

# Set output files to write to the same folder.
filepath = os.path.dirname(xmlin)
if filepath[-1:] != "/":
    filepath += "/"

outFile = filepath + 'Polygon.csv'
colorFile = filepath + 'Colors.csv'

out = open(outFile,'w') 
outColor = open(colorFile,'w') 

# Write header of the polygon csv file.
outString = 'Polygon ID,Point ID,X,Y'
out.write (outString)
out.write('\n')

# Write header of the color csv file.
outString = 'Polygon ID,Color Hex,Palette'
outColor.write (outString)
outColor.write('\n')

xmldoc = minidom.parse(xmlin)
shapeNum = 0

# Loop through each line of the file and parse it into xml components
itemlist = xmldoc.getElementsByTagName('path')
for s in itemlist:
    shapeNum += 1
    pointNum = 0

    # Get fill color attributes.
    style = s.attributes['style'].value
    style = style.replace("fill:", "")
    colorHex = style[:7]
    outString = str(shapeNum) + ',' + colorHex + ','+ '<color>' + colorHex + '</color>'
    outColor.write (outString)
    outColor.write('\n')

    # Loop through the points for each polygon.
    points = s.attributes['d'].value
    pointsList = points.split(" ")
    pointIsX = True
    for point in pointsList:

        if point.find(",") > -1:
            # This string has a comma in it, so it contains a coordinate.
            pointNum += 1
    
            pList = point.split(",")

            for p in pList:
                if pointIsX == True:
                    x = p
                    pointIsX = False
                else:
                    y = p
                    pointIsX = True

                    # Now that we have both x and y, write the point to the file.        
                    outString = str(shapeNum) + ',' + str(pointNum) + ',' + str(x) + ',' + str(y) 
                    out.write (outString)
                    out.write('\n')

out.close()
outColor.close()

messagebox.showinfo('Complete', 'Output files, polygon.csv and colors.csv have been written to the following directory: ' + filepath)
