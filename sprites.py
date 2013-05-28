import pygame
from consts import *
from vec import vec
from pygame.locals import *

class sprite:
    def __init__(self):
        self.img     = None     # pygame.img.load('path') goes on the right side of this assignment, and gives the sprite a fixed image
        self.blk     = vec(0,0) # block index
        self.pos     = vec(0,0) # position (bottom left of image)
        self.vel     = vec(0,0) # velocity
        self.dim     = vec(0,0) # dimensions of sprite (in pixels)
        self.F       = vec(0,0) # net force acting on sprite
        self.secondF = vec(0,0) # F used for quantifying additional forces exerted on sprite after first move
        self.m       = 1.0      # mass
        self.walks   = False    # whether the sprite has feet with which it walks (this matters for friction)
        self.flipped = False    # False means the sprite's image looks as loaded (facing right, probably), and True means it is flipped the other way (facing left, probably)
        self.solid   = False    # setting this to true will make the sprite interact with other sprites as though it is solid
    def envExertion(self,env):
        self.F += env.exert(self)
    def tileExertion(self,tile):
        # processes interaction with tiles at a distance
        self.F += tile.exert(self)
    def tileTouch(self,tile,oldself):
        # processes interaction with tiles while touching them; default is that it won't pass through tiles that are solid on sides that they say they are solid on
        sides,self = tile.touch(self,oldself)
    def spriteExertion(self,sprite):
        # processes interaction with a sprite at a distance
        self.F += sprite.exert(self)
    def spriteTouch(self,sprite,oldself):
        # processes interaction with a sprite when touching the sprite
        sides,self = sprite.touch(self,oldself)
    def move(self,env):
        self = env.move(self)
    def moveAgain(self,env):
        self = env.moveAgain(self)
    def locomotion(self,env):
        # movement that the sprite makes each frame by itself
        pass
    def exert(self,sprite):
        return vec(0,0)
    def touch(self,sprite,oldsprite):
        return sprite
class player(sprite):
    def __init__(self):
        self.img = pygame.image.load('images/player/stand.png')
        self.blk = vec(0,0)      # block index
        self.pos = vec(50,50)
        self.vel = vec(0,0)      # velocity
        self.dim = vec(self.img.get_width(),self.img.get_height())
        self.F   = vec(0,0)      # net force acting on sprite
        self.m   = 1.0           # mass
        self.secondF = vec(0,0)  # F used for quantifying additional forces exerted on sprite after first move
        self.walks       = True  # whether the sprite has feet with which it walks (this matters for friction)
        self.lastPressed = None  # The key, out of left or right, that was pressed last frame
        self.flipped     = False # False means the sprite's image looks as loaded (facing right, probably), and True means it is flipped the other way (facing left, probably)
        self.solid       = False # setting this to true will make the sprite interact with other sprites as though it is solid
        self.supported   = False # whether there is something for the player to jump off of
        self.lrvel       = 0     # added velocity from controls
    def tileTouchAction(self,tile):
        # the player is unaffected by horizontal friction, and can jump off of stuff below him
        sides,self = tile.collision(self)
        if 'top' in sides:
            self.supported = True
    def spriteTouchActian(self,sprite):
        # ditto from tileTouchAction()
        sides,self = tile.collision(self)
        if 'top' in sides:
            self.supported = True
    def locomotion(self):
        self.lrvel = 0 # added momentum from pressing left and right: see below
        lkey,rkey = pygame.key.get_pressed()[K_LEFT],pygame.key.get_pressed()[K_RIGHT]
        if not (lkey or rkey):
            self.lastPressed = None
        elif lkey and not rkey:
            self.lrvel = -3.
            if not self.flipped:
                self.img = pygame.transform.flip(self.img,True,False)
            self.flipped = True
            self.lastPressed = K_LEFT
        elif not lkey and rkey:
            self.lrvel = 3.
            if self.flipped:
                self.img = pygame.transform.flip(self.img,True,False)
            self.flipped = False
            self.lastPressed = K_RIGHT
        elif lkey and rkey:
            if self.lastPressed == K_LEFT:
                self.lrvel = 4.
                if self.flipped:
                    self.img = pygame.transform.flip(self.img,True,False)
                self.flipped = False
            elif self.lastPressed == K_RIGHT:
                self.lrvel = -4.
                if not self.flipped:
                    self.img = pygame.transform.flip(self.img,True,False)
                self.flipped = True
        if pygame.key.get_pressed()[K_UP] and self.supported:
            self.vel.y += 6.
        self.supported = False
    def move(self,env):
        self.pos.x += self.lrvel
        self = env.move(self)
