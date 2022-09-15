import bpy

from mathutils import Vector, Matrix

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
    bl_description = "copy and paste vertex location"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):

        #一度編集モードを切らないと選択した頂点情報を取得できない
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle() #編集モードに戻す


        # activeObj 最後に選択した奴
        # selected_object かつ activeObj ではないもの →　最初に選択したやつ
        # activeObj のところに、最初に選択した奴を持っていく

        print('activeObj' + str(bpy.context.active_object))
        print('selectedObj' + str(bpy.context.selected_objects))

        # active のindex がわかればよいかも
        # もしくはactive を取り除いたリスト

        # まず、selectedのなかでactiveのindexがいくつかを出す
        # active の頂点の座標をworldで出す

        activeObj = bpy.context.active_object
        activeObjVertices = []
        for selectedV in [v for v in activeObj.data.vertices if v.select]:
            vInfo = {}
            vInfo['vertex'] = selectedV
            vInfo['worldPos'] = activeObj.matrix_world @ selectedV.co
            activeObjVertices.append(vInfo)

            
        # selectedVertexes = []
        # for index, obj in enumerate(bpy.context.selected_objects):
        #     if index == activeObjIndex:
        #             continue

        #     for selectedV in [v for v in selectedObj.data.vertices if v.select]:
        #         vertexInfo = {}
        #         vertexInfo['vertex'] = selectedV
        #         selectedVertexes.append(vertexInfo)

        #print(selectedVertexes)
        #print(hoge[0].data.vertices[0].co)
        #print(hoge[1].data.vertices[2].co)

        #mat = selectedObjects[1].matrix_world
        #print(mat @ hoge[1].data.vertices[2].co)
        #//a = [v for v in hoge if v.select]
        #print(a)

        # for o in hoge:
        #     selected = [v for v in o if v.select]
        #     for s in selected:
        #         print(s)

        #selected が1種や同じObjの頂点が含まれるなら工夫が必要

        if len(bpy.context.selected_objects) > 1:
            for selectedObj in bpy.context.selected_objects:
                if selectedObj == activeObj:
                    continue

                localPos = selectedObj.matrix_world.inverted() @ activeObjVertices[0]['worldPos']
                bpy.ops.object.editmode_toggle()
                
                for selectedV in [v for v in selectedObj.data.vertices if v.select]:
                    selectedV.co = [localPos[0], localPos[1], localPos[2]]

                bpy.ops.object.editmode_toggle()

        # if len(selectedVertexes) > 1:
        #     # for ループで回す
        #     selectedVIndex = selectedVertexes[0]['vertex'].index
        #     # world座標にしていたのを対象のオブジェクトのlocal座標に直す
        #     #localPos = bpy.context.selected_objects[0].matrix_world.inverted() @ selectedVertexes[1]['worldPos']
        #     #それぞれのローカルに置き換える
        #     localPos = bpy.context.active_object.matrix_world.inverted() @ selectedVertexes[1]['worldPos']
        #     lastSelectedVPos = [localPos[0], localPos[1], localPos[2]]
        #     bpy.ops.object.editmode_toggle()

        #     #bpy.context.selected_objects[0].data.vertices[selectedVIndex].co = lastSelectedVPos
        #     #ここで変えるのはactiveObject 以外の選択ObjVertex
        #     bpy.context.active_object.data.vertices[selectedVIndex].co = lastSelectedVPos

        #     bpy.ops.object.editmode_toggle()


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