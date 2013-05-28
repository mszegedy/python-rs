# Contains environments for blocks
from math import sqrt
from consts import *
from vec import vec

class classical:
    # an environment that functions according to Newtonian physics
    def exert(self,sprite):
        # takes a sprite and calculates a force to be exerted on it, which it returns
        return vec(-0.02*sprite.vel.x**2.,-0.02*sprite.vel.x**2.-0.33) # gravity and air resistance
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
        return sprite
    def moveAgain(self,sprite):
        # takes a sprite for the second time in the main loop and moves it again, accounting for
        # the fact that it's already moved the sprite once this frame, and then returns the sprite
        sprite.pos += sprite.secondF/sprite.m
        if not (0 <= sprite.pos.x and sprite.pos.x < BLKX):
            offset = sprite.pos.x//BLKX
            sprite.blk.x += offset
            sprite.pos.x -= offset*BLKX
        if not (0 <= sprite.pos.y and sprite.pos.y < BLKY):
            offset = sprite.pos.y//BLKY
            sprite.blk.y += offset
            sprite.pos.y -= offset*BLKY
        sprite.F = vec(0,0)
        sprite.secondF = vec(0,0)
        return sprite
class relativistic:
    # an environment that functions according to Einsteinian physics
    def __init__(self,c):
        self.c = c # the speed of light
    def exert(self,sprite):
        # takes a sprite and calculates a force to be exerted on it, which it returns
        return vec(-0.02*sprite.vel.x**2,-0.02*sprite.vel.x**2-0.33) # gravity and air resistance
    def move(self,sprite):
        invLorentz = sqrt(1.-(sprite.vel/self.c)**2) # the inverse of the Lorentz factor
        sprite.vel += sprite.F/sprite.m
        sprite.pos += invLorentz*sprite.vel
        sprite.scale = invLorentz*sprite.vel
        if not (0 <= sprite.pos.x and sprite.pos.x < BLKX):
            offset = sprite.pos.x//BLKX
            sprite.blk.x += offset
            sprite.pos.x -= offset*BLKX
        if not (0 <= sprite.pos.y and sprite.pos.y < BLKY):
            offset = sprite.pos.y//BLKY
            sprite.blk.y += offset
            sprite.pos.y -= offset*BLKY
        return sprite
    def moveAgain(self,sprite):
        # takes a sprite for the second time in the main loop and moves it again, accounting for
        # the fact that it's already moved the sprite once this frame, and then returns the sprite
        invLorentz = sqrt(1.-(sprite.vel/self.c)**2) # the inverse of the Lorentz factor
        sprite.pos += sprite.secondF*invLorentz/sprite.m
        if not (0 <= sprite.pos.x and sprite.pos.x < BLKX):
            offset = sprite.pos.x//BLKX
            sprite.blk.x += offset
            sprite.pos.x -= offset*BLKX
        if not (0 <= sprite.pos.y and sprite.pos.y < BLKY):
            offset = sprite.pos.y//BLKY
            sprite.blk.y += offset
            sprite.pos.y -= offset*BLKY
        sprite.F = vec(0,0)
        sprite.secondF = vec(0,0)
        return sprite
