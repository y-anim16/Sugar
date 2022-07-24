import bpy

bl_info = {
    "name": "Berries",
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

class SetOriginToSelected(bpy.types.Operator):
    bl_idname = "object.set_origin_to_selected"
    bl_label = "SetOriginToSelected"
    bl_description = "選択対象を原点とします"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        
        #3Dカーソルはワールド原点に戻しておく
        bpy.ops.view3d.snap_cursor_to_center()

        return {'FINISHED'}

class AddShowHideKeyFrame(bpy.types.Operator):
    bl_idname = "object.add_show_hide_key_frame"
    bl_label = "AddShowHideKeyFrame"
    bl_description = "非アクティブ化するキーフレームを追加します"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        print('start')
        isHide = True
        # タイムライン上でキーが消えるのが困るので、viewport上では箱で表示
        displayType = 'BOUNDS'
        
        if bpy.context.object.hide_render:
            isHide = False
            displayType = 'TEXTURED'

        bpy.context.object.hide_render = isHide
        bpy.context.object.display_type = displayType
        # キーフレーム挿入
        bpy.context.object.keyframe_insert(data_path = 'hide_render')
        bpy.context.object.keyframe_insert(data_path = 'display_type')

        # 子オブジェクトも合わせて
        for c in bpy.context.object.children_recursive:
            c.hide_render = isHide
            c.display_type = displayType
            c.keyframe_insert(data_path = 'hide_render')
            c.keyframe_insert(data_path = 'display_type')
 
        print('finished')
        return {'FINISHED'}

#TODO Add new command class.
class NEW_COMMAND_CLASS(bpy.types.Operator):
    bl_idname = "object.new_command"
    bl_label = "NewCommand"
    bl_description = "NewCommandDescription"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        #TODO Add command.

        return {'FINISHED'}


class BerriesUi(bpy.types.Panel):
    bl_idname = "object.berries_ui"
    bl_label = "Berries"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Sugar"

    def draw(self, context):
        layout = self.layout
        
        if bpy.context.mode == 'EDIT_MESH':
            op_cls = SetOriginToSelected
            layout.operator(op_cls.bl_idname, text = "Set origin to selected")

        if bpy.context.mode == 'OBJECT':
            op_cls = AddShowHideKeyFrame
            layout.operator(op_cls.bl_idname, text = "Add Show/Hide key frame")

        #TODO ここで新しいコマンドのボタン登録
        #op_cls = NEW_CLASS_NAME
        #layout.operator(op_cls.bl_idname, text = "NEW_BUTTON_NAME")
        

classes = [
    SetOriginToSelected,
    AddShowHideKeyFrame,

    #TODO ここで新しく追加したコマンドクラスの登録
    #NEW_CLASS_NAME,

    BerriesUi
]

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()