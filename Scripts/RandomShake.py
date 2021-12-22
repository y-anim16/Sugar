import bpy

from random import randint

INTERVAL = 2
FRAME_COUNT = 3
RAND_MIN = -5
RAND_MAX = 5
FACTOR = 0.2

bl_info = {
    "name": "RandomShake",
    "author": "",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "",
    "description": "",
    "warning": "",
    "support": "TESTING",
    "doc_url": "",
    "tracker_url": "",
    "category": "Object"
}

addon_keymaps = []

class SetRandomShake(bpy.types.Operator):
    bl_idname = "object.random_shake"
    bl_label = "RandomShake"
    bl_description = "指定フレーム数だけランダムシェイクを行いキーを打ちます"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        active_obj = context.active_object
        oldLocation = [active_obj.location[0], active_obj.location[1], active_obj.location[2]]
        oldRotation = [active_obj.rotation_euler[0], active_obj.rotation_euler[1], active_obj.rotation_euler[2]]
        oldScale = [active_obj.scale[0], active_obj.scale[1], active_obj.scale[2]]
        currentFrame = bpy.context.scene.frame_current

        for i in range(0, FRAME_COUNT - 1):
            bpy.context.scene.frame_set(currentFrame)

            #get random value
            x = randint(RAND_MIN, RAND_MAX) * FACTOR
            y = randint(RAND_MIN, RAND_MAX) * FACTOR
            z = randint(RAND_MIN, RAND_MAX) * FACTOR

            #operate transform
            bpy.ops.transform.translate(value=(x, y, z))
            bpy.ops.transform.rotate(value=x, orient_axis='X')
            bpy.ops.transform.rotate(value=y, orient_axis='Y')
            bpy.ops.transform.rotate(value=z, orient_axis='Z')
            bpy.ops.transform.resize(value=(x, y, z))

            #insert keyframe (only active object)
            #TODO apply all selected object
            #TODO switchable on/off by checkbox?
            bpy.context.object.keyframe_insert(data_path="location", index=-1)
            bpy.context.object.keyframe_insert(data_path="rotation_euler", index=-1)
            bpy.context.object.keyframe_insert(data_path="scale", index=-1)

            currentFrame += INTERVAL

        bpy.context.scene.frame_set(currentFrame)
        active_obj.location = oldLocation
        active_obj.rotation_euler = oldRotation
        active_obj.scale = oldScale
        bpy.context.object.keyframe_insert(data_path="location", index=-1)
        bpy.context.object.keyframe_insert(data_path="rotation_euler", index=-1)
        bpy.context.object.keyframe_insert(data_path="scale", index=-1)
        return {'FINISHED'}

def menu_fn(self, context):
    self.layout.separator()
    self.layout.operator(SetRandomShake.bl_idname)

classes = [
    SetRandomShake,
]

def register_shortcut():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new(
            idname=SetRandomShake.bl_idname,
            type='I',
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
    bpy.types.VIEW3D_MT_mesh_add.append(menu_fn)
    register_shortcut()


def unregister():
    unregister_shortcut()
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_fn)
    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()