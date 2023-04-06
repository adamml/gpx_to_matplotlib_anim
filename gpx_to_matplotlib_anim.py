import xml.etree.ElementTree as Tree
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter
import numpy as np

FILE = ".gpx"

gpx_raw_as_tree = Tree.parse(FILE)
gpx_raw_root = gpx_raw_as_tree.getroot()

gpx_as_list_of_lists = list(zip(*[
    [float(t.attrib['lat']), float(t.attrib['lon']), float(t[0].text)] 
     for t in gpx_raw_root.iter("{http://www.topografix.com/GPX/1/1}trkpt")]))

#
# TODO: Remove any pauses...
#

#
# Process for elevation shading and sector type (uphill or downhill)
#
max_ele = max(gpx_as_list_of_lists[2])
min_ele = min(gpx_as_list_of_lists[2])

colours = [0] * len(gpx_as_list_of_lists[0])
stage = [0] * len(gpx_as_list_of_lists[0])

i = 0
while i < len(gpx_as_list_of_lists[1]):
    if i > 0 and gpx_as_list_of_lists[2][i] < gpx_as_list_of_lists[2][i-1]:
        colours[i] = (181/255, 254/255, 10/255, (((gpx_as_list_of_lists[2][i] - min_ele) / (max_ele - min_ele)) * 0.7) + 0.3)
        stage[i] = 1
    else:
        colours[i] = (1, 1, 1, (((gpx_as_list_of_lists[2][i] - min_ele) / (max_ele - min_ele)) * 0.7) + 0.3)
    i += 1

fig = plt.figure()
fig.patch.set_facecolor('#5A5A5A')
gs = fig.add_gridspec(16, 16)

ax0 = fig.add_subplot(gs[0:12, :])
ax0.patch.set_facecolor('#5A5A5A')
ax0.axis('off')
ax0.scatter(gpx_as_list_of_lists[1],
            gpx_as_list_of_lists[0],
            c=colours, s=2)
ax0.axis('equal')

ax1 = fig.add_subplot(gs[12:17, 3:14])
ax1.patch.set_facecolor('#5A5A5A')
ax1.axis('off')
ax1.plot(range(len(gpx_as_list_of_lists[0])), gpx_as_list_of_lists[2], 'white', linewidth=3)
ax1.fill_between(
    x=range(len(gpx_as_list_of_lists[0])),
    y2=gpx_as_list_of_lists[2],
    y1=0,
    where=(np.array(stage)==1)
)

hi1, = ax1.plot([0, 0],[0, gpx_as_list_of_lists[2][0]],
    color=(252/255, 3/255, 74/255, 0.3),
    linewidth=8)
hi2, = ax1.plot([0, 0],[0, gpx_as_list_of_lists[2][0]],
    color=(252/255, 3/255, 74/255, 0.5),
    linewidth=6)
hi3, = ax1.plot([0, 0],[0, gpx_as_list_of_lists[2][0]],
    color=(252/255, 3/255, 74/255, 0.7),
    linewidth=4)
hi4, = ax1.plot([0, 0],[0, gpx_as_list_of_lists[2][0]],
    color=(252/255, 3/255, 74/255, 0.9),
    linewidth=2)

s1 = ax0.scatter(gpx_as_list_of_lists[1][0],
            gpx_as_list_of_lists[0][0],
            color=(252/255, 3/255, 74/255, 0.3), s=64)
s2 = ax0.scatter(gpx_as_list_of_lists[1][0],
            gpx_as_list_of_lists[0][0],
            color=(252/255, 3/255, 74/255, 0.5), s=48)
s3 = ax0.scatter(gpx_as_list_of_lists[1][0],
            gpx_as_list_of_lists[0][0],
            color=(252/255, 3/255, 74/255, 0.7), s=32)
s4 = ax0.scatter(gpx_as_list_of_lists[1][0],
            gpx_as_list_of_lists[0][0],
            color=(252/255, 3/255, 74/255, 0.9), s=16)

def animate(i):
    hi1.set_data([i, i], [0, gpx_as_list_of_lists[2][i]])
    hi2.set_data([i, i], [0, gpx_as_list_of_lists[2][i]])
    hi3.set_data([i, i], [0, gpx_as_list_of_lists[2][i]])
    hi4.set_data([i, i], [0, gpx_as_list_of_lists[2][i]])
    
    s1.set_offsets([gpx_as_list_of_lists[1][i], gpx_as_list_of_lists[0][i]])
    s2.set_offsets([gpx_as_list_of_lists[1][i], gpx_as_list_of_lists[0][i]])
    s3.set_offsets([gpx_as_list_of_lists[1][i], gpx_as_list_of_lists[0][i]])
    s4.set_offsets([gpx_as_list_of_lists[1][i], gpx_as_list_of_lists[0][i]])
    
    if i % 1000 == 0:
        print(i)
    
    return hi1, hi2, hi3, hi4

anim = FuncAnimation(fig, animate,
                     frames = range(len(gpx_as_list_of_lists[0])), interval = 1)

anim.save("anim.MP4", 
          writer=FFMpegWriter(fps=(len(gpx_as_list_of_lists[0]))/90))
