import bpy
from bpy.props import (
    IntProperty,
    FloatVectorProperty,
    BoolVectorProperty)
from random import randint

INTERVAL = 2
FRAME_COUNT = 3
RAND_MIN = -5
RAND_MAX = 5
CONVERT_INT_FACTOR = 1000
UNDO_FLAOT_FACTOR = 0.001
ValueX = 0
ValueY = 1
ValueZ = 2

bl_info = {
    "name": "RandomShake",
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

class SetRandomShake(bpy.types.Operator):
    bl_idname = "object.random_shake"
    bl_label = "RandomShake"
    bl_description = "指定フレーム数だけランダムシェイクを行いキーを打ちます"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        sc = context.scene

        insertableMoveAxes = self.Insertable(sc.InsertableMoveAxes)
        insertableRotateAxes = self.Insertable(sc.InsertableRotateAxes)
        insertableResizeAxes = self.Insertable(sc.InsertableResizeAxes)

        active_obj = context.active_object
        oldLocation = [active_obj.location[ValueX], active_obj.location[ValueY], active_obj.location[ValueZ]]
        oldRotation = [active_obj.rotation_euler[ValueX], active_obj.rotation_euler[ValueY], active_obj.rotation_euler[ValueZ]]
        oldScale = [active_obj.scale[ValueX], active_obj.scale[ValueY], active_obj.scale[ValueZ]]
        currentFrame = bpy.context.scene.frame_current

        for i in range(0, sc.FrameCount - 1):
            bpy.context.scene.frame_set(currentFrame)

            #TODO apply all selected object

            #operate transform
            if insertableMoveAxes:
                movement = self.GetRandomValues(sc.InsertableMoveAxes, sc.MovementMinMax)
                bpy.ops.transform.translate(value = (movement[ValueX], movement[ValueY], movement[ValueZ]))
                self.InsertKeys(sc.InsertableMoveAxes, "location")

            if insertableRotateAxes:
                rotation = self.GetRandomValues(sc.InsertableRotateAxes, sc.RotationMinMax)
                bpy.ops.transform.rotate(value = rotation[ValueX], orient_axis = 'X')
                bpy.ops.transform.rotate(value = rotation[ValueY], orient_axis = 'Y')
                bpy.ops.transform.rotate(value = rotation[ValueZ], orient_axis = 'Z')
                self.InsertKeys(sc.InsertableRotateAxes, "rotation_euler")

            if insertableResizeAxes:
                scale = self.GetRandomValues(sc.InsertableResizeAxes, sc.ScaleMinMax)
                bpy.ops.transform.resize(value = (scale[ValueX], scale[ValueY], scale[ValueZ]))
                self.InsertKeys(sc.InsertableResizeAxes, "scale")

            currentFrame += sc.Interval

        bpy.context.scene.frame_set(currentFrame)
        
        if insertableMoveAxes:
            active_obj.location = oldLocation
            self.InsertKeys(sc.InsertableMoveAxes, "location")

        if insertableRotateAxes:
            active_obj.rotation_euler = oldRotation
            self.InsertKeys(sc.InsertableRotateAxes, "rotation_euler")
        
        if insertableResizeAxes:
            active_obj.scale = oldScale
            self.InsertKeys(sc.InsertableResizeAxes, "scale")
        return {'FINISHED'}
    
    def Insertable(self, insertableAxes):
        for insertable in insertableAxes:
            if (insertable):
                return True
        return False
    
    def GetRandomValues(self, insertableAxes, randomRange):
        randomValues = [0, 0, 0]
        
        minConvertedInt = int(randomRange[0] * CONVERT_INT_FACTOR)
        maxConvertedInt = int(randomRange[1] * CONVERT_INT_FACTOR)
        
        for index, randomValue in enumerate(randomValues):
            if insertableAxes[index]:
                randomValues[index] = randint(minConvertedInt, maxConvertedInt) * UNDO_FLAOT_FACTOR
            else:
                randomValues[index] = 0
        return randomValues
    
    def InsertKeys(self, insertableAxes, dataPath):
        if insertableAxes[ValueX] and insertableAxes[ValueY] and insertableAxes[ValueZ]:
            bpy.context.object.keyframe_insert(data_path = dataPath)
            return

        if insertableAxes[ValueX]:
            bpy.context.object.keyframe_insert(data_path = dataPath, index = 0)
        if insertableAxes[ValueY]:
            bpy.context.object.keyframe_insert(data_path = dataPath, index = 1)
        if insertableAxes[ValueZ]:
            bpy.context.object.keyframe_insert(data_path = dataPath, index = 2)

class RandomShakeUi(bpy.types.Panel):

    bl_idname = "object.random_shake_ui"
    bl_label = "RandomShake"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Sugar"
    bl_context = "objectmode"

    def draw(self, context):
        op_cls = SetRandomShake
        sc = context.scene
        layout = self.layout
        layout.operator(op_cls.bl_idname, text = "Shake", icon = 'PLUS')
        layout.prop(sc, "FrameCount", text = "Frame Count")
        layout.prop(sc, "Interval", text = "Interval")

class MovePanelUi(bpy.types.Panel):
    
    bl_idname = "object.move_panel_ui"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Movement"
    bl_category = "Sugar"
    bl_parent_id = "object.random_shake_ui"

    def draw(self, context):
        sc = context.scene
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        flow = layout.grid_flow(row_major=True, columns=0, even_columns=False, even_rows=False, align=False)
        col = flow.column()

        subcol = col.column()
        subcol.prop(sc, "MovementMinMax", text = "Min/Max")
        subcol.prop(sc, "InsertableMoveAxes", text = "Enable key insertable axis")

class RotationPanelUi(bpy.types.Panel):
    
    bl_idname = "object.rotation_panel_ui"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Rotation"
    bl_category = "Sugar"
    bl_parent_id = "object.random_shake_ui"

    def draw(self, context):
        sc = context.scene
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        flow = layout.grid_flow(row_major=True, columns=0, even_columns=False, even_rows=False, align=False)
        col = flow.column()

        subcol = col.column()
        subcol.prop(sc, "RotationMinMax", text = "Min/Max")
        subcol.prop(sc, "InsertableRotateAxes", text = "Enable key insertable axis")

class ScalePanelUi(bpy.types.Panel):
    
    bl_idname = "object.scale_panel_ui"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Scale"
    bl_category = "Sugar"
    bl_parent_id = "object.random_shake_ui"

    def draw(self, context):
        sc = context.scene
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        flow = layout.grid_flow(row_major=True, columns=0, even_columns=False, even_rows=False, align=False)
        col = flow.column()

        subcol = col.column()
        subcol.prop(sc, "ScaleMinMax", text = "Min/Max")
        subcol.prop(sc, "InsertableResizeAxes", text = "Enable key insertable axis")


def menu_fn(self, context):
    self.layout.separator()
    self.layout.operator(SetRandomShake.bl_idname)

def init_props():
    sc = bpy.types.Scene

    sc.FrameCount = IntProperty(
        name = "FrameCount",
        description = "FrameCount",
        default = 3,
        max = 9999,
        min = 1
    )
    sc.Interval = IntProperty(
        name = "Interval",
        description = "Interval",
        default = 1,
        max = 99,
        min = 0
    )
    sc.MovementMinMax = FloatVectorProperty(
        name = "MovementMinMax",
        description = "MovementMinMax",
        default = (-1.0, 1.0),
        size = 2,
        max = 5.0,
        min = -5.0
    )
    sc.InsertableMoveAxes = BoolVectorProperty(
        name = "InsertableMoveAxes",
        default = (True, True, True),
        subtype = 'XYZ',
    )
    sc.RotationMinMax = FloatVectorProperty(
        name = "RotationMinMax",
        description = "RotationMinMax",
        default = (-1.0, 1.0),
        size = 2,
        max = 5.0,
        min = -5.0
    )
    sc.InsertableRotateAxes = BoolVectorProperty(
        name = "InsertableRotateAxes",
        default = (True, True, True),
        subtype = 'XYZ',
    )
    sc.ScaleMinMax = FloatVectorProperty(
        name = "ScaleMinMax",
        description = "ScaleMinMax",
        default = (-1.0, 1.0),
        size = 2,
        max = 5.0,
        min = -5.0
    )
    sc.InsertableResizeAxes = BoolVectorProperty(
        name = "InsertableResizeAxes",
        default = (True, True, True),
        subtype = 'XYZ',
    )

def clear_props():
    sc = bpy.types.Scene

    del sc.FrameCount
    del sc.Interval
    del sc.MovementMinMax
    del sc.InsertableMoveAxes
    del sc.RotationMinMax
    del sc.InsertableRotateAxes
    del sc.ScaleMinMax
    del sc.InsertableResizeAxes

classes = [
    SetRandomShake,
    RandomShakeUi,
    MovePanelUi,
    RotationPanelUi,
    ScalePanelUi
]

def register_shortcut():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new(
            idname = SetRandomShake.bl_idname,
            type = 'I',
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