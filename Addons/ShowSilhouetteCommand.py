import bpy
from bpy.props import (BoolProperty, EnumProperty, IntProperty, PointerProperty)

bl_info = {
    "name": "ShowSilhouette",
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
ViewPortLight = 'STUDIO'
ShadingColorType = 'MATERIAL'
ShadingSingleColor = (0.799338, 0.799338, 0.799338)
ViewBackGround = 'MATCAP'
ViewBackColor = (0.050, 0.050, 0.050) #これはグローバルじゃなくても良さそうな
ShowBackfaceCulling = False
ShowXray = False
ShowShadows = False
ShowCavity = False
UseDof = False
ShowObjectOutline = True

class MOI_Properties(bpy.types.PropertyGroup):
    pressing = BoolProperty(
        name="一定間隔でオブジェクト移動中",
        description="一定間隔でオブジェクト移動中か？",
        default=False
    )

class ShowSilhouette(bpy.types.Operator):
    bl_idname = "object.show_silhouette"
    bl_label = "ShowSilhouette"
    bl_description = "指定フレーム数だけランダムシェイクを行いキーを打ちます"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        sc = context.scene
        props = sc.moi_props
        if props.pressing:
            return {'CANCELLED'}
        else :
            props.pressing = True
            global ViewPortLight
            global ShadingColorType
            global ShadingSingleColor
            global ViewBackGround
            global ViewBackColor

            global ShowBackfaceCulling
            global ShowXray
            global ShowShadows
            global ShowCavity
            global UseDof
            global ShowObjectOutline
            
            ViewPortLight = bpy.context.space_data.shading.light
            ShadingColorType = bpy.context.space_data.shading.color_type
            ShadingSingleColor = bpy.context.space_data.shading.single_color
            ViewBackGround = bpy.context.space_data.shading.background_type
            ViewBackColor = bpy.context.space_data.shading.background_color

            ShowBackfaceCulling = bpy.context.space_data.shading.show_backface_culling
            ShowXray = bpy.context.space_data.shading.show_xray
            ShowShadows = bpy.context.space_data.shading.show_shadows
            ShowCavity = bpy.context.space_data.shading.show_cavity
            UseDof = bpy.context.space_data.shading.use_dof
            ShowObjectOutline = bpy.context.space_data.shading.show_object_outline

            #色が元に戻らない
            bpy.context.space_data.shading.light = 'FLAT'
            bpy.context.space_data.shading.color_type = 'SINGLE'
            bpy.context.space_data.shading.single_color = (0, 0, 0)
            bpy.context.space_data.shading.background_type = 'VIEWPORT'
            bpy.context.space_data.shading.background_color = (1, 1, 1)

            bpy.context.space_data.shading.show_backface_culling = False
            bpy.context.space_data.shading.show_xray = False
            bpy.context.space_data.shading.show_shadows = False
            bpy.context.space_data.shading.show_cavity = False
            bpy.context.space_data.shading.use_dof = False
            bpy.context.space_data.shading.show_object_outline = False
            #ポーズモードじゃないとき死ぬ
            bpy.ops.pose.hide(unselected=True)
            bpy.ops.pose.hide(unselected=False)
            return {'FINISHED'}

class ShowSilhouette2(bpy.types.Operator):
    bl_idname = "object.show_silhouette2"
    bl_label = "ShowSilhouette2"
    bl_description = "指定フレーム数だけランダムシェイクを行いキーを打ちます"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        sc = context.scene
        props = sc.moi_props
        if props.pressing is False:
            return {'CANCELLED'}
        else:
            props.pressing = False
            global ViewPortLight
            global ShadingColorType
            global ViewBackGround
            global ViewBackColor
            
            global ShowBackfaceCulling
            global ShowXray
            global ShowShadows
            global ShowCavity
            global UseDof
            global ShowObjectOutline
            
            bpy.context.space_data.shading.light = ViewPortLight
            bpy.context.space_data.shading.color_type = ShadingColorType
            bpy.context.space_data.shading.single_color = ShadingSingleColor
            bpy.context.space_data.shading.background_type = ViewBackGround
            bpy.context.space_data.shading.background_color = ViewBackColor
            
            bpy.context.space_data.shading.show_backface_culling = ShowBackfaceCulling
            bpy.context.space_data.shading.show_xray = ShowXray
            bpy.context.space_data.shading.show_shadows = ShowShadows
            bpy.context.space_data.shading.show_cavity = ShowCavity
            bpy.context.space_data.shading.use_dof = UseDof
            bpy.context.space_data.shading.show_object_outline = ShowObjectOutline
            bpy.ops.pose.reveal()
            return {'FINISHED'}

class ShowSilhouetteUi(bpy.types.Panel):

    bl_idname = "object.show_silhouette"
    bl_label = "ShowSilhouette"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Sugar"

    def draw(self, context):
        op_cls = ShowSilhouette
        layout = self.layout
        layout.operator(op_cls.bl_idname, text = "ShowSilhouette")

classes = [
    MOI_Properties,
    ShowSilhouette,
    ShowSilhouette2,
    ShowSilhouetteUi
]

def init_props():
    sc = bpy.types.Scene
    sc.moi_props = PointerProperty(
        name="プロパティ",
        description="本アドオンで利用するプロパティ一覧",
        type=MOI_Properties
    )


# プロパティの削除
def clear_props():
    sc = bpy.types.Scene
    del sc.moi_props

def register_shortcut():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new(
            idname = ShowSilhouette.bl_idname,
            type = 'F5',
            value = 'PRESS',
            shift = False,
            ctrl = False,
            alt = False
        )
        addon_keymaps.append((km,kmi))
        km2 = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi2 = km.keymap_items.new(
            idname = ShowSilhouette2.bl_idname,
            type = 'F5',
            value = 'RELEASE',
            shift = False,
            ctrl = False,
            alt = False
        )
        addon_keymaps.append((km2,kmi2))

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