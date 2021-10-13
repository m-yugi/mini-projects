#import and initialization
from os import pipe
import pygame
from sys import exit
from pygame import time
import random

from pygame.constants import K_RETURN
from pygame.display import get_active
from pygame.transform import rotate
#pygame.mixer.pre_init(frequency=44100,size=16,channels=1,buffer=512  )
pygame.init()
#all functions
def draw_floor():
    screen.blit(floor,(floor_move,800))
    screen.blit(floor,(floor_move+576,800))
#gap pls
def draw_bg():
    screen.blit(sky,(bg_move,0))
    screen.blit(sky,(bg_move-576,0))
#gap pls
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx-=5
    return pipes
#gap pls
def draw_pipes(pipes_list):
    for pipe in pipes_list:
        if pipe.bottom>=800:
            screen.blit(pipes,pipe)
        else:
            flip_pipe=pygame.transform.flip(pipes,False,True)
            screen.blit(flip_pipe,pipe)
#gap pls
def create_pipes():
    random_pipe=random.choice(pipe_hights)
    bottom_pipes=pipes.get_rect(midtop=(700,random_pipe))
    top_pipes=pipes.get_rect(midbottom=(700,random_pipe-300))
    return bottom_pipes,top_pipes
#gap pls
def check_collision(pipe_list):
    for pipe in pipe_list:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rect.top<=-100 or bird_rect.bottom>=900:
        return False
    return True
#gap_pls
def rotate_bird(bird):
    new_bird=pygame.transform.rotozoom(bird,-bird_movement*3,1) 
    return new_bird
#gap pls
def bird_anime():
    new_bird=bird_list[bird_index]
    new_bird_rect=new_bird.get_rect(center=(100,bird_rect.centery))
    return new_bird,new_bird_rect
#gap pls
def update_score(score,high_score):
    if score>high_score:
        high_score=score
    return high_score
#gap pls
def score_display(game_state):
    if game_state=='main_game':
        score_surf=game_font.render(str(int(score)),True,(255,255,255))
        score_rect=score_surf.get_rect(center=(288,100))
        screen.blit(score_surf,score_rect)
    if game_state=='game_over':
        score_surf=game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect=score_surf.get_rect(center=(288,100))
        screen.blit(score_surf,score_rect)

        high_score_surf=game_font.render(f'High Score: {int(high_score)}',True,(255,255,255))
        high_score_rect=score_surf.get_rect(center=(200,700))
        screen.blit(high_score_surf,high_score_rect)
#gap pls
clock=pygame.time.Clock()
screen=pygame.display.set_mode((576,1024))
pygame.display.set_caption('fly boie')
#game variables
gravity=0.25 
bird_movement=0
game_active=True
score=0
high_score=0
#font
game_font=pygame.font.Font('flappy bird/04B_19.TTF',40)
#background
sky=pygame.image.load('flappy bird/assets/background-day.png').convert_alpha()
sky=pygame.transform.rotozoom(sky,0,2)
bg_move=0
#floor
floor=pygame.image.load('flappy bird/assets/base.png').convert_alpha()
floor=pygame.transform.rotozoom(floor,0,2)
floor_move=0
#flappy bird
bird_downdlap=pygame.transform.rotozoom(pygame.image.load('flappy bird/assets/bluebird-downflap.png'),0,2).convert_alpha()
bird_midflap=pygame.transform.rotozoom(pygame.image.load('flappy bird/assets/bluebird-midflap.png'),0,2).convert_alpha()
bird_upflap=pygame.transform.rotozoom(pygame.image.load('flappy bird/assets/bluebird-upflap.png'),0,2).convert_alpha()
bird_list=[bird_downdlap,bird_midflap,bird_upflap]
bird_index=0
bird=bird_list[bird_index]
bird_rect=bird.get_rect(center=(100,512))
bird_event=pygame.USEREVENT+1
pygame.time.set_timer(bird_event,200)
#bird=pygame.image.load('flappy bird/assets/bluebird-midflap.png').convert_alpha()
#bird=pygame.transform.rotozoom(bird,0,2)
#bird_rect=bird.get_rect(center=(100,512))

#pipes
pipes=pygame.image.load('flappy bird/assets/pipe-green.png').convert_alpha()
pipes=pygame.transform.rotozoom(pipes,0,2)
pipes_list=[]
pipe_timer=pygame.USEREVENT
pygame.time.set_timer(pipe_timer,1200)
pipe_hights=[200,400,600,800]

game_overlay=pygame.transform.rotozoom(pygame.image.load('flappy bird/assets/message.png').convert_alpha(),0,2)
game_overlay_rect=game_overlay.get_rect(center=(288,400))
#muzicuu
flap_sound=pygame.mixer.Sound('flappy bird/sound/sfx_wing.wav')
death_sound=pygame.mixer.Sound('flappy bird/sound/sfx_hit.wav')
score_sound=pygame.mixer.Sound('flappy bird/sound/sfx_point.wav')
score_sound_count=100
#game loop
while True:
    #event manager
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
        if event.type==pipe_timer:
            pipes_list.extend(create_pipes())
        if event.type==bird_event:
            if bird_index<2:
                bird_index+=1
            else:
                bird_index=0
            bird,bird_rect=bird_anime()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE and game_active:
                bird_movement=0
                bird_movement-=12
                flap_sound.play()
            if event.key==pygame.K_RETURN and game_active==False:
                score=0
                game_active=True
                pipes_list.clear()
                bird_rect.center=(100,512)
                bird_movement=0
    #bg screen
    bg_move+=1
    draw_bg()
    if bg_move>=576:
        bg_move=0
    if game_active:
        #pipes
        pipes_list=move_pipes(pipes_list)
        draw_pipes(pipes_list)
        score+=0.01
        score_display('main_game')
        score_sound_count -=1
        if score_sound_count<=0:
            score_sound.play()
            score_sound_count=100
    #flappy bird
        bird_movement+=gravity
        rotated_bird=rotate_bird(bird)
        bird_rect.centery+=bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active=check_collision(pipes_list)
    else:
        screen.blit(game_overlay,game_overlay_rect)
        high_score=update_score(score,high_score)
        score_display('game_over')
    #floor screen
    floor_move-=1
    draw_floor()
    if floor_move<= -576:
        floor_move=0
    pygame.display.update()
    clock.tick(120)