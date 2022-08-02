#TODO previewとまではいかなくても視覚的なわかりやすさがもう少しほしいかも
from logging import exception
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

class ExpandFrame(bpy.types.Operator):
    bl_idname = "object.frame_expansion"
    bl_label = "AddOrRemoveFrame"
    bl_description = "フレームの追加・削除をします"

    __running = False
    __handle = None
    __timer = None

    # モーダルモード中はTrueを返す
    @classmethod
    def is_running(cls):
        return cls.__running

    def modal(self, context, event):
        sc = context.scene
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
                cls.__draw, (context, ), 'WINDOW', 'POST_PIXEL'
            )

    @classmethod
    def __handle_remove(cls, context):
        if cls.is_running():
            # 描画関数の登録を解除
            bpy.types.SpaceDopeSheetEditor.draw_handler_remove(
                cls.__handle, 'WINDOW'
            )
            cls.__handle = None

    @classmethod
    def __draw(cls, context):
        # リージョンの幅を取得するため、描画先のリージョンを得る
        region = get_region(context, 'DOPESHEET_EDITOR', 'WINDOW')

        # 追加・削除するフレーム数を描画
        if region is not None:
            blf.color(0, 1.0, 1.0, 1.0, 1.0)
            blf.size(0, 24, 72)
            blf.position(0, 100, 100, 0)
            
            global AddFrameCount
            if AddFrameCount > 0:
                blf.draw(0, "AddFrameCount : " + '+' + str(AddFrameCount))
            else:
                blf.draw(0, "AddFrameCount : " + str(AddFrameCount))

    def invoke(self, context, event):
        op_cls = ExpandFrame
        if context.area.type == 'DOPESHEET_EDITOR':
            if not self.is_running():
                #再生中だったら停止する
                bpy.ops.screen.animation_cancel(restore_frame=False)
                # モーダルモードを開始
                context.window_manager.modal_handler_add(self)
                #終了時、モーダルモード自動更新のため、タイマーを起動しておく
                op_cls.__timer = context.window_manager.event_timer_add(0.001, window=context.window)
                op_cls.__handle_add(context)
                op_cls.__running = True
                return {'RUNNING_MODAL'}
            else:
                context.window_manager.event_timer_remove(op_cls.__timer)
                op_cls.__timer = None

                global AddFrameCount
                if AddFrameCount != 0:
                    #フレームの追加→キーの移動になるので、現在のフレームから先をすべて選択
                    bpy.ops.action.select_leftright(mode='RIGHT', extend=False)

                    # markerの移動(ver3.2以降)
                    major = bpy.app.version[0]
                    minor = bpy.app.version[1]
                    if major >= 3 and minor >= 2:
                        try:
                            # 現在のフレームから先のマーカーをすべて選択
                            bpy.ops.marker.select_leftright(mode='RIGHT', extend=False)
                            # マーカーの移動
                            bpy.ops.marker.move(frames=AddFrameCount)
                        except:
                            print('no marker')
                    
                    # フレームの追加・削除(全体のフレーム数を変更しキーを移動させる)
                    bpy.context.scene.frame_end += AddFrameCount
                    bpy.context.scene.frame_preview_end += AddFrameCount
                    bpy.ops.transform.transform(mode='TIME_TRANSLATE', value=(AddFrameCount, 0, 0, 0))

                    # 次の操作に備えて0に戻しておく
                    AddFrameCount = 0
                    
                    #フレーム操作を行ったので、undo登録
                    bpy.ops.ed.undo_push()

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
        if not op_cls.is_running():
            layout.operator(op_cls.bl_idname, text="Start")
        else:
            layout.operator(op_cls.bl_idname, text="Add Frame")

classes = [
    ExpandFrame,
    ExpandFrameUi,
]

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
    register_shortcut()

def unregister():
    unregister_shortcut()
    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()