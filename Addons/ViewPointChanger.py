import bpy
from bpy.types import Menu

bl_info = {
    "name": "ViewPointChanger",
    "author": "",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "",
    "description": "",
    "warning": "",
    "support": "TESTING",
    "doc_url": "",
    "tracker_url": "",
    "category": "3D View"
}

addon_keymaps = []

class ChangeViewPointLeft(bpy.types.Operator):
    bl_idname = "object.change_view_point_left"
    bl_label = "ChangeViewPointLeft"
    bl_description = "Change to left"

    def execute(self, context):
        bpy.ops.view3d.view_axis(type='LEFT')
        return {'FINISHED'}

class ChangeViewPointRight(bpy.types.Operator):
    bl_idname = "object.change_view_point_right"
    bl_label = "ChangeViewPointRight"
    bl_description = "Change to right"

    def execute(self, context):
        bpy.ops.view3d.view_axis(type='RIGHT')
        return {'FINISHED'}

class ChangeViewPointFront(bpy.types.Operator):
    bl_idname = "object.change_view_point_front"
    bl_label = "ChangeViewPointFront"
    bl_description = "Change to front"

    def execute(self, context):
        bpy.ops.view3d.view_axis(type='FRONT')
        return {'FINISHED'}

class ChangeViewPointBack(bpy.types.Operator):
    bl_idname = "object.change_view_point_back"
    bl_label = "ChangeViewPointBack"
    bl_description = "Change to back"

    def execute(self, context):
        bpy.ops.view3d.view_axis(type='BACK')
        return {'FINISHED'}

class ChangeViewPointTop(bpy.types.Operator):
    bl_idname = "object.change_view_point_top"
    bl_label = "ChangeViewPointTop"
    bl_description = "Change to top"

    def execute(self, context):
        bpy.ops.view3d.view_axis(type='TOP')
        return {'FINISHED'}

class ChangeViewPointBottom(bpy.types.Operator):
    bl_idname = "object.change_view_point_bottom"
    bl_label = "ChangeViewPointBottom"
    bl_description = "Change to bottom"

    def execute(self, context):
        bpy.ops.view3d.view_axis(type='BOTTOM')
        return {'FINISHED'}

class ViewPointChange_PieMenu(Menu):
    bl_idname = "object.view_point_change_pie"
    bl_label = "change_view_point"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator("object.change_view_point_left", text = "Left")
        pie.operator("object.change_view_point_right", text = "Right")
        pie.operator("object.change_view_point_front", text = "Front")
        pie.operator("object.change_view_point_back", text = "Back")
        pie.operator("object.change_view_point_top", text = "Top")
        pie.operator("object.change_view_point_bottom", text = "Bottom")
        
class CallViewPointChangePieMenu(bpy.types.Operator):
    bl_idname = "object.view_point_change_caller"
    bl_label = "pie_menu_caller"

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name="object.view_point_change_pie")
        return {'FINISHED'}

classes = {
    ChangeViewPointLeft,
    ChangeViewPointRight,
    ChangeViewPointFront,
    ChangeViewPointBack,
    ChangeViewPointTop,
    ChangeViewPointBottom,
    ViewPointChange_PieMenu,
    CallViewPointChangePieMenu
}

def register_shortcut():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new(
            idname = CallViewPointChangePieMenu.bl_idname,
            type = 'V',
            value = 'PRESS',
            shift = False,
            ctrl = False,
            alt = True
        )
        addon_keymaps.append((km,kmi))

def unregister_shortcut():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

def register():
    for c in classes:
        bpy.utils.register_class(c)
    register_shortcut()

def unregister():
    unregister_shortcut()
    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()