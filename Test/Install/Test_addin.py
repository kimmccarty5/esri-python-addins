import arcpy
import pythonaddins
import os

class ToolClass2(object):
    """Implementation for custom_select_tool_addin.tool (Tool)"""
    def __init__(self):
        self.enabled = True
        self.shape = "Rectangle"
        #self.gdbPath = r'C:\temp\california.gdb'
        #self.txtPath = os.path.join(arcpy.env.scratchFolder,'california.txt')
        
    def onRectangle(self, rectangle_geometry):
        pass """
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
        """     


class ToolClass4(object):
    """Implementation for addin_addin.tool (Tool)"""
    def __init__(self):
        self.enabled = True
        self.shape = "Rectangle" 

    def onRectangle(self, rectangle_geometry):
        
        ext = rectangle_geometry  
        array = arcpy.Array()  
        array.add(arcpy.Point(ext.XMin, ext.YMin))  
        array.add(arcpy.Point(ext.XMin, ext.YMax))  
        array.add(arcpy.Point(ext.XMax, ext.YMax))  
        array.add(arcpy.Point(ext.XMax, ext.YMin))  
        array.add(arcpy.Point(ext.XMin, ext.YMin)) 
        sr = arcpy.SpatialReference(4326)
        polygon = arcpy.Polygon(array, sr)  
        arcpy.CopyFeatures_management(polygon, "in_memory//Polygon_Extent")  
        arcpy.MakeFeatureLayer_management("in_memory//Polygon_Extent", 'selectLyr')
        arcpy.MakeFeatureLayer_management('events', 'eventsLyr')
        
        arcpy.AddMessage(arcpy.GetCount_management('eventsLyr'))
        f = open(r'C:\Users\kim9578\Desktop\Cases\Addin\log.txt','a')
        n = arcpy.GetCount_management('eventsLyr')
        f.write(str(n) + '\n')
        f.close()
        
        arcpy.SelectLayerByLocation_management('eventsLyr', 'INTERSECT','selectLyr')
        n = arcpy.GetCount_management('eventsLyr')
        f = open(r'C:\Users\kim9578\Desktop\Cases\Addin\log.txt','a')
        f.write(str(n) + '\n')
        f.close()
        
        f = open(r'C:\Users\kim9578\Desktop\Cases\Addin\log.txt','a')
        f.write(ext.XMin, ext.YMin)
        f.close()
        
        arcpy.Delete_management("in_memory//Polygon_Extent")
        arcpy.Delete_management('selectLyr')
        arcpy.Delete_management('eventsLyr')