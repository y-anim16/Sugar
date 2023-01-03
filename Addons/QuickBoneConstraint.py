import bpy
from bpy.types import Menu

bl_info = {
    "name": "QuickBoneConstraint",
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

class CopyLocationBC(bpy.types.Operator):
    bl_idname = "object.copy_location_bc"
    bl_label = "CopyLocationBC"
    bl_description = "copy_location_bc"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selectedObj = bpy.context.active_object
        selectedBone = bpy.context.selected_pose_bones[0]
        bpy.ops.object.posemode_toggle()

        # Empty生成
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        
        # ボーンコンストレイント設定
        bpy.ops.object.constraint_add(type='COPY_LOCATION')
        bpy.context.object.constraints["Copy Location"].target = selectedObj
        bpy.context.object.constraints["Copy Location"].subtarget = selectedBone.name
        
        # Bake action (obj)
        frameStart = bpy.context.scene.frame_start
        frameEnd = bpy.context.scene.frame_end
        bpy.ops.nla.bake(frame_start=frameStart, frame_end=frameEnd, visual_keying=True, clear_constraints=True, bake_types={'OBJECT'})
        
        # Emptyを非選択にし、選択していたボーンをアクティブにする
        emptyObj = bpy.context.object
        emptyObj.select_set(False)
        selectedObj.select_set(True)
        bpy.context.view_layer.objects.active = selectedObj
        bpy.ops.object.posemode_toggle()

        # 選択していたボーンにBC設定
        bpy.ops.pose.constraint_add(type='COPY_LOCATION')
        selectedBone.constraints["Copy Location"].target = emptyObj

        # Bake action (bone)
        # bpy.ops.nla.bake(frame_start=frameStart, frame_end=frameEnd, visual_keying=True, clear_constraints=True, use_current_action=True, bake_types={'POSE'})

        # Emptyに選択を戻す
        bpy.ops.object.posemode_toggle()
        bpy.context.object.select_set(False)
        emptyObj.select_set(True)
        bpy.context.view_layer.objects.active = emptyObj

        # Cycle作成
        area = bpy.context.area
        old_type = area.type
        area.type = 'GRAPH_EDITOR'
        bpy.ops.graph.extrapolation_type(type='MAKE_CYCLIC')
        area.type = old_type

        # bpy.ops.object.delete(use_global=False, confirm=False)

        # 選択状態をもとに戻す
        # selectedObj.select_set(True)
        # bpy.context.view_layer.objects.active = selectedObj
        # bpy.ops.object.posemode_toggle()

        return {'FINISHED'}

class CopyRotationBC(bpy.types.Operator):
    bl_idname = "object.copy_rotation_bc"
    bl_label = "CopyRotationBC"
    bl_description = "copy_rotation_bc"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selectedObj = bpy.context.active_object
        selectedBone = bpy.context.selected_pose_bones[0]
        bpy.ops.object.posemode_toggle()

        # Empty生成
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        
        # ボーンコンストレイント設定
        bpy.ops.object.constraint_add(type='COPY_ROTATION')
        bpy.context.object.constraints["Copy Rotation"].target = selectedObj
        bpy.context.object.constraints["Copy Rotation"].subtarget = selectedBone.name
        
        # Bake action (obj)
        frameStart = bpy.context.scene.frame_start
        frameEnd = bpy.context.scene.frame_end
        bpy.ops.nla.bake(frame_start=frameStart, frame_end=frameEnd, visual_keying=True, clear_constraints=True, bake_types={'OBJECT'})
        
        # Emptyを非選択にし、選択していたボーンをアクティブにする
        emptyObj = bpy.context.object
        emptyObj.select_set(False)
        selectedObj.select_set(True)
        bpy.context.view_layer.objects.active = selectedObj
        bpy.ops.object.posemode_toggle()

        # 選択していたボーンにBC設定
        bpy.ops.pose.constraint_add(type='COPY_ROTATION')
        selectedBone.constraints["Copy Rotation"].target = emptyObj

        # Bake action (bone)
        # bpy.ops.nla.bake(frame_start=frameStart, frame_end=frameEnd, visual_keying=True, clear_constraints=True, use_current_action=True, bake_types={'POSE'})

        # Emptyに選択を戻す
        bpy.ops.object.posemode_toggle()
        bpy.context.object.select_set(False)
        emptyObj.select_set(True)
        bpy.context.view_layer.objects.active = emptyObj

        # Cycle作成
        area = bpy.context.area
        old_type = area.type
        area.type = 'GRAPH_EDITOR'
        bpy.ops.graph.extrapolation_type(type='MAKE_CYCLIC')
        area.type = old_type

        # bpy.ops.object.delete(use_global=False, confirm=False)

        # 選択状態をもとに戻す
        # selectedObj.select_set(True)
        # bpy.context.view_layer.objects.active = selectedObj
        # bpy.ops.object.posemode_toggle()

        return {'FINISHED'}

class QuickBC_PieMenu(Menu):
    bl_idname = "object.quick_bc_pie"
    bl_label = "quick_bc"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator("object.copy_location_bc", text = "CopyLocation")
        pie.operator("object.copy_rotation_bc", text = "CopyRotation")
        
class CallQuickBCPieMenu(bpy.types.Operator):
    bl_idname = "object.quick_bc_caller"
    bl_label = "quick_bc_pie_caller"

    def execute(self, context):
        selectedBonesCount = len(bpy.context.selected_pose_bones)
        if bpy.context.mode == 'POSE' and selectedBonesCount == 1:
            bpy.ops.wm.call_menu_pie(name="object.quick_bc_pie")
        return {'FINISHED'}

classes = {
    CopyLocationBC,
    CopyRotationBC,
    QuickBC_PieMenu,
    CallQuickBCPieMenu
}

def register_shortcut():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new(
            idname = CallQuickBCPieMenu.bl_idname,
            type = 'F7',
            value = 'PRESS',
            shift = False,
            ctrl = False,
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