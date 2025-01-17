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
    bl_description = "copy and paste vertex location"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):

        if len(bpy.context.selected_objects) <= 0:
            return {'FINISHED'}

        #一度編集モードを切らないと選択した頂点情報を取得できない
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle() #編集モードに戻す
        
        activeObj = bpy.context.active_object
        activeVWorldPositions = []
        for selectedV in [v for v in activeObj.data.vertices if v.select]:
            if activeObj.data.shape_keys == None or activeObj.active_shape_key.name == 'Basis':
                worldPos = activeObj.matrix_world @ selectedV.co
            else: # 移動先もシェイプキーによって変形している座標
                activeShapeKeyV = activeObj.active_shape_key.data[selectedV.index]
                worldPos = activeObj.matrix_world @ activeShapeKeyV.co
            activeVWorldPositions.append(worldPos)

        # 複数のメッシュ
        if len(bpy.context.selected_objects) > 1:
            for selectedObj in bpy.context.selected_objects:
                if selectedObj == activeObj:
                    continue
                bpy.ops.object.editmode_toggle()
                
                for i, selectedV in enumerate([v for v in selectedObj.data.vertices if v.select]):
                    if selectedObj.data.shape_keys == None:
                        localPos = selectedObj.matrix_world.inverted() @ activeVWorldPositions[0]
                        selectedV.co = [localPos[0], localPos[1], localPos[2]]
                    else:
                        if selectedObj.active_shape_key.name == 'Basis':
                            self.report({'ERROR'}, 'Active shape key is "Basis"')
                            return {'CANCELLED'}
                        if len(activeVWorldPositions) > 1:
                            # 必ずしも想定通りの向きになるとは限らないので適用させる頂点を変えられるようにする必要がある
                            localPos = selectedObj.matrix_world.inverted() @ activeVWorldPositions[i]
                        else:
                            localPos = selectedObj.matrix_world.inverted() @ activeVWorldPositions[0]
                        selectedObj.active_shape_key.data[selectedV.index].co = [localPos[0], localPos[1], localPos[2]]

                bpy.ops.object.editmode_toggle()

        # １つのメッシュ
        elif len(bpy.context.selected_objects) == 1:
            selectedVertices = [v for v in bpy.context.object.data.vertices if v.select]
            if len(selectedVertices) <= 1:
                return {'FINISHED'}

            # TODO: 選択順は関係ない
            firstSelectedIndex = selectedVertices[0].index
            lastSelectedPos = [selectedVertices[1].co[0], selectedVertices[1].co[1], selectedVertices[1].co[2]]
            bpy.ops.object.editmode_toggle()

            bpy.context.object.data.vertices[firstSelectedIndex].co = lastSelectedPos

            bpy.ops.object.editmode_toggle()

        return {'FINISHED'}    

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