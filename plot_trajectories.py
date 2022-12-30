# Example code to plot trajectories in BrainRender from stereotaxic coordinates 
import math
import numpy as np

from brainrender import Scene
from brainrender.actors import Cylinder
from brainrender import settings
from bg_atlasapi import show_atlases

# Extension to cylinder class to allow specification of start and end coordinates.
# Thanks to Ian Hawes for this.
class Cylinder2(Cylinder):

    def __init__(self, pos_from, pos_to, root, color='powderblue', alpha=1, radius=350):
        from vedo import shapes
        from brainrender.actor import Actor

        mesh = shapes.Cylinder(pos=[pos_from, pos_to], c=color, r=radius, alpha=alpha)
        Actor.__init__(self, mesh, name="Cylinder", br_class="Cylinder")                                         


# Function to convert stereotaxic coordinates to ABA CCF
# SC is an array with stereotaxic coordinates to be transformed
# Returns an array containing corresponding CCF coordinates in μm
# Conversion is from this post, which explains the opposite transformation: https://community.brain-map.org/t/how-to-transform-ccf-x-y-z-coordinates-into-stereotactic-coordinates/1858/3
# Warning: this is very approximate
# Warning: the X, Y, Z schematic at the top of the linked post is incorrect, scroll down for correct one.
def StereoToCCF(SC = np.array([1,1,1]), angle = -0.0873):
    # Stretch
    stretch = SC/np.array([1,0.9434,1])
    # Rotate
    rotate = np.array([(stretch[0] * math.cos(angle) - stretch[1] * math.sin(angle)), (stretch[0] * math.sin(angle) + stretch[1] * math.cos(angle)), stretch[2]])
    #Translate
    trans = rotate + np.array([5400, 440, 5700])
    return(trans)


# Injection site for LEC targetting from Vandrey et al. 2022
# Coordinate are [anterior-posterior, superior-inferior, left-right
# 3.8 mm posterior, 4 mm lateral
Inj1 = StereoToCCF(np.array([3800,0,4000]))
# Target (my guess)
Tar1 = StereoToCCF(np.array([4200,4000,4000]))

# Bregma to 4 mm immediately below Bregma (sanity check)
Inj2 = StereoToCCF(np.array([0,0,0]))
Tar2 = StereoToCCF(np.array([0,4000,0]))



settings.SHADER_STYLE = 'plastic'  # other options: metallic, plastic, shiny, glossy, cartoon, default
settings.ROOT_ALPHA = .1   # this sets how transparent the brain outline is
settings.SHOW_AXES = True  # shows/hides the ABA CCF axes from the image
#show_atlases()  # this will print a list of atlases that you could use
scene = Scene(root=False, inset=False, atlas_name="allen_mouse_10um")  # makes a scene instance

root = scene.add_brain_region("root", alpha=0.1, color="grey")  # this is the brain outline
mec = scene.add_brain_region("ENTm", alpha=0.2, color="lightskyblue", hemisphere=None)


# Example cylinder #1. Illustrates extent of the ABA coordinate space.
actor = Cylinder2([0, 0, 0], [13200, 8000, 11400], scene.root, color='blue', radius=10)
scene.add(actor)

# Example cylinder #2. LEC.
actor = Cylinder2(Inj1, Tar1, scene.root, color='green', radius=100)
scene.add(actor)

# Example cylinder #3. Bregma.
actor = Cylinder2(Inj2, Tar2, scene.root, color='red', radius=100)
scene.add(actor)


scene.render(zoom=1.2)
