#再生中だったら停止したほうがよさそう

from contextlib import nullcontext
import bpy
from bpy.props import IntProperty, BoolProperty, PointerProperty
import blf

bl_info = {
    "name": "FrameExpansion",
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

# リージョン情報の取得
def get_region(context, area_type, region_type):
    region = None
    area = None

    # 指定されたエリアの情報を取得する
    for a in context.screen.areas:
        if a.type == area_type:
            area = a
            break
    else:
        return None
    # 指定されたリージョンの情報を取得する
    for r in area.regions:
        if r.type == region_type:
            region = r
            break

    return region

addon_keymaps = []
AddFrameCount = 0

class FrameExpandProperties(bpy.types.PropertyGroup):
    pressing = BoolProperty(
        name="キー入力中",
        description="キー入力中か",
        default=False
    )
    add_frame_count = IntProperty(
        name="フレーム追加する数",
        description="フレーム追加する数",
        default=0
    )

class ExpandFrame(bpy.types.Operator):
    bl_idname = "object.frame_expansion"
    bl_label = "AddOrRemoveFrame"
    bl_description = "フレームの追加・削除をします"

    # Trueの場合は、マウスをドラッグさせたときに、アクティブなオブジェクトが
    # 回転する（Trueの場合は、モーダルモード中である）
    __running = False
    __handle = None

    # モーダルモード中はTrueを返す
    @classmethod
    def is_running(cls):
        return cls.__running

    def modal(self, context, event):
        sc = context.scene
        props = sc.frame_expand_prps

        global AddFrameCount

        # エリアを再描画
        if context.area:
            context.area.tag_redraw()

        # モーダルモードを終了
        if not self.is_running():
            return {'FINISHED'}

        # マウスホイール回転で追加・削除するフレーム数を調整
        if event.type == 'WHEELUPMOUSE':
            if self.is_running():
                AddFrameCount += 1
                return {'RUNNING_MODAL'}
        elif event.type == 'WHEELDOWNMOUSE':
            if self.is_running():
                AddFrameCount -= 1
                return {'RUNNING_MODAL'}

        return {'PASS_THROUGH'}

    @classmethod
    def __handle_add(cls, context):
        if not cls.is_running():
            # 描画関数の登録
            cls.__handle = bpy.types.SpaceDopeSheetEditor.draw_handler_add(
                cls.__draw, (context, ), 'HEADER', 'POST_PIXEL'
            )

    @classmethod
    def __handle_remove(cls, context):
        if cls.is_running():
            # 描画関数の登録を解除
            bpy.types.SpaceDopeSheetEditor.draw_handler_remove(
                cls.__handle, 'HEADER'
            )
            cls.__handle = None

    @classmethod
    def __draw(cls, context):
        # リージョンの幅を取得するため、描画先のリージョンを得る
        region = get_region(context, 'DOPESHEET_EDITOR', 'HEADER')

        # 追加・削除するフレーム数を描画
        # TODO 追加は「+」を付けて描画したい
        if region is not None:
            blf.color(0, 1.0, 1.0, 1.0, 1.0)
            blf.size(0, 12, 72)
            blf.position(0, region.width - 400, region.height - 20.0, 0)
            
            global AddFrameCount
            blf.draw(0, "AddFrameCount : " + str(AddFrameCount))

    def invoke(self, context, event):
        op_cls = ExpandFrame

        print('invoke')

        #TODO フラグ管理がうまくいっていない
        if context.area.type == 'DOPESHEET_EDITOR':
            # [開始] ボタンが押された時の処理
            if not self.is_running():
                print('run modal')
                # モーダルモードを開始
                context.window_manager.modal_handler_add(self)
                op_cls.__handle_add(context)
                op_cls.__running = True
                return {'RUNNING_MODAL'}
            # [終了] ボタンが押された時の処理
            else:
                print('exit modal')
                bpy.ops.action.select_leftright(mode='RIGHT', extend=False)
                
                # フレームの追加・削除
                # TODO 0だったら何もしない
                global AddFrameCount
                bpy.context.scene.frame_end += AddFrameCount
                bpy.ops.transform.transform(mode='TIME_TRANSLATE', value=(AddFrameCount, 0, 0, 0))

                op_cls.__handle_remove(context)
                op_cls.__running = False
                return {'FINISHED'}
        else:
            return {'CANCELLED'}


class ExpandFrameUi(bpy.types.Panel):

    bl_label = "Add or Remove Frame"
    bl_space_type = 'DOPESHEET_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Suger"
    bl_context = "objectmode"

    def draw(self, context):
        op_cls = ExpandFrame

        layout = self.layout
        # [開始] / [終了] ボタンを追加
        if not op_cls.is_running():
            layout.operator(op_cls.bl_idname, text="開始", icon='PLAY')
        else:
            layout.operator(op_cls.bl_idname, text="終了", icon='PAUSE')

classes = [
    ExpandFrame,
    ExpandFrameUi,
    FrameExpandProperties,
]

def init_props():
    sc = bpy.types.Scene
    sc.frame_expand_prps = PointerProperty(
        name="frameExpandProperties",
        description="",
        type=FrameExpandProperties
    )

def clear_props():
    sc = bpy.types.Scene
    del sc.frame_expand_prps

def register_shortcut():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="Dopesheet Generic", space_type="DOPESHEET_EDITOR")
        kmi = km.keymap_items.new(
            idname = ExpandFrame.bl_idname,
            type = 'F6',
            value = 'PRESS',
            shift = False,
            ctrl = False,
            alt = False
        )
        addon_keymaps.append((km,kmi))
        km2 = kc.keymaps.new(name="Dopesheet Generic", space_type="DOPESHEET_EDITOR")
        kmi2 = km.keymap_items.new(
            idname = ExpandFrame.bl_idname,
            type = 'F6',
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