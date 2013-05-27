# Contains environments for blocks
from consts import *
from vec import vec

class newtonian: # an environment that functions according to Newtonian physics
    def exert(self,sprite):
        # takes a sprite and calculates a force to be exerted on it, which it returns
        return vec(0,-0.33) # gravity and air resistance
    def move(self,sprite):
        # takes a sprite and returns a new position for it based on the forces acting on it
        sprite.vel += sprite.F/sprite.m
        sprite.pos += sprite.vel
        if not (0 <= sprite.pos.x and sprite.pos.x < BLKX):
            offset = sprite.pos.x//BLKX
            sprite.blk.x += offset
            sprite.pos.x -= offset*BLKX
        if not (0 <= sprite.pos.y and sprite.pos.y < BLKY):
            offset = sprite.pos.y//BLKY
            sprite.blk.y += offset
            sprite.pos.y -= offset*BLKY
        sprite.F = vec(0,0)
        return sprite
    def moveAgain(self,sprite):
        # takes a sprite for the second time in the main loop and moves it again, accounting for
        # the fact that it's already moved the sprite once this frame, and then returns the sprite
        sprite.pos += sprite.F/sprite.m
        if not (0 <= sprite.pos.x and sprite.pos.x < BLKX):
            offset = sprite.pos.x//BLKX
            sprite.blk.x += offset
            sprite.pos.x -= offset*BLKX
        if not (0 <= sprite.pos.y and sprite.pos.y < BLKY):
            offset = sprite.pos.y//BLKY
            sprite.blk.y += offset
            sprite.pos.y -= offset*BLKY
        sprite.F = vec(0,0)
        return sprite
