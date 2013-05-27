import pygame,envs,tiles,sprites
from vec import vec

class image:
    # an image to display in a block
    def __init__(self,pos,imgpath):
        self.blk = vec(0,0)                             # block in which to display image (set during creation of block in which it is)
        self.pos = pos                                  # position at which to display image
        self.img = pygame.image.load('images/'+imgpath) # the actual image
class block:
    # a block in the face of the world; contains stuff for the player to interact with
    def __init__(self,index,env,tiles,sprites,fgimages,bgimages):
        self.i        = index    # the index of the block
        self.env      = env      # the physics environment of the block
        self.tiles    = tiles    # the tiles inside the block
        self.sprites  = sprites  # the sprites inside the block
        self.bgimages = bgimages # images to display inside the block behind the sprites
        self.fgimages = fgimages # images to display inside the block in front of the sprites
        for l in (self.tiles,self.sprites,self.bgimages,self.fgimages): # sets the block of every
            for i,o in enumerate(l):                                    # object in the block to
                l[i].blk = self.i                                       # the index of this one
    def __repr__(self):
        return str(self.i)

def getBlock(i):
    # gets a block from the world at vector index i
    if i == vec(0,0):
        return block(vec(0,0),
                     envs.newtonian(),
                     [tiles.solid(vec(10.,10.),
                                  vec(300.,10.)),
                      tiles.solid(vec(310.,20.),
                                  vec(300.,10.))],
                     [],
                     [],
                     [image(vec(10.,10.),'world/black.png'),
                      image(vec(310.,20.),'world/black.png')])
    else:
        return block(vec(None,None),
                     envs.newtonian(),
                     [],
                     [],
                     [],
                     [])
