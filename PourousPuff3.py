# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# PourousPuff3.py
# Created on: 2015-10-05 16:59:14.00000
#   (generated by ArcGIS/ModelBuilder)
# Usage: PourousPuff3 <Thick30m> <Poros3> <Tracking_time> <WLelevm> <Trans> 
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy

arcpy.env.workspace ="C:/PROJECTS/MILLVILLE/Data/FlowModels.gdb"



WLelevm = arcpy.GetParameterAsText(2)
if WLelevm == '#' or not WLelevm:
    WLelevm = "WLelev" # provide a default value if unspecified

desc = arcpy.Describe(WLelevm)
outExtent = desc.extent
rastProp = arcpy.GetRasterProperties_management(WLelevm,"CELLSIZEX")

thickness = float(arcpy.GetParameterAsText(0))
if thickness == '#' or not thickness:
    thickness = 30

porosity = float(arcpy.GetParameterAsText(1))
if porosity == '#' or not porosity:
    porosity = 0.20

cellSize = rastProp.getOutput(0)
arcpy.AddMessage("cell size =" + str(cellSize))

if arcpy.Exists("Thick"):
    arcpy.Delete_management("Thick")
else:
    pass    
Thick = arcpy.sa.CreateConstantRaster(thickness, "FLOAT", cellSize, outExtent)
Thick.save("Thick")

if arcpy.Exists("Poros"):
    arcpy.Delete_management("Poros")
else:
    pass

Poros = arcpy.sa.CreateConstantRaster(porosity, "FLOAT", cellSize, outExtent)
Poros.save("Poros")


Trans = arcpy.GetParameterAsText(3)
if Trans == '#' or not Trans:
    Trans = "Trans" # provide a default value if unspecified

# Local variables:

Particl_TXT = "C:\\PROJECTS\\MILLVILLE\\Data\\Particl_TXT"

if arcpy.Exists("C:/PROJECTS/MILLVILLE/Data/DarcyDir.tif"):
    arcpy.Delete_management("C:/PROJECTS/MILLVILLE/Data/DarcyDir.tif")
    arcpy.Delete_management("C:/PROJECTS/MILLVILLE/Data/DarcyMag.tif")
else:
    pass
arcpy.CheckOutExtension("Spatial")
Output_direction_raster = arcpy.sa.DarcyVelocity(WLelevm, Poros, Thick, Trans, "C:/PROJECTS/MILLVILLE/Data/DarcyMag.tif")
Output_direction_raster.save("C:/PROJECTS/MILLVILLE/Data/DarcyDir.tif")


tracking_times = range(int(arcpy.GetParameterAsText(4)),int(arcpy.GetParameterAsText(5)), int(arcpy.GetParameterAsText(6)))

if arcpy.Exists(Particl_TXT):
    arcpy.Delete_management(Particl_TXT)
else:
    pass

for i in tracking_times:
    FL = "FL" + str(i)
    # Process: Particle Track
    arcpy.sa.ParticleTrack(Output_direction_raster,"C:/PROJECTS/MILLVILLE/Data/DarcyMag.tif", "431911 4615424", Particl_TXT, "30", str(i), FL)

    # Process: Porous Puff
    PP = arcpy.sa.PorousPuff(Particl_TXT, Poros, Thick, 1000000, "", "", 3, 1, 0)
    PP.save("PP"+str(i))

