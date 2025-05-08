import pygame, sys, math
from pytmx.util_pygame import load_pygame
from spread_sheet import *
from random import randint
from pygame import VIDEORESIZE
from Timer import Timer

# classes
class Player (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.degree=0
        self.animation_index = 0
        self.player_state = 0
        self.spreadsheet = SpriteSheet('Graphics/Player/player_sprite_sheet.png')
        sprite = self.spreadsheet.get_image(0, 0, 90, 90, 'black')

        self.player_rect = sprite.get_rect(center=(screen_w/2, screen_h/2))
        self.player_dest_camera = pygame.Rect(screen_w/2, screen_h/2, 90, 90)
        self.time= 1000
        self.spell_cooldown_timer= Timer(self.time)
        self.spell_cooldown_timer.deactivate()
        self.spell=Spells(self.player_dest_camera, self.player_rect)
        camera_group = CameraGroup()
        self.warp_points_rect_list = []

    def player_input(self):
        global  player_pos
        keys = pygame.key.get_pressed()
        mouse_state = pygame.mouse.get_pressed()
        temp_pos = self.aim()
        mouse_list = [None]*10
        player_pos = self.player_rect
        if keys[pygame.K_w]:
            if not self.player_rect.top <= -2750 and self.player_dest_camera.top <= 465:
                self.player_rect.top -= 10
            else:
                self.player_dest_camera.top -=10

        if keys[pygame.K_s]:
            if not self.player_rect.bottom >= 800 and self.player_dest_camera.top >= 465:
                self.player_rect.bottom += 10
            else:
                self.player_dest_camera.bottom +=10

        if keys[pygame.K_a]:
            if not self.player_rect.left <= 165 and self.player_dest_camera.left <= 915:
                self.player_rect.left -= 10
            else:
                self.player_dest_camera.left -=10
        if keys[pygame.K_d]:
            if not self.player_rect.right >=1375 and self.player_dest_camera.left >=915:
                self.player_rect.right += 10
            else:
                self.player_dest_camera.right +=10


        self.spell_cooldown_timer.update()
        if not self.spell_cooldown_timer.active:

            if mouse_state[0] and not self.spell_cooldown_timer.active:
                mouse_list[0]= pygame.mouse.get_pos()
                self.spell.fireball(mouse_list, temp_pos)
                self.spell_cooldown_timer.activate()

            if mouse_state[2] and not self.spell_cooldown_timer.active:
                mouse_list[1]= pygame.mouse.get_pos()
                self.spell.water_attack(mouse_list, temp_pos)
                self.spell_cooldown_timer.activate()

        else:
            if keys[pygame.K_c]:
                spell_surf = pygame.image.load('Graphics/spells/spell.png').convert()
                spell_rect = spell_surf.get_rect(center = ( temp_pos[0], temp_pos[1]))
                screen.blit(spell_surf, spell_rect)
            if keys[pygame.K_v]:
                pygame.draw.rect(screen, '#117bf5', pygame.Rect(spell_direction[0], spell_direction[1], 50, 50))
            if keys[pygame.K_b]:
                pygame.draw.rect(screen, '#3b9c4e', pygame.Rect(spell_direction[0], spell_direction[1], 50, 50))
        self.spell.update()

    def collision (self):
        global map_id
        if self.player_rect.bottom >= 800:
            self.player_rect.bottom = 800
            if self.player_dest_camera.bottom >= 890:
                self.player_dest_camera.bottom = 890
        if self.player_rect.top <= -2750:
            self.player_rect.top= -2750
            if self.player_dest_camera.top <= 50:
                self.player_dest_camera.top = 50
        if self.player_rect.left <= 165:
            self.player_rect.left = 165
            if self.player_dest_camera.left <=120:
                self.player_dest_camera.left =120
        if self.player_rect.right >= 1375:
            self.player_rect.right= 1375
            if self.player_dest_camera.right >=1945:
                self.player_dest_camera.right = 1945

    def animation_state(self):
        animation_list = []
        animation_steps = [1, 1, 1, 1, 2, 2, 2, 2]
        step_counter = 0
        for animation in animation_steps:
            temp_img_list = []
            for _ in range(animation):
                temp_img_list.append(self.spreadsheet.get_image(step_counter * 90, 0, 90, 90, 'black'))
                step_counter += 1
            animation_list.append(temp_img_list)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_w] or keys[pygame.K_d]:
            self.animation_index += 0.05

        if self.animation_index >= len(animation_list[self.player_state]):
            self.animation_index = 0
        if keys[pygame.K_a]:
            self.player_state = 7
        if keys[pygame.K_d]:
            self.player_state = 5
        if keys[pygame.K_s]:
            self.player_state = 4
        if keys[pygame.K_w]:
            self.player_state = 6
        if self.player_rect.bottom >= 800 or self.player_rect.top <= -525 or self.player_rect.left <= 165 or self.player_rect.right >= 1375:
            screen.blit(animation_list[int(self.player_state)][int(self.animation_index)], self.player_dest_camera)
        else:
            screen.blit(animation_list[int(self.player_state)][int(self.animation_index)], self.player_dest_camera)

    def aim(self):
        mouse_pos = [pygame.mouse.get_pos()]
        if mouse_pos[0][1] > self.player_dest_camera.centery:
            self.degree= math.asin((self.player_dest_camera.centerx - mouse_pos[0][0]) /
                              math.sqrt(pow((self.player_dest_camera.centerx - mouse_pos[0][0]), 2)
                                        + pow((mouse_pos[0][1] - self.player_dest_camera.centery ), 2)))

            temp_pos = [int(self.player_rect.centerx - 100 * math.sin(self.degree)),
                        int(self.player_rect.centery + 100 * math.cos(self.degree))]
        else:
            self.degree = math.asin((mouse_pos[0][0] - self.player_dest_camera.centerx) / math.sqrt(
                pow((mouse_pos[0][0] - self.player_dest_camera.centerx), 2) + pow((self.player_dest_camera.centery - mouse_pos[0][1]), 2)))
            temp_pos = [int(100 * math.sin(self.degree) + self.player_rect.centerx),
                        int(self.player_rect.centery - 100 * math.cos(self.degree))]

            return temp_pos

        return temp_pos

    def update(self):
        self.player_input()
        self.animation_state()
        self.collision()

class Spells (pygame.sprite.Sprite):
    def __init__ (self, player_pos, player_rect):
        super().__init__()
        self.fireball_surf = pygame.image.load('Graphics/spells/spell.png').convert_alpha()
        fireball_rect = self.fireball_surf.get_rect(center=(-100, -100))
        self.water_surf = pygame.image.load('Graphics/spells/spell_1.png').convert_alpha()
        water_rect = self.water_surf.get_rect(center=(-100, -100))
        self.sprite = pygame.image.load('Graphics/spells/spell.png').convert()
        self.degree_list = [[0.0,0.0], [0.0,0.0]]
        self.spell_rect_list = [fireball_rect, water_rect]
        self.spell_activity = [0]*3
        self.mouse_pos =0
        self.player_pos = player_pos
        self.player_rect = player_rect
        self.spell_call = [False, False, False]
        self.offset = pygame.math.Vector2()

    def fireball(self, mouse_list, position):
        self.sprite = self.fireball_surf
        fireball_rect = self.fireball_surf.get_rect(center=(position[0], position[1]))
        self.spell_rect_list [0] = fireball_rect
        if mouse_list[0]:
            self.spell_call[0] = True
            self.spell_activity[0] = 1
            self.mouse_pos = mouse_list[0]
        self.degree_calc( self.mouse_pos)
        self.spell_movement()

    def water_attack(self, mouse_list, position):
        self.sprite = self.water_surf
        water_rect = self.water_surf.get_rect(center=(position[0], position[1]))
        self.spell_rect_list [1] = water_rect
        if mouse_list[1]:
            self.spell_call[1] = True
            self.spell_activity[1] = 2
            self.mouse_pos = mouse_list[1]
        self.degree_calc( self.mouse_pos)
        self.spell_movement()


    def degree_calc (self, mouse_pos):
        if self.spell_call [0]:
            self.degree_list[0][0] = math.asin((self.player_pos.centery - mouse_pos[1]) / math.sqrt(pow((self.player_pos.centerx - mouse_pos[0]), 2) + pow((mouse_pos[1] - self.player_pos.centery), 2))) #sin
            self.degree_list[0][1] = math.acos((mouse_pos[0] - self.player_pos.centerx) / math.sqrt(pow((self.player_pos.centerx - mouse_pos[0]), 2) + pow((mouse_pos[1] - self.player_pos.centery), 2))) #cos
            self.spell_call[0] = False
        if self.spell_call[1]:
            self.degree_list[1][0] = math.asin((self.player_pos.centery - mouse_pos[1]) / math.sqrt(pow((self.player_pos.centerx - mouse_pos[0]), 2) + pow((mouse_pos[1] - self.player_pos.centery), 2)))
            self.degree_list[1][1] = math.acos((mouse_pos[0] - self.player_pos.centerx) / math.sqrt(pow((self.player_pos.centerx - mouse_pos[0]), 2) + pow((mouse_pos[1] - self.player_pos.centery), 2)))
            self.spell_call[1] = False
        # print(math.degrees(self.degree_list[0][0]))
        # print(math.degrees(self.degree_list[0][1]))

    def spell_movement(self):
        self.offset.x = self.player_rect.centerx - screen_w/2
        self.offset.y = self.player_rect.centery - screen_h/2
        if self.spell_activity[0] ==1:
            spell_surf = pygame.transform.rotozoom(self.fireball_surf, 0, 1.5)
            if self.mouse_pos[1] < self.player_pos.centery:

                self.spell_rect_list[0][0] += 10*math.cos(self.degree_list[0][1])
                self.spell_rect_list[0][1] -= 10*math.sin(self.degree_list[0][0])
            else:

                self.spell_rect_list[0][0] += 10 * math.cos(self.degree_list[0][1])
                self.spell_rect_list[0][1] -= 10 * math.sin(self.degree_list[0][0])

            screen.blit(spell_surf, self.spell_rect_list[0].center -self.offset )

        if self.spell_activity[1] ==2:

            if self.mouse_pos[1] < self.player_pos.centery:
                self.spell_rect_list[1][0] += 10*math.cos(self.degree_list[1][1])
                self.spell_rect_list[1][1] -= 10*math.sin(self.degree_list[1][0])
                spell_surf = pygame.transform.rotozoom(self.water_surf,  math.degrees(self.degree_list[1][1]), 1.5)
            else:
                self.spell_rect_list[1][0] += 10 * math.cos(self.degree_list[1][1])
                self.spell_rect_list[1][1] -= 10 * math.sin(self.degree_list[1][0])
                spell_surf = pygame.transform.rotozoom(self.water_surf, - math.degrees(self.degree_list[1][1]), 1.5)

            screen.blit(spell_surf,self.spell_rect_list[1].center -self.offset)

    def update(self):
        self.spell_movement()

class Tiles (pygame.sprite.Sprite):
    def __init__ (self, pos, surf, groups):
        super().__init__(groups)
        self.image = pygame.transform.rotozoom(surf, 0, 3)
        self.rect = self.image.get_rect(topleft = pos)

class CameraGroup (pygame.sprite.Group):
    def __init__ (self):
        super().__init__()
        self.offset = pygame.math.Vector2(750, 3250)
        self.half_w = screen.get_size()[0]//2
        self.half_h = screen.get_size()[1]//2
        self.offset_pos = pygame.math.Vector2()

    def center_target_camera(self, target):
        self.offset.x = target.centerx - self.half_w +750
        self.offset.y = target.centery - self.half_h +3250

    def warp_points(self):
        for obj in tmx_data.objects:
            pos = obj.x, obj.y
            if obj.type == 'warp':
                rect = pygame.Rect(obj.x * 3 - self.offset.x, obj.y * 3 - self.offset.y, obj.width * 3, obj.height * 3)

    def custom_draw(self, screen, player):
        self.center_target_camera(player)

        for sprite in sprite_group.sprites():
            self.offset_pos =  sprite.rect.topleft - self.offset
            screen.blit(sprite.image, self.offset_pos)

    def custom_draw_foreground(self, screen):

        self.offset_pos = (foreground_group.sprites()[1].rect.x, foreground_group.sprites()[1].rect.y+2250) - self.offset
        screen.blit(foreground_group.sprites()[1].image, self.offset_pos)
        screen.blit(foreground_group.sprites()[3].image, self.offset_pos)
        self.offset_pos = (foreground_group.sprites()[1].rect.x, foreground_group.sprites()[1].rect.y) - self.offset
        screen.blit(foreground_group.sprites()[1].image, self.offset_pos)
        screen.blit(foreground_group.sprites()[3].image, self.offset_pos)

# env, background
def home_screen(a, b):
    global button_quit, button_options, button_play
    if a > 1440 and b >765:
        screen.blit(pygame.image.load('Graphics/env/Game_name.png'), (a*0.025, b*0.05))
        button_play = screen.blit(pygame.image.load('Graphics/env/button_start.png'), (a*0.025 +250, b*0.392))
        button_options = screen.blit(pygame.image.load('Graphics/env/button_option.png'), (a*0.025 +250, b*0.588))
        button_quit = screen.blit(pygame.image.load('Graphics/env/button_quit.png'), (a*0.025 +250, b*0.784))
    else:
        screen.blit(pygame.transform.rotozoom(pygame.image.load('Graphics/env/Game_name.png'), 0, 0.5), (a*0.025, b*0.05))
        button_play = screen.blit(pygame.transform.rotozoom(pygame.image.load('Graphics/env/button_start.png'), 0, 0.5), (a*0.025 +50, b*0.392))
        button_options = screen.blit(pygame.transform.rotozoom(pygame.image.load('Graphics/env/button_option.png'), 0, 0.5), (a*0.025 +50, b*0.588))
        button_quit= screen.blit(pygame.transform.rotozoom(pygame.image.load('Graphics/env/button_quit.png'), 0, 0.5), (a*0.025 +50, b*0.784))

    return  button_quit, button_options, button_play

def option_screen ():
    global button_2_rect, button_2_surf

    option_background=pygame.image.load('Graphics/env/options_background.png').convert_alpha()
    option_background = pygame.transform.scale(option_background, (int(pygame.display.Info().current_w), int(pygame.display.Info().current_h)))
    screen.blit(option_background,  (0,0))

    button_1= pygame.image.load('Graphics/env/button_1.png').convert()
    button_1 = pygame.transform.scale(button_1, (int(pygame.display.Info().current_w*0.26), int(pygame.display.Info().current_h*0.099)))
    screen.blit(button_1, (400, 250))

    if mouse_use:
        button_1_text= pygame.font.Font.render(pygame.font.Font(None, 60), 'mouse', False, 'black')
        button_1_text_rect= button_1_text.get_rect(topleft=(500, 300))

        button_2_surf = pygame.image.load('Graphics/env/button_2.png').convert()
        button_2_surf = pygame.transform.scale(button_2_surf, ( int(pygame.display.Info().current_w * 0.052), int(pygame.display.Info().current_h * 0.099)))
        button_2_rect = button_2_surf.get_rect(topleft=(300, 250))

    else:
        button_1_text= pygame.font.Font.render(pygame.font.Font(None, 60),'keyboard', False, 'black')
        button_1_text_rect= button_1_text.get_rect(topleft=(500, 300))

        button_2_surf = pygame.image.load('Graphics/env/button_3.png').convert()
        button_2_surf = pygame.transform.scale(button_2_surf, (
        int(pygame.display.Info().current_w * 0.052), int(pygame.display.Info().current_h * 0.099)))
        button_2_rect = button_2_surf.get_rect(topleft=(900, 250))

    screen.blit(button_1_text, button_1_text_rect)
    screen.blit(button_2_surf, button_2_rect)

    return option_background, button_1, button_2_surf, button_1_text

def game_screen(a, b):
    screen1= pygame.draw.rect(screen, '#43b52f', pygame.Rect(0,0, a, b))
    health = pygame.draw.rect(screen, '#f71634', pygame.Rect(0,0, 500, 100))

def enviroment_movement (env_list):
    if env_list:
        for env_rect in env_list:
            env_rect.x -= 5
            screen.blit(cloud_sprites[0], env_rect)

        env_list = [env for env in env_list if env.x >-300]

        return env_list
    else: return []

clock = pygame.time.Clock()
pygame.init()

monitor_size= [pygame.display.Info().current_w, pygame.display.Info().current_h]
screen_w = monitor_size[0]
screen_h = monitor_size[1] - 60
screen = pygame.display.set_mode((screen_w, screen_h), pygame.RESIZABLE)
button_quit=pygame.rect.Rect(0,0,0,0)
button_options=pygame.rect.Rect(0,0,0,0)
button_play=pygame.rect.Rect(0,0,0,0)
button_2_rect = pygame.rect.Rect(0,0,0,0)
button_2_surf= pygame.surface.Surface((0,0))
spell_direction= []

# Clouds
cloud_surf_1 = pygame.image.load('Graphics/env/cloud.png').convert_alpha()
cloud_surf_2 = pygame.image.load('Graphics/env/cloud_1.png').convert_alpha()
cloud_sprites= [cloud_surf_1, cloud_surf_2]

# background
sky_surf = pygame.image.load('Graphics/env/Sky.png').convert()
forest_surf = pygame.transform.scale2x(pygame.image.load('Graphics/env/forest.png').convert_alpha())

envi_rect_list= []

player = pygame.sprite.GroupSingle()
player.add(Player())
player_pos = pygame.Rect(screen_w//2,screen_h//2,0,0)

tmx_data = load_pygame('Graphics/maps/map_1.tmx')
camera_group = CameraGroup()


sprite_group = pygame.sprite.Group()
foreground_group = pygame.sprite.Group()
warp_group = pygame.sprite.Group()

for layer in tmx_data.visible_layers:
    if hasattr(layer, 'data'):
        for x,y,surf in layer.tiles():
            pos = (x*90, y*90)
            Tiles(pos = pos, surf = surf, groups = sprite_group)
        for obj in tmx_data.objects:
            pos = obj.x, obj.y
            if obj.type == 'foreground':
                Tiles(pos = pos, surf = obj.image.convert_alpha(), groups=foreground_group)

game_active = False
options_active = False
mouse_use= True

fullscreen = False

# Timer
envi_timer = pygame.USEREVENT + 1
pygame.time.set_timer(envi_timer, randint(4000, 6000))

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.WINDOWSHOWN:
            for _ in range(randint(3, 5) ):
                if randint( 0, 2):
                    envi_rect_list.append(cloud_sprites[0].get_rect(midbottom=(randint(200, 1920), randint(100, 510))))
                else:
                     envi_rect_list.append(cloud_sprites[1].get_rect(midbottom=(randint(500, 1920), randint(100, 510))))

        if event.type == envi_timer:
            if randint(0, 2):
                envi_rect_list.append(cloud_surf_1.get_rect(midbottom=(randint( 1920, 2000), randint(int(pygame.display.Info().current_w*0.1), int(pygame.display.Info().current_h*0.5)) ) ) )
            else:
                envi_rect_list.append(cloud_surf_2.get_rect(midbottom=(randint( 1920, 2000), randint(int(pygame.display.Info().current_w*0.1), int(pygame.display.Info().current_h*0.5) ))))

        if event.type == VIDEORESIZE:
            if not fullscreen:
                if event.w >=960 and event.h >=510:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                else:
                    event.w = 960
                    event.h = 510
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        if event.type == pygame.KEYDOWN:
            if options_active:
                if event.key ==pygame.K_ESCAPE:
                    options_active=False
            if game_active:
                if event.key == pygame.K_ESCAPE:
                    game_active= False
            if event.key == pygame.K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), pygame.RESIZABLE)

    if game_active:
        camera_group.update()
        camera_group.custom_draw(screen, player_pos)

        camera_group.warp_points()
        player.update()
        camera_group.custom_draw_foreground(screen)

    if not game_active:
        if not options_active:
            sky_surf = pygame.transform.scale(sky_surf, (pygame.display.Info().current_w, pygame.display.Info().current_h))
            forest_surf = pygame.transform.scale(forest_surf, (pygame.display.Info().current_w, pygame.display.Info().current_h))

            screen.blit(sky_surf, (0, 0))
            envi_rect_list = enviroment_movement(envi_rect_list)
            screen.blit(forest_surf, (0, 0))
            if not fullscreen:
                if screen_w*(3/4) <= pygame.display.Info().current_w and screen_h*(3/4) <= pygame.display.Info().current_h:
                    w=pygame.display.Info().current_w
                    h=pygame.display.Info().current_h
                    home_screen(w, h)
                else:
                    w=pygame.display.Info().current_w
                    h=pygame.display.Info().current_h
                    home_screen(w, h)
            # else:
            #     w=monitor_size[0]
            #     h=monitor_size[1]
            #     home_screen(w, h)

            if pygame.mouse.get_pressed()[0]:
                if button_quit.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    exit()

                if button_play.collidepoint(pygame.mouse.get_pos()):
                    game_active=True

                # if button_options.collidepoint(pygame.mouse.get_pos()):
                #     options_active = True

        else :
            option_screen()
            if pygame.mouse.get_pressed()[0]:
                if button_2_rect.collidepoint(pygame.mouse.get_pos()):
                    if mouse_use:
                       mouse_use = False
                    else: mouse_use = True

    pygame.display.update()
    clock.tick(60)