import arcpy

# Author: James Stephaniuk
# October 19, 2015
#
# Populates and aligns a graphic box with data from an shapefile attribute table.

mxd = arcpy.mapping.MapDocument("CURRENT")
# Feature class name.
mapLyr = arcpy.mapping.ListLayers(mxd,"PUT_NAME_OF_LAYER_WITH_SVA_INFO_HERE")[0]

# SVA container (graphic box) name. Match this name to the SVA Box element name in ArcMap.
svaBox = "svaBox"

# Graphic box layout settings.
padding = 0.2 # Distance (in inches) around edge of box to inner elements.
spacer = 0.1  # Distance (in inches) between inner elements.

# SVA source feature class field names. Add the field names from the layer that you want to populate the SVA Table.
svaTxtField  = "FIELD_NAME"
facilityName = "FIELD_NAME"
addrNo       = "FIELD_NAME"
addrName     = "FIELD_NAME"
city         = "FIELD_NAME"

# SVA text element names. Match these names to the element names in ArcMap.
SVATitleText  = "SVATitle"
svaTitleElem0 = "SVA_TitleElem0"
svaTitleElem1 = "SVA_TitleElem1"
svaTitleElem2 = "SVA_TitleElem2"
svaTitleElem3 = "SVA_TitleElem3"
svaTxtElem0   = "SVA_textElem0"
svaTxtElem1   = "SVA_textElem1"
svaTxtElem2   = "SVA_textElem2"
svaTxtElem3   = "SVA_textElem3"

mainTitle     = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", SVATitleText)[0]
svaTitle      = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTitleElem0)[0]
facTitle      = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTitleElem1)[0]
addrTitle     = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTitleElem2)[0]
cityTitle     = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTitleElem3)[0]
svaTxtElem    = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTxtElem0)[0]
facTxtElem    = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTxtElem1)[0]
addrTxtElem   = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTxtElem2)[0]
cityTxtElem   = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", svaTxtElem3)[0]

elemLst = [svaTxtElem, facTxtElem, addrTxtElem, cityTxtElem]

# Captions cannot be empty therefore a single char. Set all font sizes to same.
for elem in elemLst:
	elem.text = " "

# Populate columns.
rows = arcpy.SearchCursor(mapLyr.dataSource)
for row in rows:
	svaTxtElem.text  += "{}\n".format(row.getValue(svaTxtField))
	facTxtElem.text  += "{}\n".format(row.getValue(facilityName))
	addrTxtElem.text += "{} ".format(row.getValue(addrNo))
	addrTxtElem.text += "{}\n".format(row.getValue(addrName))
	cityTxtElem.text += "{}\n".format(row.getValue(city))

# Slice off leading space char.
for elem in elemLst:
	elem.text = elem.text[1:]

svaBox = arcpy.mapping.ListLayoutElements(mxd, "GRAPHIC_ELEMENT", svaBox)[0]

# Position main title elem.
mainTitle.elementPositionX = svaBox.elementPositionX + padding
mainTitle.elementPositionY = svaBox.elementPositionY - padding

# Position the titles and text elements relative to main title and each other.
# Col 1
widthCol1 = max(svaTitle.elementWidth, svaTxtElem.elementWidth) 
svaTitle.elementPositionX = svaTxtElem.elementPositionX = mainTitle.elementPositionX
svaTitle.elementPositionY = mainTitle.elementPositionY - svaTitle.elementHeight - padding # Uses padding instead of spacer to give main title more room.
svaTxtElem.elementPositionY = svaTitle.elementPositionY - svaTitle.elementHeight
# Col 2
widthCol2 = max(facTitle.elementWidth, facTxtElem.elementWidth)
facTitle.elementPositionY = svaTitle.elementPositionY
facTxtElem.elementPositionY = svaTxtElem.elementPositionY
facTitle.elementPositionX = svaTitle.elementPositionX + widthCol1 + spacer
facTxtElem.elementPositionX = svaTxtElem.elementPositionX + widthCol1 + spacer
# Col 3
widthCol3 = max(addrTitle.elementWidth, addrTxtElem.elementWidth)
addrTitle.elementPositionY = facTitle.elementPositionY
addrTxtElem.elementPositionY = facTxtElem.elementPositionY
addrTitle.elementPositionX = facTitle.elementPositionX + widthCol2 + spacer
addrTxtElem.elementPositionX = facTxtElem.elementPositionX + widthCol2 + spacer
# Col 4
widthCol4 = max(cityTitle.elementWidth, cityTxtElem.elementWidth)
cityTitle.elementPositionY = addrTitle.elementPositionY
cityTxtElem.elementPositionY = addrTxtElem.elementPositionY
cityTitle.elementPositionX = addrTitle.elementPositionX + widthCol3 + spacer
cityTxtElem.elementPositionX = addrTxtElem.elementPositionX + widthCol3 + spacer

# Set the svaBox height and width derived from text elements heights and widths.
tallestTxtElem = max(svaTxtElem.elementHeight, facTxtElem.elementHeight, addrTxtElem.elementHeight, cityTxtElem.elementHeight)
tallestTitleElem = max(svaTitle.elementHeight, facTitle.elementHeight, addrTitle.elementHeight, cityTitle.elementHeight)
colsWidths = widthCol1 + widthCol2 + widthCol3 + widthCol4
textWidth = colsWidths + (spacer * 3)
svaBox.elementHeight = tallestTxtElem + tallestTitleElem + mainTitle.elementHeight + (padding * 2)
svaBox.elementWidth = max(textWidth, mainTitle.elementWidth) + (padding * 2)