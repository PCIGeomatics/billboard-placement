'''**********************************************************

	PCI Geomatics(C) & esri(C) - Automatic DSM Extraction
	
**********************************************************'''

print ""
print ""
print "***************************************************************"
print ""
print "       -= PCI Geomatics(C) & esri(C) Platform Solutions =-"
print "         Automatic DSM Extraction and Visibility Analysis"
print ""
print "***************************************************************"

print ""
print ""
print "***************************************************************"
print "      		Initializing Libraries"
print "***************************************************************"
print ""

from pci.epipolar2 import *
from pci.autodem2 import *
from pci.fexport import *
from pci.exceptions import *
from pathcheck import *
from sys import argv
import arcpy
from arcpy import env
import arcpy.mapping
import locale
import os
import shutil
import calendar, time

arcpy.CheckOutExtension("3D") #Licensing the ArcGIS 3D Analyst extension
arcpy.env.overwriteOutput = True
print "esri's ArcPy environment successfully loaded."

locale.setlocale( locale.LC_ALL, "" )
locale.setlocale( locale.LC_NUMERIC, "C" )

print ""
print "Initialization Complete"
print ""

print ""
print "***************************************************************"
print "                         User Inputs"
print "***************************************************************"
print ""

in_folder = raw_input("Specify the ingest folder: ")
normalize_path(in_folder)
print ""

print ""
point_file = raw_input("Specify the vector point layer (possible locations for billboard): ")
print ""
road_file = raw_input("Specify the vector road layer used for the billboard analysis: ")
print ""

verify_control_files = [point_file, road_file]
for validate in verify_control_files:
    validate_files(validate)

print ""
out_folder = raw_input("Specify the output directory: ")
if not os.path.exists(out_folder): 
    os.makedirs(out_folder)
    print "output path created"
print ""
    
print "User Parameters Verified!" 
print ""

start_time = calendar.timegm(time.gmtime()) #Current time in seconds since epoch

print ""
print "***************************************************************"
print "              PCI - Running Epipolar Generation"
print "***************************************************************"
print ""

intermediate_outputs = out_folder + '/intermediate_results/'

if not os.path.exists(intermediate_outputs): 
    os.makedirs(intermediate_outputs)

#Set Epipolar Parameters
mfile = in_folder + '*.pix'  
dbic = [1,2,3]      # Integer
mmseg = []      # Integer
dbiw = []      # Integer
srcbgd = u"" 
selmthd = u"OPT" 
minpc = []      # Integer
sampling = [2]      # Integer
epi_outdir = intermediate_outputs + 'epipolars'
outbgd = [0]     # Float
tfile = u"" 
genopt = u"" 
memsize = [1024]      # Integer

os.mkdir(epi_outdir)

try:
	epipolar2( mfile, dbic, mmseg, dbiw, srcbgd, selmthd, minpc,
			  sampling, epi_outdir, outbgd, tfile, genopt, memsize )
except PCIException, e:
    print e
except Exception, e:
    print e

print "Epipolar Generation Complete!"
print ""

print ""
print "***************************************************************"
print "                 PCI - Running DSM Extraction"
print "***************************************************************"
print ""

#Set autodem2 parameters
mfile = intermediate_outputs + 'epipolars\\e*.pix' 
dbic = [1]      # Integer
dbiw = []      # Integer
minmaxel = []     # Float
failvalu = []      # Integer
backelev = [-32768]     # Float
demdet = u"" 
tertype = u"" 
datatype = u"" 
extinter = []      # Integer
demedit = u"" 
scorchan = u"no" 
wallis = u"" 
tfile = u"" 
dsm_outdir = intermediate_outputs + 'dsm' 
filedsm = intermediate_outputs + 'dsm_Urban.pix' 
demclip = u"" 
mapunits = u"" 
upleft = []     # Float
loright = []     # Float
pxszout = [1.0, 1.00]     # Float
mergeopt = u"blend" 

os.mkdir(dsm_outdir)

try:
    autodem2( mfile, dbic, dbiw, minmaxel, failvalu, backelev, demdet, 
			tertype, datatype, extinter, demedit, scorchan, wallis, 
			tfile, dsm_outdir, filedsm, demclip, mapunits, upleft, loright, 
			pxszout, mergeopt )
except PCIException, e:
    print e
except Exception, e:
    print e

print "DSM Extraction Complete!"
print ""

#Export DSM to 32bit GeoTIFF (PCI Geomatica)
fili	=	filedsm
filo	=	intermediate_outputs + 'dsm_urban.tif'
dbiw	=	[]
dbic	=	[1]
dbib	=	[]
dbvs	=	[]
dblut	=	[]
dbpct	=	[]
ftype	=	"TIF"
foptions =  u""

try:
	fexport( fili, filo, dbiw, dbic, dbib, dbvs, dblut, dbpct, ftype, foptions )
except PCIException, e:
    print e
except Exception, e:
    print e

print ""
print "***************************************************************"
print "                 esri - Running Visibility Analysis                 "
print "***************************************************************"
print ""

print "Creating File Geodatabase"
arcpy.CreateFileGDB_management(intermediate_outputs, 'pci_esri-solution.gdb') #Create output file GeoDatabase
print "File Geodatabase created successfully!"
print ""

geodatabase_file = intermediate_outputs + 'pci_esri-solution.gdb'

vis_raster = geodatabase_file + '/Visibility_raster'

Analysis_type = "OBSERVERS"
Import_Surface_Raster = filo
Input_Observer_Feature = point_file
Output_Raster = vis_raster
AboGLevel = ""
NODATA= [-32768]

# Process: Visibility
print ""
print "Beginning Visibility Analysis"
arcpy.Visibility_3d(Import_Surface_Raster, Input_Observer_Feature, Output_Raster, AboGLevel, Analysis_type, "NODATA", "1", "FLAT_EARTH", "0.13", "5", "", "1.5", "", "100", "", "", "", "")
print "Visibility Analysis complete!"

# Convert Raster to Polygon in ArcGIS

inRaster = vis_raster
out_poly_folder = intermediate_outputs + "polygons/"
outPolygons = out_poly_folder + "visibility_poly.shp"
field = "VALUE"

if not os.path.isdir(out_poly_folder):
    os.mkdir(out_poly_folder)

print ""
print "Running Raster to Polygon Conversion"
# Execute RasterToPolygon
arcpy.RasterToPolygon_conversion(inRaster, outPolygons, "NO_SIMPLIFY", field)
print ""
print "Raster to Polygon Conversion Completed!"
print ""

print ""
print "***************************************************************"
print "              esri - Intersect Analysis with Roads               "
print "***************************************************************"
print ""

print "Beginning Intersect Analysis"

final_outputs = out_folder + '/final_results/'
vis_road_dir = final_outputs + 'road_visibility/'

roads = road_file
visibility_poly = outPolygons
inFeatures = [roads, visibility_poly]
roads_Intersect = vis_road_dir + 'road_visibility.shp'  

print 

if not os.path.exists(vis_road_dir): 
    os.makedirs(vis_road_dir)
    print "output path created"
print ""
  
arcpy.Intersect_analysis(inFeatures, roads_Intersect, "ALL", "", "LINE")
print ""
print "Intersect Analysis Complete"

print ""
print "***************************************************************"
print "                esri - Creating ArcMap Project                 "
print "***************************************************************"
print ""

input_folder = in_folder[:-6]
mosaic_file = input_folder + 'mosaic_ref.tif'
map_doc = input_folder + 'projFile.mxd'

print "Gathering Output files"
print""

# get the map document 
mxd = arcpy.mapping.MapDocument(map_doc)  

# get the data frame 
df = arcpy.mapping.ListDataFrames(mxd,"*")[0]

# create a new layer 
road_layer = arcpy.mapping.Layer(roads_Intersect)
road_orig = arcpy.mapping.Layer(road_file)
point_layer = arcpy.mapping.Layer(point_file)

layer_list = [road_layer, road_orig, point_layer]
 
# add the layer to the map at the bottom of the TOC in data frame 0 
for add_layers in layer_list:
    arcpy.mapping.AddLayer(df, add_layers,"BOTTOM")
    
#arcpy.MakeRasterLayer_management(mosaic_file, "Mosaic_tif3", "", "248886 5184779.25 251513.25 5187957", "")
    
map_file_final = final_outputs + 'Vis_analysis.mxd'

mxd.saveACopy(map_file_final)

shutil.copy(mosaic_file, final_outputs)

print ""
print "ALL PROCESSING COMPLETE!"
print ""

end_time = calendar.timegm(time.gmtime()) #Current time in seconds since epoch

process_time = end_time - start_time

print "Processing took " + str(process_time) + " seconds!"

print ""
print "      MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMZZZZZZZMMMMMMMMMMMMMMMMMMMMM"
print "      MMMMMMMMMMMMMMMMMMMMMMMMM,,,,.......MMZZZZZMMMMMMMMMMMMMMMMM"
print "      MMMMMMMMMMMMMMMMMMMM,,,,,,............$ZZZZZZMMMMMMMMMMMMMMM"
print "      MMMMMMMMMMMMMMMM,,,,,,,...,...........ZZZZZZZMMZMMMMMMMMMMMM"
print "      MMMMMMMMMMMMMM,,,,,,,,...,:..==,====.~ZZZZZZZ=.MMZZZMMMMMMMM"
print "      MMMMMMMMMMMM,~===:,,..~,~,..~..=====?ZZZZZZZZ:==MMZZZZZMMMMM"
print "      MMMMMMMMMM,,,,======.~=...~=:...===ZZZZZZZZZZ.,===ZZZZZZZMMM"
print "      MMMMMMMMM,,,,=============,===..=+ZZZZZZZZZZ,:.====ZZZZZZZMM"
print "      MMMMMMMM,,,===========,....=....ZZZZZZZZZZ+~..====IZZZZZZZMM"
print "      MMMMMMM,,~==========....==~..,ZZZZZZZZZZZ..=.=====ZZZZZZZZMM"
print "      MMMMMM,,============,.=====ZZZZZZZZZZZZ$......===ZZZZZZZZZMM"
print "      MMMMM,==========..=======ZZZZZZZZZZZZZ.........=7ZZZZZZZZZMM"
print "      MMMM,,=========,~.:===7ZZZZZZZZZZZZZ.........==ZZZZZZZZZZMMM"
print "      MMMM,:==========~==7ZZZZZZZZZZZZZZ.. .........ZZZZZZZZZZZMMM"
print "      MMM,~===========IZZZZZZZZZZZZZZZ............ZZZZZZZZZZZZ==MM"
print "      MMM,,===,~===ZZZZZZZZZZZZZZZZ~............+ZZZZZZZZZZZZ===MM"
print "      MM,,===,,,ZZZZZZZZZZZZZZZZZ..............ZZZZZZZZZZZZI====MM"
print "      MM,,==?ZZZZZZZZZZZZZZZZZ+..............ZZZZZZZZZZZZZ======MM"
print "      MM,ZZZZZZZZZZZZZZZZZZZ..............~ZZZZZZZZZZZZZ?========M"
print "      MZZZZZZZZZZZZZZZZZZ...............ZZZZZZZZZZZZZZZ==========M"
print "      MZZZZZZZZZZZZZZZ,,,.............ZZZZZZZZZZZZZZZ============M"
print "      MZZZZZZZZZZZZ,,,,,,,.........$ZZZZZZZZZZZZZZZ=============MM"
print "      MZZZZZZZZ$======,,,,,......ZZZZZZZZZZZZZZZZ..========~====MM"
print "      MZZZZZ:,,,,========,,,,.ZZZZZZZZZZZZZZZZZ......=~,,,,,,===MM"
print "      MZZ,,,,,,,==========,IZZZZZZZZZZZZZZZZZ........,,,,,,,,==MMM"
print "      M???,,,,,:========7ZZZZZZZZZZZZZZZZZ~.......,,,,,,,,,,~==MMM"
print "      MMM?,,,,,,=====7ZZZZZZZZZZZZZZZZZZ,..,,,,,,,,,,,,,,,,,==MMMM"
print "      MMMMM,,,,,,=+ZZZZZZZZZZZZZZZZZZZ,,,,,,,,,,,,,,,,,,,,,,=,MMMM"
print "      MMMMMM,,,7ZZZZZZZZZZZZZZZZZZZ====,,,,,,,,,,,,,,,,,,,,=,MMMMM"
print "      MMMMMMZZZZZZZZZZZZZZZZZZZZ======,,,,,,,,,,,,,,,,,,,,=,MMMMMM"
print "      MMMMZZZZZZZZZZZZZZZZZZZ+=======,,,,,,,,,,,,,,,,,,,,=,MMMMMMM"
print "      MMMMZZZZZZZZZZZZZZZZ?==========,,,,,,,,,,,,,,,,,,,:,MMMMMMMM"
print "      MMMMZZZZZZZZZZZZZ?==========:,,,,,,,,,,,,,,,,,,,,,MMMMMMMMMM"
print "      MMMMMZZZZZZZZZ7,,,,=========,,,,,,,,,,,,,,,,,,,,,MMMMMMMMMMM"
print "      MMMMMMZZZZZ7??,,,,,,,=====,,,,,,,,,,,,,,,,,,,,,MMMMMMMMMMMMM"
print "      MMMMMMMZ$???????+,,,,,,==,,,,,,,,,,,,,,,,,,,MMMMMMMMMMMMMMMM"
print "      MMMMMMMMMMMMMMMMMMM,,,,,,,,,,,,,,,,,,,,,,MMMMMMMMMMMMMMMMMMM"
print "      MMMMMMMMMMMMMMMMMMMMMMMM,,,,,,,,,,,,MMMMMMMMMMMMMMMMMMMMMMMM"
print "      MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"

print ""
print " d888888b db   db  .d8b.  d8b   db db   dD   db    db  .d88b.  db    db"
print "  ~~88~~' 88   88 d8' `8b 888o  88 88 ,8P'   `8b  d8' .8P  Y8. 88    88"
print "    88    88ooo88 88ooo88 88V8o 88 88,8P      `8bd8'  88    88 88    88"
print "    88    88~~~88 88~~~88 88 V8o88 88`8b        88    88    88 88    88"
print "    88    88   88 88   88 88  V888 88 `88.      88    `8b  d8' 88b  d88"
print "    YP    YP   YP YP   YP VP   V8P YP   YD      YP     `Y88P'  ~Y8888P'"
