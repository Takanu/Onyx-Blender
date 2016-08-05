import bpy
from bpy.types import Operator
from .object_lib import ActivateObject, FocusObject, SelectObject
from .update import Update_ObjectOrigin, Update_ObjectVGOrigin

class BH_Update_Origin(Operator):
    """Updates the origin point based on each object's origin setting, for all selected objects"""

    bl_idname = "origin.update_origin"
    bl_label = ""

    def execute(self, context):
        print(self)

        atv = context.active_object
        sel = context.selected_objects

        for obj in sel:

            FocusObject(obj)
            Update_ObjectOrigin(obj, context)

        FocusObject(atv)
        Update_ObjectOrigin(atv, context)

        for obj in sel:
            SelectObject(obj)

        ActivateObject(atv)

        return {'FINISHED'}
