#IMPORT SYSTEM MODULES
import os
import sys, string
import arcpy
from arcpy import env
from arcpy.sa import *
print("Libraries Success")
arcpy.CheckOutExtension("Spatial") # Check out ArcGIS Spatial Analyst extension license
env.overwriteOutput = True # Allow files to be overwritten
print("Environment Success")
workspace = "C:\\users\\library\\Downloads\\wuifolder\\" # Make sure all other input files are in this folder!
Houses =  workspace + "strdataclipeed.shp" # point, housing locations; be sure that there is a field called "value1" where all points have 1 assigned to this column
Water = workspace + "water.tif" # polygon, waterbodies; '0' for unbuildable and '1' for areas where housed can be built
WildlandBase = workspace + "wildland.tif" # binary raster, wildland vegetation ('1' for veg that can carry fire, '0' otherwise)
farcover = workspace + "wildveg2400.tif" # '1' for cells within 2400m of vegetation patches that are larger than 5km^2, '0' otherwise
study_area = workspace + "county.shp" # shapefile of study area to clip final product
output_folder_name = workspace + "output2" + "\\" 
temp_folder_name = workspace + "temp18jan2149" + "\\" 
arcpy.env.extent = WildlandBase
print("Wrokspaces Success")
if not os.path.exists(temp_folder_name):
    os.makedirs(temp_folder_name)
tempWorkSpace = temp_folder_name
if not os.path.exists(output_folder_name):
    os.makedirs(output_folder_name)
outWorkSpace = output_folder_name
outFile = outWorkSpace + "result_table.txt"
fout = open(outFile, 'w')
fout.write("radius non-WUI intermix interface\n")
for n in range(100, 1100, 100):
#for n in range(100, 200, 100):
    print (n)
    field = "value1" # aca es imprescindible que se elija un campo (columna) que tenga valores "1", porque es el valor que va a tomar como numero de houses. 
    NbrHouses = PointStatistics(Houses,field,"30",NbrCircle(str(n), "MAP"),"SUM")
    NbrHouses.save(tempWorkSpace+"nbrhouses")
    print ("neighborhood statistics complete")
    DensHouses = (arcpy.Raster(tempWorkSpace+"nbrhouses") / ( 3.14 * float(str(n)) * float(str(n))) * 1000000) > 6.17
    DensHouses.save(tempWorkSpace+"denshouses")
    print ("housing density converted")
    OutCon = Con(IsNull(tempWorkSpace+"denshouses"),0, tempWorkSpace+"denshouses")
    OutCon.save(tempWorkSpace+"outcon")
    print ("NODATA replaced by 0")
    denshouse_nonwater = Raster(tempWorkSpace+"outcon") * Raster(Water)
    denshouse_nonwater.save(tempWorkSpace+"denshs_nonwtr")
    print ("water replaced by 0")
    NbrCover = FocalStatistics(arcpy.Raster(WildlandBase), NbrCircle(str(n), "MAP"), "SUM")
    NbrCover.save(tempWorkSpace+"nbrcover")
    NbrCoverZero = FocalStatistics(EqualTo(arcpy.Raster(WildlandBase),0), NbrCircle(str(n), "MAP"), "SUM")
    sumCover = NbrCover+NbrCoverZero
    sumCover.save(tempWorkSpace+"sumCover_"+str(n))
    wildcover = float(1)*NbrCover/(NbrCover+NbrCoverZero)
    wildcover50 = wildcover > 0.5
    wildcover50.save(tempWorkSpace+"wildcover50")
    print ("near wildland cover calculated")
    IMWui = Con((Raster(tempWorkSpace+"denshs_nonwtr") == 1) & (wildcover50 == 1), 1 , 0)
    IMWui.save(tempWorkSpace+"imwui")
    IFWui = Raster(tempWorkSpace+"denshs_nonwtr") * Raster(farcover)
    IFWui.save(tempWorkSpace+"ifwui")
    Wui = Con(IMWui == 1, 1, Con(IFWui == 1, 2 , 0))
    Wui.save(tempWorkSpace+"wui_map_" + str(n))
    arcpy.RasterToPolygon_conversion(tempWorkSpace+"wui_map_" + str(n), tempWorkSpace+"wui_polig_" + str(n), "NO_SIMPLIFY", "VALUE")
    arcpy.Clip_analysis(tempWorkSpace+"wui_polig_" + str(n)+".shp", study_area, outWorkSpace+"wui_polig_" + str(n))
    print ("wui calculated")
    rows = arcpy.SearchCursor(Wui,"","","COUNT")
    row = rows.next()
    fout.write(str(n))
    while row:
        print (row.COUNT)
        fout.write(" " + str(row.COUNT))
        row = rows.next()
    fout.write("\n")
    print ("results exported")
    Wui = None
fout.close()