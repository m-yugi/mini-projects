#from _typeshed import Self
import pygame
from random import randint
from sys import exit
from pygame import K_SPACE
from pygame import key
from pygame.constants import K_RETURN
pygame.init()

#class player(pygame.sprite.Sprite()):
#    def __init__(self):
#        super().__init__()
#        boie_walk=pygame.image.load('jump_boie/graphics/Player/player_walk_1.png').convert_alpha()
#        boie_walk2=pygame.image.load('jump_boie/graphics/Player/player_walk_2.png').convert_alpha()
#        self.player_list=[boie_walk,boie_walk2]
#
#        self.player_index=0
#
#        self.player_jump=pygame.image.load('jump_boie/graphics/Player/jump.png').convert_alpha()
#        self.image=self.player_list[self.player_index]
#        self.rect=self.image.get_rect(midbottom=(200,300))
#        self.gravity= 0
#        def player_input(self):
#            keys=pygame.key.get_pressed()
#            if keys[pygame.K_SPACE] and self.rect.bottom>=300:
#                self.gravity=-20
#        def animation(self):
#           
#        def apply_gravity(self):
#            self.gravity+=1
#            self.rect.y+=self.gravity
#            if self.rect.bottom >=300:
#                self.rect.bottom=300
#        def update(self):
#            self.player_input()
#            self.apply_gravity()
def display_score():
    curr_time=int(pygame.time.get_ticks()/1000)-start_time
    score_surf=testfont.render(f'SCORE : {curr_time}',False,(64,64,64))
    score_rect=score_surf.get_rect(center=(400,100))
    screen.blit(score_surf,score_rect)
    return curr_time

def obstical_movement(obstical_list):
    if obstical_list:
        for obst in obstical_list:
            obst.right -=5 
            if obst.bottom==300:
                screen.blit(snail_surf,obst)
            else:
                screen.blit(fly_surf,obst)
        obstical_list=[obst for obst in obstical_list if obst.right> -100]
        return obstical_list
    else: return []

def collisions(player,obsticals):
    if obsticals:
        for obst in obsticals:
            if(player.colliderect(obst)): return False
    return True

def player_anime():
    global player_surf,player_index

    if player1.bottom <300:
        player_surf=player_jump
    else:
        player_index +=0.1
        if player_index >=len(player_list): player_index=0
        player_surf=player_list[int(player_index)]

screen=pygame.display.set_mode((800,400))

pygame.display.set_caption('jump boie')

clock=pygame.time.Clock()

testfont=pygame.font.Font('jump_boie/font/Pixeltype.ttf',50)

sky=pygame.image.load('jump_boie/graphics/sky.png').convert_alpha()

ground=pygame.image.load('jump_boie/graphics/ground.png').convert_alpha()

snail=pygame.image.load('jump_boie/graphics/snail/snail1.png').convert_alpha()

snail2=pygame.image.load('jump_boie/graphics/snail/snail2.png').convert_alpha()

snail_list=[snail,snail2]

snail_index=0

snail_surf=snail_list[snail_index]

boie_walk=pygame.image.load('jump_boie/graphics/Player/player_walk_1.png').convert_alpha()

boie_walk2=pygame.image.load('jump_boie/graphics/Player/player_walk_2.png').convert_alpha()

player_list=[boie_walk,boie_walk2]

player_index=0

player_jump=pygame.image.load('jump_boie/graphics/Player/jump.png').convert_alpha()

player_surf=player_list[player_index]

player1=boie_walk.get_rect(midbottom=(80,300))

player_stand=pygame.image.load('jump_boie/graphics/Player/player_stand.png').convert_alpha()

player_stand=pygame.transform.rotozoom(player_stand,0,2)

stand_rect=player_stand.get_rect(center=(400,200))

#player2=pygame.sprite.GroupSingle()
#player2.add(player())

gravity=0

game_active=False

start_time=0

realscore=0


fly=pygame.image.load('jump_boie/graphics/fly/fly1.png').convert_alpha()

fly2=pygame.image.load('jump_boie/graphics/fly/fly2.png').convert_alpha()

fly_list=[fly,fly2]

fly_index=0

fly_surf=fly_list[fly_index]

obstical=[]

text=testfont.render('jump boieeeee',False,(64,64,64))

text_surf=text.get_rect(center=(400,50))

score=testfont.render('score',False,(64,64,64))

score_surf=score.get_rect(center=(400,100))

game_start=testfont.render('press enter to start ',False,(64,64,64))

game_rect=game_start.get_rect(center=(400,350))

game_sound=pygame.mixer.Sound('jump_boie/audio/music.wav')
game_sound.set_volume(0.1)
game_sound.play(loops=-1)
jump_sound=pygame.mixer.Sound('jump_boie/audio/jump.mp3')
jump_sound.set_volume(0.4)
timer=pygame.USEREVENT+1

pygame.time.set_timer(timer,1500)

snail_timer=pygame.USEREVENT+2
pygame.time.set_timer(snail_timer,500)

fly_timer=pygame.USEREVENT+3
pygame.time.set_timer(fly_timer,200)

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            #game_sound.play()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE and player1.bottom>=300:
                    gravity=-20
                    jump_sound.play()
            if event.type==pygame.MOUSEBUTTONDOWN:
                if player1.collidepoint(event.pos) and player1.bottom>=300:
                    gravity=-20
            if event.type==pygame.MOUSEBUTTONDOWN:
                if player1.bottom>=300:
                    gravity=-20
        else:
            if event.type==pygame.KEYDOWN and event.key==K_RETURN:
                start_time=int(pygame.time.get_ticks()/1000)
                game_active=True
        if game_active:
            if event.type==timer:
                if randint(0,2):
                    obstical.append(snail.get_rect(midbottom=(randint(900,1100),300)))
                else:
                    obstical.append(fly.get_rect(bottomright=(randint(900,1100),200)))
            if event.type==snail_timer:
                if snail_index==0:
                    snail_index=1
                else:
                    snail_index=0
                snail_surf=snail_list[snail_index]
            if event.type==fly_timer:
                if fly_index==0:
                    fly_index=1
                else:
                    fly_index=0
                fly_surf=fly_list[fly_index]
    if game_active:
        #basic back ground
        screen.blit(sky,(0,0))
        screen.blit(ground,(0,300))
        realscore=display_score()
        #player mechanics
        gravity+=1
        player1.y+=gravity
        if player1.bottom>=300: player1.bottom=300
        player_anime()
        screen.blit(player_surf,player1)
        #player2.draw(screen)
        #player2.update()
        #obstical movment
        obstical=obstical_movement(obstical)

        # collisions
        game_active=collisions(player1,obstical)

    else:
        obstical.clear()
        player1.midbottom=(80,300)
        gravity=0
        game_score=testfont.render(f'your score is : {realscore}',False,(64,64,64))
        score_rect=game_score.get_rect(center=(400,350))
        screen.fill((250,174,230))
        screen.blit(player_stand,stand_rect)
        screen.blit(text,text_surf)

        if realscore>0: screen.blit(game_score,score_rect)
        else: screen.blit(game_start,game_rect)
        
    pygame.display.update()
    clock.tick(60)