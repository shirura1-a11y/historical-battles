"""Blender 4.x: deterministic, simplified Sekigahara diorama. No render by default."""
import bpy, math, random, sys, argparse
from pathlib import Path
from mathutils import Vector
p=argparse.ArgumentParser(); p.add_argument('--render',action='store_true'); p.add_argument('--start',type=int,default=1); p.add_argument('--end',type=int,default=2100); p.add_argument('--out',default='build'); a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
rng=random.Random(1600); s=bpy.context.scene
s.display.render_aa='FXAA'; s.render.engine='BLENDER_WORKBENCH'; s.display.shading.light='STUDIO'; s.display.shading.color_type='MATERIAL'; s.display.shading.show_shadows=True; s.display.shading.show_cavity=True
s.display.shading.background_type='WORLD'; s.world.color=(.035,.045,.06)
s.render.resolution_x=720; s.render.resolution_y=1280; s.render.resolution_percentage=100; s.render.fps=30; s.frame_start=1; s.frame_end=2100
s.render.image_settings.file_format='PNG'; s.render.film_transparent=False
out=Path(a.out).resolve(); (out/'frames').mkdir(parents=True,exist_ok=True); s.render.filepath=str(out/'frames'/'frame_')
def mat(name,c):
 m=bpy.data.materials.new(name); m.diffuse_color=(*c,1); return m
red=mat('Western • red',(.72,.055,.06)); blue=mat('Eastern • blue',(.035,.22,.8)); earth=mat('Plain',(.25,.33,.19)); rock=mat('Hills',(.17,.25,.17)); road=mat('Road',(.53,.43,.28)); dark=mat('Armour',(.09,.1,.12)); smoke=mat('Smoke',(.5,.51,.49)); gold=mat('Standards',(.94,.75,.34))
def cube(name,loc,scale,m,parent=None):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc); o=bpy.context.object; o.name=name; o.scale=scale; o.data.materials.append(m); o.parent=parent; return o
def key(o,t,loc):
 o.location=loc; o.keyframe_insert('location',frame=1+round(t*30))
def height(x,y):
 return sum(h*math.exp(-((x-cx)**2+(y-cy)**2)/w) for cx,cy,h,w in [(-10,7,4,22),(-8,-9,4.5,22),(11,10,4,28),(0,13,3,18)])
# North is +Y, east is +X; geographic distances are compressed.
verts=[(x,y,height(x,y)) for y in range(-16,17) for x in range(-16,17)]; faces=[]
for j in range(32):
 for i in range(32):
  k=j*33+i; faces.append((k,k+1,k+34,k+33))
mesh=bpy.data.meshes.new('Terrain'); mesh.from_pydata(verts,[],faces); mesh.update(); o=bpy.data.objects.new('Sekigahara basin',mesh); s.collection.objects.link(o); o.data.materials.append(earth)
for i in range(48):
 x=-15+i*.64; y=.7*math.sin(x*.18); cube('Nakasendo schematic', (x,y,height(x,y)+.05),(.7,.65,.06),road)
for i in range(90):
 x=rng.uniform(-15,15); y=rng.choice([-1,1])*rng.uniform(9,15)
 bpy.ops.mesh.primitive_cone_add(vertices=5,radius1=.45,depth=1.4,location=(x,y,height(x,y)+.7)); bpy.context.object.data.materials.append(rock)
# Ishida at Sasao (NW), Ukita/Konishi in west, Otani SW, Kobayakawa on Matsuo SW.
units=[('Ishida Mitsunari',-8,7,red),('Ukita Hideie',-6,2,red),('Konishi Yukinaga',-6,-1,red),('Otani Yoshitsugu',-5,-5,red),('Kobayakawa Hideaki',-8,-9,red),('Fukushima Masanori',5,1,blue),('Ii / Matsudaira',4,4,blue),('Kuroda / Hosokawa',5,7,blue),('Tokugawa Ieyasu',10,3,blue)]
for idx,(name,x,y,m) in enumerate(units):
 root=bpy.data.objects.new(name,None); s.collection.objects.link(root); z=height(x,y)+.1
 for row in range(4):
  for col in range(5):
   xx=(col-2)*.38; yy=(row-1.5)*.4
   cube(name+' soldier',(xx,yy,.38),(.25,.23,.65),m,root); cube('Helmet',(xx,yy,.78),(.29,.28,.2),dark,root)
 for xx in [-.7,.7]:
  cube('Flag pole',(xx,0,1.2),(.045,.045,2.3),gold,root)
  flag=cube('Banner',(xx+.21,0,1.9),(.42,.06,.65),m,root)
  for t in range(0,71,2):
   flag.rotation_euler.z=.18*math.sin(t*2+idx); flag.keyframe_insert('rotation_euler',frame=1+t*30)
 key(root,0,(x,y,z)); key(root,15,(x,y,z))
 if idx==4:
  key(root,55,(x,y,z)); key(root,61,(-4,-5,1)); key(root,66,(-2,-4,.4)); key(root,70,(-1,-3,.4))
 else:
  cx=x*.22; cy=y*.65
  key(root,35,(cx,cy,height(cx,cy)+.15)); key(root,55,(cx+.25,cy,.3))
  key(root,66,((-12 if idx<4 else -2),cy+2,.35)); key(root,70,((-15 if idx<4 else -3),cy+3,.35))
for i in range(24):
 x=rng.uniform(-2,2); y=rng.uniform(-4,5)
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1,location=(x,y,.7)); o=bpy.context.object; o.name='Stylized clash smoke'; o.data.materials.append(smoke)
 for t in range(0,71):
  size=0 if t<35 or t>65 else .2+.6*((t+i)%4)/4
  o.scale=(size,size,size*1.5); o.keyframe_insert('scale',frame=1+t*30)
  key(o,t,(x+.3*math.sin(t+i),y,.8+((t+i)%4)*.4))
bpy.ops.object.camera_add(); cam=bpy.context.object; s.camera=cam; cam.data.type='ORTHO'
for t,pos,target,zoom in [(0,(11,-14,15),(0,0,0),15),(3,(18,-24,27),(0,0,0),37),(15,(17,-23,28),(0,0,0),37),(35,(12,-17,21),(0,0,0),25),(55,(8,-17,22),(-2,-3,0),27),(63,(7,-18,24),(-5,-3,0),31),(70,(15,-24,30),(-2,0,0),37)]:
 key(cam,t,pos); cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler(); cam.keyframe_insert('rotation_euler',frame=1+round(t*30)); cam.data.ortho_scale=zoom; cam.data.keyframe_insert('ortho_scale',frame=1+round(t*30))
# Camera interpolation is smooth; troop motion stays legible and has no overshoot.
for obj in bpy.data.objects:
 if obj.animation_data and obj.animation_data.action and obj!=cam:
  for fc in obj.animation_data.action.fcurves:
   for k in fc.keyframe_points: k.interpolation='LINEAR'
s.frame_set(1); bpy.ops.wm.save_as_mainfile(filepath=str(out/'sekigahara.blend'))
if a.render:
 s.frame_start=a.start; s.frame_end=a.end; bpy.ops.render.render(animation=True)
