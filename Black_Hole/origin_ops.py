import bpy
from bpy.props import IntProperty, BoolProperty, FloatProperty, EnumProperty, PointerProperty, StringProperty, CollectionProperty
from bpy.types import Operator
from .object_lib import ActivateObject, FocusObject, SelectObject, RecordSelectedState, RestoreSelectedState


class BH_Origin_MeshBase(Operator):
    """Sets the origin to the base of the mesh in a local orientation."""

    bl_idname = "origin.mesh_base"
    bl_label = ""

    def execute(self, context):

        selRecord = RecordSelectedState(context)

        # Find all the selected objects in the scene
        sel = context.selected_objects
        for item in context.selected_objects:

            FocusObject(item)
            mode = ''
            mode = item.mode
            bpy.ops.object.mode_set(mode='OBJECT')

            # Enter the object!
            object_data = bpy.context.object.data
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action="DESELECT")
            bpy.ops.object.editmode_toggle()

            #Setup the correct tools to select vertices
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
            sel_mode = context.tool_settings.mesh_select_mode
            context.tool_settings.mesh_select_mode = [True, False, False]
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

            i = -1
            lowestZ = 0

            # First find the lowest Z value in the object
            for vertex in object_data.vertices:
                i += 1
                #print (i)

                # Used to define a reference point for the first vertex, in case 0 is
                # lower than any vertex on the model.
                if i == 0:
                    lowestZ = vertex.co.z

                else:
                    if vertex.co.z < lowestZ:
                        lowestZ = vertex.co.z

            # Now select all vertices with lowestZ

            for vertex in object_data.vertices:
                if vertex.co.z == lowestZ:
                    vertex.select = True
                    #print("Vertex Selected!")

            #Restore previous settings
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
            context.tool_settings.mesh_select_mode = sel_mode
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)


            # Saves the current cursor location
            cursor_loc = bpy.data.scenes[bpy.context.scene.name].cursor_location
            previous_cursor_loc = [cursor_loc[0], cursor_loc[1], cursor_loc[2]]

            # Snap the cursor
            bpy.ops.object.editmode_toggle()
            bpy.ops.view3D.snap_cursor_to_selected()
            bpy.ops.mesh.select_all(action="DESELECT")
            bpy.ops.object.editmode_toggle()

            # Set the origin
            FocusObject(item)
            bpy.ops.object.origin_set(type ='ORIGIN_CURSOR')

            # Restore the original cursor location
            bpy.data.scenes[bpy.context.scene.name].cursor_location = previous_cursor_loc

            # Set the object point type
            item.BHObj.origin_point = '1'

            bpy.ops.object.mode_set(mode=mode)

        RestoreSelectedState(selRecord)
        return {'FINISHED'}


class BH_Origin_MeshLowest(Operator):
    """Sets the origin to the lowest point of the mesh in a global orientation."""

    bl_idname = "origin.mesh_lowest"
    bl_label = ""

    def execute(self, context):
        selRecord = RecordSelectedState(context)

        # Find all the selected objects in the scene
        sel = context.selected_objects
        for item in context.selected_objects:

            FocusObject(item)
            mode = ''
            mode = item.mode
            bpy.ops.object.mode_set(mode='OBJECT')

            object_data = bpy.context.object.data
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action="DESELECT")
            bpy.ops.object.editmode_toggle()

            #Setup the correct tools to select vertices
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
            sel_mode = context.tool_settings.mesh_select_mode
            context.tool_settings.mesh_select_mode = [True, False, False]
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

            i = -1
            lowestZ = 0

            # First find the lowest Z value in the object
            for vertex in object_data.vertices:
                i += 1
                #print (i)

                # This code converts vertex coordinates from object space to world space.
                vertexWorld = item.matrix_world * vertex.co

                # Used to define a reference point for the first vertex, in case 0 is
                # lower than any vertex on the model.
                if i == 0:
                    lowestZ = vertexWorld.z

                else:
                    if vertexWorld.z < lowestZ:
                        lowestZ = vertexWorld.z

            # Now select all vertices with lowestZ

            for vertex in object_data.vertices:
                vertexWorld = item.matrix_world * vertex.co

                if vertexWorld.z == lowestZ:
                    vertex.select = True
                    #print("Vertex Selected!")

            #Restore previous settings
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
            context.tool_settings.mesh_select_mode = sel_mode
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)


            # Saves the current cursor location
            cursor_loc = bpy.data.scenes[bpy.context.scene.name].cursor_location
            previous_cursor_loc = [cursor_loc[0], cursor_loc[1], cursor_loc[2]]

            # Snap the cursor
            bpy.ops.object.editmode_toggle()
            bpy.ops.view3D.snap_cursor_to_selected()
            bpy.ops.mesh.select_all(action="DESELECT")
            bpy.ops.object.editmode_toggle()

            # Set the origin
            FocusObject(item)
            bpy.ops.object.origin_set(type ='ORIGIN_CURSOR')

            # Restore the original cursor location
            bpy.data.scenes[bpy.context.scene.name].cursor_location = previous_cursor_loc

            # Set the object point type
            item.BHObj.origin_point = '2'
            bpy.ops.object.mode_set(mode=mode)

        RestoreSelectedState(selRecord)
        return {'FINISHED'}

class BH_Origin_MeshCOM(Operator):
    """Sets the origin to the lowest point of the mesh in a global orientation."""

    bl_idname = "origin.mesh_centerofmass"
    bl_label = ""

    def execute(self, context):

        selRecord = RecordSelectedState(context)

        # Set the origin
        sel = context.selected_objects
        for item in context.selected_objects:

            FocusObject(item)
            mode = ''
            mode = item.mode
            bpy.ops.object.mode_set(mode='OBJECT')

            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            item.BHObj.origin_point = '3'
            bpy.ops.object.mode_set(mode=mode)

        RestoreSelectedState(selRecord)

        return {'FINISHED'}


class BH_OriginVertexGroup(Operator):
    """Sets the origin to the selected vertex group."""

    bl_idname = "origin.mesh_vgroup"
    bl_label = ""

    def execute(self, context):
        selRecord = RecordSelectedState(context)

        # Find all the selected objects in the scene
        sel = context.selected_objects
        for item in context.selected_objects:

            FocusObject(item)
            mode = ''
            mode = item.mode
            bpy.ops.object.mode_set(mode='OBJECT')

            object_data = bpy.context.object.data
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action="DESELECT")
            bpy.ops.object.editmode_toggle()

            #Setup the correct tools to select vertices
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
            sel_mode = context.tool_settings.mesh_select_mode
            context.tool_settings.mesh_select_mode = [True, False, False]
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

            index = int(bpy.context.active_object.BHObj.vertex_groups) - 1

            #Search through all vertices in the object to find the ones belonging to the
            #Selected vertex group
            for vertex in object_data.vertices:
                for group in vertex.groups:
                    if group.group == index:
                        vertex.select = True
                        #print("Vertex Selected!")

            #Restore previous settings
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
            context.tool_settings.mesh_select_mode = sel_mode
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)


            # Saves the current cursor location
            cursor_loc = bpy.data.scenes[bpy.context.scene.name].cursor_location
            previous_cursor_loc = [cursor_loc[0], cursor_loc[1], cursor_loc[2]]

            # Snap the cursor
            bpy.ops.object.editmode_toggle()
            bpy.ops.view3D.snap_cursor_to_selected()
            bpy.ops.mesh.select_all(action="DESELECT")
            bpy.ops.object.editmode_toggle()

            # Set the origin
            FocusObject(item)
            bpy.ops.object.origin_set(type ='ORIGIN_CURSOR')

            # Restore the original cursor location
            bpy.data.scenes[bpy.context.scene.name].cursor_location = previous_cursor_loc

            # Set the object point type
            item.BHObj.origin_point = '4'
            bpy.ops.object.mode_set(mode=mode)

        RestoreSelectedState(selRecord)
        return {'FINISHED'}

class BH_OriginCursor(Operator):
    """Sets the origin to the selected vertex group."""

    bl_idname = "origin.mesh_cursor"
    bl_label = ""

    def execute(self, context):

        # Set the origin
        sel = context.selected_objects
        for item in context.selected_objects:

            FocusObject(item)
            mode = ''
            mode = item.mode
            bpy.ops.object.mode_set(mode='OBJECT')

            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            item.BHObj.origin_point = '3'
            bpy.ops.object.mode_set(mode=mode)

        return {'FINISHED'}
