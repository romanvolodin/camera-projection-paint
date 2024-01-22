import bpy

def view3d_find():
    # returns first 3d view, normally we get from context
    for area in bpy.context.window.screen.areas:
        if area.type == 'VIEW_3D':
            v3d = area.spaces[0]
            rv3d = v3d.region_3d
            for region in area.regions:
                if region.type == 'WINDOW':
                    return region, rv3d
    return None, None

def view3d_camera_border(scene):
    obj = scene.camera
    cam = obj.data

    frame = cam.view_frame(scene=scene)

    # move from object-space into world-space
    frame = [obj.matrix_world @ v for v in frame]

    # move into pixelspace
    from bpy_extras.view3d_utils import location_3d_to_region_2d
    region, rv3d = view3d_find()
    frame_px = [location_3d_to_region_2d(region, rv3d, v) for v in frame]
    return frame_px

frame_px = view3d_camera_border(bpy.context.scene)
a,b,c,d = frame_px
print(f"{a=}")
print(f"{b=}")
print(f"{c=}")
print(f"{d=}")
ax,ay = a
cx,cy = c

dim_x = (ax-cx)/2
dim_y = (ay-cy)/2

pos_x = cx + dim_x
pos_y = cy + dim_y

print()
print(dim_x, dim_y)

brush = bpy.data.brushes['ProjectionDraw']
brush.stencil_dimension = (dim_x, dim_y)
brush.stencil_pos = (pos_x, pos_y)
