import pygame, os, random
pygame.init()
pygame.font.init()
os.chdir(os.path.dirname(__file__))

font = pygame.font.Font('../pygame Fonts/medieval_font.ttf', 60) 
ui_font = pygame.font.Font(None, 25)

player_speed = 200
screen_width = 1280
screen_height = 720
tile_size = 64
world_width_tiles = 500
world_height_tiles = 500
world_width = world_width_tiles * tile_size
world_height = world_height_tiles * tile_size
character_scaling = 0.5

#HUB
hub_width_tiles = 15
hub_height_tiles = 15
hub_width = hub_width_tiles * tile_size
hub_height = hub_height_tiles * tile_size
hub_spawn = hub_width // 2, hub_height // 2

hub_min_x = world_width // 2 - hub_width
hub_min_y = world_height // 2 - hub_height
hub_max_x = hub_min_x + hub_width
hub_max_y = hub_min_y + hub_height

hub_spawn_x = (hub_min_x - hub_max_x) // 2
hub_spawn_x = (hub_min_y - hub_max_x) // 2

#hp bar
player_hp = 100
max_hp = 100 
hp_regeneration_rate = 1
post_damage_invincibility_time = 0.3
player_invincibility_timer = 0

hp_bar_width = 400
hp_bar_height = 20
hp_bar_x = screen_width // 2 - hp_bar_width // 2
hp_bar_y = 550
hp_bar_color_full = (0, 255, 0)      # Grün 
hp_bar_color_empty = (255, 0, 0)    # Rot 
hp_bar_bg_color = (60, 60, 60)      # Dunkelgrau 


#mana_bar
player_mana = 100
max_mana = 100
mana_regeneration_rate = 1

mana_bar_width = 400
mana_bar_height = 20
mana_bar_x = hp_bar_x
mana_bar_y = hp_bar_y + hp_bar_height 
mana_bar_bg_color = (60, 60, 60)

#spawn pos
player_pos = pygame.math.Vector2(world_width_tiles * 32,   world_height_tiles * 32)
direction = "down"

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
delta_time = 0.1

def load_and_scale(path):
    img = pygame.image.load(path)
    img = pygame.transform.scale(img, (img.get_width() * character_scaling, img.get_height() * character_scaling))
    return img

def load_player_sprites():
    return {
        'looking_up_left_img': load_and_scale("../pygame Bilder/ghost_looking_up_left.png"),
        'looking_up_img': load_and_scale("../pygame Bilder/ghost_looking_up.png"),
        'looking_up_right_img': load_and_scale("../pygame Bilder/ghost_looking_up_right.png"),
        'looking_right_img': load_and_scale("../pygame Bilder/ghost_looking_right.png"),
        'looking_down_right_img': load_and_scale("../pygame Bilder/ghost_looking_down_right.png"),
        'looking_down_img': load_and_scale("../pygame Bilder/ghost_looking_down.png"),
        'looking_down_left_img': load_and_scale("../pygame Bilder/ghost_looking_down_left.png"),
        'looking_left_img': load_and_scale("../pygame Bilder/ghost_looking_left.png"),
    }
player_sprites = load_player_sprites() 

def get_direction(keys, direction):
    move_up = keys[pygame.K_w]
    move_right = keys[pygame.K_d]
    move_down = keys[pygame.K_s]
    move_left = keys[pygame.K_a]

    if move_up:
        direction = 'up'
    if move_right:
        direction = 'right'
    if move_down:
        direction = 'down'
    if move_left:
        direction = 'left'
    if move_up and move_left:
        direction = 'up_left'
    if move_up and move_right:
        direction = 'up_right'
    if move_down and move_right:
        direction = 'down_right'
    if move_down and move_left:
        direction = 'down_left'    
    return direction

ui_big_box = pygame.image.load('../pygame Bilder/ui_big_box.png').convert_alpha()
ui_small_box = pygame.image.load('../pygame Bilder/ui_small_box.png').convert_alpha()
ui_tiny_box = pygame.image.load('../pygame Bilder/ui_tiny_box.png').convert_alpha()
ui_big_box = pygame.transform.scale(ui_big_box, (550, 130))
ui_small_box = pygame.transform.scale(ui_small_box, (600, 150))
ui_tiny_box = pygame.transform.scale(ui_tiny_box, (600, 150))
main_menu_background = pygame.image.load('../pygame Bilder/main_menu_background.png').convert()
main_menu_background = pygame.transform.scale(main_menu_background, (screen_width, screen_height))
grass_tile = pygame.image.load('../pygame Bilder/grass_tile.png').convert()
tile_size = 64

# Pause Manu
pause_menu_resume_rect = ui_big_box.get_rect()
pause_menu_options_rect = ui_big_box.get_rect()
pause_menu_quit_rect = ui_big_box.get_rect()

pause_menu_resume_rect.center = (screen_width // 2, screen_height // 2 - 150)
pause_menu_options_rect.center = (screen_width // 2, screen_height // 2)
pause_menu_quit_rect.center = (screen_width // 2, screen_height // 2 + 150)

pause_menu_buttons = [pause_menu_resume_rect, pause_menu_options_rect, pause_menu_quit_rect]
pause_menu_button_images = [ui_big_box, ui_big_box, ui_big_box]

def render_pause_menu_glow_text(font, text, color=(255,255,255), glow_color=(0,0,0)):
    text_surface = font.render(text, True, color)
    glow = font.render(text, True, glow_color)
    w, h = text_surface.get_size()
    glow_surface = pygame.Surface((w+8, h+8), pygame.SRCALPHA)
    offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for ox, oy in offsets:
        glow_surface.blit(glow, (ox+4, oy+4))
    glow_surface.blit(text_surface, (2, 2))
    return glow_surface
text_color = (0, 0, 0) #Schwarz
glow_color = (64, 0, 128)  #Dunkles Lila

pause_menu_resume_text = render_pause_menu_glow_text(font, "Resume", color=text_color, glow_color=glow_color)
pause_menu_options_text = render_pause_menu_glow_text(font, "Options", color=text_color, glow_color=glow_color)
pause_menu_quit_text = render_pause_menu_glow_text(font, "Quit and Save", color=text_color, glow_color=glow_color)

pause_menu_resume_text_rect = pause_menu_resume_text.get_rect(center=pause_menu_resume_rect.center)
pause_menu_options_text_rect = pause_menu_options_text.get_rect(center=pause_menu_options_rect.center)
pause_menu_quit_text_rect = pause_menu_quit_text.get_rect(center=pause_menu_quit_rect.center)

def pause_menu_select(events, selected_index, game_state, running, last_game_state):
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if selected_index == 0:
                    game_state = last_game_state
                elif selected_index == 1: 
                    game_state = 'hub'
                elif selected_index == 2:
                    game_state = 'main_menu'

    return running, game_state

def draw_pause_menu_buttons(buttons, selected_index): # Beim Ausführen der Funktion immer angeben, welche Buttons genutzt werden sollen
    for i, rect in enumerate(buttons):
        if i == selected_index:
            scale_factor = 1.2
                
            temp_img = pygame.transform.scale(pause_menu_button_images[i],
                                                (int(pause_menu_button_images[i].get_width()*scale_factor),
                                                 int(pause_menu_button_images[i].get_height()*scale_factor)))
            temp_rect = temp_img.get_rect(center=rect.center)
            screen.blit(temp_img, temp_rect)

            glow_text_surface = render_pause_menu_glow_text(font, ["Resume","Back to Hub","Quit and Save"][i], color=text_color, glow_color=glow_color)
            glow_text_surface = pygame.transform.scale(glow_text_surface,
                                                        (int(glow_text_surface.get_width()*scale_factor),
                                                         int(glow_text_surface.get_height()*scale_factor)))
            glow_text_rect = glow_text_surface.get_rect(center=temp_rect.center)
            screen.blit(glow_text_surface, glow_text_rect)
        else:
            screen.blit(pause_menu_button_images[i], rect)
            glow_text_surface = render_pause_menu_glow_text(font, ["Resume","Back to Hub","Quit and Save"][i],
                                                 color=text_color, glow_color=glow_color)
            glow_text_rect = glow_text_surface.get_rect(center=rect.center)
            screen.blit(glow_text_surface, glow_text_rect)


# Main Menu
main_menu_start_rect = ui_big_box.get_rect()
main_menu_options_rect = ui_big_box.get_rect()
main_menu_exit_rect = ui_big_box.get_rect()

main_menu_start_rect.center = (screen_width // 2, screen_height // 2 - 150)
main_menu_options_rect.center = (screen_width // 2, screen_height // 2)
main_menu_exit_rect.center = (screen_width // 2, screen_height // 2 + 150)

main_menu_buttons = [main_menu_start_rect, main_menu_options_rect, main_menu_exit_rect]
main_menu_button_images = [ui_big_box, ui_big_box, ui_big_box]
selected_index = 0



def draw_main_menu_buttons(buttons): # Beim Ausführen der Funktion immer angeben, welche Buttons genutzt werden sollen
    for i, rect in enumerate(buttons):
        if i == selected_index:
            scale_factor = 1.2
                
            temp_img = pygame.transform.scale(main_menu_button_images[i],
                                                (int(main_menu_button_images[i].get_width()*scale_factor),
                                                 int(main_menu_button_images[i].get_height()*scale_factor)))
            temp_rect = temp_img.get_rect(center=rect.center)
            screen.blit(temp_img, temp_rect)

            glow_text_surface = render_main_menu_glow_text(font, ["Start","Options","Exit"][i], color=text_color, glow_color=glow_color)
            glow_text_surface = pygame.transform.scale(glow_text_surface,
                                                        (int(glow_text_surface.get_width()*scale_factor),
                                                         int(glow_text_surface.get_height()*scale_factor)))
            glow_text_rect = glow_text_surface.get_rect(center=temp_rect.center)
            screen.blit(glow_text_surface, glow_text_rect)
        else:
            screen.blit(main_menu_button_images[i], rect)
            glow_text_surface = render_main_menu_glow_text(font, ["Start","Options","Exit"][i],
                                                 color=text_color, glow_color=glow_color)
            glow_text_rect = glow_text_surface.get_rect(center=rect.center)
            screen.blit(glow_text_surface, glow_text_rect)


def main_menu_select(events, selected_index, running, game_state):
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if selected_index == 0:
                    game_state = 'game_running'   
                elif selected_index == 1: # Später noch zu Optionen oder Stats ändern oder so
                    running = False
                elif selected_index == 2:
                    running = False              

    return running, game_state

def menu_navigation(events, selected_index, num_buttons): #Für num_buttons immer len([Genutze Buttons]) eingeben
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                selected_index = (selected_index + 1) % num_buttons
            elif event.key == pygame.K_UP:
                selected_index = (selected_index - 1) % num_buttons
    return selected_index

def handle_quit(events):
    for event in events:
        if event.type == pygame.QUIT:
            return False
    return True


def update_player_position(keys, player_pos, speed, dt):
    direction = pygame.math.Vector2(0, 0)

    if keys[pygame.K_w]:
        direction.y -= 1
    if keys[pygame.K_s]:
        direction.y += 1
    if keys[pygame.K_a]:
        direction.x -= 1
    if keys[pygame.K_d]:
        direction.x += 1

    if direction.length() != 0:
        direction.normalize_ip()

    player_pos += direction * speed * dt
    return player_pos


def check_if_paused(events, keys, game_state, last_game_state):
    for event in events:
        if event.type == pygame.KEYDOWN:
            if game_state == 'game_running' or game_state == 'hub':
                if keys[pygame.K_ESCAPE]:
                    last_game_state = game_state
                    game_state = 'pause_menu'
            elif game_state == 'pause_menu':
                if keys[pygame.K_ESCAPE]:
                    game_state = last_game_state
    return game_state, last_game_state

#-------------------------------------------------------------------------------------------------------------------------------------rendering
def render_main_menu_glow_text(font, text, color=(255,255,255), glow_color=(0,0,0)):
    text_surface = font.render(text, True, color)
    glow = font.render(text, True, glow_color)
    w, h = text_surface.get_size()
    glow_surface = pygame.Surface((w+8, h+8), pygame.SRCALPHA)
    offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for ox, oy in offsets:
        glow_surface.blit(glow, (ox+4, oy+4))
    glow_surface.blit(text_surface, (2, 2))
    return glow_surface
text_color = (0, 0, 0) #Schwarz
glow_color = (64, 0, 128)  #Dunkles Lila


main_menu_start_text = render_main_menu_glow_text(font, "Start", color=text_color, glow_color=glow_color)
main_menu_options_text = render_main_menu_glow_text(font, "Options", color=text_color, glow_color=glow_color)
main_menu_exit_text = render_main_menu_glow_text(font, "Exit", color=text_color, glow_color=glow_color)

main_menu_start_text_rect = main_menu_start_text.get_rect(center=main_menu_start_rect.center)
main_menu_options_text_rect = main_menu_options_text.get_rect(center=main_menu_options_rect.center)
main_menu_exit_text_rect = main_menu_exit_text.get_rect(center=main_menu_exit_rect.center)

def render_world(screen, player_pos, player_sprites, direction, grass_tile, tile_size, world_width, world_height, enemy_list):
    screen.fill((255, 255, 255))

    offset_x = player_pos.x - screen_width // 2
    offset_y = player_pos.y - screen_height // 2

    start_x = int(max(0, offset_x // tile_size) )
    end_x   = int(min(world_width_tiles,  (offset_x + screen_width)  // tile_size + 1)) 
    start_y = int(max(0, offset_y // tile_size))
    end_y   = int(min(world_height_tiles, (offset_y + screen_height) // tile_size + 1))

    for i in range(start_x, end_x):
        for j in range(start_y, end_y):
            screen.blit(grass_tile, (i * tile_size - offset_x,
                                     j * tile_size - offset_y))
            
    player_sprite = player_sprites["looking_" + direction + "_img"]
    player_rect = player_sprite.get_rect(center =(screen_width // 2, screen_height // 2))
    screen.blit(player_sprite, player_rect)

def render_hp_bar(screen, ui_font, current_hp, max_hp):

    if current_hp <= 0:
        hp_percentage = 0
    else:
        hp_percentage = max(0, min(1.0, current_hp / max_hp))

    fill_width = int(hp_bar_width * hp_percentage)

    green = (0, 255, 0)
    red = (255, 0, 0)
    gray = (60, 60, 60)

    if hp_percentage >= 0.20:
        bar_color = green
    if hp_percentage < 0.20 and hp_percentage > 0:
        bar_color = red
    if hp_percentage == 0:
        bar_color = gray

    pygame.draw.rect(screen, bar_color, (hp_bar_x, hp_bar_y, fill_width, hp_bar_height))

    pygame.draw.rect(screen, (0, 0, 0), (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height), 2) # Randbreite 2

    hp_text = ui_font.render(f"{int(current_hp)} / {max_hp}", True, (0, 0, 0))
    text_rect = hp_text.get_rect(center=(hp_bar_x + hp_bar_width // 2, hp_bar_y + hp_bar_height // 2))
    screen.blit(hp_text, text_rect)

def render_mana_bar(screen, ui_font, current_mana, max_mana):

    pygame.draw.rect(screen, mana_bar_bg_color, (mana_bar_x, mana_bar_y, mana_bar_width, mana_bar_height))

    blue = (0, 0, 255) # Hellblau
    dark_blue = (0, 100, 200) # Blau
    gray = (60, 60, 60) # Dunkelgrau

    if max_mana <= 0:
        mana_percentage = 0
    else:
        mana_percentage = max(0, min(1.0, current_mana / max_mana))

    fill_width = int(mana_bar_width * mana_percentage)

    if mana_percentage >= 0.50:
        bar_color = blue
    if mana_percentage < 0.50 and mana_percentage > 0:
        bar_color = dark_blue
    if mana_percentage == 0:
        bar_color = gray

    pygame.draw.rect(screen, bar_color, (mana_bar_x, mana_bar_y, fill_width, mana_bar_height))

    pygame.draw.rect(screen, (0, 0, 0), (mana_bar_x, mana_bar_y, mana_bar_width, mana_bar_height), 2) # Randbreite 2

    mana_text = ui_font.render(f" {int(current_mana)} / {max_mana}", True, (255, 255, 255))
    text_rect = mana_text.get_rect(center=(mana_bar_x + mana_bar_width // 2, mana_bar_y + mana_bar_height // 2))
    screen.blit(mana_text, text_rect)

#----------------------------------------------------------------------------------------------------------------HUB
def load_npc_sprites():
    return {
        'Adventurer_img' : load_and_scale('../pygame Bilder/Marlon.png')
    }

class npc: #--------------------------------------------------------npc
    def __init__(self, x, y, npc_type):
        self.pos = pygame.math.Vector2(x, y)
        self.npc_type = npc_type  #npc Name
        self.npc_sprites = load_npc_sprites()
        self.npc_sprite = self.npc_sprites[self.npc_type + '_img']
        self.rect = self.npc_sprite.get_rect(center=self.pos)
        self.interaction_range = 60  

    def render(self, screen, offset_x, offset_y):
        screen.blit(self.sprite, (self.rect.x - offset_x, self.rect.y - offset_y))

    def get_npc_rect(self, offset_x, offset_y):
        return pygame.Rect(self.rect.x - offset_x, self.rect.y - offset_y, self.rect.width, self.rect.height)
    
Adventurer = npc(hub_min_x -100, hub_min_y - 100, 'Adventurer')
    

npc_list = []

def render_hub(screen, player_pos, player_sprites, direction, grass_tile, tile_size, world_width, world_height, enemy_list):
    screen.fill((255, 255, 255))

    offset_x = player_pos.x - screen_width // 2
    offset_y = player_pos.y - screen_height // 2

    start_x = int(max(hub_min_x, offset_x) // tile_size)
    end_x   = int(min(hub_max_x, (offset_x + screen_width) // tile_size + 1))
    start_y = int(max(hub_min_y, offset_y) // tile_size)
    end_y   = int(min(hub_max_y, (offset_y + screen_height) // tile_size + 1))

    for i in range(start_x, end_x):
        for j in range(start_y, end_y):
            screen.blit(grass_tile, (i * tile_size - offset_x,
                                     j * tile_size - offset_y))
            
    player_sprite = player_sprites["looking_" + direction + "_img"]
    player_rect = player_sprite.get_rect(center =(screen_width // 2, screen_height // 2))
    screen.blit(player_sprite, player_rect)

    border_screen_x = hub_min_x - offset_x
    border_screen_y = hub_min_y - offset_y
    pygame.draw.rect(screen, (255, 0, 0), (border_screen_x, border_screen_y, hub_width, hub_height), 3)
#----------------------------------------------------------------------------------------------------------------Enemies
def check_player_enemy_collision(player_pos, player_sprites, direction, enemy_list, player_hp, player_invincibility_timer, post_damage_invincibility_time):

    if player_invincibility_timer > 0:
        return player_hp, player_invincibility_timer

    player_sprite = player_sprites["looking_" + direction + "_img"]
    player_rect = player_sprite.get_rect(center=player_pos)

    for e in enemy_list:
        enemy_rect = pygame.Rect(e.pos.x - e.enemy_width // 2, e.pos.y - e.enemy_height // 2, e.enemy_width, e.enemy_height)

        if player_rect.colliderect(enemy_rect):
            player_hp -= e.dmg
            if player_hp < 0:
                player_hp = 0
            player_invincibility_timer = post_damage_invincibility_time
    return player_hp, player_invincibility_timer    

def load_enemy_sprites():
    return {
        'unarmed_villager_img' : load_and_scale('../pygame Bilder/Marlon.png')
    }

def scale_enemy_sprite(sprite, enemy_width, enemy_height):
    return pygame.transform.scale(sprite, (enemy_width, enemy_height))

#def spawn_random_enemy(enemy_list, player_pos, min_distance_from_player=100):
    max_attempts = 3
    for _ in range(max_attempts):
        spawn_x = random.randint(player_pos - 500, player_pos + 500)
        spawn_y = random.randint(player_pos - 500, player_pos + 500)
        spawn_pos = pygame.math.Vector2(spawn_x, spawn_y)

        distance_to_player = (player_pos - spawn_pos).length()
        if distance_to_player >= min_distance_from_player:

            new_enemy = enemy(spawn_x, spawn_y, 75, 100, 100, 10, 10, 3, 100, 'idle', 50, 1.5, 1.5, 100, 100, 'unarmed_villager')
            
            enemy_list.append(new_enemy)
            print(f"Ein neuer Gegner wurde bei ({spawn_x}, {spawn_y}) gespawnt!")
            return enemy_list


            


class enemy:
    def __init__(self, x, y, hostile_speed, return_speed, hp, dmg, attack_range, attack_speed, detection_range, state, random_movement_range, random_movement_speed, scaling_factor, enemy_width, enemy_height, enemy_type):
        self.pos = pygame.math.Vector2(x, y) 
        self.spawn_pos = pygame.math.Vector2(x, y)
        self.hostile_speed = hostile_speed
        self.return_speed = return_speed
        self.hp = hp 
        self.dmg = dmg 
        self.attack_range = attack_range
        self.attack_speed = attack_speed
        self.detection_range = detection_range * 2.5
        self.hostile_detection_range = self.detection_range * 1.5
        self.leash_range = self.hostile_detection_range * 1.5
        self.enemy_state = state 
        self.random_movement_range = random_movement_range 
        self.random_movement_speed = random_movement_speed
        self.scaling_factor = scaling_factor
        self.enemy_width = enemy_width
        self.enemy_height = enemy_height
        self.enemy_sprites = load_enemy_sprites()
        self.enemy_type = enemy_type
        self.unscaled_sprite = self.enemy_sprites[self.enemy_type + '_img']
        self.enemy_sprite = scale_enemy_sprite(self.unscaled_sprite, self.enemy_width, self.enemy_height)

    def update_enemy_position(self, player_pos, dt):
        if self.enemy_state == 'hostile':
            direction = player_pos - self.pos
            direction.normalize_ip()
            self.pos += direction * self.hostile_speed * dt
        if self.enemy_state == 'returning':
            direction = self.spawn_pos - self.pos
            if direction.length() > 0:
                direction.normalize_ip()
                self.pos += direction * self.return_speed * dt
        if self.enemy_state == 'idle':
            pass

    def get_enemy_state(self, player_pos):
        distance_to_player = (player_pos - self.pos).length()

        print(f"State: {self.enemy_state}, Distance: {distance_to_player:.2f}, Leash: {self.leash_range:.2f}")

        if self.enemy_state == 'idle':
            if self.detection_range > distance_to_player:
                self.enemy_state = 'hostile'
        
        elif self.enemy_state == 'hostile':
            if self.leash_range < distance_to_player:
                self.enemy_state = 'returning'

        else:
            if self.detection_range // 2 > distance_to_player:
                self.enemy_state = 'hostile'
            elif (self.spawn_pos - self.pos).length() < 5:
                self.enemy_state = 'idle'


        
# x, y, hostile_speed, return_speed, hp, dmg, atack_range, attack_speed, detection_range, state, random_movement_range, random_movement_speed, scaling_factor, size_x, size_y, sprites, enemy_type
moglon = enemy(world_width_tiles * 32 + 200, world_height_tiles * 32 + 200, 75, 100, 100, 10, 10, 3, 100, 'idle', 50, 1.5, 1.5, 100, 100, 'unarmed_villager')
moglon2 = enemy(world_width_tiles * 32 + 350, world_height_tiles * 32 + 350, 90, 100, 100, 3, 10, 10, 100, 'idle', 50, 1.5, 1.5, 100, 100, 'unarmed_villager')

enemy_list = []

enemy_list.append(moglon)
enemy_list.append(moglon2)


#-------------------------------------------------------------------------------------------------------------------------Inventory

slot_size = 70
slot_spacing = 3
selected_slot = 0

slot_img = pygame.image.load("../pygame Bilder/square_inventory_slot.png").convert_alpha()
slot_img = pygame.transform.scale(slot_img, (slot_size, slot_size))

class Inventory:
    def __init__(self, x, y, columns, rows, slot_size=80, slot_spacing=10, scale_factor=1.2):
        self.x = x
        self.y = y
        self.columns = columns
        self.rows = rows
        self.slot_size = slot_size
        self.slot_spacing = slot_spacing
        self.scale_factor = scale_factor

        self.slots = [None] * (columns * rows)
        self.selected_slot = 0

        self.slot_img = pygame.image.load("../pygame Bilder/square_inventory_slot.png").convert_alpha()
        self.slot_img = pygame.transform.scale(self.slot_img, (slot_size, slot_size))

    def navigate_inventory(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.selected_slot = (self.selected_slot + 1) % len(self.slots)
                if event.key == pygame.K_LEFT:
                    self.selected_slot = (self.selected_slot - 1) % len(self.slots)
                if event.key == pygame.K_DOWN:
                    self.selected_slot = (self.selected_slot + self.columns) % len(self.slots)
                if event.key == pygame.K_UP:
                    self.selected_slot = (self.selected_slot - self.columns) % len(self.slots)

    def draw_inventory(self, screen):
        for index in range(len(self.slots)):
            col = index % self.columns
            row = index // self.columns

            slot_x = self.x + col * (self.slot_size + self.slot_spacing)
            slot_y = self.y + row * (self.slot_size + self.slot_spacing)

            if index == self.selected_slot:
                scaled = int(self.slot_size * self.scale_factor)
                temp_img = pygame.transform.scale(self.slot_img, (scaled, scaled))
                temp_rect = temp_img.get_rect(center=(slot_x + self.slot_size//2,
                                                      slot_y + self.slot_size//2))
                screen.blit(temp_img, temp_rect)
            else:
                screen.blit(self.slot_img, (slot_x, slot_y))

    def self_center_inventory(self, screen_width, screen_height):
        inventory_width  = self.columns * self.slot_size + (self.columns - 1) * self.slot_spacing
        inventory_height = self.rows * self.slot_size + (self.rows - 1) * self.slot_spacing

        self.x = screen_width // 2 - inventory_width // 2
        self.y = screen_height // 2 - inventory_height // 2



main_inventory = Inventory(0, 0, 8, 3, 60, 3)
equipment_inventory = Inventory(0, 0, 2, 2, 120, 20)
spell_inventory = Inventory(0, 0, 2, 2, 120, 20)

main_inventory.self_center_inventory(screen_width, screen_height)
equipment_inventory.self_center_inventory(screen_width, screen_height)
spell_inventory.self_center_inventory(screen_width, screen_height)

inventorys = [main_inventory, equipment_inventory, spell_inventory]
active_inventory = 'main_inventory'

def check_for_inventory(events, keys, active_inventory):
    for event in events:
        if event.type == pygame.KEYDOWN:
            if keys[pygame.K_TAB]:
                if active_inventory == 'main_inventory':
                    active_inventory = 'equipment_inventory'
                elif active_inventory == 'equipment_inventory':
                    active_inventory = 'spell_inventory'
                elif active_inventory == 'spell_inventory':
                    active_inventory = 'main_inventory'
    return active_inventory
                

    
def check_if_inventory(events, keys, game_state):
    for event in events:
        if event.type == pygame.KEYDOWN:
            if game_state == 'game_running':
                if keys[pygame.K_e]:
                    game_state = 'inventory'
            elif game_state == 'inventory':
                if keys[pygame.K_e]:
                    game_state = 'game_running'
                elif keys[pygame.K_ESCAPE]:
                    game_state = 'game_running'
    return game_state


running = True
pause_selected_index = 0
game_state = 'main_menu'
last_game_state = game_state

#---------------------------------------------------------------------------------------------------Game Loop
while running:
    events = pygame.event.get()
    keys = pygame.key.get_pressed()

    delta_time = clock.tick(60) / 1000.0
    delta_time = max(0.001, min(0.1, delta_time))

    running = handle_quit(events)
        
    if game_state == 'main_menu':
        
        selected_index = menu_navigation(events, selected_index, len(main_menu_buttons))  
        running, game_state = main_menu_select(events, selected_index, running, game_state)

        screen.blit(main_menu_background, (0, 0))
        draw_main_menu_buttons(main_menu_buttons)

    elif game_state == 'game_running':

        game_state, last_game_state = check_if_paused(events, keys, game_state, last_game_state)
        game_state = check_if_inventory(events, keys, game_state)
        
        direction = get_direction(keys, direction)

        player_pos = update_player_position(keys, player_pos, player_speed, delta_time)

        #spawn_random_enemy(enemy_list, player_pos, min_distance_from_player=100)


        #for e in enemy_list:
        #    e.get_enemy_state(player_pos)
        #    e.update_enemy_position(player_pos, delta_time)
        
        #if player_invincibility_timer > 0:
        #    player_invincibility_timer -= delta_time

        #player_hp, player_invincibility_timer = check_player_enemy_collision(player_pos, player_sprites, direction, enemy_list, player_hp, player_invincibility_timer, post_damage_invincibility_time)
        
        
        render_world(screen, player_pos, player_sprites, direction, grass_tile, tile_size, world_width, world_height, enemy_list)
        render_hp_bar(screen, ui_font, player_hp, max_hp)
        render_mana_bar(screen, ui_font, player_mana, max_mana)

    elif game_state == 'hub':
        if last_game_state != "hub":
            player_pos = pygame.math.Vector2(hub_spawn)
        
        game_state, last_game_state = check_if_paused(events, keys, game_state, last_game_state)
        game_state = check_if_inventory(events, keys, game_state)
        
        direction = get_direction(keys, direction)

        player_pos = update_player_position(keys, player_pos, player_speed, delta_time)

        player_pos.x = max(hub_min_x, min(hub_max_x, player_pos.x))
        player_pos.y = max(hub_min_y, min(hub_max_y, player_pos.y))

        render_hub(screen, player_pos, player_sprites, direction, grass_tile, tile_size, world_width, world_height, enemy_list)
        render_hp_bar(screen, ui_font, player_hp, max_hp)
        render_mana_bar(screen, ui_font, player_mana, max_mana)
        

    elif game_state == 'pause_menu':    

        if last_game_state == 'game_running':
            render_world(screen, player_pos, player_sprites, direction, grass_tile, tile_size, world_width, world_height, enemy_list)
        else:
            render_hub(screen, player_pos, player_sprites, direction, grass_tile, tile_size, world_width, world_height, enemy_list)
        game_state, last_game_state = check_if_paused(events, keys, game_state, last_game_state)

        pause_selected_index = menu_navigation(events, pause_selected_index, len(pause_menu_buttons))       
        running, game_state = pause_menu_select(events, pause_selected_index, game_state, running, last_game_state)
        
        draw_pause_menu_buttons(pause_menu_buttons, pause_selected_index)

    elif game_state == 'inventory':

        render_world(screen, player_pos, player_sprites, direction, grass_tile, tile_size, world_width, world_height, enemy_list)

        game_state = check_if_inventory(events, keys, game_state)
        active_inventory = check_for_inventory(events, keys, active_inventory)

        if active_inventory == 'main_inventory':
            main_inventory.draw_inventory(screen)
            main_inventory.navigate_inventory(events)
        elif active_inventory == 'equipment_inventory':
            equipment_inventory.draw_inventory(screen)
            equipment_inventory.navigate_inventory(events)
        elif active_inventory == 'spell_inventory':
            spell_inventory.draw_inventory(screen)
            spell_inventory.navigate_inventory(events)
        
    elif game_state == 'inventory_actions_menu':
        render_world(screen, player_pos, player_sprites, direction, grass_tile, tile_size, world_width, world_height, enemy_list)
            
    pygame.display.flip()
        
pygame.quit()

