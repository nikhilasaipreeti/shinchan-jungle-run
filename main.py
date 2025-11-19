"""
Shinchan Jungle Run - Educational Game
Created for learning Pygame development
Fan-made project - Not for commercial use
All Shinchan characters belong to their respective copyright owners
"""
import pygame
import random
import sys
import math
from pygame import mixer

# Initialize
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shinchan's Jungle Run")
clock = pygame.time.Clock()
font = pygame.font.SysFont("segoeui", 40)
LIGHT_GREEN = (200, 240, 200)
GREEN = (100, 180, 100)
DARK_GREEN = (70, 120, 70)
LIGHT_GRAY = (230, 230, 230)
GRAY = (180, 180, 180)
DARK_GRAY = (70, 70, 70)
WHITE = (250, 250, 250)
volume = 0.5
speed = 5
muted = False
difficulty = "Normal"


# Game Variables
def reset_game_vars():
    global player_x, player_y, velocity_y, jump_count, score, distance
    global choco_count, pudding_count, items, obstacles, bg_x
    global speed, game_over, game_won, last_space_press, space_pressed
    global can_double_jump, parents_spawned, parents_rect, volume

    player_x, player_y = 100, 300
    velocity_y = 0
    jump_count = 0
    score = 0
    choco_count = 0
    pudding_count = 0
    distance = 0
    items = []
    obstacles = []
    bg_x = 0
    speed = 5
    game_over = False
    game_won = False
    last_space_press = 0
    space_pressed = False
    can_double_jump = False
    parents_spawned = False
    parents_rect = parents_img.get_rect(midbottom=(WIDTH + 2000, 400))
    volume = 0.7  # Default volume

# Load Images
bg_img = pygame.transform.scale(pygame.image.load("assets/shinchan_files/jungle_bg.png"), (WIDTH, HEIGHT))
home_bg = pygame.transform.scale(pygame.image.load("assets/shinchan_files/home_bg.png"), (WIDTH, HEIGHT))
player_img = pygame.transform.scale(pygame.image.load("assets/shinchan_files/shinchan.png"), (80, 80))
choco_img = pygame.transform.scale(pygame.image.load("assets/shinchan_files/chocobee.png"), (50, 50))
pudding_img = pygame.transform.scale(pygame.image.load("assets/shinchan_files/pudding.png"), (50, 50))
obstacle_img = pygame.transform.scale(pygame.image.load("assets/shinchan_files/obstacle.png"), (100, 100))
parents_img = pygame.transform.scale(pygame.image.load("assets/shinchan_files/parents.png"), (100, 180))

# Load Sounds
pygame.mixer.music.load("assets/sounds/bg_music.mp3")
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1)
jump_sound = pygame.mixer.Sound("assets/sounds/jump.mp3")
collect_sound = pygame.mixer.Sound("assets/sounds/collect.mp3")
win_sound = pygame.mixer.Sound("assets/sounds/win.mp3")

# Utility Functions
def draw_text(text, x, y, size=40, color=(50, 50, 50), center=False):
    font = pygame.font.SysFont("segoeui", size, bold=True)
    label = font.render(text, True, color)
    rect = label.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(label, rect)

def draw_scoreboard():
    pygame.draw.rect(screen, (200, 160, 60), (5, 5, 200, 110), 3, border_radius=10)
    pygame.draw.rect(screen, (50, 50, 50), (5, 5, 200, 110), 1, border_radius=10)
    
    draw_text(f"Score:", 15, 10, 20, (200, 160, 60))
    draw_text(f"{score}", 100, 10, 20, (255, 0, 0))
    
    draw_text(f"Distance:", 15, 35, 20, (200, 160, 60))
    draw_text(f"{min(distance, 2000)}/2000", 100, 35, 20, (255, 0, 0))
    
    draw_text(f"Chocobees:", 15, 60, 20, (200, 160, 60))
    draw_text(f"{choco_count}", 100, 60, 20, (255, 0, 0))
    
    draw_text(f"Puddings:", 15, 85, 20, (200, 160, 60))
    draw_text(f"{pudding_count}", 100, 85, 20, (255, 0, 0))

def draw_button(text, x, y, w, h, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)
    is_hover = rect.collidepoint(mouse)

    pygame.draw.rect(screen, (180, 180, 180), (x + 4, y + 4, w, h), border_radius=12)
    pygame.draw.rect(screen, hover_color if is_hover else color, rect, border_radius=12)
    draw_text(text, x + w // 2, y + h // 2, size=30, color=(255, 255, 255), center=True)

    if is_hover and click[0] == 1 and action:
        pygame.time.delay(150)
        action()

def draw_gear_icon(x, y, size=30, color=(100, 100, 100), hover_color=(60, 60, 60)):
    mouse_pos = pygame.mouse.get_pos()
    gear_rect = pygame.Rect(x - size//2, y - size//2, size, size)
    is_hover = gear_rect.collidepoint(mouse_pos)
    
    current_color = hover_color if is_hover else color
    thickness = 3
    
    # Draw gear
    pygame.draw.circle(screen, current_color, (x, y), size//2, thickness)
    pygame.draw.circle(screen, current_color, (x, y), size//4, thickness)
    
    # Draw gear teeth
    for i in range(8):
        angle = math.radians(i * 45)
        outer_x1 = x + (size//2 - 2) * math.cos(angle)
        outer_y1 = y + (size//2 - 2) * math.sin(angle)
        outer_x2 = x + (size//2 + 5) * math.cos(angle)
        outer_y2 = y + (size//2 + 5) * math.sin(angle)
        pygame.draw.line(screen, current_color, (outer_x1, outer_y1), (outer_x2, outer_y2), thickness)
    
    return gear_rect
def show_settings():
    settings_active = True
    global volume, speed, muted, difficulty

    # Layout - ADD THESE VARIABLES
    row_gap = 60
    start_y = HEIGHT // 2 - 120
    label_x = WIDTH // 2 - 160
    control_x = WIDTH // 2 + 20
    slider_width = 200
    slider_height = 20

    # UI elements
    volume_slider = pygame.Rect(control_x, start_y, slider_width, slider_height)
    speed_slider = pygame.Rect(control_x, start_y + row_gap, slider_width, slider_height)
    mute_button = pygame.Rect(control_x, start_y + row_gap * 2, 160, 40)
    diff_button = pygame.Rect(control_x, start_y + row_gap * 3, 160, 40)

    while settings_active:
        
        screen.fill(LIGHT_GREEN)

        # 🎨 Modal background
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 220, HEIGHT // 2 - 180, 440, 400), border_radius=15)
        pygame.draw.rect(screen, GREEN, (WIDTH // 2 - 220, HEIGHT // 2 - 180, 440, 400), 3, border_radius=15)

        # 🏷 Title
        draw_text("SETTINGS", WIDTH // 2, HEIGHT // 2 - 150, 32, DARK_GREEN, center=True)

        # 🔊 Volume row
        draw_text("Volume:", label_x, start_y + slider_height // 2, 22, DARK_GRAY, center=False)
        pygame.draw.rect(screen, LIGHT_GRAY, volume_slider, border_radius=10)
        pygame.draw.rect(screen, DARK_GRAY, volume_slider, 2, border_radius=10)
        pygame.draw.rect(screen, GREEN,
                         (volume_slider.x + 2, volume_slider.y + 2,
                          (volume_slider.width - 4) * volume, volume_slider.height - 4),
                         border_radius=8)
        draw_text(f"{int(volume * 100)}%", control_x + slider_width + 10, start_y + 10, 20, DARK_GRAY)

        # ⚡ Speed row
        draw_text("Game Speed:", label_x, start_y + row_gap + slider_height // 2, 22, DARK_GRAY, center=False)
        pygame.draw.rect(screen, LIGHT_GRAY, speed_slider, border_radius=10)
        pygame.draw.rect(screen, DARK_GRAY, speed_slider, 2, border_radius=10)
        pygame.draw.rect(screen, GREEN,
                         (speed_slider.x + 2, speed_slider.y + 2,
                          (speed_slider.width - 4) * (speed / 10), speed_slider.height - 4),
                         border_radius=8)
        draw_text(f"{speed:.1f}", control_x + slider_width + 10, start_y + row_gap + 10, 20, DARK_GRAY)

        # 🔇 Sound row
        draw_text("Sound:", label_x, start_y + row_gap * 2 + 20, 22, DARK_GRAY, center=False)
        pygame.draw.rect(screen, LIGHT_GRAY, mute_button, border_radius=10)
        pygame.draw.rect(screen, DARK_GRAY, mute_button, 2, border_radius=10)
        button_color = GREEN if not muted else (200, 100, 100)
        pygame.draw.rect(screen, button_color, 
                        (mute_button.x + 2, mute_button.y + 2, 
                         mute_button.width - 4, mute_button.height - 4), 
                        border_radius=8)
        draw_text("MUTED" if muted else "SOUND ON", mute_button.centerx, mute_button.centery,
                  22, WHITE, center=True)

        # 🎮 Difficulty row
        draw_text("Difficulty:", label_x, start_y + row_gap * 3 + 20, 22, DARK_GRAY, center=False)
        pygame.draw.rect(screen, LIGHT_GRAY, diff_button, border_radius=10)
        pygame.draw.rect(screen, DARK_GRAY, diff_button, 2, border_radius=10)
        
        # Color code difficulty
        if difficulty == "Easy":
            diff_color = (100, 200, 100)  # Light green
        elif difficulty == "Normal":
            diff_color = (100, 150, 200)  # Light blue
        else:  # Hard
            diff_color = (200, 100, 100)  # Light red
            
        pygame.draw.rect(screen, diff_color, 
                        (diff_button.x + 2, diff_button.y + 2, 
                         diff_button.width - 4, diff_button.height - 4), 
                        border_radius=8)
        draw_text(difficulty, diff_button.centerx, diff_button.centery, 22, WHITE, center=True)

        # ⬅ Back button
        back_rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 170, 120, 40)
        pygame.draw.rect(screen, LIGHT_GRAY, back_rect, border_radius=10)
        pygame.draw.rect(screen, DARK_GRAY, back_rect, 2, border_radius=10)
        pygame.draw.rect(screen, GREEN, 
                        (back_rect.x + 2, back_rect.y + 2, 
                         back_rect.width - 4, back_rect.height - 4), 
                        border_radius=8)
        draw_text("BACK", WIDTH // 2, HEIGHT // 2 + 190, 25, WHITE, center=True)

        # 🎮 Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    settings_active = False

                elif volume_slider.collidepoint(event.pos):
                    volume = max(0, min(1, (event.pos[0] - volume_slider.x) / volume_slider.width))
                    # In a real game, you would update the sound volume here

                elif speed_slider.collidepoint(event.pos):
                    speed = max(3, min(10, (event.pos[0] - speed_slider.x) / speed_slider.width * 10))

                elif mute_button.collidepoint(event.pos):
                    muted = not muted
                    # In a real game, you would mute/unmute sounds here

                elif diff_button.collidepoint(event.pos):
                    # Cycle difficulty: Easy → Normal → Hard → back to Easy
                    if difficulty == "Easy":
                        difficulty = "Normal"
                    elif difficulty == "Normal":
                        difficulty = "Hard"
                    else:
                        difficulty = "Easy"

        pygame.display.update()
        clock.tick(60)

# State flags
on_home = True
reset_game_vars()

def run_game():
    global player_x, player_y, velocity_y, jump_count, score, distance
    global choco_count, pudding_count, bg_x, speed, game_over, game_won
    global last_space_press, space_pressed, can_double_jump, items, obstacles
    global parents_spawned, parents_rect

    spawn_timer = 0
    obstacle_timer = 0
    running = True

    while running:
        screen.fill(LIGHT_GREEN)

        # Background scroll
        bg_x -= speed
        if bg_x <= -WIDTH:
            bg_x = 0
        screen.blit(bg_img, (bg_x, 0))
        screen.blit(bg_img, (bg_x + WIDTH, 0))

        screen.blit(player_img, (player_x, player_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_time = pygame.time.get_ticks()
                    if current_time - last_space_press < 300 and not space_pressed:
                        if can_double_jump and jump_count < 2:
                            velocity_y = -20
                            jump_count += 1
                            jump_sound.play()
                            can_double_jump = False
                    else:
                        if jump_count < 2:
                            velocity_y = -20
                            jump_count += 1
                            jump_sound.play()
                            if jump_count == 1:
                                can_double_jump = True
                    last_space_press = current_time
                    space_pressed = True
                elif event.key == pygame.K_ESCAPE:  # ESC opens settings
                    show_settings()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    space_pressed = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if settings gear was clicked
                gear_rect = pygame.Rect(WIDTH-40, 10, 30, 30)
                if gear_rect.collidepoint(event.pos):
                    show_settings()

        if not game_over and not game_won:
            # Gravity and ground check
            velocity_y += 1
            player_y += velocity_y
            if player_y >= 300:
                player_y = 300
                velocity_y = 0
                jump_count = 0
                can_double_jump = False

            distance += speed
            
            # Spawn items
            spawn_timer += 1
            if spawn_timer > 60 and distance < 2000:
                kind = random.choice(['choco', 'pudding'])
                img = choco_img if kind == 'choco' else pudding_img
                y_pos = random.randint(180, 250)
                rect = img.get_rect(midbottom=(WIDTH + 50, y_pos))
                items.append({'type': kind, 'img': img, 'rect': rect})
                spawn_timer = 0

            # Spawn obstacles
            obstacle_timer += 1
            if obstacle_timer > 120 and distance < 2000:
                rect = obstacle_img.get_rect(midbottom=(WIDTH + 50, 400))
                obstacles.append({'img': obstacle_img, 'rect': rect})
                obstacle_timer = 0

            # Draw and check items
            for item in items[:]:
                item['rect'].x -= speed
                screen.blit(item['img'], item['rect'])
                if pygame.Rect(player_x, player_y, 80, 80).colliderect(item['rect']):
                    collect_sound.play()
                    if item['type'] == 'choco':
                        score += 1
                        choco_count += 1
                    else:
                        score += 3
                        pudding_count += 1
                    items.remove(item)
                elif item['rect'].right < 0:
                    items.remove(item)

            # Draw and check obstacles
            for obs in obstacles[:]:
                obs['rect'].x -= speed
                screen.blit(obs['img'], obs['rect'])
                if pygame.Rect(player_x, player_y, 80, 80).colliderect(obs['rect']):
                    game_over = True
                elif obs['rect'].right < 0:
                    obstacles.remove(obs)

            # Draw parents at the end
            if distance >= 2000 - WIDTH and not parents_spawned:
                parents_spawned = True
            
            if parents_spawned:
                parents_rect.x -= speed
                screen.blit(parents_img, parents_rect)
                
                if pygame.Rect(player_x, player_y, 60, 60).colliderect(parents_rect):
                    game_won = True
                    win_sound.play()

            draw_scoreboard()
            
            # Draw settings gear (top right)
            gear_rect = draw_gear_icon(WIDTH-25, 25)

        elif game_won:
            draw_text("You found your parents!", WIDTH // 2, HEIGHT // 2 - 60, size=50, center=True)
            draw_text("Game Completed Successfully!", WIDTH // 2, HEIGHT // 2 - 10, size=40, center=True)
            draw_text(f"Final Score: {score}", WIDTH // 2, HEIGHT // 2 + 40, size=40, center=True)
            draw_text("Press R to Restart", WIDTH // 2, HEIGHT // 2 + 100, center=True)
            
            if pygame.key.get_pressed()[pygame.K_r]:
                reset_game_vars()
                return

        else:  # Game over
            draw_text("GAME OVER", WIDTH // 2, HEIGHT // 2 - 40, size=60, center=True)
            draw_text("Press R to Restart", WIDTH // 2, HEIGHT // 2 + 10, center=True)
            
            if pygame.key.get_pressed()[pygame.K_r]:
                reset_game_vars()
                return

        pygame.display.update()
        clock.tick(60)

def home_screen():
    global on_home
    while on_home:
        screen.blit(home_bg, (0, 0))

        # 🎨 Base color theme (teal-like tones)
        base_color = (0, 128, 128)   # Normal teal
        button_color = (0, 100, 100) # Darker teal for button
        text_color = (100, 200, 200) # Lighter teal for text

        # ✅ Draw button with shades of teal
        draw_button("Start Game", WIDTH // 2 - 100, 280, 200, 60,
                    button_color, base_color, start_game)

        # ✅ Draw text in a lighter shade of teal
        draw_text("Help Shinchan collect Chocobees & Puddings!",
                  WIDTH // 2, 140, size=25, color=text_color, center=True)

        # ⚙️ Draw settings gear on home screen
        gear_rect = draw_gear_icon(WIDTH - 25, 25)

        # 🎮 Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if gear_rect.collidepoint(event.pos):
                    show_settings()

        pygame.display.update()
        clock.tick(60)


def start_game():
    global on_home
    on_home = False
    reset_game_vars()
    run_game()
    on_home = True
    home_screen()


# 🚀 Start game
home_screen()
