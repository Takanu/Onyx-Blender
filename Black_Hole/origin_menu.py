import bpy
from bpy.types import Menu

class PieSculptMaskStandard(Menu):
    bl_idname = "pie.originextra"
    bl_label = "Mask Tools"

    def draw(self, context):
        print("Drawing Pie")
        layout = self.layout
        pie = layout.menu_pie()
        # 4 - LEFT
        pie.operator("origin.mesh_base", text="To Mesh Base")
        # 6 - RIGHT
        pie.operator("origin.mesh_centerofmass", text="To Center of Mass")
        # 2 - BOTTOM
        pie.operator("origin.update_origin", text="Update Origins")
        # 8 - TOP
        pie.operator("origin.mesh_vgroup", text="To Vertex Group")
        # 7 - TOP - LEFT
        pie.operator("origin.mesh_cursor", text="To 3D Cursor")
        # 1 - BOTTOM - LEFT
        pie.operator("origin.mesh_lowest", text="To Mesh Lowest")
        # 9 - TOP - RIGHT
        #pie.operator("paint.mask_lasso_gesture", text="Lasso Mask", icon="BORDER_LASSO")
        # 3 - BOTTOM - RIGHT
        #pie.operator("wm.call_menu_pie", text="Replace Mask with Group", icon="MOD_MASK").name = "pie.maskfromgroup"
