import bpy

from random import randint

INTERVAL = 2
FRAME_COUNT = 3
RAND_MIN = -5
RAND_MAX = 5
FACTOR = 0.2

currentFrame = bpy.context.scene.frame_current

for i in range(0, FRAME_COUNT):
    bpy.context.scene.frame_set(currentFrame)

    #get random value
    x = randint(RAND_MIN, RAND_MAX) * FACTOR
    y = randint(RAND_MIN, RAND_MAX) * FACTOR
    z = randint(RAND_MIN, RAND_MAX) * FACTOR

    #operate transform
    bpy.ops.transform.translate(value=(x, y, z))
    #TODO all axis
    bpy.ops.transform.rotate(value=1, orient_axis='Z')
    bpy.ops.transform.resize(value=(x, y, z))

    #insert keyframe (only active object)
    #TODO apply all selected object
    #TODO switchable on/off by checkbox?
    bpy.context.object.keyframe_insert(data_path="location", index=-1)
    bpy.context.object.keyframe_insert(data_path="rotation_euler", index=-1)
    bpy.context.object.keyframe_insert(data_path="scale", index=-1)

    currentFrame += INTERVAL