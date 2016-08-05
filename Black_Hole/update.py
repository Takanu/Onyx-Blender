import bpy
from .object_lib import ActivateObject, FocusObject, SelectObject, RecordSelectedState, RestoreSelectedState

#//////////////////////////////// - UPDATES - ///////////////////////////
def Update_ObjectOrigin(self, context):

    return

    if sel.BHObj.update_toggle is False:
        SetMeshOrigin(newInt)

    return None

def Update_ObjectVGOrigin(self, context):

    return

    # Create an array to store all found objects
    objects_to_select = []
    objects_to_make_active = []

    print("Rawr?")

    # Store the active object
    objects_to_make_active.append(bpy.context.active_object)

    # Find all the selected objects in the scene and store them
    for object in context.selected_objects:
        objects_to_select.append(object)

    # Focus on the object with the newly selected vertex group
    FocusObject(bpy.context.active_object.object)

    # Get the origin point and call the respective def
    newEnum = int(self.origin_point)
    VGSelect = int(bpy.context.active_object.BHObj.vertex_groups)

    # If the index isnt one (which is the None selection), change the origin!)
    if VGSelect != 1:
        SetMeshOrigin(newEnum)

    bpy.ops.object.select_all(action='DESELECT')

    # Re-select all stored objects
    for objectSelect in objects_to_select:
        bpy.ops.object.select_pattern(pattern=objectSelect.name)

    for objectActive in objects_to_make_active:
        bpy.ops.object.select_pattern(pattern=objectActive.name)
        bpy.context.scene.objects.active = objectActive

    return None

def SetMeshOrigin(newInt):

    # Base
    if newInt == 1:
        bpy.ops.origin.mesh_base()
    # Lowest
    if newInt == 2:
        bpy.ops.origin.mesh_lowest()
    # COM
    if newInt == 3:
        bpy.ops.origin.mesh_centreofmass()
    # Vertex Group
    if newInt == 4:
        bpy.ops.origin.mesh_vgroup()
    # Cursor
    if newInt == 5:
        bpy.ops.origin.mesh_cursor()
