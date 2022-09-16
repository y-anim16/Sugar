import bpy

bl_info = {
    "name": "ADDON_NAME",
    "author": "",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "",
    "description": "",
    "warning": "",
    "support": "TESTING",
    "doc_url": "",
    "tracker_url": "",
    "category": "All"
}

addon_keymaps = []

class FunctionName(bpy.types.Operator):
    bl_idname = "object.function_name"
    bl_label = "FunctionName"
    bl_description = ""
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        print('Hello world')
        return {'FINISHED'}

classes = [
    FunctionName,
]

def register_shortcut():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new(
            idname = FunctionName.bl_idname,
            type = 'G',
            value = 'PRESS',
            shift = True,
            ctrl = True,
            alt = False
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