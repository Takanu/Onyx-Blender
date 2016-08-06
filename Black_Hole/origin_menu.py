import bpy
from bpy.types import Menu

class PieOriginVGroup(Menu):
    bl_idname = "pie.originvgroup"
    bl_label = "Select Mask"

    def draw(self, context):
        print("Drawing Pie")
        layout = self.layout
        pie = layout.menu_pie()

        ob = context.object
        group = ob.vertex_groups.active
        i = 0

        if ob:
            for group in ob.vertex_groups:
                if i > 7:
                    break
                pie.operator("origin.mesh_vgroup", text=group.name, icon="GROUP_VERTEX").index = i
                i += 1

class PieOriginStandard(Menu):
    bl_idname = "pie.originextra"
    bl_label = "Mask Tools"

    def draw(self, context):
        print("Drawing Pie")
        layout = self.layout
        pie = layout.menu_pie()
        # 4 - LEFT
        pie.operator("origin.mesh_base", text="To Mesh Base", icon="CURSOR")
        # 6 - RIGHT
        pie.operator("origin.mesh_centerofmass", text="To Center of Mass", icon="CURSOR")
        # 2 - BOTTOM
        pie.operator("origin.update_origin", text="Update Origins", icon="ROTATE")
        # 8 - TOP
        pie.operator("wm.call_menu_pie", text="To Vertex Group", icon="GROUP_VERTEX").name = "pie.originvgroup"
        # 7 - TOP - LEFT
        pie.operator("origin.mesh_cursor", text="To 3D Cursor", icon="CURSOR")
        # 1 - BOTTOM - LEFT
        pie.operator("origin.mesh_lowest", text="To Mesh Lowest", icon="CURSOR")
        # 9 - TOP - RIGHT
        #pie.operator("paint.mask_lasso_gesture", text="Lasso Mask", icon="BORDER_LASSO")
        # 3 - BOTTOM - RIGHT
        #pie.operator("wm.call_menu_pie", text="Replace Mask with Group", icon="MOD_MASK").name = "pie.maskfromgroup"
