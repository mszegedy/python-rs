import pygame
from consts import *
from vec import vec

class tile():
    # base tile: it has a position and size, and it interacts in theory, but it doesn't do anything
    def __init__(self,pos,dimensions):
        self.blk    = vec(0,0)                # world block the tile is in
        self.pos    = pos                     # the x and y position of the tile relative to the block's bottom left and the tile's bottom left
        self.dim    = dimensions              # the dimensions of the block as a vector
    def distanceAction(self,sprite):
        # returns a force exerted on a sprite in blk at pos
        return vec(0,0)
    def collision(self,sprite):
        return sprite
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
    def collision(self,sprite):
        # takes a sprite, calculates collision with it, returns it bundled in a tuple with "sides" (see below)
        relspritepos = vec(BLKX*(sprite.blk.x-self.blk.x)+sprite.pos.x,BLKY*(sprite.blk.y-self.blk.y)+sprite.pos.x)
        spritetop = relspritepos.y+sprite.dim.y-1.
        spritebottom = relspritepos.y
        spriteleft = relspritepos.x
        spriteright = relspritepos.x+sprite.dim.x-1.
        sides = [] # sides from which the tile was impacted upon; returned as part of a tuple with the sprite itself
        if (spritebottom <= self.top+1) and (spritetop > self.top) and (spriteright >= self.left) and (spriteleft <= self.right):
            sprite.vel.y = 0
            sprite.pos.y = self.top+1.
            if not sprite.walks:
                sprite.F.x += sprite.F.y*self.fric
            sides.append('top')
        if (spritetop >= self.bottom-1) and (spritebottom < self.bottom) and (spriteright >= self.left) and (spriteleft <= self.right):
            sprite.vel.y = 0
            sprite.pos.y = self.bottom-sprite.dim.y
            if not sprite.walks:
                sprite.F.x += sprite.F.y*self.fric
            sides.append('bottom')
        if (spriteright >= self.left-1) and (spriteleft < self.left) and (spritetop >= self.bottom) and (spritebottom <= self.top):
            sprite.vel.x = 0
            sprite.pos.x = self.left-sprite.dim.x
            sprite.F.y += sprite.F.x*self.fric
            sides.append('left')
        if (spriteleft <= self.right+1) and (spriteright > self.right) and (spritetop >= self.bottom) and (spriteright <= self.top):
            sprite.vel.x = 0
            sprite.pos.x = self.right+1.
            sprite.F.y += sprite.F.x*self.fric
            sides.append('right')
        return (sprite,sides)
class platform(solid):
    # A tile solid on the top and passable every other way
    def collision(self,sprite):
        # takes a sprite, calculates collision with it, returns it bundled in a tuple with "sides" (see below)
        relpos = vec(BLKX*(sprite.blk.x-self.blk.x)+sprite.pos.x,BLKY*(sprite.blk.y-self.blk.y)+sprite.pos.x)
        spritetop = relpos.y+sprite.dim.y-1.
        spritebottom = relpos.y
        spriteleft = relpos.x
        spriteright = relpos.x+sprite.dim.x-1.
        sides = [] # sides from which the tile was impacted upon; returned as part of a tuple with the sprite itself
        if (spritetop <= self.top+1) and (spritetop > self.top) and (spriteright >= self.left) and (spriteleft <= self.right):
            sprite.vel.y = 0
            sprite.pos.y = self.top+1.
            if not sprite.walks:
                sprite.F.x += sprite.F.y*self.fric
            sides.append('top')
        return (sprite,sides)
