#!/usr/bin/python
#
# RELATIVISTIC SUN
# by Michael Szegedy

import pygame,sys,world
from collections import deque
from consts import *
from sprites import player
from vec import vec
from pygame.locals import *

class camera:
    # for containing the block and position of the camera
    def __init__(self):
        self.blk = vec(0,0) # index of block in which the camera resides
        self.pos = vec(0,0) # position relative to bottom left corner of camera window

# Start game
pygame.init()
screen = pygame.display.set_mode((SCRX,SCRY)) # create the screen
pygame.display.set_caption('Relativistic Sun') # give the screen's window a title
# Create deque of onscreen items
player = player()
loaded = deque(()) # The first level of recursion contains deques of vertical columns of blocks, and each deque contains the blocks in a column arranged bottom to top
for i in xrange(-2,3):
    loaded.append(deque())
    for j in xrange(-2,3):
        col = loaded.pop()
        col.append(world.getBlock(player.blk+vec(i,j)))
        loaded.append(col)
while True:
#    print 'NEW ITERATION:\n',loaded
    # Check whether to quit or not
    for event in pygame.event.get():
        if event.type == QUIT: sys.exit()
    #########################################
    # make stuff interact with other stuff! #
    #########################################
    # load the player's environment into a trio of lists so that they can interact
    tiles,oldsprites,envtable = [], [], [[],[],[],[],[]]
    for i in xrange(5):
        col = loaded.popleft()
        for j in xrange(5):
            blk = col.popleft()
            tiles.extend(blk.tiles)
            oldsprites.extend(blk.sprites)
            envtable[i].append(blk.env)
            col.appendleft(blk)
            col.rotate(-1)
        loaded.appendleft(col)
        loaded.rotate(-1)
    # start interacting!
    newsprites = oldsprites
    for sprite in newsprites+[player]:
#        print '\n\nSPRITE:',sprite
#        print 'STEP Z:\nF =',sprite.F,'\nvel =',sprite.vel,'\npos =',sprite.pos,'\nblk =',sprite.blk
        sprite.environmentAction(envtable[int(sprite.blk.x-player.blk.x+2)][int(sprite.blk.y-player.blk.y+2)])
#        print 'STEP A:\nF =',sprite.F,'\nvel =',sprite.vel,'\npos =',sprite.pos,'\nblk =',sprite.blk
        for tile in tiles:
#            print 'STEP B USING',tile,':\nF =',sprite.F,'\nvel =',sprite.vel,'\npos =',sprite.pos,'\nblk =',sprite.blk
            sprite.tileDistanceAction(tile)
        for oldsprite in oldsprites:
#            print 'STEP C USING',oldsprite,': F =',sprite.F,'\nvel =',sprite.vel,'\npos =',sprite.pos,'\nblk =',sprite.blk
            sprite.spriteDistanceAction(oldsprite)
        sprite.move(envtable[int(player.blk.x-sprite.blk.x+2)][int(player.blk.x+2)])
#        print 'STEP D:\nF =',sprite.F,'\nvel =',sprite.vel,'\npos =',sprite.pos,'\nblk =',sprite.blk
        for tile in tiles:
            sprite.tileTouchAction(tile)
#            print 'STEP E USING',tile,':\nF =',sprite.F,'\nvel =',sprite.vel,'\npos =',sprite.pos,'\nblk =',sprite.blk
        for oldsprite in oldsprites:
            sprite.spriteTouchAction(oldsprite)
#            print 'STEP F USING',oldsprite,':\nF =',sprite.F,'\nvel =',sprite.vel,'\npos =',sprite.pos,'\nblk =',sprite.blk
        sprite.locomotion()
#        print 'STEP G:\nF =',sprite.F,'\nvel =',sprite.vel,'\npos =',sprite.pos,'\nblk =',sprite.blk
        sprite.moveAgain(envtable[int(player.blk.x-sprite.blk.x+2)][int(player.blk.x+2)])
#        print 'STEP H:\nF =',sprite.F,'\nvel =',sprite.vel,'\npos =',sprite.pos,'\nblk =',sprite.blk
#    print loaded
    # store the modified sprites
    for i in xrange(-2,3):
        col = loaded.popleft()
        for j in xrange(-2,3):
            blk = col.popleft()
            blk.sprites = []
            for index,sprite in enumerate(newsprites):
                if sprite.blk == player.blk+vec(i,j):
                    blk.sprites.append(sprite)
                    del newsprites[index]
            col.appendleft(blk)
            col.rotate(-1)
        loaded.appendleft(col)
        loaded.rotate(-1)
    ######################################################
    # load new blocks if the player has gone off-center! #
    ######################################################
    loaded.rotate(2)
    col = loaded.pop()
    col.rotate(2)
    blk = col.pop() # the symmetry
    col.append(blk) # is beautiful
    col.rotate(-2)
    loaded.append(col)
    loaded.rotate(-2)
#    print loaded
    if player.blk != blk.i:
        if player.blk.y-blk.i.y >= 1:
            for k in xrange(-2,3):
                col = loaded.pop()
                col.popleft()
                col.append(world.getBlock(player.blk+vec(k,2)))
                loaded.append(col)
                loaded.rotate(1)
        if player.blk.y-blk.i.y <= -1:
            for k in xrange(-2,3):
                col = loaded.pop()
                col.pop()
                col.appendleft(world.getBlock(player.blk+vec(k,-2)))
                loaded.append(col)
                loaded.rotate(1)
        if player.blk.x-blk.i.x >= 1:
            loaded.popleft()
            col = deque(())
            for k in xrange(-2,3):
                col.append(world.getBlock(player.blk+vec(2,k)))
            loaded.append(col)
        if player.blk.x-blk.i.x <= -1:
            loaded.pop()
            col = deque(())
            for k in xrange(-2,3):
                col.appendleft(world.getBlock(player.blk+vec(-2,k)))
            loaded.appendleft(col)
    ###############################
    # now just render everything! #
    ###############################
    # load relevant sprites, images, and indices into lists for rendering
    sprites,bgimages,fgimages,indextable = [], [], [], [[],[],[]]
    loaded.rotate(-1)
    for i in xrange(3):
        col = loaded.popleft()
        col.rotate(-1)
        for j in xrange(3):
            blk = col.popleft()
            sprites.extend(blk.sprites)
            bgimages.extend(blk.bgimages)
            fgimages.extend(blk.fgimages)
            indextable[i].append(blk.i)
            col.appendleft(blk)
            col.rotate(-1)
        col.rotate(-1)
        loaded.appendleft(col)
        loaded.rotate(-1)
    loaded.rotate(-1)
    # make the camera
    cam = camera()
    # set camera x position
    if indextable[0][1].x == None and player.pos.x < SCRX/2:
        cam.pos.x = player.pos.x/2.
        #cam.pos.x = 0
    elif indextable[2][1].x == None and player.pos.x+player.dim.y > BLKX-SCRX:
        cam.pos.x = (BLKX+player.pos.x-SCRX)/2.
        #cam.pos.x = BLKX-SCRX
    else:
        cam.pos.x = player.pos.x-SCRX/2.
    # set camera y position
    if indextable[1][0].y == None and player.pos.y < SCRY/2:
        cam.pos.y = player.pos.y/2.
        #cam.pos.y = 0
    elif indextable[1][2].y == None and player.pos.y+player.dim.y > BLKY-SCRY:
        cam.pos.y = (BLKY+player.pos.y-SCRY)/2.
        #cam.pos.y = BLKY-SCRY
    else:
        cam.pos.y = player.pos.y-SCRY/2.
    # fix camera positions if it has gone outside of the player's block
    if not (0 <= cam.pos.x and cam.pos.x < BLKX):
        offset = cam.pos.x//BLKX
        cam.blk.x += offset
        cam.pos.x -= offset*BLKX
    if not (0 <= cam.pos.y and cam.pos.y < BLKY):
        offset = cam.pos.y//BLKY
        cam.blk.y += offset
        cam.pos.y -= offset*BLKY
    # actually start drawing!
    screen.fill((230,230,255))
    for item in bgimages+sprites+[player]+fgimages:
        try:
            screen.blit(item.img,(int((item.blk.x-cam.blk.x)*BLKX+item.pos.x-cam.pos.x),int(SCRY-((item.blk.y-cam.blk.y)*BLKY+item.pos.y+item.img.get_height()-cam.pos.y))))
        except TypeError:
            pass
    pygame.display.update()
    pygame.time.delay(25)
