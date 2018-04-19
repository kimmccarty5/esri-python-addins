import arcpy
import os
import pythonaddins

class ToolClass2(object):
    """Implementation for custom_select_tool_addin.tool (Tool)"""
    def __init__(self):
        self.enabled = True
        self.shape = "Rectangle"
        #self.gdbPath = r'C:\temp\california.gdb'
        self.txtPath = os.path.join(arcpy.env.scratchFolder,'california.txt')
        
    def onRectangle(self, rectangle_geometry):
        #pythonaddins.MessageBox(type(rectangle_geometry), 'debug', 0)
        
        polygon = rectangle_geometry.polygon

        mxd = arcpy.mapping.MapDocument("CURRENT")
        layer = arcpy.mapping.ListLayers(mxd)[0]
        # copy the polygon into an in-memory dataset     

        #get the total # of records in the table
        count = arcpy.GetCount_management(layer).getOutput(0)

        # Record the total # of records to the text file
        pythonaddins.MessageBox('The eventsLayer has %s records' % count, 'Count', 0)

        with open(self.txtPath, 'a') as writer:
            writer.write('table has %s records.\n' % count)

        #select the record that intersect with the rectangle geometry
        selection = arcpy.SelectLayerByLocation_management(in_layer=layer, 
            overlap_type='INTERSECT', select_features=polygon, selection_type='NEW_SELECTION')

        # get the total # of records selected
        count = arcpy.GetCount_management(selection).getOutput(0)
        
        #write to the text file the # of selected features in each polygon
        with open(self.txtPath, 'a') as writer:
            writer.write('You selected %s records.\n' % count)
            writer.write('The polygon used was %s.\n' % polygon.JSON)

        # clean up the variables
        for item in ['in_memory']:
            arcpy.Delete_management(item)

        # say where text file can be found
        pythonaddins.MessageBox('Text file is @ %s.' % self.txtPath, 'Count', 0)

