import bpy

bl_info = {
    "name": "VertexCopyPaste",
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

class CopyAndPasteVertex(bpy.types.Operator):
    bl_idname = "object.copy_and_paste_vertex"
    bl_label = "CopyAndPasteVertex"
    bl_description = ""
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):

        #一度編集モードを切らないと選択した頂点情報を取得できない
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle() #編集モードに戻す

        selectedVertexes = [v for v in bpy.context.object.data.vertices if v.select]
        if len(selectedVertexes) > 0:
            print(selectedVertexes[0].co)

        return {'FINISHED'}


# class BerriesUi(bpy.types.Panel):
#     bl_idname = "object.berries_ui"
#     bl_label = "Berries"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = "Sugar"

#     def draw(self, context):
#         layout = self.layout
        
#         if bpy.context.mode == 'EDIT_MESH':
#             op_cls = SetOriginToSelected
#             layout.operator(op_cls.bl_idname, text = "Set origin to selected")

#         if bpy.context.mode == 'OBJECT':
#             op_cls = AddShowHideKeyFrame
#             layout.operator(op_cls.bl_idname, text = "Add Show/Hide key frame")

#         #TODO ここで新しいコマンドのボタン登録
#         #op_cls = NEW_CLASS_NAME
#         #layout.operator(op_cls.bl_idname, text = "NEW_BUTTON_NAME")
        

classes = [
    CopyAndPasteVertex,
]

def register_shortcut():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new(
            idname = CopyAndPasteVertex.bl_idname,
            type = 'X',
            value = 'PRESS',
            shift = True,
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