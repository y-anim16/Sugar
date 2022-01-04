import bpy
from bpy.props import (IntProperty)

bl_info = {
    "name": "ShowSilhouette",
    "author": "",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "",
    "description": "",
    "warning": "",
    "support": "TESTING",
    "doc_url": "",
    "tracker_url": "",
    "category": "Animation"
}

addon_keymaps = []

class ShowSilhouette(bpy.types.Operator):
    bl_idname = "object.show_silhouette"
    bl_label = "ShowSilhouette"
    bl_description = "指定フレーム数だけランダムシェイクを行いキーを打ちます"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.context.space_data.shading.light = 'FLAT'
        #bpy.ops.mesh.primitive_ico_sphere_add()
        print("サンプル 2-1: ICO球を生成しました。")

        return {'FINISHED'}

class ShowSilhouette2(bpy.types.Operator):
    bl_idname = "object.show_silhouette2"
    bl_label = "ShowSilhouette2"
    bl_description = "指定フレーム数だけランダムシェイクを行いキーを打ちます"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        #bpy.context.space_data.shading.light = 'FLAT'
        bpy.ops.mesh.primitive_ico_sphere_add()
        print("サンプル 2-1: ICO球を生成しました。")

        return {'FINISHED'}

class ShowSilhouetteUi(bpy.types.Panel):

    bl_idname = "object.show_silhouette"
    bl_label = "ShowSilhouette"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Sugar"

    def draw(self, context):
        op_cls = ShowSilhouette
        layout = self.layout
        layout.operator(op_cls.bl_idname, text = "ShowSilhouette")

classes = [
    ShowSilhouette,
    ShowSilhouette2,
    ShowSilhouetteUi
]

def register_shortcut():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new(
            idname = ShowSilhouette.bl_idname,
            type = 'F5',
            value = 'PRESS',
            shift = False,
            ctrl = False,
            alt = False
        )
        addon_keymaps.append((km,kmi))
        km2 = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi2 = km.keymap_items.new(
            idname = ShowSilhouette2.bl_idname,
            type = 'F5',
            value = 'RELEASE',
            shift = False,
            ctrl = False,
            alt = False
        )
        addon_keymaps.append((km2,kmi2))

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