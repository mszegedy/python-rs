import pygame
from consts import *
from vec import vec

class tile():
    # base tile: it has a position and size, and it interacts in theory, but it doesn't do anything
    def __init__(self,pos,dimensions):
        self.blk    = vec(0,0)   # world block the tile is in
        self.pos    = pos        # the x and y position of the tile relative to the block's bottom left and the tile's bottom left
        self.dim    = dimensions # the dimensions of the block as a vector
    def exert(self,sprite):
        # returns a force exerted on a sprite in blk at pos
        return vec(0,0)
    def touch(self,sprite):
        # takes a sprite, calculates collision with it, returns it bundled in a tuple with a tuple of the sides the sprite touched
        return (sprite,())
class solid(tile):
    # a tile solid on all sides
    def __init__(self,pos,dimensions):
        self.blk    = vec(0,0)                # world block the tile is in
        self.pos    = pos                     # the x and y position of the tile relative to the block's bottom left and the tile's bottom left
        self.dim    = dimensions              # the dimensions of the block as a vector
        self.top    = self.pos.y+self.dim.y-1 # the y value of the top of the tile
        self.bottom = self.pos.y              # the y value of the bottom of the tile
        self.left   = self.pos.x              # the x value of the left side of the tile
        self.right  = self.pos.x+self.dim.x-1 # the x value of the right side of the tile
        self.fric   = -0.02                   # the proportionality of the force exerted on the tile vs the force of friction that the tile exerts in return
    def touch(self,sprite,oldsprite):
        # takes a sprite, calculates collision with it, returns it bundled in a tuple with a tuple of the sides the sprite touched
        relspritepos = vec(BLKX*(sprite.blk.x-self.blk.x)+sprite.pos.x,BLKY*(sprite.blk.y-self.blk.y)+sprite.pos.y)
#        print 'NOW COLLISION:\nrelspritepos =',relspritepos
        reloldspritepos = vec(BLKX*(oldsprite.blk.x-self.blk.x)+oldsprite.pos.x,BLKY*(sprite.blk.y-self.blk.y)+oldsprite.pos.y)
#        print 'reloldspritepos =',reloldspritepos
        spritetop = relspritepos.y+sprite.dim.y-1.
#        print 'spritetop =',spritetop
        spritebottom = relspritepos.y
#        print 'spritebottom =',spritebottom
        spriteleft = relspritepos.x
#        print 'spriteleft =',spriteleft
        spriteright = relspritepos.x+sprite.dim.x-1.
#        print 'spriteright =',spriteright
        oldspritetop = reloldspritepos.y+oldsprite.dim.y-1.
#        print 'oldspritetop =',oldspritetop
        oldspritebottom = reloldspritepos.y
#        print 'oldspritebottom =',oldspritebottom
        oldspriteleft = reloldspritepos.x
#        print 'oldspriteleft =',oldspriteleft
        oldspriteright = reloldspritepos.x+oldsprite.dim.x-1.
#        print 'oldspriteright =',oldspriteright,'\nTILE STATE:\nself.top =',self.top,'\nself.bottom =',self.bottom,'\nself.left =',self.left,'\nself.right =',self.right
        sides = [] # sides from which the tile was impacted upon; returned as part of a tuple with the sprite itself
        if (spritebottom <= self.top+1 and self.top+1 <= oldspritebottom) and (spriteright >= self.left and self.right >= spriteleft):
            sprite.vel.y = 0
            sprite.pos.y = self.top+1.
            sprite.blk = self.blk
            if not sprite.walks:
                sprite.F.x += sprite.F.y*self.fric
            sides.append('top')
        if (spritetop >= self.bottom-1 and self.bottom-1 >= oldspritetop) and (spriteright >= self.left and self.right >= spriteleft):
            sprite.vel.y = 0
            sprite.pos.y = self.bottom-sprite.dim.y
            sprite.blk = self.blk
            if not sprite.walks:
                sprite.F.x += sprite.F.y*self.fric
            sides.append('bottom')
        if (spriteright >= self.left-1 and self.left-1 >= oldspriteright) and (spritetop >= self.bottom and self.top >= spritebottom):
            sprite.vel.x = 0
            sprite.pos.x = self.left-sprite.dim.x
            sprite.blk = self.blk
            sprite.F.y += sprite.F.x*self.fric
            sides.append('left')
        if (spriteleft <= self.right+1 and self.right+1 <= oldspriteleft) and (spritetop >= self.bottom and self.top >= spritebottom):
            sprite.vel.x = 0
            sprite.pos.x = self.right+1.
            sprite.blk = self.blk
            sprite.F.y += sprite.F.x*self.fric
            sides.append('right')
        return (sides,sprite)
class platform(tile):
    # a tile solid only at the top
    def __init__(self,pos,dimensions):
        self.blk    = vec(0,0)                # world block the tile is in
        self.pos    = pos                     # the x and y position of the tile relative to the block's bottom left and the tile's bottom left
        self.dim    = dimensions              # the dimensions of the block as a vector
        self.top    = self.pos.y+self.dim.y-1 # the y value of the top of the tile
        self.bottom = self.pos.y              # the y value of the bottom of the tile
        self.left   = self.pos.x              # the x value of the left side of the tile
        self.right  = self.pos.x+self.dim.x-1 # the x value of the right side of the tile
        self.fric   = -0.02                   # the proportionality of the force exerted on the tile vs the force of friction that the tile exerts in return
    def touch(self,sprite,oldsprite):
        # takes a sprite, calculates collision with it, returns it bundled in a tuple with a tuple of the sides the sprite touched
        relspritepos = vec(BLKX*(sprite.blk.x-self.blk.x)+sprite.pos.x,BLKY*(sprite.blk.y-self.blk.y)+sprite.pos.y)
#        print 'NOW COLLISION:\nrelspritepos =',relspritepos
        reloldspritepos = vec(BLKX*(oldsprite.blk.x-self.blk.x)+oldsprite.pos.x,BLKY*(sprite.blk.y-self.blk.y)+oldsprite.pos.y)
#        print 'reloldspritepos =',reloldspritepos
        spritebottom = relspritepos.y
#        print 'spritebottom =',spritebottom
        spriteleft = relspritepos.x
#        print 'spriteleft =',spriteleft
        spriteright = relspritepos.x+sprite.dim.x-1.
#        print 'spriteright =',spriteright
        oldspritebottom = reloldspritepos.y
#        print 'oldspritebottom =',oldspritebottom
        oldspriteleft = reloldspritepos.x
#        print 'oldspriteleft =',oldspriteleft
        oldspriteright = reloldspritepos.x+oldsprite.dim.x-1.
#        print 'oldspriteright =',oldspriteright,'\nTILE STATE:\nself.top =',self.top,'\nself.bottom =',self.bottom,'\nself.left =',self.left,'\nself.right =',self.right
        sides = [] # sides from which the tile was impacted upon; returned as part of a tuple with the sprite itself
        if (spritebottom <= self.top+1 and self.top+1 <= oldspritebottom) and (spriteright >= self.left and self.right >= spriteleft):
            sprite.vel.y = 0
            sprite.pos.y = self.top+1.
            sprite.blk = self.blk
            if not sprite.walks:
                sprite.F.x += sprite.F.y*self.fric
            sides.append('top')
        return (sides,sprite)
