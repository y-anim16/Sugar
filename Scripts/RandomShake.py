import bpy
from bpy.props import FloatProperty, BoolProperty, IntProperty

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

class RandomShakeUi(bpy.types.Panel):

    bl_label = "RandomShake"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Sugar"
    bl_context = "objectmode"

    @classmethod
    def poll(cls, context):
        #オブジェクトが選択されているときのみ表示
        for o in bpy.data.objects:
            if o.type == 'MESH' and o.select_get():
                return True
        return False

    def draw(self, context):
        sc = context.scene
        layout = self.layout
        # layout.operator(
        #     "hoge", text = "Insert Keys"
        # )

        layout.prop(sc, "FrameCount", text = "FrameCount")
        layout.prop(sc, "movement", text = "movement")
        layout.prop(sc, "InsertKey", text = "InsertKey")


def menu_fn(self, context):
    self.layout.separator()
    self.layout.operator(SetRandomShake.bl_idname)

def init_props():
    sc = bpy.types.Scene

    sc.movement = FloatProperty(
        name = "movement",
        description = "movement",
        default = 1.0,
        max = 5.0,
        min = -5.0
    )
    sc.FrameCount = IntProperty(
        name = "FrameCount",
        description = "FrameCount",
        default = 3,
        max = 9999,
        min = 1
    )
    sc.InsertKey = BoolProperty(
        name = "InsertKey",
        default = True
    )

def clear_props():
    sc = bpy.types.Scene

    del sc.movement

classes = [
    SetRandomShake,
    RandomShakeUi
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
    init_props()
    register_shortcut()

def unregister():
    unregister_shortcut()
    clear_props()
    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()