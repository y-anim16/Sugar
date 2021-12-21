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

class SetRandomShake(bpy.types.Operator):
    bl_idname = "object.random_shake"
    bl_label = "RandomShake"
    bl_description = "ランダムシェイクを行いキーを打ちます"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        #bpy.ops.mesh.primitive_ico_sphere_add()
        #print("サンプル 2-1: ICO球を生成しました。")

        currentFrame = bpy.context.scene.frame_current

        for i in range(0, FRAME_COUNT):
            bpy.context.scene.frame_set(currentFrame)

            #get random value
            x = randint(RAND_MIN, RAND_MAX) * FACTOR
            y = randint(RAND_MIN, RAND_MAX) * FACTOR
            z = randint(RAND_MIN, RAND_MAX) * FACTOR

            #operate transform
            bpy.ops.transform.translate(value=(x, y, z))
            #TODO all axis
            bpy.ops.transform.rotate(value=1, orient_axis='Z')
            bpy.ops.transform.resize(value=(x, y, z))

            #insert keyframe (only active object)
            #TODO apply all selected object
            #TODO switchable on/off by checkbox?
            bpy.context.object.keyframe_insert(data_path="location", index=-1)
            bpy.context.object.keyframe_insert(data_path="rotation_euler", index=-1)
            bpy.context.object.keyframe_insert(data_path="scale", index=-1)

            currentFrame += INTERVAL

        return {'FINISHED'}

def menu_fn(self, context):
    self.layout.separator()
    self.layout.operator(SetRandomShake.bl_idname)

classes = [
    SetRandomShake,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_fn)
    print("サンプル 1-5: アドオン『サンプル 1-5』が有効化されました。")


def unregister():
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_fn)
    for c in classes:
        bpy.utils.unregister_class(c)
    print("サンプル 1-5: アドオン『サンプル 1-5』が無効化されました。")


if __name__ == "__main__":
    register()